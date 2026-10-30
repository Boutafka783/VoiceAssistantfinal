const express = require('express');
const sgMail = require('@sendgrid/mail');
const crypto = require('crypto');
const admin = require('firebase-admin');
const multer = require('multer'); // تمت الإضافة لاستقبال ملفات الفيديو

const app = express();
app.use(express.json());

// إعداد multer لاستقبال ملفات الفيديو في الذاكرة (حد أقصى 100 ميجابايت)
const upload = multer({ 
    storage: multer.memoryStorage(), 
    limits: { fileSize: 100 * 1024 * 1024 } 
});

// ============================================================================
// 1. متغيرات البيئة
// ============================================================================
const LICENSE_SECRET           = process.env.LICENSE_SECRET;
const SENDGRID_KEY             = process.env.SENDGRID_KEY;
const NOWPAYMENTS_IPN_SECRET   = process.env.NOWPAYMENTS_IPN_SECRET;
const FIREBASE_SERVICE_ACCOUNT = process.env.FIREBASE_SERVICE_ACCOUNT;
const FIREBASE_STORAGE_BUCKET  = process.env.FIREBASE_STORAGE_BUCKET;
const REPLICATE_TOKEN          = process.env.REPLICATE_TOKEN;
const BASE_URL                 = (process.env.BASE_URL || '').replace(/\/+$/, '');

// معرّفات إصدارات النماذج على Replicate
const REPLICATE_VIDEO_VERSION  = process.env.REPLICATE_VIDEO_VERSION;
const REPLICATE_MUSIC_VERSION  = process.env.REPLICATE_MUSIC_VERSION;
const REPLICATE_EDIT_VIDEO_VERSION = process.env.REPLICATE_EDIT_VIDEO_VERSION; // إضافة: للنموذج الذي يعدل الفيديو

const ALLOW_APP_LICENSE_MARKERS = process.env.ALLOW_APP_LICENSE_MARKERS === 'true';

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
            storageBucket: FIREBASE_STORAGE_BUCKET || `${serviceAccount.project_id}.appspot.com`
        });
        db = admin.firestore();
        bucket = admin.storage().bucket();
        firebaseReady = true;
        console.log("✅ Firebase Admin initialized.");
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

function safeEqual(a, b) {
    const x = Buffer.from(String(a || ''));
    const y = Buffer.from(String(b || ''));
    return x.length === y.length && crypto.timingSafeEqual(x, y);
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
    return safeEqual(expected, m[2]);
}

function isValidDeviceId(deviceId) {
    return typeof deviceId === 'string' && /^[A-Za-z0-9_-]{6,64}$/.test(deviceId);
}

function webhookToken(deviceId, type) {
    return crypto.createHmac('sha256', LICENSE_SECRET)
        .update(`WH|${deviceId}|${type}`).digest('hex').substring(0, 32);
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

async function checkAndIncrementQuota(deviceId, type) {
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
            const err = new Error('Daily limit reached'); err.code = 'DAILY_LIMIT'; throw err;
        }
        const elapsed = Date.now() - (data.lastRequestAt || 0);
        if (elapsed < 60_000) {
            const err = new Error('Cooldown active'); err.code = 'COOLDOWN'; err.waitSeconds = Math.ceil((60_000 - elapsed) / 1000); throw err;
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

        if (!safeEqual(receivedSig, expectedSig)) return res.status(401).send("Invalid signature");

        const { payment_status, order_description, customer_email } = req.body;
        const paymentId = req.body.payment_id ? String(req.body.payment_id) : null;

        if (payment_status !== 'finished' && payment_status !== 'confirmed') {
            return res.status(200).send('Not confirmed yet');
        }

        const emailToSend = customer_email || order_description;
        if (!emailToSend || !emailToSend.includes('@')) return res.status(400).send('Invalid email');

        if (firebaseReady && paymentId) {
            const orderRef = db.collection('orders').doc(paymentId);
            const orderDoc = await orderRef.get();
            if (orderDoc.exists) return res.status(200).send('Already processed');
        }

        const licenseKey = generateLicenseKey();
        if (SENDGRID_KEY) {
            const msg = {
                to: emailToSend,
                from: 'tijara6@gmail.com',
                subject: 'تم تفعيل نسختك المدفوعة من Zevorix AI',
                html: `<h3>كود التفعيل: <strong>${licenseKey}</strong></h3>`,
            };
            await sgMail.send(msg);
        }

        if (firebaseReady && paymentId) {
            await db.collection('orders').doc(paymentId).set({
                email: emailToSend, licenseKey, status: 'issued', createdAt: admin.firestore.FieldValue.serverTimestamp()
            });
        }
        res.status(200).send('License sent successfully');
    } catch (error) {
        res.status(500).send('Error');
    }
});

// ============================================================================
// 6. توليد الفيديو والموسيقى (Endpoints)
// ============================================================================
app.post(['/api/generate', '/api/generate-video', '/api/generate-music'], async (req, res) => {
    const body = req.body || {};
    const prompt = typeof body.prompt === 'string' ? body.prompt.trim() : '';
    const { deviceId, licenseKey } = body;

    let type = body.type;
    if (req.path.endsWith('-video')) type = 'video';
    if (req.path.endsWith('-music')) type = 'music';

    if (prompt.length < 3 || prompt.length > 500) return res.status(400).json({ error: 'Invalid prompt' });
    if (!isValidDeviceId(deviceId) || !['video', 'music'].includes(type)) return res.status(400).json({ error: 'Invalid request' });

    const appMarker = ALLOW_APP_LICENSE_MARKERS && (licenseKey === 'lifetime' || licenseKey === 'subscription');
    if (!isValidLicenseKey(licenseKey) && !appMarker) return res.status(401).json({ error: 'Invalid license' });

    try {
        if (!appMarker) await bindLicenseToDevice(licenseKey, deviceId);
        const quota = await checkAndIncrementQuota(deviceId, type);
        res.status(200).json({ status: 'started', remaining: quota.remaining });

        triggerReplicateAsync(prompt, deviceId, type).catch(err => {
            console.error(`Background error (${type}):`, err.message);
            sendNotification(deviceId, `${type}_error`, { error: 'Generation failed to start' });
        });
    } catch (e) {
        if (e.message === 'LICENSE_BOUND_TO_OTHER_DEVICE') return res.status(403).json({ error: 'License used on another device' });
        if (e.code === 'DAILY_LIMIT') return res.status(429).json({ error: 'Daily limit reached' });
        if (e.code === 'COOLDOWN') return res.status(429).json({ error: 'Please wait', waitSeconds: e.waitSeconds });
        return res.status(500).json({ error: 'Internal error' });
    }
});

// ============================================================================
// 7. تعديل الفيديو (جديد)
// ============================================================================
app.post('/api/edit-video', upload.single('video'), async (req, res) => {
    const { deviceId, licenseKey, prompt } = req.body;
    const file = req.file;

    if (!isValidDeviceId(deviceId)) return res.status(400).json({ error: 'Invalid device' });
    if (!file) return res.status(400).json({ error: 'No video file uploaded' });
    if (!prompt || prompt.length < 3) return res.status(400).json({ error: 'Invalid prompt' });

    const appMarker = ALLOW_APP_LICENSE_MARKERS && (licenseKey === 'lifetime' || licenseKey === 'subscription');
    if (!isValidLicenseKey(licenseKey) && !appMarker) return res.status(401).json({ error: 'Invalid license' });

    try {
        if (!firebaseReady) throw new Error("DB_NOT_READY");
        if (!appMarker) await bindLicenseToDevice(licenseKey, deviceId);
        const quota = await checkAndIncrementQuota(deviceId, 'video');
        res.status(200).json({ status: 'started', remaining: quota.remaining });

        // المعالجة في الخلفية
        processVideoEdit(file, prompt, deviceId).catch(err => {
            console.error("Edit Video Error:", err.message);
            sendNotification(deviceId, 'video_error', { error: 'Edit failed' });
        });

    } catch (e) {
        return res.status(500).json({ error: 'Internal error' });
    }
});

// ============================================================================
// 8. التكامل مع Replicate
// ============================================================================
async function triggerReplicateAsync(prompt, deviceId, type) {
    if (!REPLICATE_TOKEN || !BASE_URL) throw new Error("Missing env vars");
    const configured = type === 'video' ? REPLICATE_VIDEO_VERSION : REPLICATE_MUSIC_VERSION;
    if (!configured) throw new Error(`REPLICATE_${type.toUpperCase()}_VERSION is missing`);
    
    const version = configured.includes(':') ? configured.split(':').pop() : configured;
    const webhookUrl = `${BASE_URL}/webhook/replicate?deviceId=${encodeURIComponent(deviceId)}&type=${type}&token=${webhookToken(deviceId, type)}&prompt=${encodeURIComponent(prompt)}`;

    const response = await fetch('https://api.replicate.com/v1/predictions', {
        method: 'POST',
        headers: { 'Authorization': `Token ${REPLICATE_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ version, input: { prompt }, webhook: webhookUrl, webhook_events_filter: ['completed'] }),
    });

    if (!response.ok) throw new Error(await response.text());
    console.log(`🚀 ${type} job started for ${deviceId}`);
}

async function processVideoEdit(file, prompt, deviceId) {
    if (!REPLICATE_EDIT_VIDEO_VERSION) throw new Error("REPLICATE_EDIT_VIDEO_VERSION is missing");

    // 1. رفع الفيديو الأصلي إلى Firebase Storage
    const originalFileName = `originals/${deviceId}/${Date.now()}.mp4`;
    const bucketFile = bucket.file(originalFileName);
    await bucketFile.save(file.buffer, { contentType: file.mimetype || 'video/mp4' });
    
    const [publicUrl] = await bucketFile.getSignedUrl({
        version: 'v4',
        action: 'read',
        expires: Date.now() + 60 * 60 * 1000 // صالح لمدة ساعة
    });

    // 2. إرسال الطلب إلى Replicate (النموذج المخصص لتعديل الفيديو)
    const version = REPLICATE_EDIT_VIDEO_VERSION.includes(':') ? REPLICATE_EDIT_VIDEO_VERSION.split(':').pop() : REPLICATE_EDIT_VIDEO_VERSION;
    const webhookUrl = `${BASE_URL}/webhook/replicate?deviceId=${encodeURIComponent(deviceId)}&type=video&token=${webhookToken(deviceId, 'video')}&prompt=${encodeURIComponent(prompt)}`;

    const response = await fetch('https://api.replicate.com/v1/predictions', {
        method: 'POST',
        headers: { 'Authorization': `Token ${REPLICATE_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
            version,
            input: { 
                prompt: prompt,
                video: publicUrl // معظم نماذج التعديل تستخدم حقل video أو init_video
            },
            webhook: webhookUrl,
            webhook_events_filter: ['completed']
        }),
    });

    if (!response.ok) throw new Error(await response.text());
    console.log(`🚀 Edit video job started for ${deviceId}`);
}

// ============================================================================
// 9. استقبال النتيجة من Replicate -> Firebase Storage -> Push Notification
// ============================================================================
app.post('/webhook/replicate', async (req, res) => {
    const { deviceId, type, prompt, token } = req.query;

    if (!isValidDeviceId(deviceId) || !['video', 'music'].includes(type) || !safeEqual(token, webhookToken(deviceId, type))) {
        return res.status(401).send('Unauthorized');
    }

    const { output, status, error } = req.body || {};
    res.status(200).send('OK');

    if (status !== 'succeeded' || !output) {
        return sendNotification(deviceId, `${type}_error`, { error: String(error || 'Generation failed') });
    }

    const remoteUrl = Array.isArray(output) ? output[0] : output;
    if (typeof remoteUrl !== 'string' || !remoteUrl.startsWith('https://')) {
        return sendNotification(deviceId, `${type}_error`, { error: 'Invalid output' });
    }
    if (!firebaseReady) return;

    const ext = type === 'video' ? 'mp4' : 'mp3';
    const fileName = `${type}s/${deviceId}/${Date.now()}.${ext}`;

    try {
        const download = await fetch(remoteUrl);
        if (!download.ok) throw new Error(`Download failed: HTTP ${download.status}`);
        const buffer = Buffer.from(await download.arrayBuffer());

        const bucketFile = bucket.file(fileName);
        await bucketFile.save(buffer, { contentType: type === 'video' ? 'video/mp4' : 'audio/mpeg' });

        const [signedUrl] = await bucketFile.getSignedUrl({
            version: 'v4',
            action: 'read',
            expires: Date.now() + 7 * 24 * 3600 * 1000 - 5 * 60 * 1000
        });

        await db.collection(`${type}s`).doc(deviceId).collection('items').add({
            url: signedUrl, prompt: prompt || '', createdAt: admin.firestore.FieldValue.serverTimestamp()
        });

        await sendNotification(deviceId, `${type}_ready`, { url: signedUrl, prompt: String(prompt || '') });
        console.log(`✅ ${type} ready for ${deviceId}`);

    } catch (err) {
        console.error(`❌ Upload failed for ${deviceId}:`, err.message);
        await sendNotification(deviceId, `${type}_error`, { error: 'Failed to save file' });
    }
});

// ============================================================================
// 10. إشعارات FCM
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
// 11. تشغيل السيرفر
// ============================================================================
const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
});
