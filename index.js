const express = require('express');
const sgMail = require('@sendgrid/mail');
const crypto = require('crypto');
const admin = require('firebase-admin');

const app = express();
app.use(express.json());

// ============================================================================
// 1. متغيرات البيئة (تُضبط في Render Environment Variables)
// ============================================================================
const LICENSE_SECRET          = process.env.LICENSE_SECRET;
const SENDGRID_KEY            = process.env.SENDGRID_KEY;
const NOWPAYMENTS_IPN_SECRET  = process.env.NOWPAYMENTS_IPN_SECRET;
const FIREBASE_SERVICE_ACCOUNT = process.env.FIREBASE_SERVICE_ACCOUNT; // JSON نصي

if (!LICENSE_SECRET) {
    console.error("FATAL: LICENSE_SECRET is missing! Server cannot start.");
    process.exit(1);
}
if (SENDGRID_KEY) {
    sgMail.setApiKey(SENDGRID_KEY);
} else {
    console.error("WARNING: SENDGRID_KEY is missing. Emails will fail.");
}

// ============================================================================
// 2. تهيئة Firebase Admin (لإرسال إشعارات الفيديو)
// ============================================================================
let firebaseReady = false;
try {
    if (FIREBASE_SERVICE_ACCOUNT) {
        const serviceAccount = JSON.parse(FIREBASE_SERVICE_ACCOUNT);
        admin.initializeApp({
            credential: admin.credential.cert(serviceAccount),
        });
        firebaseReady = true;
        console.log("✅ Firebase Admin initialized.");
    } else {
        console.warn("⚠️  FIREBASE_SERVICE_ACCOUNT not set. Video notifications will be disabled.");
    }
} catch (e) {
    console.error("❌ Firebase Admin init failed:", e.message);
}

// ============================================================================
// 3. دوال مساعدة (التوقيع + توليد الكود)
// ============================================================================
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
    const bytes = crypto.randomBytes(6);
    for (let i = 0; i < 6; i++) {
        nonce += ALPHABET.charAt(bytes[i] % ALPHABET.length);
    }
    const signature = crypto.createHmac('sha256', LICENSE_SECRET)
        .update(`ZEV|${nonce}`)
        .digest('hex')
        .toUpperCase()
        .substring(0, 8);
    return `ZEV-${nonce}-${signature}`;
}

// ============================================================================
// 4. صحة السيرفر (Health Check) - مفيد لـ Render
// ============================================================================
app.get('/', (req, res) => {
    res.json({
        service: 'Zevorix AI Backend',
        status: 'ok',
        features: {
            payment: !!NOWPAYMENTS_IPN_SECRET,
            email: !!SENDGRID_KEY,
            video: firebaseReady,
        },
        time: new Date().toISOString(),
    });
});

app.get('/health', (req, res) => {
    res.json({
        uptime: process.uptime(),
        firebase: firebaseReady,
        sendgrid: !!SENDGRID_KEY,
        nowpayments: !!NOWPAYMENTS_IPN_SECRET,
    });
});

// ============================================================================
// 5. تدفق الدفع والتفعيل (لم يتغير شيء - كما كان)
// ============================================================================
app.post('/paymentWebhook', async (req, res) => {
    try {
        const receivedSig = req.headers['x-nowpayments-sig'];
        const sortedBody = JSON.stringify(deepSort(req.body));

        if (!NOWPAYMENTS_IPN_SECRET) {
            return res.status(500).send("Server configuration error");
        }

        const expectedSig = crypto.createHmac('sha512', NOWPAYMENTS_IPN_SECRET)
            .update(sortedBody).digest('hex');

        if (receivedSig !== expectedSig) {
            console.log("Invalid signature.");
            return res.status(401).send("Invalid signature");
        }

        const { payment_status, order_description, customer_email } = req.body;
        if (payment_status !== 'finished' && payment_status !== 'confirmed') {
            return res.status(200).send('Payment not confirmed yet');
        }

        const emailToSend = customer_email || order_description;
        if (!emailToSend || !emailToSend.includes('@')) {
            console.log("No valid email in payload:", req.body);
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
                     <p>افتح التطبيق، اذهب إلى (الحصة → تفعيل)، وأدخل الكود لفتح جميع الميزات.</p>
                   </div>`,
        };

        await sgMail.send(msg);
        console.log(`✅ License sent to ${emailToSend} | Key: ${licenseKey}`);
        res.status(200).send('License sent successfully');
    } catch (error) {
        console.error("Error processing webhook:", error);
        res.status(500).send('Error processing webhook');
    }
});

// ============================================================================
// 6. البنية التحتية لتوليد الفيديو
// ============================================================================
const VIDEO_COOLDOWN_MS = 60 * 1000; // دقيقة واحدة بين كل طلب لكل جهاز
const deviceCooldowns = new Map();

// تنظيف دوري للذاكرة (كل ساعة)
setInterval(() => {
    const now = Date.now();
    for (const [deviceId, ts] of deviceCooldowns.entries()) {
        if (now - ts > 24 * 60 * 60 * 1000) deviceCooldowns.delete(deviceId);
    }
}, 60 * 60 * 1000);

app.post('/api/generate-video', async (req, res) => {
    const { prompt, deviceId, licenseKey } = req.body || {};

    if (!prompt || typeof prompt !== 'string' || prompt.trim().length < 3) {
        return res.status(400).json({ error: 'Missing or too short prompt' });
    }
    if (!deviceId || typeof deviceId !== 'string') {
        return res.status(400).json({ error: 'Missing deviceId' });
    }

    // حماية بسيطة: منع الطلبات المتكررة السريعة لكل جهاز
    const now = Date.now();
    const lastRequest = deviceCooldowns.get(deviceId) || 0;
    if (now - lastRequest < VIDEO_COOLDOWN_MS) {
        const waitSec = Math.ceil((VIDEO_COOLDOWN_MS - (now - lastRequest)) / 1000);
        return res.status(429).json({
            error: 'Please wait before generating another video',
            waitSeconds: waitSec,
        });
    }
    deviceCooldowns.set(deviceId, now);

    console.log(`🎬 Video request | device=${deviceId} | license=${licenseKey || 'none'} | prompt="${prompt}"`);

    // نرد على التطبيق فوراً حتى لا يبقى "جارٍ المعالجة" معلقاً
    res.status(200).json({ status: 'started', message: 'Video generation started' });

    // التوليد في الخلفية
    generateVideoAsync(prompt, deviceId).catch(err => {
        console.error(`❌ Failed to generate video for ${deviceId}:`, err.message);
    });
});

async function generateVideoAsync(prompt, deviceId) {
    try {
        const videoUrl = await generateVideoWithProvider(prompt);
        await sendVideoReadyNotification(deviceId, videoUrl, prompt);
        console.log(`✅ Video ready for device_${deviceId}: ${videoUrl}`);
    } catch (error) {
        console.error(`❌ Video generation error for ${deviceId}:`, error.message);
        await sendVideoErrorNotification(deviceId, prompt, error.message).catch(() => {});
    }
}

/**
 * 🔄 TO SWAP WITH A REAL PROVIDER LATER:
 *
 * Contract: (prompt: string) => Promise<string>  // returns a video URL
 *
 * When you subscribe to Replicate / Runway / Luma / Pika etc.,
 * replace this function body with the actual API call. Nothing else in
 * the file needs to change — the notification system, rate limiting,
 * and app integration will keep working as-is.
 */
async function generateVideoWithProvider(prompt) {
    // ⏳ MOCK: simulate a 15-second generation delay
    console.log(`⏳ [MOCK] Generating for: "${prompt}"...`);
    await new Promise(resolve => setTimeout(resolve, 15000));

    // 🎬 Mock video URL (Big Buck Bunny sample)
    return "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4";
}

async function sendVideoReadyNotification(deviceId, videoUrl, prompt) {
    if (!firebaseReady) {
        console.warn("⚠️  Firebase not ready, skipping push notification.");
        return;
    }
    try {
        await admin.messaging().send({
            data: {
                type: 'video_ready',
                url: videoUrl,
                prompt: prompt || '',
            },
            topic: `device_${deviceId}`,
            android: {
                priority: 'high',
                ttl: 24 * 60 * 60 * 1000, // 24 hours
            },
        });
        console.log(`📱 Notification sent to topic device_${deviceId}`);
    } catch (error) {
        console.error(`❌ Notification failed for device_${deviceId}:`, error.message);
    }
}

async function sendVideoErrorNotification(deviceId, prompt, errorMessage) {
    if (!firebaseReady) return;
    try {
        await admin.messaging().send({
            data: {
                type: 'video_error',
                prompt: prompt || '',
                error: (errorMessage || 'unknown error').substring(0, 200),
            },
            topic: `device_${deviceId}`,
        });
    } catch (e) {
        // silent
    }
}

// ============================================================================
// 7. تشغيل السيرفر
// ============================================================================
const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
    console.log(`   Firebase:    ${firebaseReady ? '✅ ready' : '❌ disabled'}`);
    console.log(`   SendGrid:    ${SENDGRID_KEY ? '✅ ready' : '❌ disabled'}`);
    console.log(`   NOWPayments: ${NOWPAYMENTS_IPN_SECRET ? '✅ ready' : '❌ disabled'}`);
});
