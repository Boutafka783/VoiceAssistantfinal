const express = require('express');
const sgMail = require('@sendgrid/mail');
const crypto = require('crypto');

const app = express();
app.use(express.json());

// ⚠️ مهم جداً: غير هذا السر واكتب نفس المفتاح الذي وضعته في التطبيق (LICENSE_SECRET)
const LICENSE_SECRET = "Zevorix_Master_Key_2026"; 

const SENDGRID_KEY = "YOUR_SENDGRID_KEY_HERE"; // سنضع المفتاح لاحقاً
const NOWPAYMENTS_IPN_SECRET = "YOUR_IPN_SECRET_HERE"; // سنضع المفتاح لاحقاً

sgMail.setApiKey(SENDGRID_KEY);

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
        const receivedSig = req.headers['x-nowpayments-sig'];
        const sortedBody = JSON.stringify(req.body, Object.keys(req.body).sort());
        const expectedSig = crypto.createHmac('sha512', NOWPAYMENTS_IPN_SECRET).update(sortedBody).digest('hex');

        if (receivedSig !== expectedSig) return res.status(401).send("Invalid signature");

        const { payment_status, order_description } = req.body;
        if (payment_status !== 'finished' && payment_status !== 'confirmed') return res.status(200).send('Payment not confirmed yet');

        const licenseKey = generateLicenseKey();
        const customerEmail = order_description; 

        const msg = {
            to: customerEmail,
            from: 'tijara6@gmail.com', // ⚠️ ضع إيميلك الموثق لاحقاً
            subject: 'تم تفعيل نسختك المدفوعة من Zevorix AI',
            html: `<h3>شكراً لشرائك!</h3><p>كود التفعيل الخاص بك هو: <strong>${licenseKey}</strong></p><p>أدخله في التطبيق لفتح جميع الميزات.</p>`,
        };

        await sgMail.send(msg);
        res.status(200).send('License sent successfully');
    } catch (error) {
        console.error(error);
        res.status(500).send('Error');
    }
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
