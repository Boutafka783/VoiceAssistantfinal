const express = require('express');
const sgMail = require('@sendgrid/mail');
const crypto = require('crypto');
const admin = require('firebase-admin');
const multer = require('multer');
const fs = require('fs'); 

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
const REPLICATE_VIDEO_VERSION      = process.env.REPLICATE_VIDEO_VERSION;
const REPLICATE_MUSIC_VERSION      = process.env.REPLICATE_MUSIC_VERSION;
const REPLICATE_EDIT_VIDEO_VERSION = process.env.REPLICATE_EDIT_VIDEO_VERSION;

// للاختبار: يسمح بكلمة lifetime لتجاوز النقاط
const ALLOW_APP_LICENSE_MARKERS = process.env.ALLOW_APP_LICENSE_MARKERS === 'true';

if (!LICENSE_SECRET) {
    console.error("FATAL: LICENSE_SECRET is missing!");
    process.exit(1);
}
if (SENDGRID_KEY) sgMail.setApiKey(SENDGRID_KEY);

// ============================================================================
// 2. تهيئة Firebase Admin (تقرأ من المفتاح المشفر Base64)
// ============================================================================
let firebaseReady = false;
let db, bucket;

try {
    let serviceAccount = null;

    if (process.env.FIREBASE_KEY_BASE64) {
        const decoded = Buffer.from(process.env.FIREBASE_KEY_BASE64, 'base64').toString('utf8');
        serviceAccount = JSON.parse(decoded);
        console.log("✅ Found Firebase key in Base64 variable.");
    } 
    else if (fs.existsSync('/etc/secrets/firebase-key.json')) {
        const fileContent = fs.readFileSync('/etc/secrets/firebase-key.json', 'utf8');
        serviceAccount = JSON.parse(fileContent);
        console.log("✅ Found Firebase key in Secret File.");
    }
    else if (FIREBASE_SERVICE_ACCOUNT) {
        serviceAccount = JSON.parse(FIREBASE_SERVICE_ACCOUNT);
        if (serviceAccount.private_key) {
            serviceAccount.private_key = serviceAccount.private_key.replace(/\\n/g, '\n');
        }
        console.log("✅ Found Firebase key in Environment Variables.");
    }

    if (serviceAccount) {
        admin.initializeApp({
            credential: admin.credential.cert(serviceAccount),
            storageBucket: FIREBASE_STORAGE_BUCKET || `${serviceAccount.project_id}.appspot.com`
        });
        db = admin.firestore();
        bucket = admin.storage().bucket();
        firebaseReady = true;
        console.log("🔥 Firebase Admin initialized successfully.");
    } else {
        console.warn("⚠️ Firebase key not found.");
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

function isValidJobId(jobId) {
    return typeof jobId === 'string' && /^[A-Za-z0-9]{10,40}$/.test(jobId);
}

// التوكن الآن مرتبط أيضاً بمعرّف المهمة (jobId)
function webhookToken(deviceId, type, jobId) {
    return crypto.createHmac('sha256', LICENSE_SECRET)
        .update(`WH|${deviceId}|${type}|${jobId || ''}`).digest('hex').substring(0, 32);
}

// ----------------------------------------------------------------------------
// خصم النقاط + إنشاء سجل مهمة (job) في نفس العملية (Transaction)
// ----------------------------------------------------------------------------
async function deductCredits(licenseKey, deviceId, cost, type, prompt) {
    if (!firebaseReady) throw new Error("DB_NOT_READY");
    const ref = db.collection('licenses').doc(licenseKey);
    const jobRef = db.collection('jobs').doc();

    const remaining = await db.runTransaction(async (tx) => {
        const doc = await tx.get(ref);
        if (!doc.exists) throw new Error('INVALID_LICENSE');
        
        const data = doc.data();
        
        if (data.deviceId && data.deviceId !== deviceId) {
            throw new Error('LICENSE_BOUND_TO_OTHER_DEVICE');
        }
        
        const currentCredits = data.credits || 0;
        if (currentCredits < cost) {
            throw new Error('INSUFFICIENT_CREDITS');
        }

        tx.update(ref, {
            deviceId: deviceId,
            credits: admin.firestore.FieldValue.increment(-cost),
            lastUsedAt: admin.firestore.FieldValue.serverTimestamp()
        });

        tx.set(jobRef, {
            licenseKey,
            deviceId,
            type,
            cost,
            prompt,
            status: 'pending',
            refunded: false,
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });
        
        return currentCredits - cost;
    });

    return { remaining, jobId: jobRef.id };
}

async function createFreeJob(deviceId, type, prompt) {
    if (!firebaseReady) return null;
    const jobRef = db.collection('jobs').doc();
    await jobRef.set({
        licenseKey: null,
        deviceId,
        type,
        cost: 0,
        prompt,
        status: 'pending',
        refunded: false,
        createdAt: admin.firestore.FieldValue.serverTimestamp()
    });
    return jobRef.id;
}

// ----------------------------------------------------------------------------
// تسجيل فشل المهمة + إرجاع النقاط تلقائياً
// ----------------------------------------------------------------------------
async function failJob(jobId, reason) {
    if (!firebaseReady || !jobId) return { refunded: false };
    const jobRef = db.collection('jobs').doc(jobId);
    const failureRef = db.collection('failures').doc();

    return await db.runTransaction(async (tx) => {
        const jobDoc = await tx.get(jobRef);
        if (!jobDoc.exists) return { refunded: false };

        const job = jobDoc.data();
        if (job.status === 'failed') return { refunded: !!job.refunded }; 

        let licenseRef = null;
        if (job.licenseKey && job.cost > 0) {
            licenseRef = db.collection('licenses').doc(job.licenseKey);
        }

        if (licenseRef) {
            tx.update(licenseRef, {
                credits: admin.firestore.FieldValue.increment(job.cost)
            });
        }

        tx.update(jobRef, {
            status: 'failed',
            refunded: !!licenseRef,
            failReason: String(reason).substring(0, 500),
            failedAt: admin.firestore.FieldValue.serverTimestamp()
        });

        tx.set(failureRef, {
            jobId,
            deviceId: job.deviceId,
            licenseKey: job.licenseKey || null,
            type: job.type,
            cost: job.cost,
            prompt: job.prompt || '',
            reason: String(reason).substring(0, 500),
            refunded: !!licenseRef,
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });

        return { refunded: !!licenseRef };
    });
}

async function handleFailure(jobId, deviceId, type, reason, publicMessage) {
    let refunded = false;
    try {
        const result = await failJob(jobId, reason);
        refunded = result.refunded;
    } catch (e) {
        console.error(`❌ failJob error (${jobId}):`, e.message);
    }
    await sendNotification(deviceId, `${type}_error`, {
        error: publicMessage,
        refunded: String(refunded)
    });
}

// ============================================================================
// 4. مسارات الخدمة
// ============================================================================
app.get('/', (req, res) => {
    res.json({ status: 'ok', features: { firebase: firebaseReady, replicate: !!REPLICATE_TOKEN } });
});

app.post('/api/balance', async (req, res) => {
    const { licenseKey, deviceId } = req.body;
    if (!isValidLicenseKey(licenseKey) || !isValidDeviceId(deviceId)) {
        return res.status(400).json({ error: 'Invalid request' });
    }
    try {
        const doc = await db.collection('licenses').doc(licenseKey).get();
        if (!doc.exists) return res.status(404).json({ error: 'License not found' });
        
        const data = doc.data();
        if (data.deviceId && data.deviceId !== deviceId) {
            return res.status(403).json({ error: 'License used on another device' });
        }
        res.json({ credits: data.credits || 0 });
    } catch (e) {
        res.status(500).json({ error: 'Internal error' });
    }
});

app.post('/paymentWebhook', async (req, res) => {
    try {
        const receivedSig = req.headers['x-nowpayments-sig'];
        const sortedBody = JSON.stringify(deepSort(req.body));
        if (!NOWPAYMENTS_IPN_SECRET) return res.status(500).send("Config error");

        const expectedSig = crypto.createHmac('sha512', NOWPAYMENTS_IPN_SECRET)
            .update(sortedBody).digest('hex');

        if (!safeEqual(receivedSig, expectedSig)) return res.status(401).send("Invalid signature");

        const { payment_status, order_description, customer_email, price_amount } = req.body;
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

        let creditsToAdd = 0;
        const amount = parseFloat(price_amount || 0);
        if (amount >= 130) creditsToAdd = 1400;
        else if (amount >= 65) creditsToAdd = 650;
        else if (amount >= 30) creditsToAdd = 300;
        else if (amount >= 10) creditsToAdd = 100;
        else return res.status(400).send('Amount too low');

        const licenseKey = generateLicenseKey();

        if (SENDGRID_KEY) {
            const msg = {
                to: emailToSend,
                from: 'tijara6@gmail.com',
                subject: 'تم تفعيل نسختك المدفوعة من Zevorix AI',
                html: `<h3>شكراً لشرائك!</h3>
                       <p>كود التفعيل الخاص بك: <strong>${licenseKey}</strong></p>
                       <p>لقد تم إضافة <strong>${creditsToAdd} نقطة</strong> لرصيدك.</p>`,
            };
            await sgMail.send(msg);
        }

        if (firebaseReady) {
            if (paymentId) {
                await db.collection('orders').doc(paymentId).set({
                    email: emailToSend, licenseKey, status: 'issued', createdAt: admin.firestore.FieldValue.serverTimestamp()
                });
            }
            await db.collection('licenses').doc(licenseKey).set({
                credits: creditsToAdd,
                createdAt: admin.firestore.FieldValue.serverTimestamp()
            });
        }
        
        res.status(200).send('License sent successfully');
    } catch (error) {
        console.error('Payment webhook error:', error.message);
        res.status(500).send('Error');
    }
});

app.post(['/api/generate-video', '/api/generate-music'], async (req, res) => {
    const body = req.body || {};
    const prompt = typeof body.prompt === 'string' ? body.prompt.trim() : '';
    const { deviceId, licenseKey } = body;
    const type = req.path.endsWith('-video') ? 'video' : 'music';

    if (prompt.length < 3 || prompt.length > 500) return res.status(400).json({ error: 'Invalid prompt' });
    if (!isValidDeviceId(deviceId)) return res.status(400).json({ error: 'Invalid device' });

    const cost = type === 'video' ? 15 : 5; 
    const appMarker = ALLOW_APP_LICENSE_MARKERS && (licenseKey === 'lifetime' || licenseKey === 'subscription');

    try {
        let remaining = 9999;
        let jobId = null;
        if (appMarker) {
            jobId = await createFreeJob(deviceId, type, prompt);
        } else {
            if (!isValidLicenseKey(licenseKey)) return res.status(401).json({ error: 'Invalid license' });
            ({ remaining, jobId } = await deductCredits(licenseKey, deviceId, cost, type, prompt));
        }

        res.status(200).json({ status: 'started', remaining });

        triggerReplicateAsync(prompt, deviceId, type, jobId).catch(err => {
            console.error(`Background error (${type}):`, err.message);
            handleFailure(jobId, deviceId, type, `Start failed: ${err.message}`, 'Generation failed to start');
        });
    } catch (e) {
        if (e.message === 'INSUFFICIENT_CREDITS') return res.status(402).json({ error: 'Insufficient credits' });
        if (e.message === 'LICENSE_BOUND_TO_OTHER_DEVICE') return res.status(403).json({ error: 'License used on another device' });
        if (e.message === 'INVALID_LICENSE') return res.status(401).json({ error: 'Invalid license' });
        console.error('Generate route error:', e.message);
        return res.status(500).json({ error: 'Internal error' });
    }
});

app.post('/api/edit-video', upload.single('video'), async (req, res) => {
    const body = req.body || {};
    const deviceId = body.deviceId;
    const licenseKey = body.licenseKey;
    const prompt = typeof body.prompt === 'string' ? body.prompt.trim() : '';
    const file = req.file;

    if (!isValidDeviceId(deviceId)) return res.status(400).json({ error: 'Invalid device' });
    if (!file) return res.status(400).json({ error: 'No video file uploaded' });
    if (prompt.length < 3 || prompt.length > 500) return res.status(400).json({ error: 'Invalid prompt' });

    const cost = 15; 
    const appMarker = ALLOW_APP_LICENSE_MARKERS && (licenseKey === 'lifetime' || licenseKey === 'subscription');

    try {
        let remaining = 9999;
        let jobId = null;
        if (appMarker) {
            jobId = await createFreeJob(deviceId, 'video', prompt);
        } else {
            if (!isValidLicenseKey(licenseKey)) return res.status(401).json({ error: 'Invalid license' });
            ({ remaining, jobId } = await deductCredits(licenseKey, deviceId, cost, 'video', prompt));
        }

        res.status(200).json({ status: 'started', remaining });

        processVideoEdit(file, prompt, deviceId, jobId).catch(err => {
            console.error("Edit Video Error:", err.message);
            handleFailure(jobId, deviceId, 'video', `Edit failed: ${err.message}`, 'Edit failed');
        });
    } catch (e) {
        if (e.message === 'INSUFFICIENT_CREDITS') return res.status(402).json({ error: 'Insufficient credits' });
        if (e.message === 'LICENSE_BOUND_TO_OTHER_DEVICE') return res.status(403).json({ error: 'License used on another device' });
        if (e.message === 'INVALID_LICENSE') return res.status(401).json({ error: 'Invalid license' });
        console.error('Edit route error:', e.message);
        return res.status(500).json({ error: 'Internal error' });
    }
});

app.use((err, req, res, next) => {
    if (err instanceof multer.MulterError) {
        if (err.code === 'LIMIT_FILE_SIZE') return res.status(413).json({ error: 'Video too large (max 100MB)' });
        return res.status(400).json({ error: 'Upload error' });
    }
    return res.status(500).json({ error: 'Internal error' });
});

// ============================================================================
// 5. التكامل مع Replicate
// ============================================================================
function buildWebhookUrl(deviceId, type, jobId, prompt) {
    return `${BASE_URL}/webhook/replicate?deviceId=${encodeURIComponent(deviceId)}&type=${type}&jobId=${encodeURIComponent(jobId || '')}&token=${webhookToken(deviceId, type, jobId)}&prompt=${encodeURIComponent(prompt)}`;
}

async function triggerReplicateAsync(prompt, deviceId, type, jobId) {
    if (!REPLICATE_TOKEN || !BASE_URL) throw new Error("Missing env vars");
    const configured = type === 'video' ? REPLICATE_VIDEO_VERSION : REPLICATE_MUSIC_VERSION;
    if (!configured) throw new Error(`REPLICATE_${type.toUpperCase()}_VERSION is missing`);

    const version = configured.includes(':') ? configured.split(':').pop() : configured;
    const webhookUrl = buildWebhookUrl(deviceId, type, jobId, prompt);

    const response = await fetch('https://api.replicate.com/v1/predictions', {
        method: 'POST',
        headers: { 'Authorization': `Token ${REPLICATE_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ version, input: { prompt }, webhook: webhookUrl, webhook_events_filter: ['completed'] }),
    });

    if (!response.ok) throw new Error(await response.text());
    console.log(`🚀 ${type} job started for ${deviceId}`);
}

async function processVideoEdit(file, prompt, deviceId, jobId) {
    if (!REPLICATE_TOKEN || !BASE_URL) throw new Error("Missing env vars");
    if (!REPLICATE_EDIT_VIDEO_VERSION) throw new Error("REPLICATE_EDIT_VIDEO_VERSION is missing");

    const originalFileName = `originals/${deviceId}/${Date.now()}.mp4`;
    const bucketFile = bucket.file(originalFileName);
    await bucketFile.save(file.buffer, { contentType: file.mimetype || 'video/mp4' });

    const [publicUrl] = await bucketFile.getSignedUrl({
        version: 'v4',
        action: 'read',
        expires: Date.now() + 60 * 60 * 1000 
    });

    const version = REPLICATE_EDIT_VIDEO_VERSION.includes(':') ? REPLICATE_EDIT_VIDEO_VERSION.split(':').pop() : REPLICATE_EDIT_VIDEO_VERSION;
    const webhookUrl = buildWebhookUrl(deviceId, 'video', jobId, prompt);

    const response = await fetch('https://api.replicate.com/v1/predictions', {
        method: 'POST',
        headers: { 'Authorization': `Token ${REPLICATE_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
            version,
            input: { prompt: prompt, video: publicUrl },
            webhook: webhookUrl,
            webhook_events_filter: ['completed']
        }),
    });

    if (!response.ok) throw new Error(await response.text());
    console.log(`🚀 Edit video job started for ${deviceId}`);
}

// ============================================================================
// 6. استقبال النتيجة من Replicate
// ============================================================================
app.post('/webhook/replicate', async (req, res) => {
    const { deviceId, type, prompt, token } = req.query;
    const jobId = typeof req.query.jobId === 'string' ? req.query.jobId : '';

    if (!isValidDeviceId(deviceId) || !['video', 'music'].includes(type)) {
        return res.status(401).send('Unauthorized');
    }
    if (jobId && !isValidJobId(jobId)) {
        return res.status(401).send('Unauthorized');
    }
    if (!safeEqual(token, webhookToken(deviceId, type, jobId))) {
        return res.status(401).send('Unauthorized');
    }

    const { output, status, error } = req.body || {};
    res.status(200).send('OK');

    if (status !== 'succeeded' || !output) {
        return handleFailure(jobId, deviceId, type, `Replicate status=${status}: ${error || 'no output'}`, 'Generation failed');
    }

    const remoteUrl = Array.isArray(output) ? output[0] : output;
    if (typeof remoteUrl !== 'string' || !remoteUrl.startsWith('https://')) {
        return handleFailure(jobId, deviceId, type, 'Invalid output URL from Replicate', 'Invalid output');
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

        if (jobId) {
            await db.collection('jobs').doc(jobId).update({
                status: 'completed',
                completedAt: admin.firestore.FieldValue.serverTimestamp()
            }).catch(e => console.error('Job update error:', e.message));
        }

        await sendNotification(deviceId, `${type}_ready`, { url: signedUrl, prompt: String(prompt || '') });
        console.log(`✅ ${type} ready for ${deviceId}`);

    } catch (err) {
        console.error(`❌ Upload failed for ${deviceId}:`, err.message);
        await handleFailure(jobId, deviceId, type, `Save failed: ${err.message}`, 'Failed to save file');
    }
});

// ============================================================================
// 7. إشعارات FCM
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
// 8. تشغيل السيرفر
// ============================================================================
const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
});
