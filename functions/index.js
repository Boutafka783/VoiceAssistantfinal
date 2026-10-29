const functions = require("firebase-functions");
const sgMail = require("@sendgrid/mail");
const crypto = require('crypto');

// ⚠️ مهم جداً: غير هذا السطر واكتب السر الخاص بك (نفس المفتاح الذي وضعته في GitHub Secrets باسم LICENSE_SECRET)
const LICENSE_SECRET = "YOUR_SUPER_SECRET_KEY_HERE"; 

// ⚠️ ضع هنا مفتاح IPN Secret الخاص بـ NOWPayments لاحقاً
const NOWPAYMENTS_IPN_SECRET = functions.config().nowpayments?.ipn_secret || "YOUR_IPN_SECRET_HERE";

// ⚠️ ضع هنا مفتاح SendGrid لاحقاً
sgMail.setApiKey(functions.config().sendgrid?.key || "YOUR_SENDGRID_KEY_HERE");

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

exports.paymentWebhook = functions.https.onRequest(async (req, res) => {
    // التحقق من توقيع بوابة الدفع (لمنع التزوير)
    const receivedSig = req.headers['x-nowpayments-sig'];
    const sortedBody = JSON.stringify(req.body, Object.keys(req.body).sort());
    const expectedSig = crypto.createHmac('sha512', NOWPAYMENTS_IPN_SECRET).update(sortedBody).digest('hex');

    // إذا كان التوقيع غير صحيح، يتم رفض الطلب
    if (receivedSig !== expectedSig) return res.status(401).send("Invalid signature");
    
    const { payment_status, order_description } = req.body;
    // التأكد من أن الدفع قد اكتمل
    if (payment_status !== 'finished' && payment_status !== 'confirmed') return res.status(200).send('Payment not confirmed yet');

    // توليد كود الترخيص
    const licenseKey = generateLicenseKey();
    // نفترض أنك تمرر إيميل المشتري في حقل order_description عند إنشاء رابط الدفع
    const customerEmail = order_description; 

    // تجهيز رسالة البريد الإلكتروني
    const msg = {
        to: customerEmail,
        from: 'noreply@yourdomain.com', // ⚠️ يجب توثيق هذا البريد في SendGrid
        subject: 'تم تفعيل نسختك المدفوعة من Zevorix AI',
        html: `<h3>شكراً لشرائك!</h3><p>كود التفعيل الخاص بك هو: <strong>${licenseKey}</strong></p><p>أدخله في التطبيق لفتح جميع الميزات.</p>`,
    };

    try {
        await sgMail.send(msg);
        res.status(200).send('License sent successfully');
    } catch (error) {
        console.error(error);
        res.status(500).send('Error sending email');
    }
});
