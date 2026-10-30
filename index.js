const express = require('express');
const sgMail = require('@sendgrid/mail');
const crypto = require('crypto');

const app = express();
app.use(express.json());

// 1. إجبار السيرفر على قراءة المفاتيح من Render، وإلا سيتوقف (لحماية الأكواد)
const LICENSE_SECRET = process.env.LICENSE_SECRET;
const SENDGRID_KEY = process.env.SENDGRID_KEY;
const NOWPAYMENTS_IPN_SECRET = process.env.NOWPAYMENTS_IPN_SECRET;

if (!LICENSE_SECRET) {
    console.error("FATAL: LICENSE_SECRET is missing! Cannot start server.");
    process.exit(1); 
}
if (SENDGRID_KEY) {
    sgMail.setApiKey(SENDGRID_KEY);
} else {
    console.error("WARNING: SENDGRID_KEY is missing.");
}

// دالة لترتيب الكائنات المتداخلة لضمان صحة توقيع NOWPayments
function deepSort(obj) {
    if (Array.isArray(obj)) return obj.map(deepSort);
    if (obj !== null && typeof obj === 'object') {
        return Object.keys(obj).sort().reduce((result, key) => {
            result[key] = deepSort(obj[key]);
            return result;
        }, {});
    }
    return obj;
}

function generateLicenseKey() {
    const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";
    let nonce = "";
    // 2. استخدام crypto.randomBytes بدلاً من Math.random العشوائي
    const bytes = crypto.randomBytes(6);
    for (let i = 0; i < 6; i++) {
        nonce += ALPHABET.charAt(bytes[i] % ALPHABET.length);
    }
    const message = `ZEV|${nonce}`;
    const signature = crypto.createHmac('sha256', LICENSE_SECRET).update(message).digest('hex').toUpperCase().substring(0, 8);
    return `ZEV-${nonce}-${signature}`;
}

app.post('/paymentWebhook', async (req, res) => {
    try {
        // التحقق من توقيع بوابة الدفع (باستخدام الترتيب العميق)
        const receivedSig = req.headers['x-nowpayments-sig'];
        const sortedBody = JSON.stringify(deepSort(req.body));
        
        if (!NOWPAYMENTS_IPN_SECRET) {
            return res.status(500).send("Server configuration error");
        }

        const expectedSig = crypto.createHmac('sha512', NOWPAYMENTS_IPN_SECRET).update(sortedBody).digest('hex');

        if (receivedSig !== expectedSig) {
            console.log("Invalid signature.");
            return res.status(401).send("Invalid signature");
        }

        const { payment_status, order_description, customer_email } = req.body;
        if (payment_status !== 'finished' && payment_status !== 'confirmed') {
            return res.status(200).send('Payment not confirmed yet');
        }

        // 3. جلب البريد الإلكتروني من NOWPayments
        // (إذا كان المستخدم يدخله في صفحة الدفع، سيكون في customer_email، وإلا سنستخدم order_description)
        const emailToSend = customer_email || order_description;

        if (!emailToSend || !emailToSend.includes('@')) {
             console.log("No valid email found in payload:", req.body);
             return res.status(400).send('Invalid customer email');
        }

        const licenseKey = generateLicenseKey();

        const msg = {
            to: emailToSend,
            from: 'tijara6@gmail.com',
            subject: 'تم تفعيل نسختك المدفوعة من Zevorix AI',
            html: `<div dir="rtl" style="font-family: Arial, sans-serif;">
                     <h3>شكراً لشرائك Zevorix AI!</h3>
                     <p>كود التفعيل الخاص بك هو: </p>
                     <h2 style="color: #4F5BD5; font-family: monospace;">${licenseKey}</h2>
                     <p>افتح التطبيق، اذهب إلى (الحصة -> تفعيل)، وأدخل الكود لفتح جميع الميزات.</p>
                   </div>`,
        };

        await sgMail.send(msg);
        console.log(`License sent to ${emailToSend} | Key: ${licenseKey}`);
        res.status(200).send('License sent successfully');
    } catch (error) {
        console.error("Error processing webhook:", error);
        res.status(500).send('Error processing webhook');
    }
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
