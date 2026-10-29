const express = require('express');
const sgMail = require('@sendgrid/mail');
const crypto = require('crypto');

const app = express();
app.use(express.json());

// ⚠️ قراءة المفاتيح بأمان من إعدادات Render السرية (Environment Variables)
const LICENSE_SECRET = process.env.LICENSE_SECRET || "Zevorix_Master_Key_2026"; 
const SENDGRID_KEY = process.env.SENDGRID_KEY;
const NOWPAYMENTS_IPN_SECRET = process.env.NOWPAYMENTS_IPN_SECRET;

if (SENDGRID_KEY) {
    sgMail.setApiKey(SENDGRID_KEY);
} else {
    console.error("WARNING: SENDGRID_KEY is missing in Environment Variables!");
}

function generateLicenseKey() {
    const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";
    let nonce = "";
    for (let i = 0; i < 6; i++) {
        nonce += ALPHABET.charAt(Math.floor(Math.random() * ALPHABET.length));
    }
    const message = `ZEV|${nonce}`;
    const signature = crypto.createHmac('sha256', LICENSE_SECRET).update(message).digest('hex').toUpperCase().substring(0, 8);
    return `ZEV-${nonce}-${signature}`;
}

app.post('/paymentWebhook', async (req, res) => {
    try {
        // 1. التحقق من توقيع بوابة الدفع
        const receivedSig = req.headers['x-nowpayments-sig'];
        const sortedBody = JSON.stringify(req.body, Object.keys(req.body).sort());
        
        if (!NOWPAYMENTS_IPN_SECRET) {
            console.error("NOWPAYMENTS_IPN_SECRET is missing!");
            return res.status(500).send("Server configuration error");
        }

        const expectedSig = crypto.createHmac('sha512', NOWPAYMENTS_IPN_SECRET).update(sortedBody).digest('hex');

        if (receivedSig !== expectedSig) {
            console.log("Invalid signature. Expected:", expectedSig, "Received:", receivedSig);
            return res.status(401).send("Invalid signature");
        }

        // 2. التأكد من أن الدفع مكتمل
        const { payment_status, order_description } = req.body;
        if (payment_status !== 'finished' && payment_status !== 'confirmed') {
            return res.status(200).send('Payment not confirmed yet');
        }

        // 3. توليد الكود وإرسال الإيميل
        const licenseKey = generateLicenseKey();
        const customerEmail = order_description; 

        if (!customerEmail || !customerEmail.includes('@')) {
             return res.status(400).send('Invalid customer email in order_description');
        }

        const msg = {
            to: customerEmail,
            from: 'tijara6@gmail.com', // البريد الموثق في SendGrid
            subject: 'تم تفعيل نسختك المدفوعة من Zevorix AI',
            html: `<h3>شكراً لشرائك!</h3>
                   <p>كود التفعيل الخاص بك هو: <strong>${licenseKey}</strong></p>
                   <p>أدخله في التطبيق لفتح جميع الميزات.</p>`,
        };

        await sgMail.send(msg);
        console.log(`License sent to ${customerEmail}`);
        res.status(200).send('License sent successfully');
    } catch (error) {
        console.error("Error:", error);
        res.status(500).send('Error processing webhook');
    }
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
