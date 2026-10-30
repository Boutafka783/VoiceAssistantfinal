const express = require('express');
const sgMail = require('@sendgrid/mail');
const crypto = require('crypto');
const admin = require('firebase-admin');

const app = express();
app.use(express.json());

// ============================================================================
// 1. متغيرات البيئة
// ============================================================================
const LICENSE_SECRET          = process.env.LICENSE_SECRET;
const SENDGRID_KEY            = process.env.SENDGRID_KEY;
const NOWPAYMENTS_IPN_SECRET  = process.env.NOWPAYMENTS_IPN_SECRET;
const FIREBASE_SERVICE_ACCOUNT = process.env.FIREBASE_SERVICE_ACCOUNT;
const REPLICATE_TOKEN         = process.env.REPLICATE_TOKEN;
const BASE_URL                = process.env.BASE_URL; // مثل https://your-app.onrender.com

if (!LICENSE_SECRET) {
    console.error("FATAL: LICENSE_SECRET is missing!");
    process.exit(1);
}
if (SENDGRID_KEY) sgMail.setApiKey(SENDGRID_KEY);

// ============================================================================
// 2. تهيئة Firebase Admin
// ============================================================================
let firebaseReady = false;
let db, bucket;

try {
    if (FIREBASE_SERVICE_ACCOUNT) {
        const serviceAccount = JSON.parse(FIREBASE_SERVICE_ACCOUNT);
        admin.initializeApp({
            credential: admin.credential.cert(serviceAccount),
            storageBucket: `${serviceAccount.project_id}.appspot.com`
        });
        db = admin.firestore();
        bucket = admin.storage().bucket();
        firebaseReady = true;
        console.log("✅ Firebase Admin initialized (Firestore + Storage + Messaging).");
    } else {
        console.warn("⚠️ FIREBASE_SERVICE_ACCOUNT not set.");
    }
} catch (e) {
    console.error("❌ Firebase Admin init failed:", e.message);
}

// ============================================================================
// 3. دوال مساعدة
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
    for (let i = 0; i < 6; i++) nonce += ALPHABET.charAt(bytes[i] % ALPHABET.length);
    const signature = crypto.createHmac('sha256', LICENSE_SECRET)
        .update(`ZEV|${nonce}`).digest('hex').toUpperCase().substring(0, 8);
    return `ZEV-${nonce}-${signature}`;
}

function isValidLicenseKey(key) {
    if (!key || typeof key !== 'string') return false;
    const m = key.match(/^ZEV-([A-Z2-7]{6})-([A-F0-9]{8})$/);
    if (!m) return false;
    const expected = crypto.createHmac('sha256', LICENSE_SECRET)
        .update(`ZEV|${m[1]}`).digest('hex').toUpperCase().substring(0, 8);
    return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(m[2]));
}

// ============================================================================
// 4. منطق Firestore (الأكواد والحصص)
// ============================================================================
async function bindLicenseToDevice(licenseKey, deviceId) {
    if (!firebaseReady) throw new Error("DB_NOT_READY");
    const ref = db.collection('licenses').doc(licenseKey);
    
    return await db.runTransaction(async (tx) => {
        const doc = await tx.get(ref);
        if (!doc.exists) {
            tx.set(ref, {
                deviceId,
                firstUsedAt: admin.firestore.FieldValue.serverTimestamp(),
                lastUsedAt: admin.firestore.FieldValue.serverTimestamp()
            });
            return true;
        }
        const data = doc.data();
        if (data.deviceId !== deviceId) throw new Error('LICENSE_BOUND_TO_OTHER_DEVICE');
        
        tx.update(ref, { lastUsedAt: admin.firestore.FieldValue.serverTimestamp() });
        return true;
    });
}

async function checkAndIncrementQuota(deviceId, type) { // type: 'video' أو 'music'
    if (!firebaseReady) throw new Error("DB_NOT_READY");
    const today = new Date().toISOString().slice(0, 10);
    const quotaRef = db.collection('quotas').doc(deviceId);
    const DAILY_LIMIT = 50;

    return await db.runTransaction(async (tx) => {
        const doc = await tx.get(quotaRef);
        
        if (!doc.exists || doc.data().day !== today) {
            tx.set(quotaRef, { day: today, used: 1, lastRequestAt: Date.now() });
            return { used: 1, remaining: DAILY_LIMIT - 1 };
        }

        const data = doc.data();
        if (data.used >= DAILY_LIMIT) {
            const err = new Error('Daily limit reached');
            err.code = 'DAILY_LIMIT';
            throw err;
        }

        const elapsed = Date.now() - (data.lastRequestAt || 0);
        if (elapsed < 60_000) {
            const err = new Error('Cooldown active');
            err.code = 'COOLDOWN';
            err.waitSeconds = Math.ceil((60_000 - elapsed) / 1000);
            throw err;
        }

        tx.update(quotaRef, { used: data.used + 1, lastRequestAt: Date.now() });
        return { used: data.used + 1, remaining: DAILY_LIMIT - data.used - 1 };
    });
}

// ============================================================================
// 5. مسارات الخدمة (Health & Webhooks)
// ============================================================================
app.get('/', (req, res) => {
    res.json({ status: 'ok', features: { firebase: firebaseReady, replicate: !!REPLICATE_TOKEN } });
});

app.post('/paymentWebhook', async (req, res) => {
    try {
        const receivedSig = req.headers['x-nowpayments-sig'];
        const sortedBody = JSON.stringify(deepSort(req.body));
        
        if (!NOWPAYMENTS_IPN_SECRET) return res.status(500).send("Config error");
        
        const expectedSig = crypto.createHmac('sha512', NOWPAYMENTS_IPN_SECRET)
            .update(sortedBody).digest('hex');
            
        if (receivedSig !== expectedSig) return res.status(401).send("Invalid signature");

        const { payment_status, order_description, customer_email, payment_id } = req.body;
        if (payment_status !== 'finished' && payment_status !== 'confirmed') {
            return res.status(200).send('Not confirmed yet');
        }

        const emailToSend = customer_email || order_description;
        if (!emailToSend || !emailToSend.includes('@')) return res.status(400).send('Invalid email');

        // 1. منع التكرار (Idempotency)
        if (firebaseReady && payment_id) {
            const orderRef = db.collection('orders').doc(payment_id);
            const orderDoc = await orderRef.get();
            if (orderDoc.exists) return res.status(200).send('Already processed');
        }

        // 2. توليد الكود وإرساله
        const licenseKey = generateLicenseKey();
        const msg = {
            to: emailToSend,
            from: 'tijara6@gmail.com',
            subject: 'تم تفعيل نسختك المدفوعة من Zevorix AI',
            html: `<div dir="rtl" style="font-family: Arial, sans-serif;">
                     <h3>شكراً لشرائك Zevorix AI!</h3>
                     <p>كود التفعيل الخاص بك هو: </p>
                     <h2 style="color: #4F5BD5; font-family: monospace;">${licenseKey}</h2>
                   </div>`,
        };
        await sgMail.send(msg);

        // 3. حفظ الطلب في قاعدة البيانات
        if (firebaseReady && payment_id) {
            await db.collection('orders').doc(payment_id).set({
                email: emailToSend,
                licenseKey,
                status: 'issued',
                createdAt: admin.firestore.FieldValue.serverTimestamp()
            });
        }

        console.log(`✅ License sent to ${emailToSend} | Key: ${licenseKey}`);
        res.status(200).send('License sent successfully');
    } catch (error) {
        console.error("Webhook error:", error);
        res.status(500).send('Error');
    }
});

// ============================================================================
// 6. توليد الفيديو والموسيقى (Endpoints)
// ============================================================================
app.post('/api/generate', async (req, res) => {
    const { prompt, deviceId, licenseKey, type } = req.body || {}; // type: 'video' | 'music'

    if (!prompt || prompt.trim().length < 3) return res.status(400).json({ error: 'Invalid prompt' });
    if (!deviceId || !['video', 'music'].includes(type)) return res.status(400).json({ error: 'Invalid request' });
    if (!isValidLicenseKey(licenseKey)) return res.status(401).json({ error: 'Invalid license' });

    try {
        // 1. ربط الكود بالجهاز (لمنع المشاركة)
        await bindLicenseToDevice(licenseKey, deviceId);
        
        // 2. فحص الحصة والكول داون
        const quota = await checkAndIncrementQuota(deviceId, type);
        
        res.status(200).json({ status: 'started', remaining: quota.remaining });

        // 3. التوليد في الخلفية (بدون حجب الرد)
        triggerReplicateAsync(prompt, deviceId, type).catch(err => 
            console.error(`Background error (${type}):`, err.message));

    } catch (e) {
        if (e.message === 'LICENSE_BOUND_TO_OTHER_DEVICE') return res.status(403).json({ error: 'License used on another device' });
        if (e.code === 'DAILY_LIMIT') return res.status(429).json({ error: 'Daily limit reached' });
        if (e.code === 'COOLDOWN') return res.status(429).json({ error: 'Please wait', waitSeconds: e.waitSeconds });
        return res.status(500).json({ error: 'Internal error' });
    }
});

// ============================================================================
// 7. التكامل مع Replicate
// ============================================================================
async function triggerReplicateAsync(prompt, deviceId, type) {
    if (!REPLICATE_TOKEN || !BASE_URL) {
        throw new Error("REPLICATE_TOKEN or BASE_URL missing in env vars");
    }

    // حدد النموذج بناءً على النوع (يمكنك تغيير الـ Version Hash لاحقاً)
    const version = type === 'video' 
        ? 'minimax/video-01:YOUR_VIDEO_MODEL_VERSION_HASH' // استبدلها بالـ hash الفعلي
        : 'meta/musicgen:YOUR_MUSIC_MODEL_VERSION_HASH';   // استبدلها بالـ hash الفعلي

    const webhookUrl = `${BASE_URL}/webhook/replicate?deviceId=${deviceId}&type=${type}&prompt=${encodeURIComponent(prompt)}`;

    const response = await fetch('https://api.replicate.com/v1/predictions', {
        method: 'POST',
        headers: {
            'Authorization': `Token ${REPLICATE_TOKEN}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            version,
            input: { prompt },
            webhook: webhookUrl,
            webhook_events_filter: ['completed']
        }),
    });

    if (!response.ok) throw new Error(`Replicate API error: ${await response.text()}`);
    console.log(`🚀 ${type} job started for device ${deviceId}`);
}

// ============================================================================
// 8. استقبال النتيجة من Replicate -> Firebase Storage -> Push Notification
// ============================================================================
app.post('/webhook/replicate', async (req, res) => {
    const { deviceId, type, prompt } = req.query;
    const { output, status, error } = req.body;

    res.status(200).send('OK'); // نرد فوراً لـ Replicate

    if (status !== 'succeeded' || !output) {
        console.error(`❌ Replicate failed for ${deviceId}:`, error);
        return sendNotification(deviceId, `${type}_error`, { error: error || 'Generation failed' });
    }

    const remoteUrl = Array.isArray(output) ? output[0] : output;
    const ext = type === 'video' ? 'mp4' : 'mp3';
    const fileName = `${type}s/${deviceId}/${Date.now()}.${ext}`;

    try {
        // 1. تحميل الملف ورفعه إلى Firebase Storage
        const bucketFile = bucket.file(fileName);
        await bucketFile.save(await (await fetch(remoteUrl)).buffer(), { contentType: type === 'video' ? 'video/mp4' : 'audio/mpeg' });
        
        // 2. توليد رابط دائم (صلاحيته 7 أيام)
        const [signedUrl] = await bucketFile.getSignedUrl({
            action: 'read',
            expires: Date.now() + 7 * 24 * 3600 * 1000
        });

        // 3. حفظ السجل في Firestore
        await db.collection(`${type}s`).doc(deviceId).collection('items').add({
            url: signedUrl,
            prompt: prompt,
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });

        // 4. إرسال إشعار للمستخدم
        await sendNotification(deviceId, `${type}_ready`, { url: signedUrl, prompt });
        console.log(`✅ ${type} ready for ${deviceId}: ${signedUrl}`);

    } catch (err) {
        console.error(`❌ Upload failed for ${deviceId}:`, err.message);
        await sendNotification(deviceId, `${type}_error`, { error: 'Failed to save file' });
    }
});

// ============================================================================
// 9. إشعارات FCM
// ============================================================================
async function sendNotification(deviceId, type, data) {
    if (!firebaseReady) return;
    try {
        await admin.messaging().send({
            data: { type, ...data },
            topic: `device_${deviceId}`,
            android: { priority: 'high', ttl: 24 * 60 * 60 * 1000 },
        });
        console.log(`📱 Notification (${type}) sent to device_${deviceId}`);
    } catch (e) {
        console.error(`Notification error:`, e.message);
    }
}

// ============================================================================
// 10. تشغيل السيرفر
// ============================================================================
const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
    console.log(`   Replicate: ${REPLICATE_TOKEN ? '✅' : '❌'}`);
    console.log(`   Firebase:  ${firebaseReady ? '✅' : '❌'}`);
});
