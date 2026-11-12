#!/usr/bin/env node
// ══════════════════════════════════════════════════════════════════════════════
// Zevorix AI & Gradiometer — Backend v8
// Production-ready: rate limits · SSRF guard · fixed models · TTS credits
//                 · no-loopback circuit · trust proxy · async refund
//
// Dependencies: npm install googleapis   (Google Play Developer API — credit packs)
// Play Store env: PLAY_SERVICE_ACCOUNT (JSON) · PLAY_PACKAGE_NAME (applicationId) ·
//                 SUPPORT_EMAIL (shown on /privacy and /delete-data) · APP_NAME (optional)
// Free/paid switch: Firebase Remote Config parameter is_payment_enabled (fallback: Firestore config/app), cached 60 s.
// Public pages for Play Console: GET /privacy (privacy policy URL) · GET /delete-data (data deletion URL)
// ══════════════════════════════════════════════════════════════════════════════

'use strict';

const express = require('express');
const crypto = require('crypto');
const admin = require('firebase-admin');

// Google Play Developer API (Service Account) — verifies and consumes credit-pack purchases.
let androidPublisher = null;
try {
    const { google } = require('googleapis');
    const playCreds = JSON.parse(process.env.PLAY_SERVICE_ACCOUNT || '{}');
    if (playCreds.client_email && playCreds.private_key) {
        const auth = new google.auth.GoogleAuth({
            credentials: playCreds,
            scopes: ['https://www.googleapis.com/auth/androidpublisher']
        });
        androidPublisher = google.androidpublisher({ version: 'v3', auth });
        console.log('✅ Google Play Developer API ready');
    } else {
        console.warn('⚠️ Play API not configured: PLAY_SERVICE_ACCOUNT missing');
    }
} catch (e) {
    console.warn('⚠️ Play API not configured:', e.message);
}
const multer = require('multer');
const fs = require('fs');
const nacl = require('tweetnacl');
const dns = require('dns').promises;
const net = require('net');

process.on('uncaughtException', (err) => console.error('❌ CRITICAL:', err.message, err.stack));
process.on('unhandledRejection', (reason) => console.error('❌ UNHANDLED:', reason));

const app = express();
// v8: Trust the first proxy (Render / Cloudflare) so req.ip is the real client IP.
// This makes req.ip safe even if the client sends a fake X-Forwarded-For header.
app.set('trust proxy', 1);
app.use(express.json({ limit: '25mb' }));

const upload = multer({
    storage: multer.memoryStorage(),
    limits: { fileSize: 100 * 1024 * 1024 }
});

// ============================================================================
// 1. Environment
// ============================================================================
const LICENSE_SECRET           = process.env.LICENSE_SECRET;
const ED25519_PRIVATE_KEY_RAW  = (process.env.ED25519_PRIVATE_KEY || '').trim();
const FIREBASE_SERVICE_ACCOUNT = process.env.FIREBASE_SERVICE_ACCOUNT;
const FIREBASE_STORAGE_BUCKET  = process.env.FIREBASE_STORAGE_BUCKET;
const REPLICATE_TOKEN          = process.env.REPLICATE_TOKEN;
const BASE_URL                 = (process.env.BASE_URL || '').replace(/\/+$/, '');

const REPLICATE_VIDEO_VERSION      = process.env.REPLICATE_VIDEO_VERSION;
const REPLICATE_MUSIC_VERSION      = process.env.REPLICATE_MUSIC_VERSION;
const REPLICATE_EDIT_VIDEO_VERSION = process.env.REPLICATE_EDIT_VIDEO_VERSION;

// Multi-key Gemini (comma-separated)
const GEMINI_API_KEYS = (process.env.GEMINI_API_KEY || '').split(',').map(k => k.trim()).filter(Boolean);
let currentGeminiKeyIndex = 0;
const deadGeminiKeys = new Set();

function getNextGeminiKey() {
    if (GEMINI_API_KEYS.length === 0) return null;
    for (let i = 0; i < GEMINI_API_KEYS.length; i++) {
        const key = GEMINI_API_KEYS[currentGeminiKeyIndex];
        currentGeminiKeyIndex = (currentGeminiKeyIndex + 1) % GEMINI_API_KEYS.length;
        if (!deadGeminiKeys.has(key)) return key;
    }
    deadGeminiKeys.clear();
    return GEMINI_API_KEYS[0];
}

const OPENAI_API_KEY = (process.env.OPENAI_API_KEY || '').trim();
const CLAUDE_API_KEY = (process.env.CLAUDE_API_KEY || '').trim();
const DEEPSEEK_API_KEY = (process.env.DEEPSEEK_API_KEY || '').trim();

if (!LICENSE_SECRET) { console.error('FATAL: LICENSE_SECRET is missing!'); process.exit(1); }

const ED25519_PRIVATE_KEY = (() => {
    if (!ED25519_PRIVATE_KEY_RAW) { console.error('FATAL: ED25519_PRIVATE_KEY missing!'); process.exit(1); }
    let bytes;
    try {
        bytes = /^[0-9a-fA-F]{128}$/.test(ED25519_PRIVATE_KEY_RAW)
            ? Buffer.from(ED25519_PRIVATE_KEY_RAW, 'hex')
            : Buffer.from(ED25519_PRIVATE_KEY_RAW, 'base64');
    } catch (e) { console.error('FATAL: ED25519_PRIVATE_KEY decode failed:', e.message); process.exit(1); }
    if (!bytes || bytes.length !== 64) { console.error('FATAL: ED25519_PRIVATE_KEY must be 64 bytes'); process.exit(1); }
    return bytes;
})();
const ED25519_PUBLIC_KEY = nacl.sign.keyPair.fromSecretKey(ED25519_PRIVATE_KEY).publicKey;

console.log('🔐 Ed25519 loaded (pub: ' + Buffer.from(ED25519_PUBLIC_KEY).toString('hex').substring(0, 16) + '…)');
console.log('🤖 AI keys: Gemini=' + (GEMINI_API_KEYS.length > 0 ? `✓ (${GEMINI_API_KEYS.length})` : '✗') + ' OpenAI=' + (OPENAI_API_KEY ? '✓' : '✗') + ' Claude=' + (CLAUDE_API_KEY ? '✓' : '✗') + ' DeepSeek=' + (DEEPSEEK_API_KEY ? '✓' : '✗'));

// ============================================================================
// 2. Firebase Admin
// ============================================================================
let firebaseReady = false;
let db = null, bucket = null;

try {
    let sa = null;
    if (process.env.FIREBASE_KEY_BASE64) {
        sa = JSON.parse(Buffer.from(process.env.FIREBASE_KEY_BASE64, 'base64').toString('utf8'));
    } else if (fs.existsSync('/etc/secrets/firebase-key.json')) {
        sa = JSON.parse(fs.readFileSync('/etc/secrets/firebase-key.json', 'utf8'));
    } else if (FIREBASE_SERVICE_ACCOUNT) {
        sa = JSON.parse(FIREBASE_SERVICE_ACCOUNT);
        if (sa.private_key) sa.private_key = sa.private_key.replace(/\\n/g, '\n');
    }
    if (sa) {
        admin.initializeApp({
            credential: admin.credential.cert(sa),
            storageBucket: FIREBASE_STORAGE_BUCKET || `${sa.project_id}.appspot.com`
        });
        db = admin.firestore();
        bucket = admin.storage().bucket();
        firebaseReady = true;
        console.log('🔥 Firebase ready.');
    } else { console.warn('⚠️ Firebase key missing — DB features disabled.'); }
} catch (e) { console.error('❌ Firebase init failed:', e.message); }

let gradDb = null;
try {
    const gradKeyB64 = process.env.GRADIOMETER_FIREBASE_KEY_BASE64;
    if (gradKeyB64) {
        const gradSA = JSON.parse(Buffer.from(gradKeyB64, 'base64').toString('utf8'));
        if (gradSA.private_key) gradSA.private_key = gradSA.private_key.replace(/\\n/g, '\n');
        const gradApp = admin.initializeApp({ credential: admin.credential.cert(gradSA) }, 'gradiometer');
        gradDb = admin.firestore(gradApp);
        console.log('🔥 Gradiometer Firebase ready.');
    }
} catch (e) { console.error('❌ Gradiometer Firebase failed:', e.message); }

// ============================================================================
// 3. Helpers
// ============================================================================
function deepSort(obj) {
    if (Array.isArray(obj)) return obj.map(deepSort);
    if (obj !== null && typeof obj === 'object') {
        return Object.keys(obj).sort().reduce((r, k) => { r[k] = deepSort(obj[k]); return r; }, {});
    }
    return obj;
}
function safeEqual(a, b) {
    const x = Buffer.from(String(a || '')); const y = Buffer.from(String(b || ''));
    return x.length === y.length && crypto.timingSafeEqual(x, y);
}
function normalizeRole(role) {
    return (role === 'assistant' || role === 'model') ? 'assistant' : 'user';
}
function toGeminiRole(role) {
    return normalizeRole(role) === 'assistant' ? 'model' : 'user';
}

// ---- base58 + license codes ----
const BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
const NONCE_ALPHABET  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
const NONCE_LEN = 8, SIGNATURE_BYTES = 64, MAX_CODE_LENGTH = 160;

function base58Encode(bytes) {
    let n = 0n; for (const b of bytes) n = n * 256n + BigInt(b);
    let out = ''; while (n > 0n) { const r = Number(n % 58n); out = BASE58_ALPHABET[r] + out; n /= 58n; }
    for (const b of bytes) { if (b === 0) out = '1' + out; else break; }
    return out;
}
function base58Decode(str) {
    if (!str || str.length === 0 || str.length > 100) return null;
    let n = 0n; for (const ch of str) { const i = BASE58_ALPHABET.indexOf(ch); if (i < 0) return null; n = n * 58n + BigInt(i); }
    const bytes = []; while (n > 0n) { bytes.unshift(Number(n % 256n)); n /= 256n; }
    let lead = 0; for (const ch of str) { if (ch === '1') lead++; else break; }
    const r = Buffer.alloc(lead + bytes.length);
    for (let i = 0; i < bytes.length; i++) r[lead + i] = bytes[i];
    return r;
}
function generateLicenseKey() {
    let nonce = ''; const bytes = crypto.randomBytes(NONCE_LEN);
    for (let i = 0; i < NONCE_LEN; i++) nonce += NONCE_ALPHABET.charAt(bytes[i] % NONCE_ALPHABET.length);
    const sig = nacl.sign.detached(Buffer.from(nonce, 'utf-8'), ED25519_PRIVATE_KEY);
    return `ZEV-${nonce}-${base58Encode(sig)}`;
}
function isValidLicenseKey(key) {
    if (!key || typeof key !== 'string') return false;
    const t = key.trim();
    if (t.length > MAX_CODE_LENGTH) return false;
    const p = t.split('-'); if (p.length !== 3 || p[0].toUpperCase() !== 'ZEV') return false;
    const nonce = p[1].toUpperCase(), sig = p[2];
    if (nonce.length !== NONCE_LEN || !/^[A-Z2-7]+$/.test(nonce)) return false;
    if (sig.length < 80 || sig.length > 90) return false;
    const sb = base58Decode(sig);
    if (!sb || sb.length !== SIGNATURE_BYTES) return false;
    try { return nacl.sign.detached.verify(Buffer.from(nonce, 'utf-8'), sb, ED25519_PUBLIC_KEY); }
    catch { return false; }
}
const isValidDeviceId = (id) => typeof id === 'string' && /^[A-Za-z0-9_-]{6,64}$/.test(id);

// ----------------------------------------------------------------------------
// FREE MODE — controlled live from Firestore: document  config/app , field  is_payment_enabled (boolean).
//   is_payment_enabled == false (or the document is missing) -> FREE: licenseKey and credits are skipped
//                                                              on chat / image / image-edit / tts / circuit.
//   is_payment_enabled == true                               -> PAID: the normal license + credits logic.
// The value is cached in memory for 60 seconds, so changing it in Firestore takes effect within a minute
// with no redeploy. Video, music, balance, purchases, report, delete-data always need a real license.
// ----------------------------------------------------------------------------
const FREE_MODE_KEY = 'FREE_MODE';
const PAYMENT_CONFIG_TTL_MS = 60_000;      // cache lifetime
const PAYMENT_CONFIG_RETRY_MS = 10_000;    // after a failed read, retry sooner
let paymentEnabledCache = false;           // current value (default: false = free)
let paymentCacheExpiresAt = 0;
let paymentRefreshPromise = null;

// Helper: reads config/app -> is_payment_enabled. Missing document/field = false. Cached for 60 s.
// On a Firestore error the last known value is kept (false if there never was one).
async function getPaymentEnabled() {
    const now = Date.now();
    if (now < paymentCacheExpiresAt) return paymentEnabledCache;
    if (!firebaseReady) return paymentEnabledCache;
    if (!paymentRefreshPromise) {
        paymentRefreshPromise = (async () => {
            try {
                // Primary source: Firebase Remote Config parameter  is_payment_enabled  (default value).
                // Fallback (parameter missing / Remote Config error): Firestore config/app.
                let v;
                try {
                    const tpl = await admin.remoteConfig().getTemplate();
                    const param = tpl.parameters && tpl.parameters.is_payment_enabled;
                    const dv = param && param.defaultValue;
                    if (dv && typeof dv.value === 'string') v = (dv.value.trim().toLowerCase() === 'true');
                } catch (rcErr) {
                    console.warn('[config] Remote Config read failed, trying Firestore:', rcErr.message);
                }
                if (v === undefined) {
                    const snap = await db.collection('config').doc('app').get();
                    v = snap.exists ? (snap.get('is_payment_enabled') === true) : false;
                }
                paymentEnabledCache = (v === true);
                paymentCacheExpiresAt = Date.now() + PAYMENT_CONFIG_TTL_MS;
            } catch (e) {
                console.warn('[config] could not read config/app, keeping last value:', e.message);
                paymentCacheExpiresAt = Date.now() + PAYMENT_CONFIG_RETRY_MS;
            } finally {
                paymentRefreshPromise = null;
            }
            return paymentEnabledCache;
        })();
    }
    return paymentRefreshPromise;
}

// Free mode is on exactly when payment is disabled. The value is refreshed by the middleware below
// before any of the routes in FREE_MODE_ROUTES run, so this synchronous check is always current (<= 60 s old).
const isFreeKey = (k) => k === FREE_MODE_KEY && !paymentEnabledCache;
const isAcceptedKey = (k) => isFreeKey(k) || isValidLicenseKey(k);
const FREE_MODE_ROUTES = new Set([
    '/api/ai/chat', '/api/ai/chat/stream', '/api/ai/image', '/api/ai/image-edit', '/api/ai/tts', '/api/ai/circuit'
]);
const FREE_GLOBAL_PER_MIN = Math.max(1, parseInt(process.env.FREE_GLOBAL_PER_MIN || '', 10) || 900);
const FREE_IP_PER_MIN     = Math.max(1, parseInt(process.env.FREE_IP_PER_MIN || '', 10) || 150);
const FREE_IMAGE_PER_MIN  = Math.max(1, parseInt(process.env.FREE_IMAGE_PER_MIN || '', 10) || 5);
const isValidJobId = (id) => typeof id === 'string' && /^[A-Za-z0-9]{10,40}$/.test(id);
const webhookToken = (d, t, j) => crypto.createHmac('sha256', LICENSE_SECRET).update(`WH|${d}|${t}|${j || ''}`).digest('hex').substring(0, 32);

// Free-mode gate: runs BEFORE the routes. When payment is disabled in Firestore, every request to a
// FREE_MODE_ROUTES endpoint is treated as VIP (licenseKey replaced by FREE_MODE, no credit check or charge).
app.use(async (req, res, next) => {
    try {
        if (req.method === 'POST' && FREE_MODE_ROUTES.has(req.path)) {
            const paymentEnabled = await getPaymentEnabled();
            if (!paymentEnabled && req.body && typeof req.body === 'object') req.body.licenseKey = FREE_MODE_KEY;
        }
    } catch (e) { console.warn('[config] gate error:', e.message); }
    next();
});

// ----------------------------------------------------------------------------
// APP CONFIG — tells the app whether to show the "Top Up" button.
//   GET /api/config  ->  { "paymentEnabled": true | false }
//   Same value as the free-mode switch (Remote Config -> is_payment_enabled):
//     true  -> app shows the Top Up button
//     false -> app hides it (and the backend is in free mode)
// Cached server-side for 60 s; clients should not cache it (no-store).
// ----------------------------------------------------------------------------
app.get('/api/config', async (req, res) => {
    try {
        const paymentEnabled = await getPaymentEnabled();
        res.set('Cache-Control', 'no-store');
        res.json({ paymentEnabled: paymentEnabled === true });
    } catch (e) {
        console.warn('[config] /api/config error:', e.message);
        res.set('Cache-Control', 'no-store');
        res.json({ paymentEnabled: false });
    }
});

// ============================================================================
// 4. Rate Limiter (in-memory, single-instance)
// ============================================================================
class RateLimiter {
    constructor(maxPerWindow, windowMs, label) {
        this.maxPerWindow = maxPerWindow;
        this.windowMs = windowMs;
        this.label = label || 'rl';
        this.buckets = new Map();
        setInterval(() => this.cleanup(), 3_600_000).unref();
    }
    check(key) {
        const now = Date.now();
        let bucket = this.buckets.get(key);
        if (!bucket || now > bucket.resetAt) {
            bucket = { count: 0, resetAt: now + this.windowMs };
            this.buckets.set(key, bucket);
        }
        bucket.count++;
        return {
            allowed: bucket.count <= this.maxPerWindow,
            remaining: Math.max(0, this.maxPerWindow - bucket.count),
            resetAt: bucket.resetAt
        };
    }
    cleanup() {
        const now = Date.now();
        for (const [key, bucket] of this.buckets) {
            if (now > bucket.resetAt) this.buckets.delete(key);
        }
    }
}

const aiChatLimiter = new RateLimiter(30, 60_000, 'ai');
const ttsLimiter    = new RateLimiter(90, 60_000, 'tts'); // the app sends one request per sentence
const saveLimiter   = new RateLimiter(20, 60_000, 'save');
const playLimiter   = new RateLimiter(10, 60_000, 'play');
const reportLimiter = new RateLimiter(10, 60_000, 'report');
const freeGlobalLimiter = new RateLimiter(FREE_GLOBAL_PER_MIN, 60_000, 'free-global');
const freeIpLimiter     = new RateLimiter(FREE_IP_PER_MIN, 60_000, 'free-ip');
const freeImageLimiter  = new RateLimiter(FREE_IMAGE_PER_MIN, 60_000, 'free-image');

// Paid keys: bucket = the license (unchanged behaviour). FREE_MODE: per device + per IP + one global cap,
// because every free user shares the same "key" and deviceId can be rotated by a client.
function limitCheck(limiter, licenseKey, deviceId, ip) {
    if (!isFreeKey(licenseKey)) return limiter.check(licenseKey);
    const g = freeGlobalLimiter.check('all');
    if (!g.allowed) return g;
    const i = freeIpLimiter.check(ip || 'unknown');
    if (!i.allowed) return i;
    return limiter.check('free|' + deviceId);
}

// ============================================================================
// 5. SSRF Guard
// ============================================================================
function isPrivateIP(ip) {
    if (net.isIPv4(ip)) {
        const p = ip.split('.').map(Number);
        if (p[0] === 10 || p[0] === 127 || p[0] === 0) return true;
        if (p[0] === 169 && p[1] === 254) return true;
        if (p[0] === 192 && p[1] === 168) return true;
        if (p[0] === 172 && p[1] >= 16 && p[1] <= 31) return true;
        if (p[0] === 100 && p[1] >= 64 && p[1] <= 127) return true;
        return false;
    }
    if (net.isIPv6(ip)) {
        const lower = ip.toLowerCase();
        if (lower === '::1' || lower === '::') return true;
        if (/^f[cd][0-9a-f]{2}:/.test(lower)) return true;
        if (/^fe[89ab][0-9a-f]:/.test(lower)) return true;
        const m = lower.match(/^::ffff:(\d+\.\d+\.\d+\.\d+)$/);
        if (m) return isPrivateIP(m[1]);
        return false;
    }
    return false;
}

async function isSafeRemoteUrl(urlStr) {
    try {
        const u = new URL(urlStr);
        if (u.protocol !== 'https:') return { ok: false, reason: 'not https' };
        const host = u.hostname.toLowerCase();
        if (isPrivateIP(host)) return { ok: false, reason: 'private ip' };
        if (host === 'localhost' || host.endsWith('.local') || host.endsWith('.internal')) {
            return { ok: false, reason: 'local host' };
        }
        const dnsCheck = async () => {
            try { const v4 = await dns.resolve4(host); for (const a of v4) if (isPrivateIP(a)) throw new Error('private DNS'); } catch (e) { if (/private DNS/.test(e.message)) throw e; }
            try { const v6 = await dns.resolve6(host); for (const a of v6) if (isPrivateIP(a)) throw new Error('private DNS v6'); } catch (e) { if (/private DNS v6/.test(e.message)) throw e; }
        };
        await Promise.race([
            dnsCheck(),
            new Promise((_, rej) => setTimeout(() => rej(new Error('dns timeout')), 3000))
        ]).catch(e => { if (/private DNS/.test(e.message)) throw e; });
        return { ok: true };
    } catch (e) {
        return { ok: false, reason: e.message || 'invalid' };
    }
}

// ============================================================================
// 6. Credits
// ============================================================================
async function deductCredits(licenseKey, deviceId, cost, type, prompt) {
    if (isFreeKey(licenseKey)) return { remaining: 0, jobId: null }; // free mode: nothing to charge, nothing to refund
    if (!firebaseReady) throw new Error('DB_NOT_READY');
    if (!Number.isInteger(cost) || cost < 1 || cost > 200) throw new Error('INVALID_COST');
    const ref = db.collection('licenses').doc(licenseKey);
    const jobRef = db.collection('jobs').doc();
    const remaining = await db.runTransaction(async (tx) => {
        const doc = await tx.get(ref);
        if (!doc.exists) throw new Error('INVALID_LICENSE');
        const data = doc.data();
        if (data.deviceId && data.deviceId !== deviceId) throw new Error('LICENSE_BOUND_TO_OTHER_DEVICE');
        const cur = data.credits || 0;
        if (cur < cost) throw new Error('INSUFFICIENT_CREDITS');
        tx.update(ref, {
            deviceId,
            credits: admin.firestore.FieldValue.increment(-cost),
            lastUsedAt: admin.firestore.FieldValue.serverTimestamp()
        });
        tx.set(jobRef, {
            licenseKey, deviceId, type, cost,
            prompt: String(prompt || '').slice(0, 200),
            status: 'pending', refunded: false,
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });
        return cur - cost;
    });
    return { remaining, jobId: jobRef.id };
}

async function failJob(jobId, reason) {
    if (!firebaseReady || !jobId) return { refunded: false };
    const jobRef = db.collection('jobs').doc(jobId);
    const failureRef = db.collection('failures').doc();
    return await db.runTransaction(async (tx) => {
        const jd = await tx.get(jobRef);
        if (!jd.exists) return { refunded: false };
        const job = jd.data();
        if (job.status === 'failed') return { refunded: !!job.refunded };
        let licRef = null;
        if (job.licenseKey && job.cost > 0) licRef = db.collection('licenses').doc(job.licenseKey);
        if (licRef) tx.update(licRef, { credits: admin.firestore.FieldValue.increment(job.cost) });
        tx.update(jobRef, {
            status: 'failed', refunded: !!licRef,
            failReason: String(reason).slice(0, 500),
            failedAt: admin.firestore.FieldValue.serverTimestamp()
        });
        tx.set(failureRef, {
            jobId, deviceId: job.deviceId, licenseKey: job.licenseKey || null,
            type: job.type, cost: job.cost, prompt: job.prompt || '',
            reason: String(reason).slice(0, 500), refunded: !!licRef,
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });
        return { refunded: !!licRef };
    });
}

async function refundPartial(jobId, ratio = 0.5) {
    if (!firebaseReady || !jobId) return;
    try {
        await db.runTransaction(async (tx) => {
            const jobRef = db.collection('jobs').doc(jobId);
            const jd = await tx.get(jobRef);
            if (!jd.exists) return;
            const job = jd.data();
            if (job.refunded) return;
            const refund = Math.floor((job.cost || 1) * ratio);
            if (refund <= 0) return;
            if (job.licenseKey) {
                tx.update(db.collection('licenses').doc(job.licenseKey), {
                    credits: admin.firestore.FieldValue.increment(refund)
                });
            }
            tx.update(jobRef, {
                status: 'completed_partial',
                refunded: true,
                partialRefund: refund,
                completedAt: admin.firestore.FieldValue.serverTimestamp()
            });
        });
    } catch (e) { console.error('refundPartial failed:', e.message); }
}

// ============================================================================
// 7. AI Providers
// ============================================================================
const GEMINI_MODELS = [
    'gemini-3.5-flash-lite',
    'gemini-3.1-flash-lite',
    'gemini-3.7-flash',
    'gemini-3.6-flash',
    'gemini-3.5-flash',
    'gemini-3.8-flash',
    'gemini-3.8-live',
    'gemini-3.8-live-extended-thinking'
];
const OPENAI_MODELS = [
    'gpt-6-luna',
    'gpt-6.1-terra',
    'gpt-6.1-sol',
    'gpt-6-astra'
];
const CLAUDE_MODELS = [
    'claude-haiku-5-5',
    'claude-sonnet-5-5',
    'claude-opus-5-5',
    'claude-fable-5-1'
];
const DEEPSEEK_MODELS = [
    'deepseek-flash',
    'deepseek-v4-pro'
];
const OPENAI_MODEL = OPENAI_MODELS[0];
const CLAUDE_MODEL = CLAUDE_MODELS[0];
const DEEPSEEK_MODEL = DEEPSEEK_MODELS[0];

// The app lets the user pick a model per provider. The request carries
// models: { gemini, openai, claude }. Only names from the lists above are accepted;
// anything else (or nothing) falls back to the default.
function pickModel(provider, requested) {
    const list = provider === 'gemini' ? GEMINI_MODELS
        : provider === 'openai' ? OPENAI_MODELS
        : provider === 'claude' ? CLAUDE_MODELS
        : provider === 'deepseek' ? DEEPSEEK_MODELS : [];
    const m = requested && typeof requested === 'object' ? requested[provider] : null;
    return (typeof m === 'string' && list.includes(m)) ? m : null;
}

// ----------------------------------------------------------------------------
// Automatic model switching.
// The chain is: the model the user picked, then that provider's next models in list order,
// then the same for the next providers (order = the `providers` array sent by the app).
// A model that just failed (404 / 429 / 5xx / timeout / empty) is moved to the back for a while,
// so a dead model does not cost every new request a wait.
// ----------------------------------------------------------------------------
const PROVIDER_MODELS = { gemini: GEMINI_MODELS, openai: OPENAI_MODELS, claude: CLAUDE_MODELS, deepseek: DEEPSEEK_MODELS };
const MAX_MODELS_PER_PROVIDER = parseInt(process.env.MAX_MODELS_PER_PROVIDER) || 3;
const MODEL_COOLDOWN_MS = parseInt(process.env.MODEL_COOLDOWN_MS) || 60_000;
const FIRST_CHUNK_TIMEOUT_MS = parseInt(process.env.AI_FIRST_CHUNK_TIMEOUT_MS) || 30_000;
const STREAM_START_DEADLINE_MS = parseInt(process.env.AI_STREAM_START_DEADLINE_MS) || 90_000;
const ATTEMPT_TIMEOUT_MS = parseInt(process.env.AI_ATTEMPT_TIMEOUT_MS) || 120_000;
const modelCooldown = new Map(); // "provider:model" -> time until which it goes to the back of the chain

function providerHasKey(p) {
    if (p === 'gemini') return GEMINI_API_KEYS.length > 0;
    if (p === 'openai') return !!OPENAI_API_KEY;
    if (p === 'claude') return !!CLAUDE_API_KEY;
    if (p === 'deepseek') return !!DEEPSEEK_API_KEY;
    return false;
}

function markModelFailed(provider, model, err) {
    const msg = String((err && err.message) || '');
    if (/: no key/.test(msg)) return;
    const m = msg.match(/^(?:gemini|openai|claude|deepseek) (\d{3}):/);
    const status = m ? parseInt(m[1], 10) : 0;
    let ms = 0;
    if (status === 404) ms = 10 * 60_000;                       // model retired / not available for this key
    else if (status === 429 || status >= 500) ms = MODEL_COOLDOWN_MS;
    else if (!status) ms = Math.min(MODEL_COOLDOWN_MS, 30_000); // timeout, network error, empty answer
    if (ms) modelCooldown.set(`${provider}:${model}`, Date.now() + ms);
}
function markModelOk(provider, model) { modelCooldown.delete(`${provider}:${model}`); }

// fallback === false  -> only the model the user picked (the app's "use another model if it fails" switch is off)
function buildModelChain(order, models, fallback) {
    const chain = [];
    const seen = new Set();
    for (const p of order) {
        const list = PROVIDER_MODELS[p];
        if (!list || seen.has(p) || !providerHasKey(p)) continue;
        seen.add(p);
        const chosen = pickModel(p, models) || list[0];
        const rest = list.filter(m => m !== chosen);
        const ordered = fallback === false ? [chosen] : [chosen, ...rest].slice(0, MAX_MODELS_PER_PROVIDER);
        for (const model of ordered) chain.push({ provider: p, model });
    }
    const now = Date.now();
    const cooling = e => (modelCooldown.get(`${e.provider}:${e.model}`) || 0) > now;
    return [...chain.filter(e => !cooling(e)), ...chain.filter(cooling)];
}

// Wraps a stream: if the first chunk does not arrive within `ms`, fail so the next model is tried.
// Leaving early (timeout, error, client gone) aborts the upstream request.
async function* guardFirstChunk(stream, ms, abortController) {
    const it = stream[Symbol.asyncIterator]();
    let first = true;
    try {
        while (true) {
            let r;
            if (first) {
                let timer;
                const nextP = it.next();
                nextP.catch(() => {}); // a late rejection after the timeout must not crash the process
                const timeout = new Promise((_, reject) => { timer = setTimeout(() => reject(new Error('first chunk timeout')), ms); });
                try { r = await Promise.race([nextP, timeout]); } finally { clearTimeout(timer); }
                first = false;
            } else {
                r = await it.next();
            }
            if (r.done) return;
            yield r.value;
        }
    } finally {
        if (abortController) abortController.abort();
        try { Promise.resolve(it.return && it.return()).catch(() => {}); } catch (_) {}
    }
}

// One non-streaming attempt on one specific model (Gemini rotates keys: one retry on a bad/limited key).
async function callOne(provider, model, messages, systemPrompt, attachments) {
    const ac = new AbortController();
    const timer = setTimeout(() => ac.abort(), ATTEMPT_TIMEOUT_MS);
    try {
        if (provider === 'gemini') {
            let lastErr;
            const tries = Math.min(Math.max(GEMINI_API_KEYS.length, 1), 2);
            for (let i = 0; i < tries; i++) {
                const apiKey = getNextGeminiKey();
                if (!apiKey) throw new Error('gemini: no key');
                try { return await callGemini(apiKey, model, messages, systemPrompt, attachments, ac.signal); }
                catch (e) {
                    lastErr = e;
                    if (/\b40[13]\b/.test(e.message) && /api key|invalid/i.test(e.message)) deadGeminiKeys.add(apiKey);
                    else if (!/^gemini 429:/.test(e.message)) break;
                }
            }
            throw lastErr;
        }
        if (provider === 'openai') {
            if (!OPENAI_API_KEY) throw new Error('openai: no key');
            return await callOpenAI(OPENAI_API_KEY, model, messages, systemPrompt, ac.signal);
        }
        if (provider === 'claude') {
            if (!CLAUDE_API_KEY) throw new Error('claude: no key');
            return await callClaude(CLAUDE_API_KEY, model, messages, systemPrompt, attachments, ac.signal);
        }
        if (provider === 'deepseek') {
            if (!DEEPSEEK_API_KEY) throw new Error('deepseek: no key');
            return await callDeepSeek(DEEPSEEK_API_KEY, model, messages, systemPrompt, ac.signal);
        }
        throw new Error('unknown provider: ' + provider);
    } finally { clearTimeout(timer); }
}

const IMAGE_MODELS = [
    'gemini-3.1-flash-image',
    'gemini-nano-banana-2.1',
    'gemini-3.1-flash-lite-image',
    'gemini-3-pro-image',
    'gemini-2.5-flash-image'
];
const GEMINI_IMAGE_MODEL = IMAGE_MODELS[0];
const DEFAULT_TIMEOUT_MS = parseInt(process.env.AI_TIMEOUT_MS) || 300_000;

async function fetchWithTimeout(url, options = {}, timeoutMs = DEFAULT_TIMEOUT_MS) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    const outer = options.signal; // optional: lets callers cancel a slow/failed model attempt
    if (outer) {
        if (outer.aborted) controller.abort();
        else outer.addEventListener('abort', () => controller.abort(), { once: true });
    }
    try {
        return await fetch(url, { ...options, signal: controller.signal });
    } finally { clearTimeout(timer); }
}

function toGeminiParts(messages, attachments) {
    const parts = [];
    if (attachments) {
        for (const a of attachments) {
            if (a.mime && a.mime.startsWith('image/')) {
                parts.push({ inline_data: { mime_type: a.mime, data: a.data } });
            } else if (a.mime === 'application/pdf') {
                parts.push({ inline_data: { mime_type: 'application/pdf', data: a.data } });
            } else {
                try {
                    const text = Buffer.from(a.data, 'base64').toString('utf8');
                    parts.push({ text: `\n--- FILE: ${a.name} ---\n${text}\n--- END FILE ---\n` });
                } catch (_) {}
            }
        }
    }
    parts.push({ text: messages[messages.length - 1].content });
    return parts;
}

async function callGemini(apiKey, model, messages, systemPrompt, attachments, signal) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`;
    const body = {
        system_instruction: { parts: [{ text: systemPrompt }] },
        contents: [
            ...messages.slice(0, -1).map(m => ({ role: toGeminiRole(m.role), parts: [{ text: m.content }] })),
            { role: 'user', parts: toGeminiParts(messages, attachments) }
        ],
        generationConfig: { maxOutputTokens: 16384 }
    };
    const res = await fetchWithTimeout(url, { method: 'POST', headers: { 'x-goog-api-key': apiKey, 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal });
    const raw = await res.text();
    if (!res.ok) throw new Error(`gemini ${res.status}: ${raw.slice(0, 200)}`);
    const json = JSON.parse(raw);
    const text = (json.candidates?.[0]?.content?.parts || []).map(p => p.text || '').join('').trim();
    if (!text) throw new Error('gemini: empty');
    return { text, provider: 'gemini', model };
}

async function callOpenAI(apiKey, model, messages, systemPrompt, signal) {
    const url = 'https://api.openai.com/v1/chat/completions';
    const normalized = messages.map(m => ({ role: normalizeRole(m.role), content: m.content }));
    const body = { model, messages: [{ role: 'system', content: systemPrompt }, ...normalized], max_tokens: 8192 };
    const res = await fetchWithTimeout(url, { method: 'POST', headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal });
    const raw = await res.text();
    if (!res.ok) throw new Error(`openai ${res.status}: ${raw.slice(0, 200)}`);
    const json = JSON.parse(raw);
    const text = json.choices?.[0]?.message?.content?.trim();
    if (!text) throw new Error('openai: empty');
    return { text, provider: 'openai', model };
}

// DeepSeek uses an OpenAI-compatible API (text only: attachments are not sent).
async function callDeepSeek(apiKey, model, messages, systemPrompt, signal) {
    const url = 'https://api.deepseek.com/chat/completions';
    const normalized = messages.map(m => ({ role: normalizeRole(m.role), content: m.content }));
    const body = { model, messages: [{ role: 'system', content: systemPrompt }, ...normalized], max_tokens: 8192 };
    const res = await fetchWithTimeout(url, { method: 'POST', headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal });
    const raw = await res.text();
    if (!res.ok) throw new Error(`deepseek ${res.status}: ${raw.slice(0, 200)}`);
    const json = JSON.parse(raw);
    const text = json.choices?.[0]?.message?.content?.trim();
    if (!text) throw new Error('deepseek: empty');
    return { text, provider: 'deepseek', model };
}

async function callClaude(apiKey, model, messages, systemPrompt, attachments, signal) {
    const url = 'https://api.anthropic.com/v1/messages';
    const claudeMessages = messages.map(m => ({ role: normalizeRole(m.role), content: m.content }));
    if (attachments && attachments.length > 0) {
        const lastMsg = claudeMessages[claudeMessages.length - 1];
        const contentParts = [];
        for (const a of attachments) {
            if (a.mime && (a.mime.startsWith('image/') || a.mime === 'application/pdf')) {
                contentParts.push({ type: a.mime === 'application/pdf' ? 'document' : 'image', source: { type: 'base64', media_type: a.mime, data: a.data } });
            }
        }
        contentParts.push({ type: 'text', text: lastMsg.content });
        lastMsg.content = contentParts;
    }
    const body = { model, max_tokens: 8192, system: systemPrompt, messages: claudeMessages };
    const res = await fetchWithTimeout(url, { method: 'POST', headers: { 'x-api-key': apiKey, 'anthropic-version': '2023-06-01', 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal });
    const raw = await res.text();
    if (!res.ok) throw new Error(`claude ${res.status}: ${raw.slice(0, 200)}`);
    const json = JSON.parse(raw);
    const text = (json.content || []).filter(b => b.type === 'text').map(b => b.text).join('').trim();
    if (!text) throw new Error('claude: empty');
    return { text, provider: 'claude', model };
}

async function tryProvider(provider, messages, systemPrompt, attachments, models) {
    if (provider === 'gemini') {
        let lastErr;
        const maxAttempts = Math.max(3, Math.min(GEMINI_API_KEYS.length * 2, 6));
        for (let attempt = 0; attempt < maxAttempts; attempt++) {
            const apiKey = getNextGeminiKey();
            if (!apiKey) throw new Error('gemini: no key');
            const chosen = pickModel('gemini', models);
            const chain = chosen ? [chosen, ...GEMINI_MODELS.filter(m => m !== chosen)] : GEMINI_MODELS;
            const model = chain[attempt % chain.length];
            try { return await callGemini(apiKey, model, messages, systemPrompt, attachments); }
            catch (e) {
                lastErr = e;
                if (/\b40[13]\b/.test(e.message) && /api key|invalid/i.test(e.message)) deadGeminiKeys.add(apiKey);
            }
        }
        throw lastErr;
    }
    if (provider === 'openai') {
        if (!OPENAI_API_KEY) throw new Error('openai: no key');
        return await callOpenAI(OPENAI_API_KEY, pickModel('openai', models) || OPENAI_MODEL, messages, systemPrompt);
    }
    if (provider === 'claude') {
        if (!CLAUDE_API_KEY) throw new Error('claude: no key');
        return await callClaude(CLAUDE_API_KEY, pickModel('claude', models) || CLAUDE_MODEL, messages, systemPrompt, attachments);
    }
    if (provider === 'deepseek') {
        if (!DEEPSEEK_API_KEY) throw new Error('deepseek: no key');
        return await callDeepSeek(DEEPSEEK_API_KEY, pickModel('deepseek', models) || DEEPSEEK_MODEL, messages, systemPrompt);
    }
    throw new Error('unknown provider: ' + provider);
}

// --- Streaming generators ---
async function* streamGemini(apiKey, model, messages, systemPrompt, attachments, signal) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:streamGenerateContent?alt=sse`;
    const body = {
        system_instruction: { parts: [{ text: systemPrompt }] },
        contents: [
            ...messages.slice(0, -1).map(m => ({ role: toGeminiRole(m.role), parts: [{ text: m.content }] })),
            { role: 'user', parts: toGeminiParts(messages, attachments) }
        ],
        generationConfig: { maxOutputTokens: 16384 }
    };
    const res = await fetchWithTimeout(url, { method: 'POST', headers: { 'x-goog-api-key': apiKey, 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal });
    if (!res.ok) throw new Error(`gemini ${res.status}: ${await res.text()}`);
    const reader = res.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n'); buffer = lines.pop();
        for (const line of lines) {
            if (!line.startsWith('data: ')) continue;
            const data = line.slice(6);
            if (data === '[DONE]') continue;
            try {
                const json = JSON.parse(data);
                const text = (json.candidates?.[0]?.content?.parts || []).map(p => p.text || '').join('');
                if (text) yield text;
            } catch (_) {}
        }
    }
}

async function* streamOpenAI(apiKey, model, messages, systemPrompt, signal) {
    const url = 'https://api.openai.com/v1/chat/completions';
    const normalized = messages.map(m => ({ role: normalizeRole(m.role), content: m.content }));
    const body = { model, messages: [{ role: 'system', content: systemPrompt }, ...normalized], stream: true, max_tokens: 8192 };
    const res = await fetchWithTimeout(url, { method: 'POST', headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal });
    if (!res.ok) throw new Error(`openai ${res.status}: ${await res.text()}`);
    const reader = res.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n'); buffer = lines.pop();
        for (const line of lines) {
            if (!line.startsWith('data: ')) continue;
            const data = line.slice(6);
            if (data === '[DONE]') continue;
            try {
                const json = JSON.parse(data);
                const text = json.choices?.[0]?.delta?.content;
                if (text) yield text;
            } catch (_) {}
        }
    }
}

async function* streamDeepSeek(apiKey, model, messages, systemPrompt, signal) {
    const url = 'https://api.deepseek.com/chat/completions';
    const normalized = messages.map(m => ({ role: normalizeRole(m.role), content: m.content }));
    const body = { model, messages: [{ role: 'system', content: systemPrompt }, ...normalized], stream: true, max_tokens: 8192 };
    const res = await fetchWithTimeout(url, { method: 'POST', headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal });
    if (!res.ok) throw new Error(`deepseek ${res.status}: ${await res.text()}`);
    const reader = res.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n'); buffer = lines.pop();
        for (const line of lines) {
            if (!line.startsWith('data: ')) continue;
            const data = line.slice(6);
            if (data === '[DONE]') continue;
            try {
                const json = JSON.parse(data);
                const text = json.choices?.[0]?.delta?.content;
                if (text) yield text;
            } catch (_) {}
        }
    }
}

async function* streamClaude(apiKey, model, messages, systemPrompt, attachments, signal) {
    const url = 'https://api.anthropic.com/v1/messages';
    const claudeMessages = messages.map(m => ({ role: normalizeRole(m.role), content: m.content }));
    if (attachments && attachments.length > 0) {
        const lastMsg = claudeMessages[claudeMessages.length - 1];
        const contentParts = [];
        for (const a of attachments) {
            if (a.mime && (a.mime.startsWith('image/') || a.mime === 'application/pdf')) {
                contentParts.push({ type: a.mime === 'application/pdf' ? 'document' : 'image', source: { type: 'base64', media_type: a.mime, data: a.data } });
            }
        }
        contentParts.push({ type: 'text', text: lastMsg.content });
        lastMsg.content = contentParts;
    }
    const body = { model, max_tokens: 8192, system: systemPrompt, messages: claudeMessages, stream: true };
    const res = await fetchWithTimeout(url, { method: 'POST', headers: { 'x-api-key': apiKey, 'anthropic-version': '2023-06-01', 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal });
    if (!res.ok) throw new Error(`claude ${res.status}: ${await res.text()}`);
    const reader = res.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n'); buffer = lines.pop();
        for (const line of lines) {
            if (!line.startsWith('data: ')) continue;
            try {
                const json = JSON.parse(line.slice(6));
                if (json.type === 'content_block_delta' && json.delta?.text) yield json.delta.text;
            } catch (_) {}
        }
    }
}

// ============================================================================
// 8. Public routes
// ============================================================================
app.get('/', (req, res) => {
    res.json({
        status: 'ok',
        version: 'v8-production',
        features: {
            firebase: firebaseReady,
            gradiometer: !!gradDb,
            replicate: !!REPLICATE_TOKEN,
            ai: { gemini: GEMINI_API_KEYS.length > 0, openai: !!OPENAI_API_KEY, claude: !!CLAUDE_API_KEY, deepseek: !!DEEPSEEK_API_KEY },
            license: 'ed25519',
            streaming: true,
            unbuffered_sse: true,
            circuit_lab: true,
            arduino_code: true,
            tts: !!OPENAI_API_KEY,
            rate_limited: true,
            circuit_no_loopback: true,
            async_partial_refund: true,
            play_billing: !!androidPublisher
        }
    });
});

app.post('/api/balance', async (req, res) => {
    if (!firebaseReady) return res.status(503).json({ error: 'Service not ready' });
    const { licenseKey, deviceId } = req.body || {};
    if (!isValidLicenseKey(licenseKey) || !isValidDeviceId(deviceId)) return res.status(400).json({ error: 'Invalid request' });
    try {
        const doc = await db.collection('licenses').doc(licenseKey).get();
        if (!doc.exists) return res.status(404).json({ error: 'License not found' });
        const data = doc.data();
        if (data.deviceId && data.deviceId !== deviceId) return res.status(403).json({ error: 'License used on another device' });
        res.json({ credits: data.credits || 0 });
    } catch (e) { res.status(500).json({ error: 'Internal error' }); }
});

// ============================================================================
// 9. AI Chat — Streaming (SSE)
// ============================================================================
app.post('/api/ai/chat/stream', async (req, res) => {
    const body = req.body || {};
    const { licenseKey, deviceId, messages, systemPrompt, provider, providers, attachments, models, fallback } = body;
    const cost = typeof body.cost === 'number' ? Math.max(1, Math.min(10, Math.floor(body.cost))) : 1;

    if (!isValidDeviceId(deviceId) || !isAcceptedKey(licenseKey) || !Array.isArray(messages) || messages.length === 0) {
        return res.status(400).json({ error: 'Invalid request' });
    }
    if (!firebaseReady) return res.status(503).json({ error: 'Service not ready' });

    const rl = limitCheck(aiChatLimiter, licenseKey, deviceId, req.ip);
    if (!rl.allowed) {
        return res.status(429).json({ error: 'RATE_LIMIT', retryAfter: Math.ceil((rl.resetAt - Date.now()) / 1000) });
    }

    let jobId = null;
    try {
        const deduction = await deductCredits(licenseKey, deviceId, cost, 'chat', String(messages[messages.length - 1].content || '').slice(0, 200));
        jobId = deduction.jobId;
    } catch (e) {
        if (e.message === 'INSUFFICIENT_CREDITS') return res.status(402).json({ error: 'INSUFFICIENT_CREDITS' });
        if (e.message === 'LICENSE_BOUND_TO_OTHER_DEVICE') return res.status(403).json({ error: 'LICENSE_BOUND' });
        console.warn('[license] charge failed:', e.message);
        if (e.message === 'INVALID_LICENSE') return res.status(401).json({ error: 'INVALID_LICENSE', reason: 'license_not_found' });
        return res.status(503).json({ error: 'SERVER_ERROR', reason: String(e.message || '').slice(0, 120) });
    }

    res.setHeader('Content-Type', 'text/event-stream; charset=utf-8');
    res.setHeader('Cache-Control', 'no-cache, no-transform');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('X-Accel-Buffering', 'no');
    if (res.socket) res.socket.setNoDelay(true);
    res.flushHeaders();

    let clientDisconnected = false;
    res.on('close', () => { if (!res.writableEnded) clientDisconnected = true; });

    const sendChunk = (text) => {
        if (clientDisconnected) return;
        res.write(`data: ${JSON.stringify({ text })}\n\n`);
        if (typeof res.flush === 'function') res.flush();
    };
    const endStream = () => { if (!clientDisconnected) { res.write('data: [DONE]\n\n'); res.end(); } };
    const sendError = (msg) => { if (!clientDisconnected) { res.write(`data: ${JSON.stringify({ error: msg })}\n\n`); res.end(); } };

    const order = Array.isArray(providers) && providers.length > 0 ? providers : (provider ? [provider] : ['gemini', 'openai', 'claude']);

    const sendMeta = (p, model) => {
        if (clientDisconnected) return;
        res.write(`data: ${JSON.stringify({ meta: { provider: p, model } })}\n\n`);
    };

    const chain = buildModelChain(order, models, fallback);
    const startedAt = Date.now();
    let sentAnyChunk = false;
    let success = false;
    let usedProvider = null;
    let usedModel = null;

    // Try the picked model first; if it fails BEFORE sending any text, switch to the next model automatically.
    for (const { provider: p, model } of chain) {
        if (clientDisconnected || sentAnyChunk) break;
        if (Date.now() - startedAt > STREAM_START_DEADLINE_MS) break;
        const ac = new AbortController();
        try {
            let stream;
            if (p === 'gemini') {
                const apiKey = getNextGeminiKey();
                if (!apiKey) continue;
                stream = streamGemini(apiKey, model, messages, systemPrompt || '', attachments || [], ac.signal);
            } else if (p === 'openai' && OPENAI_API_KEY) {
                stream = streamOpenAI(OPENAI_API_KEY, model, messages, systemPrompt || '', ac.signal);
            } else if (p === 'claude' && CLAUDE_API_KEY) {
                stream = streamClaude(CLAUDE_API_KEY, model, messages, systemPrompt || '', attachments || [], ac.signal);
            } else if (p === 'deepseek' && DEEPSEEK_API_KEY) {
                stream = streamDeepSeek(DEEPSEEK_API_KEY, model, messages, systemPrompt || '', ac.signal);
            } else continue;

            let thisModelSent = false;
            for await (const chunk of guardFirstChunk(stream, FIRST_CHUNK_TIMEOUT_MS, ac)) {
                if (clientDisconnected) break;
                if (!thisModelSent) sendMeta(p, model);
                sendChunk(chunk);
                sentAnyChunk = true;
                thisModelSent = true;
            }
            if (thisModelSent) { success = true; usedProvider = p; usedModel = model; markModelOk(p, model); break; }
            markModelFailed(p, model, new Error('empty'));
            console.warn(`Stream ${p}/${model} returned nothing, switching model`);
        } catch (e) {
            console.warn(`Stream ${p}/${model} failed:`, String(e.message).slice(0, 200));
            ac.abort();
            if (sentAnyChunk) break;
            markModelFailed(p, model, e);
        }
    }

    if (success) {
        if (jobId) db.collection('jobs').doc(jobId).update({
            status: 'completed', completedAt: admin.firestore.FieldValue.serverTimestamp(), provider: usedProvider, model: usedModel
        }).catch(() => {});
        endStream();
    } else if (sentAnyChunk) {
        // v8: fire-and-forget refund so the stream closes immediately
        refundPartial(jobId, 0.5).catch(() => {});
        endStream();
    } else {
        try { await failJob(jobId, 'all stream providers failed'); } catch (_) {}
        sendError('AI_FAILED');
    }
});

// ============================================================================
// 10. AI Chat — Core logic (shared by /api/ai/chat and /api/ai/circuit)
// ============================================================================
// v8: extract the chat core so /api/ai/circuit can call it directly instead
//     of looping back through HTTP. Saves ~50-200ms per circuit request.
async function handleChatCore({ licenseKey, deviceId, messages, systemPrompt, provider, providers, attachments, cost, models, fallback, ip }) {
    if (!isValidDeviceId(deviceId)) return { ok: false, status: 400, body: { error: 'Invalid device' } };
    if (!Array.isArray(messages) || messages.length === 0) return { ok: false, status: 400, body: { error: 'Invalid messages' } };
    if (!isAcceptedKey(licenseKey)) return { ok: false, status: 401, body: { error: 'INVALID_LICENSE', reason: 'bad_key_signature' } };
    if (!firebaseReady) return { ok: false, status: 503, body: { error: 'Service not ready' } };

    const rl = limitCheck(aiChatLimiter, licenseKey, deviceId, ip);
    if (!rl.allowed) {
        return { ok: false, status: 429, body: { error: 'RATE_LIMIT', retryAfter: Math.ceil((rl.resetAt - Date.now()) / 1000) } };
    }

    let jobId = null;
    try {
        const d = await deductCredits(licenseKey, deviceId, cost, 'chat', String(messages[messages.length - 1].content || '').slice(0, 200));
        jobId = d.jobId;
    } catch (e) {
        if (e.message === 'INSUFFICIENT_CREDITS') return { ok: false, status: 402, body: { error: 'INSUFFICIENT_CREDITS' } };
        if (e.message === 'LICENSE_BOUND_TO_OTHER_DEVICE') return { ok: false, status: 403, body: { error: 'LICENSE_BOUND' } };
        console.warn('[license] charge failed:', e.message);
        if (e.message === 'INVALID_LICENSE') return { ok: false, status: 401, body: { error: 'INVALID_LICENSE', reason: 'license_not_found' } };
        return { ok: false, status: 500, body: { error: 'Internal error', reason: String(e.message || '').slice(0, 120) } };
    }

    const order = Array.isArray(providers) && providers.length > 0 ? providers : (provider ? [provider] : ['gemini', 'openai', 'claude']);
    let lastError = null;
    const started = Date.now();

    for (const { provider: p, model } of buildModelChain(order, models, fallback)) {
        try {
            const result = await callOne(p, model, messages, systemPrompt || '', attachments || []);
            markModelOk(p, model);
            const latencyMs = Date.now() - started;
            if (jobId) db.collection('jobs').doc(jobId).update({
                status: 'completed', completedAt: admin.firestore.FieldValue.serverTimestamp(),
                provider: result.provider, model: result.model, latencyMs
            }).catch(() => {});
            return { ok: true, status: 200, body: { text: result.text, provider: result.provider, model: result.model, latencyMs } };
        } catch (e) {
            lastError = e;
            markModelFailed(p, model, e);
            console.warn(`Model ${p}/${model} failed: ${String(e.message).slice(0, 200)}`);
        }
    }

    try { await failJob(jobId, `all providers failed: ${lastError?.message || 'unknown'}`); } catch (_) {}
    return { ok: false, status: 502, body: { error: 'AI_FAILED', message: String(lastError?.message || '').slice(0, 300) } };
}

app.post('/api/ai/chat', async (req, res) => {
    const body = req.body || {};
    const cost = typeof body.cost === 'number' ? Math.max(1, Math.min(10, Math.floor(body.cost))) : 1;

    const result = await handleChatCore({
        licenseKey: body.licenseKey,
        deviceId: body.deviceId,
        messages: body.messages,
        systemPrompt: body.systemPrompt,
        provider: body.provider,
        providers: body.providers,
        attachments: body.attachments,
        cost,
        models: body.models,
        fallback: body.fallback,
        ip: req.ip
    });

    res.status(result.status).json(result.body);
});

// ============================================================================
// 11. AI Image — Imagen 3
// ============================================================================
app.post('/api/ai/image', async (req, res) => {
    const body = req.body || {};
    const { licenseKey, deviceId, prompt } = body;
    const cost = 2;

    if (!isValidDeviceId(deviceId)) return res.status(400).json({ error: 'Invalid device' });
    if (typeof prompt !== 'string' || prompt.length < 3 || prompt.length > 1000) return res.status(400).json({ error: 'Invalid prompt' });
    if (!isAcceptedKey(licenseKey)) return res.status(401).json({ error: 'INVALID_LICENSE', reason: 'bad_key_signature' });
    if (isFreeKey(licenseKey) && !limitCheck(freeImageLimiter, licenseKey, deviceId, req.ip).allowed) return res.status(429).json({ error: 'RATE_LIMIT' });
    if (GEMINI_API_KEYS.length === 0 && !freeImageAvailable()) return res.status(503).json({ error: 'AI_NOT_CONFIGURED' });
    if (!firebaseReady) return res.status(503).json({ error: 'Service not ready' });

    // Free providers first (Agnes, then a Hugging Face Space). Credits are charged only if they all fail.
    if (freeImageAvailable() && freeImageQuotaTake(deviceId)) {
        try {
            await peekLicenseCredits(licenseKey, deviceId);   // same license checks as the paid path, nothing charged
        } catch (e) {
            freeImageQuotaGiveBack(deviceId);
            if (e.message === 'LICENSE_BOUND_TO_OTHER_DEVICE') return res.status(403).json({ error: 'LICENSE_BOUND' });
            if (e.message === 'INVALID_LICENSE') return res.status(401).json({ error: 'INVALID_LICENSE', reason: 'license_not_found' });
            return res.status(503).json({ error: 'SERVER_ERROR', reason: String(e.message || '').slice(0, 120) });
        }
        const free = await generateImageFree(prompt);
        if (free) return res.json({ image: free.image, mime: free.mime, free: true });
        freeImageQuotaGiveBack(deviceId);
    }
    if (GEMINI_API_KEYS.length === 0) return res.status(503).json({ error: 'AI_NOT_CONFIGURED' });

    let jobId = null;
    try {
        const r = await deductCredits(licenseKey, deviceId, cost, 'image', prompt);
        jobId = r.jobId;
    } catch (e) {
        if (e.message === 'INSUFFICIENT_CREDITS') return res.status(402).json({ error: 'INSUFFICIENT_CREDITS' });
        if (e.message === 'LICENSE_BOUND_TO_OTHER_DEVICE') return res.status(403).json({ error: 'LICENSE_BOUND' });
        console.warn('[license] charge failed:', e.message);
        if (e.message === 'INVALID_LICENSE') return res.status(401).json({ error: 'INVALID_LICENSE', reason: 'license_not_found' });
        return res.status(503).json({ error: 'SERVER_ERROR', reason: String(e.message || '').slice(0, 120) });
    }

    try {
        // Preferred model first (if the client asked for a valid one), then the rest as fallback.
        const wanted = typeof body.model === 'string' && IMAGE_MODELS.includes(body.model) ? body.model : null;
        const chain = wanted ? [wanted, ...IMAGE_MODELS.filter(m => m !== wanted)] : IMAGE_MODELS;
        let b64 = null, mime = 'image/png', lastErr = null;
        for (const model of chain) {
            try {
                const apiKey = getNextGeminiKey();
                const base = `https://generativelanguage.googleapis.com/v1beta/models/${model}`;
                const isImagen = model.startsWith('imagen');
                const url = base + (isImagen ? ':predict' : ':generateContent');
                const payload = isImagen
                    ? { instances: [{ prompt }], parameters: { sampleCount: 1 } }
                    : { contents: [{ role: 'user', parts: [{ text: prompt }] }],
                        generationConfig: { responseModalities: ['TEXT', 'IMAGE'] } };
                const r = await fetchWithTimeout(url, {
                    method: 'POST',
                    headers: { 'x-goog-api-key': apiKey, 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                }, 90_000);
                const raw = await r.text();
                if (!r.ok) throw new Error(`${model} ${r.status}: ${raw.slice(0, 200)}`);
                const json = JSON.parse(raw);
                if (isImagen) {
                    b64 = json.predictions?.[0]?.bytesBase64Encoded || null;
                } else {
                    const parts = json.candidates?.[0]?.content?.parts || [];
                    const img = parts.find(p => (p.inlineData || p.inline_data)?.data);
                    const d = img && (img.inlineData || img.inline_data);
                    if (d) { b64 = d.data; mime = d.mimeType || d.mime_type || 'image/png'; }
                }
                if (!b64) throw new Error(`${model}: no image in response`);
                break;
            } catch (err) {
                lastErr = err;
                console.warn('[image] model failed:', String(err.message || '').slice(0, 200));
            }
        }
        if (!b64) throw lastErr || new Error('image: all models failed');

        if (jobId) db.collection('jobs').doc(jobId).update({
            status: 'completed', completedAt: admin.firestore.FieldValue.serverTimestamp()
        }).catch(() => {});
        res.json({ image: b64, mime });
    } catch (e) {
        try { await failJob(jobId, `image failed: ${e.message}`); } catch (_) {}
        return res.status(502).json({ error: 'AI_FAILED', message: String(e.message || '').slice(0, 300) });
    }
});

// ----------------------------------------------------------------------------
// Image-edit providers. They are tried in this order and the request fails only if BOTH fail:
//   1) Gemini  gemini-3.1-flash-image-preview, gemini-2.5-flash-image, then any other Gemini image model
//   2) Agnes   Agnes-Image-2.0-Flash   (OpenAI-style multipart edit endpoint)
// Optional Render env: AGNES_IMAGE_EDIT_MODEL, AGNES_IMAGE_EDIT_PATH (default /v1/images/edits).
// ----------------------------------------------------------------------------
// Gemini models tried in this order (the first one that returns a picture wins).
// Override from Render with GEMINI_IMAGE_EDIT_MODELS="model-a,model-b" without touching the code.
const GEMINI_EDIT_MODELS = (process.env.GEMINI_IMAGE_EDIT_MODELS || '').split(',').map(x => x.trim()).filter(Boolean);
if (GEMINI_EDIT_MODELS.length === 0) GEMINI_EDIT_MODELS.push('gemini-3.1-flash-image-preview', 'gemini-2.5-flash-image');
const AGNES_EDIT_MODEL = (process.env.AGNES_IMAGE_EDIT_MODEL || 'Agnes-Image-2.0-Flash').trim();
const AGNES_EDIT_PATH = '/' + (process.env.AGNES_IMAGE_EDIT_PATH || '/v1/images/generations').trim().replace(/^\/+/, '');
// Models tried on the Agnes API hub, in this order. Replace the whole list from Render with
// AGNES_IMAGE_EDIT_MODELS="Name One,Name Two" (comma separated) without touching the code.
const AGNES_EDIT_MODELS = (process.env.AGNES_IMAGE_EDIT_MODELS || '').split(',').map(x => x.trim()).filter(Boolean);
if (AGNES_EDIT_MODELS.length === 0) AGNES_EDIT_MODELS.push('agnes-image-2.0-flash', 'agnes-image-2.1-flash', 'agnes-image-2.5-flash');
const EDIT_TOTAL_BUDGET_MS = 215_000;    // whole chain must end before the app's 240s call timeout
const GEMINI_EDIT_TIMEOUT_MS = 45_000;        // per Gemini model
const GEMINI_EDIT_TOTAL_MS = 90_000;         // all Gemini models together; leaves >=125s for Agnes
const AGNES_EDIT_TIMEOUT_MS = 110_000;   // 80s + 110s stays under the app's 240s call timeout

async function editGeminiOnce(model, prompt, mime, image, timeoutMs) {
    const apiKey = getNextGeminiKey();
    if (!apiKey) throw new Error('gemini: no key');
    const r = await fetchWithTimeout(
        `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`,
        {
            method: 'POST',
            headers: { 'x-goog-api-key': apiKey, 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contents: [{ role: 'user', parts: [
                    { text: prompt },
                    { inline_data: { mime_type: mime, data: image } }
                ] }],
                generationConfig: { responseModalities: ['TEXT', 'IMAGE'] }
            })
        }, timeoutMs);
    const raw = await r.text();
    if (!r.ok) throw new Error(`${model} ${r.status}: ${raw.slice(0, 200)}`);
    const json = JSON.parse(raw);
    const parts = json.candidates?.[0]?.content?.parts || [];
    const img = parts.find(p => (p.inlineData || p.inline_data)?.data);
    const d = img && (img.inlineData || img.inline_data);
    if (d) return { image: d.data, mime: d.mimeType || d.mime_type || 'image/png', model };
    // Text-only answer: usually a deliberate refusal. The caller records it and keeps trying the other models/providers.
    const err = new Error(`${model}: no image in response`);
    err.refusal = parts.map(p => p.text).filter(Boolean).join(' ').slice(0, 200);
    throw err;
}

// Lists the image-capable models this key can actually call (used after the configured ones all failed).
async function geminiListImageModels() {
    try {
        const apiKey = getNextGeminiKey();
        if (!apiKey) return [];
        const res = await fetchWithTimeout('https://generativelanguage.googleapis.com/v1beta/models?pageSize=200',
            { headers: { 'x-goog-api-key': apiKey } }, 12_000);
        const j = JSON.parse(await res.text());
        return (Array.isArray(j.models) ? j.models : [])
            .filter(m => m && /image/i.test(m.name || '') && (m.supportedGenerationMethods || []).includes('generateContent'))
            .map(m => String(m.name).replace(/^models\//, ''));
    } catch (_) { return []; }
}

// Tries EVERY Gemini image model: the configured ones first, then any other image model the key can see.
// A refusal or any other failure just moves on to the next model; nothing stops the chain early.
async function editImageWithGemini(prompt, mime, image) {
    if (GEMINI_API_KEYS.length === 0) throw new Error('gemini: no key');
    const deadline = Date.now() + GEMINI_EDIT_TOTAL_MS;
    const problems = [];
    const tried = new Set();
    let lastErr = null, refusal = '';
    const attempt = async (model) => {
        tried.add(model.toLowerCase());
        const left = deadline - Date.now();
        if (left < 5_000) { problems.push('Gemini timeout'); return null; }
        try {
            return await editGeminiOnce(model, prompt, mime, image, Math.min(GEMINI_EDIT_TIMEOUT_MS, left));
        } catch (e) {
            lastErr = e;
            if (e.refusal) { refusal = refusal || e.refusal; problems.push(`${geminiLabel(model)} refused`); }
            else problems.push(shortEditErr(geminiLabel(model), e.message));
            console.warn(`[image-edit] gemini "${model}" failed: ${String(e.message || '').slice(0, 160)}`);
            return null;
        }
    };
    for (const model of GEMINI_EDIT_MODELS) {
        const out = await attempt(model);
        if (out) return out;
        if (deadline - Date.now() < 5_000) break;
    }
    if (deadline - Date.now() >= 5_000) {
        const extra = (await geminiListImageModels()).filter(id => !tried.has(id.toLowerCase()));
        if (extra.length) console.warn('[image-edit] trying other Gemini image models:', extra.join(', '));
        for (const model of extra) {
            const out = await attempt(model);
            if (out) return out;
            if (deadline - Date.now() < 5_000) break;
        }
    }
    const err = new Error(problems.join(' | ') || String(lastErr && lastErr.message || 'gemini failed'));
    err.compact = problems.join(' | ');
    if (refusal) err.refusal = refusal;
    throw err;
}

function geminiLabel(model) {
    const v = (String(model).match(/gemini-(\d+(?:\.\d+)?)/i) || [])[1];
    return v ? `Gemini ${v}` : 'Gemini';
}

// One short label per provider/model so BOTH reasons fit in the app's error bubble.
function editLabel(name) {
    if (/qwen/i.test(name)) return 'Qwen';
    if (/flux/i.test(name)) return 'FLUX';
    if (/agnes/i.test(name)) return 'Agnes';
    return String(name).slice(0, 10);
}
function shortEditErr(label, msg) {
    msg = String(msg || '');
    const code = (msg.match(/\b([45]\d\d)\b/) || [])[1] || '';
    let why = (msg.match(/model_not_found|RESOURCE_EXHAUSTED|quota|rate.?limit|no image|no key|timeout|abort|unsafe|invalid/i) || [])[0] || '';
    why = why.replace(/model_not_found/i, 'nomodel').replace(/RESOURCE_EXHAUSTED/i, 'quota');
    return `${label} ${code} ${why}`.replace(/\s+/g, ' ').trim();
}

async function agnesListModels(key) {
    try {
        const res = await fetchWithTimeout(`${AGNES_ROOT}/v1/models`, { headers: { 'Authorization': `Bearer ${key}` } }, 15_000);
        const j = JSON.parse(await res.text());
        return (Array.isArray(j.data) ? j.data : []).map(m => m && m.id).filter(Boolean);
    } catch (_) { return []; }
}

// "FLUX.2 Klein" -> also "flux.2-klein", "FLUX.2-Klein": the exact id is not documented.
function modelSpellings(name) {
    const n = name.trim();
    return [...new Set([n, n.toLowerCase(), n.replace(/\s+/g, '-'), n.toLowerCase().replace(/\s+/g, '-')])];
}

async function agnesEditRaw(model, prompt, mime, image, timeoutMs) {
    const key = agnesNextKey();
    let res;
    if (/\/images\/generations$/.test(AGNES_EDIT_PATH)) {
        // Agnes image-to-image: same JSON endpoint as text-to-image, the source picture goes in "image" as a data URI.
        res = await fetchWithTimeout(`${AGNES_ROOT}${AGNES_EDIT_PATH}`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model, prompt, size: '1024x1024', n: 1,
                image: [`data:${mime};base64,${image}`],
                response_format: 'b64_json'
            })
        }, timeoutMs);
    } else {
        // OpenAI-style multipart edit endpoint (only when AGNES_IMAGE_EDIT_PATH points to one).
        const ext = (mime.split('/')[1] || 'png').replace('jpeg', 'jpg');
        const form = new FormData();
        form.append('model', model);
        form.append('prompt', prompt);
        form.append('n', '1');
        form.append('size', '1024x1024');
        form.append('response_format', 'b64_json');
        form.append('image', new Blob([Buffer.from(image, 'base64')], { type: mime }), `input.${ext}`);
        // No Content-Type header: fetch adds the multipart boundary itself.
        res = await fetchWithTimeout(`${AGNES_ROOT}${AGNES_EDIT_PATH}`, {
            method: 'POST', headers: { 'Authorization': `Bearer ${key}` }, body: form
        }, timeoutMs);
    }
    const json = await agnesJson(res, 'image-edit');
    const item = Array.isArray(json && json.data) ? json.data[0] : null;
    if (item && typeof item.b64_json === 'string' && item.b64_json.length > 100) {
        return { image: item.b64_json, mime: 'image/png', model };
    }
    const url = (item && agnesIsHttp(item.url) && item.url) || agnesDeepFind(json, ['url', 'image_url'], agnesIsHttp);
    if (!url) throw new Error('agnes image-edit: no image in response');
    return { ...(await freeImageFromUrl(url, {})), model };
}

// "no available server" (503) is a momentary capacity error on Agnes' side: one short retry before moving on.
async function agnesEditOnce(model, prompt, mime, image, timeoutMs) {
    try {
        return await agnesEditRaw(model, prompt, mime, image, timeoutMs);
    } catch (e) {
        if (/HTTP 503|no available server/i.test(String(e.message || '')) && timeoutMs > 25_000) {
            await new Promise(r => setTimeout(r, 2_500));
            return await agnesEditRaw(model, prompt, mime, image, timeoutMs - 2_500);
        }
        throw e;
    }
}

// Tries EVERY Agnes model: the configured ones (and each one's spellings) first, then any other
// image model listed on the account. Moderation rejections and any other failure just move on to the next model.
async function editImageWithAgnes(prompt, mime, image, deadline) {
    if (AGNES_API_KEYS.length === 0) throw new Error('agnes: no key');
    const problems = [];
    const tried = new Set();
    let refusal = '';
    let sawNotFound = false;

    const tryModel = async (wanted, spellings) => {
        let lastErr = null;
        for (const model of spellings) {
            tried.add(model.toLowerCase());
            const left = deadline - Date.now();
            if (left < 8_000) { lastErr = lastErr || new Error('timeout'); break; }
            try {
                return { out: await agnesEditOnce(model, prompt, mime, image, Math.min(AGNES_EDIT_TIMEOUT_MS, left)) };
            } catch (e) {
                lastErr = e;
                const msg = String(e.message || '');
                if (/moderation|safety|policy|prohibited|nsfw/i.test(msg)) { refusal = refusal || msg.slice(0, 200); break; }
                if (!/model_not_found|HTTP 404/i.test(msg)) break;   // real failure: next model, not next spelling
                sawNotFound = true;
            }
        }
        const isRefusal = lastErr && /moderation|safety|policy|prohibited|nsfw/i.test(String(lastErr.message || ''));
        problems.push(isRefusal ? `${editLabel(wanted)} refused` : shortEditErr(editLabel(wanted), lastErr && lastErr.message));
        console.warn(`[image-edit] agnes "${wanted}" failed: ${String(lastErr && lastErr.message || '').slice(0, 160)}`);
        return { out: null };
    };

    for (const wanted of AGNES_EDIT_MODELS) {
        const r = await tryModel(wanted, modelSpellings(wanted));
        if (r.out) return r.out;
    }

    // Everything configured failed: try every other image model this account can see.
    if (deadline - Date.now() >= 8_000) {
        const avail = (await agnesListModels(agnesNextKey())).filter(id => /image|edit|flux|qwen/i.test(id));
        console.warn('[image-edit] Agnes image models on this account:', avail.join(', ') || '(could not list)');
        for (const id of avail) {
            if (tried.has(id.toLowerCase())) continue;
            const r = await tryModel(id, [id]);
            if (r.out) return r.out;
        }
    } else if (sawNotFound) {
        console.warn('[image-edit] Agnes: out of time before listing account models');
    }

    const err = new Error(problems.join(' | '));
    err.compact = problems.join(' | ');
    if (refusal) err.refusal = refusal;
    throw err;
}

// ----------------------------------------------------------------------------
// Image editing: original picture + instruction -> edited picture (Gemini image models)
// ----------------------------------------------------------------------------
app.post('/api/ai/image-edit', async (req, res) => {
    const body = req.body || {};
    const { licenseKey, deviceId, prompt, image } = body;
    const mime = typeof body.mime === 'string' ? body.mime : '';
    const cost = 2;

    if (!isValidDeviceId(deviceId)) return res.status(400).json({ error: 'Invalid device' });
    if (typeof prompt !== 'string' || prompt.length < 3 || prompt.length > 1000) return res.status(400).json({ error: 'Invalid prompt' });
    if (typeof image !== 'string' || image.length < 100) return res.status(400).json({ error: 'Invalid image' });
    if (!/^image\/(png|jpeg|webp|heic|heif)$/.test(mime)) return res.status(400).json({ error: 'Unsupported image type' });
    if (!isAcceptedKey(licenseKey)) return res.status(401).json({ error: 'INVALID_LICENSE', reason: 'bad_key_signature' });
    if (isFreeKey(licenseKey) && !limitCheck(freeImageLimiter, licenseKey, deviceId, req.ip).allowed) return res.status(429).json({ error: 'RATE_LIMIT' });
    if (GEMINI_API_KEYS.length === 0 && AGNES_API_KEYS.length === 0) return res.status(503).json({ error: 'AI_NOT_CONFIGURED' });
    if (!firebaseReady) return res.status(503).json({ error: 'Service not ready' });

    let jobId = null;
    try {
        const r = await deductCredits(licenseKey, deviceId, cost, 'image', prompt);
        jobId = r.jobId;
    } catch (e) {
        if (e.message === 'INSUFFICIENT_CREDITS') return res.status(402).json({ error: 'INSUFFICIENT_CREDITS' });
        if (e.message === 'LICENSE_BOUND_TO_OTHER_DEVICE') return res.status(403).json({ error: 'LICENSE_BOUND' });
        console.warn('[license] charge failed:', e.message);
        if (e.message === 'INVALID_LICENSE') return res.status(401).json({ error: 'INVALID_LICENSE', reason: 'license_not_found' });
        return res.status(503).json({ error: 'SERVER_ERROR', reason: String(e.message || '').slice(0, 120) });
    }

    try {
        const steps = [];
        const deadline = Date.now() + EDIT_TOTAL_BUDGET_MS;
        if (GEMINI_API_KEYS.length > 0) steps.push(['Gemini', () => editImageWithGemini(prompt, mime, image)]);
        if (AGNES_API_KEYS.length > 0) steps.push(['Agnes', () => editImageWithAgnes(prompt, mime, image, deadline)]);
        let b64 = null, outMime = 'image/png', lastErr = null, refusal = '', usedModel = '';
        const errs = [];
        for (const [name, run] of steps) {
            try {
                const out = await run();
                b64 = out.image; outMime = out.mime; usedModel = out.model;
                console.log(`🖌️ image-edit ready (${name}: ${usedModel})`);
                break;
            } catch (err) {
                lastErr = err;
                errs.push(err.compact || shortEditErr(name === 'Gemini' ? 'Gemini' : name, err.message));
                console.warn(`[image-edit] ${name} failed:`, String(err.message || '').slice(0, 200));
                if (err.refusal) refusal = refusal || err.refusal;   // remembered, but the chain keeps going with the next provider
            }
        }

        if (!b64) {
            // Nothing was produced: refund through the same failure path as the other routes.
            try { await failJob(jobId, `image-edit failed: ${(lastErr && lastErr.message) || 'no image'}`); } catch (_) {}
            if (refusal) return res.status(422).json({ error: refusal });
            return res.status(502).json({ message: (errs.join(' | ') || String((lastErr && lastErr.message) || '')).slice(0, 300), error: 'AI_FAILED' });
        }

        if (jobId) db.collection('jobs').doc(jobId).update({
            status: 'completed', completedAt: admin.firestore.FieldValue.serverTimestamp()
        }).catch(() => {});
        return res.json({ image: b64, mime: outMime, model: usedModel });
    } catch (e) {
        try { await failJob(jobId, `image-edit failed: ${e.message}`); } catch (_) {}
        return res.status(502).json({ error: 'AI_FAILED', message: String(e.message || '').slice(0, 300) });
    }
});

// ============================================================================
// 12. AI TTS — Gemini (24kHz mono 16-bit PCM). Keeps the app's ten voices (Kore, Aoede, ...).
// ============================================================================
const GEMINI_TTS_VOICES = ['Kore', 'Aoede', 'Leda', 'Zephyr', 'Sulafat', 'Charon', 'Puck', 'Orus', 'Fenrir', 'Achird'];
const GEMINI_TTS_DEFAULT_VOICE = 'Kore';
// GEMINI_TTS_MODEL (Render env) can override the first model tried.
const GEMINI_TTS_MODELS = [
    (process.env.GEMINI_TTS_MODEL || '').trim(),
    'gemini-2.5-flash-preview-tts',
    'gemini-2.5-pro-preview-tts'
].filter((m, i, arr) => m && arr.indexOf(m) === i);

function resolveTtsVoice(voiceId) {
    const wanted = String(voiceId || '').trim().toLowerCase();
    return GEMINI_TTS_VOICES.find(v => v.toLowerCase() === wanted) || GEMINI_TTS_DEFAULT_VOICE;
}

// The app speaks a reply sentence by sentence (one request per sentence).
// Charge ONE credit per reply: the first request of a replyId pays, the others wait for that charge and ride along.
const TTS_REPLY_TTL_MS = 10 * 60_000;
const ttsPaidReplies = new Map(); // `${licenseKey}|${replyId}` -> { exp, charge: Promise }
setInterval(() => {
    const now = Date.now();
    for (const [k, v] of ttsPaidReplies) if (v.exp <= now) ttsPaidReplies.delete(k);
}, 60_000).unref();

async function geminiTtsPcm(text, voice) {
    let lastErr = null;
    const keyTries = Math.min(Math.max(GEMINI_API_KEYS.length, 1), 3);
    for (const model of GEMINI_TTS_MODELS) {
        for (let attempt = 0; attempt < keyTries; attempt++) {
            const apiKey = getNextGeminiKey();
            try {
                const r = await fetchWithTimeout(
                    `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`,
                    {
                        method: 'POST',
                        headers: { 'x-goog-api-key': apiKey, 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            contents: [{ parts: [{ text }] }],
                            generationConfig: {
                                responseModalities: ['AUDIO'],
                                speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: voice } } }
                            }
                        })
                    },
                    30_000
                );
                const raw = await r.text();
                if (!r.ok) {
                    lastErr = new Error(`${model} ${r.status}: ${raw.slice(0, 200)}`);
                    if (r.status === 404) break; // this model name does not exist: go to the next model
                    continue;                    // otherwise retry with the next key
                }
                const json = JSON.parse(raw);
                const parts = json.candidates?.[0]?.content?.parts || [];
                const audioPart = parts.find(p => (p.inlineData || p.inline_data)?.data);
                const data = audioPart && (audioPart.inlineData || audioPart.inline_data).data;
                if (!data) { lastErr = new Error(`${model}: no audio in response`); continue; }
                let pcm = Buffer.from(data, 'base64');
                if (pcm.length % 2 !== 0) pcm = pcm.subarray(0, pcm.length - 1);
                if (pcm.length === 0) { lastErr = new Error(`${model}: empty audio`); continue; }
                return pcm;
            } catch (e) {
                lastErr = e;
            }
        }
    }
    throw lastErr || new Error('tts: failed');
}

function sendTtsChargeError(res, e) {
    if (e && e.message === 'INSUFFICIENT_CREDITS') return res.status(402).json({ error: 'INSUFFICIENT_CREDITS' });
    console.warn('[license] charge failed:', e && e.message);
    if (e && e.message === 'INVALID_LICENSE') return res.status(401).json({ error: 'INVALID_LICENSE', reason: 'license_not_found' });
    return res.status(503).json({ error: 'SERVER_ERROR', reason: String((e && e.message) || '').slice(0, 120) });
}

app.post('/api/ai/tts', async (req, res) => {
    const body = req.body || {};
    const { licenseKey, deviceId, text, voiceId } = body;
    const cleanText = typeof text === 'string' ? text.trim() : '';
    const replyId = (typeof body.replyId === 'string' && /^[A-Za-z0-9_-]{8,64}$/.test(body.replyId)) ? body.replyId : null;

    if (!isValidDeviceId(deviceId)) return res.status(400).json({ error: 'Invalid device' });
    if (!cleanText || cleanText.length > 5000) return res.status(400).json({ error: 'Invalid text' });
    if (!isAcceptedKey(licenseKey)) return res.status(401).json({ error: 'INVALID_LICENSE', reason: 'bad_key_signature' });
    if (!firebaseReady) return res.status(503).json({ error: 'Service not ready' });

    if (GEMINI_API_KEYS.length === 0) {
        return res.status(503).json({ error: 'TTS_NOT_CONFIGURED', message: 'Gemini key not configured. App will use phone TTS.' });
    }

    const rl = limitCheck(ttsLimiter, licenseKey, deviceId, req.ip);
    if (!rl.allowed) {
        return res.status(429).json({ error: 'RATE_LIMIT', retryAfter: Math.ceil((rl.resetAt - Date.now()) / 1000) });
    }

    // One credit per reply (see ttsPaidReplies). Requests without replyId are charged one by one, as before.
    const paidKey = replyId ? `${licenseKey}|${replyId}` : null;
    let entry = paidKey ? ttsPaidReplies.get(paidKey) : null;
    if (entry && entry.exp <= Date.now()) { ttsPaidReplies.delete(paidKey); entry = null; }

    let chargePromise;
    if (entry) {
        chargePromise = entry.charge;
    } else {
        chargePromise = deductCredits(licenseKey, deviceId, 1, 'tts', cleanText.slice(0, 100));
        if (paidKey) {
            ttsPaidReplies.set(paidKey, { exp: Date.now() + TTS_REPLY_TTL_MS, charge: chargePromise });
            chargePromise.catch(() => ttsPaidReplies.delete(paidKey));
        }
    }
    let charge;
    try {
        charge = await chargePromise;
    } catch (e) {
        return sendTtsChargeError(res, e);
    }
    const jobId = entry ? null : ((charge && charge.jobId) || null); // only the request that paid can refund

    try {
        const pcmBuffer = await geminiTtsPcm(cleanText, resolveTtsVoice(voiceId));

        if (jobId) db.collection('jobs').doc(jobId).update({
            status: 'completed', completedAt: admin.firestore.FieldValue.serverTimestamp()
        }).catch(() => {});

        res.set('Content-Type', 'application/octet-stream');
        res.set('X-Sample-Rate', '24000');
        res.set('X-Channels', '1');
        res.send(pcmBuffer);
    } catch (e) {
        if (jobId) {
            if (paidKey) ttsPaidReplies.delete(paidKey); // refunded: the next sentence pays again
            try { await failJob(jobId, `tts failed: ${e.message}`); } catch (_) {}
        }
        return res.status(502).json({ error: 'TTS_FAILED', message: String(e.message || '').slice(0, 200) });
    }
});

// ============================================================================
// 13. Video / Music / Edit Video
// ============================================================================
app.post(['/api/generate-video', '/api/generate-music'], async (req, res) => {
    const body = req.body || {};
    const prompt = typeof body.prompt === 'string' ? body.prompt.trim() : '';
    const { deviceId, licenseKey } = body;
    const type = req.path.endsWith('-video') ? 'video' : 'music';
    if (prompt.length < 3 || prompt.length > 500) return res.status(400).json({ error: 'Invalid prompt' });
    if (!isValidDeviceId(deviceId)) return res.status(400).json({ error: 'Invalid device' });

    const cost = type === 'video' ? 60 : 5;
    try {
        if (!isValidLicenseKey(licenseKey)) return res.status(401).json({ error: 'Invalid license' });

        // Free path first (Agnes AI). Credits are charged only if the free provider fails
        // and the paid fallback below has to run.
        if (type === 'video' && useFreeVideo(body.model) && agnesQuotaTake(deviceId)) {
            let credits;
            try { credits = await peekLicenseCredits(licenseKey, deviceId); }
            catch (e) { agnesQuotaGiveBack(deviceId); throw e; }
            res.status(200).json({ status: 'started', remaining: credits, free: true });
            runAgnesThenPaid({ prompt, deviceId, licenseKey, cost, model: body.model });
            return;
        }

        const { remaining, jobId } = await deductCredits(licenseKey, deviceId, cost, type, prompt);
        res.status(200).json({ status: 'started', remaining });
        (type === 'video' ? generateVideoPaidChain(prompt, deviceId, jobId, body.model) : triggerReplicateAsync(prompt, deviceId, type, jobId)).catch(err => {
            console.error(`Background error (${type}):`, err.message);
            handleFailure(jobId, deviceId, type, `Start failed: ${err.message}`, 'Generation failed to start');
        });
    } catch (e) {
        if (e.message === 'INSUFFICIENT_CREDITS') return res.status(402).json({ error: 'Insufficient credits' });
        if (e.message === 'LICENSE_BOUND_TO_OTHER_DEVICE') return res.status(403).json({ error: 'License used on another device' });
        if (e.message === 'INVALID_LICENSE') return res.status(401).json({ error: 'Invalid license' });
        return res.status(500).json({ error: 'Internal error' });
    }
});

app.post('/api/edit-video', upload.single('video'), async (req, res) => {
    const body = req.body || {};
    const { deviceId, licenseKey } = body;
    const prompt = typeof body.prompt === 'string' ? body.prompt.trim() : '';
    const file = req.file;
    if (!isValidDeviceId(deviceId)) return res.status(400).json({ error: 'Invalid device' });
    if (!file) return res.status(400).json({ error: 'No video file uploaded' });
    if (prompt.length < 3 || prompt.length > 500) return res.status(400).json({ error: 'Invalid prompt' });

    const cost = 60;
    try {
        if (!isValidLicenseKey(licenseKey)) return res.status(401).json({ error: 'Invalid license' });
        const { remaining, jobId } = await deductCredits(licenseKey, deviceId, cost, 'video', prompt);
        res.status(200).json({ status: 'started', remaining });
        (useOmni(body.model) ? editVideoWithOmni(file, prompt, deviceId, jobId) : processVideoEdit(file, prompt, deviceId, jobId)).catch(err => {
            console.error('Edit Video Error:', err.message);
            handleFailure(jobId, deviceId, 'video', `Edit failed: ${err.message}`, 'Edit failed');
        });
    } catch (e) {
        if (e.message === 'INSUFFICIENT_CREDITS') return res.status(402).json({ error: 'Insufficient credits' });
        if (e.message === 'LICENSE_BOUND_TO_OTHER_DEVICE') return res.status(403).json({ error: 'License used on another device' });
        if (e.message === 'INVALID_LICENSE') return res.status(401).json({ error: 'Invalid license' });
        return res.status(500).json({ error: 'Internal error' });
    }
});

app.post('/api/generate-video-ref', upload.fields([{ name: 'image', maxCount: 1 }, { name: 'audio', maxCount: 1 }]), async (req, res) => {
    const body = req.body || {};
    const { deviceId, licenseKey } = body;
    const prompt = typeof body.prompt === 'string' ? body.prompt.trim() : '';
    const files = req.files || {};
    const image = files.image && files.image[0];
    const audio = files.audio && files.audio[0];
    if (!isValidDeviceId(deviceId)) return res.status(400).json({ error: 'Invalid device' });
    if (!image && !audio) return res.status(400).json({ error: 'No image or audio uploaded' });
    if (prompt.length < 3 || prompt.length > 500) return res.status(400).json({ error: 'Invalid prompt' });
    if (image && (!REF_IMAGE_MIMES.includes(image.mimetype) || image.size > REF_IMAGE_MAX)) return res.status(400).json({ error: 'Invalid image' });
    if (audio && (!REF_AUDIO_MIMES.includes(audio.mimetype) || audio.size > REF_AUDIO_MAX)) return res.status(400).json({ error: 'Invalid audio' });
    if (GEMINI_API_KEYS.length === 0 && HF_REF_VIDEOS.length === 0) return res.status(503).json({ error: 'Video from image/audio is not configured' });

    const cost = 60;
    try {
        if (!isValidLicenseKey(licenseKey)) return res.status(401).json({ error: 'Invalid license' });
        if (HF_REF_VIDEOS.length > 0) {
            // Free path first: license is checked, nothing is charged unless every free Space fails.
            const credits = await peekLicenseCredits(licenseKey, deviceId);
            res.status(200).json({ status: 'started', remaining: credits, free: true });
            runRefsFreeThenGemini({ image, audio, prompt, deviceId, licenseKey, cost });
            return;
        }
        const { remaining, jobId } = await deductCredits(licenseKey, deviceId, cost, 'video', prompt);
        res.status(200).json({ status: 'started', remaining });
        generateVideoFromRefsWithOmni(image, audio, prompt, deviceId, jobId).catch(err => {
            console.error('Video-from-refs Error:', err.message);
            handleFailure(jobId, deviceId, 'video', `Image/audio video failed: ${err.message}`, 'Generation failed');
        });
    } catch (e) {
        if (e.message === 'INSUFFICIENT_CREDITS') return res.status(402).json({ error: 'Insufficient credits' });
        if (e.message === 'LICENSE_BOUND_TO_OTHER_DEVICE') return res.status(403).json({ error: 'License used on another device' });
        if (e.message === 'INVALID_LICENSE') return res.status(401).json({ error: 'Invalid license' });
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
// 14. Replicate + Webhook
// ============================================================================
function buildWebhookUrl(deviceId, type, jobId, prompt) {
    return `${BASE_URL}/webhook/replicate?deviceId=${encodeURIComponent(deviceId)}&type=${type}&jobId=${encodeURIComponent(jobId || '')}&token=${webhookToken(deviceId, type, jobId)}&prompt=${encodeURIComponent(prompt)}`;
}

async function triggerReplicateAsync(prompt, deviceId, type, jobId) {
    if (!REPLICATE_TOKEN || !BASE_URL) throw new Error('Missing env vars');
    const configured = type === 'video' ? REPLICATE_VIDEO_VERSION : REPLICATE_MUSIC_VERSION;
    if (!configured) throw new Error(`REPLICATE_${type.toUpperCase()}_VERSION missing`);
    const version = configured.includes(':') ? configured.split(':').pop() : configured;
    const response = await fetch('https://api.replicate.com/v1/predictions', {
        method: 'POST',
        headers: { 'Authorization': `Token ${REPLICATE_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ version, input: { prompt }, webhook: buildWebhookUrl(deviceId, type, jobId, prompt), webhook_events_filter: ['completed'] })
    });
    if (!response.ok) throw new Error(await response.text());
    console.log(`🚀 ${type} started for ${deviceId}`);
}

async function processVideoEdit(file, prompt, deviceId, jobId) {
    if (!REPLICATE_TOKEN || !BASE_URL) throw new Error('Missing env vars');
    if (!REPLICATE_EDIT_VIDEO_VERSION) throw new Error('REPLICATE_EDIT_VIDEO_VERSION missing');
    if (!bucket) throw new Error('Firebase Storage not ready');
    const originalFileName = `originals/${deviceId}/${Date.now()}.mp4`;
    const bucketFile = bucket.file(originalFileName);
    await bucketFile.save(file.buffer, { contentType: file.mimetype || 'video/mp4' });
    const [publicUrl] = await bucketFile.getSignedUrl({ version: 'v4', action: 'read', expires: Date.now() + 3_600_000 });
    const version = REPLICATE_EDIT_VIDEO_VERSION.includes(':') ? REPLICATE_EDIT_VIDEO_VERSION.split(':').pop() : REPLICATE_EDIT_VIDEO_VERSION;
    const response = await fetch('https://api.replicate.com/v1/predictions', {
        method: 'POST',
        headers: { 'Authorization': `Token ${REPLICATE_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ version, input: { prompt, video: publicUrl }, webhook: buildWebhookUrl(deviceId, 'video', jobId, prompt), webhook_events_filter: ['completed'] })
    });
    if (!response.ok) throw new Error(await response.text());
    console.log(`🚀 Edit video started for ${deviceId}`);
}

// ----------------------------------------------------------------------------
// Gemini Omni 1.1 Flash: video generation + video editing ONLY (Interactions API).
// Used when a Gemini key exists and the app asks for it (or sends no model).
// Music (and Replicate as a fallback) are left exactly as they were.
// ----------------------------------------------------------------------------
const GEMINI_VIDEO_MODEL = 'gemini-omni-1.1-flash';
const GEMINI_API_BASE = 'https://generativelanguage.googleapis.com';
const OMNI_TIMEOUT_MS = parseInt(process.env.OMNI_TIMEOUT_MS) || 600_000;
const OMNI_VIDEO_MIMES = ['video/mp4', 'video/mpeg', 'video/quicktime', 'video/webm', 'video/3gpp'];

function useOmni(requestedModel) {
    if (GEMINI_API_KEYS.length === 0) return false;
    return !requestedModel || requestedModel === GEMINI_VIDEO_MODEL;
}

const omniSleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// Only the Google Files host may receive the API key (the uri comes from a response).
function assertGoogleFilesUri(uri) {
    let host = '';
    try { host = new URL(String(uri)).hostname; } catch (_) {}
    if (host !== 'generativelanguage.googleapis.com') throw new Error('gemini-omni: unexpected file host');
}

async function omniCreate(apiKey, input) {
    const response = await fetchWithTimeout(`${GEMINI_API_BASE}/v1beta/interactions`, {
        method: 'POST',
        headers: { 'x-goog-api-key': apiKey, 'Content-Type': 'application/json' },
        body: JSON.stringify({
            model: GEMINI_VIDEO_MODEL,
            input,
            // URI delivery: generated videos are usually larger than the 4MB inline limit.
            response_format: { type: 'video', delivery: 'uri' }
        })
    }, OMNI_TIMEOUT_MS);
    if (!response.ok) throw new Error(`gemini-omni ${response.status}: ${(await response.text()).slice(0, 300)}`);
    return await response.json();
}

function omniExtractVideo(json) {
    if (json && json.output_video && (json.output_video.data || json.output_video.uri)) return json.output_video;
    for (const step of ((json && json.steps) || [])) {
        if (step.type !== 'model_output') continue;
        for (const part of (step.content || [])) {
            if (part.type === 'video' && (part.data || part.uri)) return part;
        }
    }
    return null;
}

async function waitGeminiFileActive(fileUri, apiKey) {
    assertGoogleFilesUri(fileUri);
    const m = String(fileUri).match(/files\/([A-Za-z0-9_-]+)/);
    if (!m) return;
    const url = `${GEMINI_API_BASE}/v1beta/files/${m[1]}`;
    const deadline = Date.now() + 180_000;
    while (Date.now() < deadline) {
        const r = await fetchWithTimeout(url, { headers: { 'x-goog-api-key': apiKey } }, 30_000);
        if (r.ok) {
            const info = await r.json();
            const state = String(info.state || '').toUpperCase();
            if (state === 'ACTIVE') return;
            if (state === 'FAILED') throw new Error('gemini-omni: file processing failed');
        }
        await omniSleep(4000);
    }
    throw new Error('gemini-omni: file processing timeout');
}

async function omniUploadVideo(apiKey, buffer, mimeType) {
    const start = await fetchWithTimeout(`${GEMINI_API_BASE}/upload/v1beta/files`, {
        method: 'POST',
        headers: {
            'x-goog-api-key': apiKey,
            'X-Goog-Upload-Protocol': 'resumable',
            'X-Goog-Upload-Command': 'start',
            'X-Goog-Upload-Header-Content-Length': String(buffer.length),
            'X-Goog-Upload-Header-Content-Type': mimeType,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ file: { display_name: 'video-edit-input' } })
    }, 60_000);
    if (!start.ok) throw new Error(`gemini-omni upload start ${start.status}: ${(await start.text()).slice(0, 200)}`);
    const uploadUrl = start.headers.get('x-goog-upload-url');
    if (!uploadUrl) throw new Error('gemini-omni upload: no upload url');
    assertGoogleFilesUri(uploadUrl);
    const up = await fetchWithTimeout(uploadUrl, {
        method: 'POST',
        headers: { 'X-Goog-Upload-Offset': '0', 'X-Goog-Upload-Command': 'upload, finalize' },
        body: buffer
    }, 300_000);
    if (!up.ok) throw new Error(`gemini-omni upload ${up.status}: ${(await up.text()).slice(0, 200)}`);
    const info = await up.json();
    const file = info.file || info;
    if (!file.uri) throw new Error('gemini-omni upload: no file uri');
    return file;
}

async function omniVideoBuffer(apiKey, part) {
    if (part.data) return Buffer.from(part.data, 'base64');
    await waitGeminiFileActive(part.uri, apiKey);
    const dl = await fetchWithTimeout(part.uri, { headers: { 'x-goog-api-key': apiKey } }, 180_000);
    if (!dl.ok) throw new Error(`gemini-omni download ${dl.status}`);
    return Buffer.from(await dl.arrayBuffer());
}

// Same storage / notification steps the Replicate webhook does, but with the bytes we already have.
async function omniSaveAndNotify(buffer, deviceId, jobId, prompt) {
    if (!firebaseReady || !bucket) throw new Error('Firebase Storage not ready');
    const bucketFile = bucket.file(`videos/${deviceId}/${Date.now()}.mp4`);
    await bucketFile.save(buffer, { contentType: 'video/mp4' });
    const [signedUrl] = await bucketFile.getSignedUrl({
        version: 'v4', action: 'read', expires: Date.now() + 7 * 24 * 3_600_000 - 5 * 60_000
    });
    await db.collection('videos').doc(deviceId).collection('items').add({
        url: signedUrl, prompt: prompt || '', createdAt: admin.firestore.FieldValue.serverTimestamp()
    });
    if (jobId) await db.collection('jobs').doc(jobId).update({
        status: 'completed', completedAt: admin.firestore.FieldValue.serverTimestamp()
    }).catch(() => {});
    await sendNotification(deviceId, 'video_ready', { url: signedUrl, prompt: String(prompt || '') });
}

// Paid chain for video generation: Gemini Omni first, then Replicate if Omni fails (and Replicate is configured).
// The Replicate result arrives later through /webhook/replicate, which also handles its own failures.
async function generateVideoPaidChain(prompt, deviceId, jobId, model) {
    if (!useOmni(model)) return triggerReplicateAsync(prompt, deviceId, 'video', jobId);
    try {
        await generateVideoWithOmni(prompt, deviceId, jobId);
    } catch (omniErr) {
        if (!REPLICATE_TOKEN || !BASE_URL || !REPLICATE_VIDEO_VERSION) throw omniErr;
        console.warn('[video] Gemini Omni failed, trying Replicate:', String(omniErr.message || '').slice(0, 200));
        try {
            await triggerReplicateAsync(prompt, deviceId, 'video', jobId);
        } catch (repErr) {
            throw new Error(`omni: ${String(omniErr.message || '').slice(0, 120)} | replicate: ${String(repErr.message || '').slice(0, 120)}`);
        }
    }
}

async function generateVideoWithOmni(prompt, deviceId, jobId) {
    let json = null, key = null, lastErr = null;
    const tries = Math.min(GEMINI_API_KEYS.length, 3);
    for (let i = 0; i < tries; i++) {
        key = getNextGeminiKey();
        try { json = await omniCreate(key, prompt); lastErr = null; break; }
        catch (e) { lastErr = e; if (!/^gemini-omni (429|500|503)/.test(e.message)) break; }
    }
    if (lastErr) throw lastErr;
    const part = omniExtractVideo(json);
    if (!part) throw new Error(`gemini-omni returned no video (status=${json && json.status})`);
    await omniSaveAndNotify(await omniVideoBuffer(key, part), deviceId, jobId, prompt);
    console.log(`🚀 ${GEMINI_VIDEO_MODEL} video ready for ${deviceId}`);
}

async function editVideoWithOmni(file, prompt, deviceId, jobId) {
    // The uploaded file only exists for the key that uploaded it: one key for the whole job.
    const key = getNextGeminiKey();
    const mime = OMNI_VIDEO_MIMES.includes(file.mimetype) ? file.mimetype : 'video/mp4';
    const uploaded = await omniUploadVideo(key, file.buffer, mime);
    await waitGeminiFileActive(uploaded.uri, key);
    const json = await omniCreate(key, [{ type: 'video', uri: uploaded.uri }, { type: 'text', text: prompt }]);
    const part = omniExtractVideo(json);
    if (!part) throw new Error(`gemini-omni returned no video (status=${json && json.status})`);
    await omniSaveAndNotify(await omniVideoBuffer(key, part), deviceId, jobId, prompt);
    console.log(`🚀 ${GEMINI_VIDEO_MODEL} edit ready for ${deviceId}`);
}

// Video from an IMAGE and/or an AUDIO file (+ text prompt) through Gemini Omni.
const REF_IMAGE_MIMES = ['image/png', 'image/jpeg', 'image/webp'];
const REF_AUDIO_MIMES = ['audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/x-wav', 'audio/wave', 'audio/ogg', 'audio/aac', 'audio/flac', 'audio/mp4', 'audio/x-m4a', 'audio/m4a'];
const REF_IMAGE_MAX = 15 * 1024 * 1024;
const REF_AUDIO_MAX = 30 * 1024 * 1024;

async function generateVideoFromRefsWithOmni(image, audio, prompt, deviceId, jobId) {
    // Uploaded files only exist for the key that uploaded them: one key for the whole job.
    const key = getNextGeminiKey();
    const input = [];
    if (image) {
        const up = await omniUploadVideo(key, image.buffer, image.mimetype);
        await waitGeminiFileActive(up.uri, key);
        input.push({ type: 'image', uri: up.uri });
    }
    if (audio) {
        const up = await omniUploadVideo(key, audio.buffer, audio.mimetype);
        await waitGeminiFileActive(up.uri, key);
        input.push({ type: 'audio', uri: up.uri });
    }
    input.push({ type: 'text', text: prompt });
    const json = await omniCreate(key, input);
    const part = omniExtractVideo(json);
    if (!part) throw new Error(`gemini-omni returned no video (status=${json && json.status})`);
    await omniSaveAndNotify(await omniVideoBuffer(key, part), deviceId, jobId, prompt);
    console.log(`🚀 ${GEMINI_VIDEO_MODEL} image/audio video ready for ${deviceId}`);
}

// ----------------------------------------------------------------------------
// Agnes AI: FREE video generation (needs a free AGNES_API_KEY from agnes-ai.com).
// Flow: POST {base}/v1/videos  ->  poll  ->  download mp4  ->  same Firebase save + FCM `video_ready`.
// If Agnes fails for any reason, the previous paid chain (Gemini Omni / Replicate) runs and
// credits are deducted only then. Everything is optional: no AGNES_API_KEY = old behaviour.
//
// Env (all optional except the key):
//   AGNES_API_KEY          one key, or several separated by commas
//   AGNES_API_BASE         default https://apihub.agnes-ai.com   (with or without /v1)
//   AGNES_VIDEO_MODEL      default agnes-video-2.5-flash
//   AGNES_VIDEO_EXTRA      JSON merged into the create request body, e.g. {"seconds":5}
//   AGNES_VIDEO_MODE       default text (text-to-video); other values: keyframe / reference
//   AGNES_DAILY_LIMIT      free videos per device per day (default 5, 0 = unlimited)
//   AGNES_TIMEOUT_MS       max wait for one video (default 600000)
//   (to turn the free path off, remove AGNES_API_KEY)
// ----------------------------------------------------------------------------
const AGNES_API_KEYS = (process.env.AGNES_API_KEY || '').split(',').map(k => k.trim()).filter(Boolean);
const AGNES_ROOT = (process.env.AGNES_API_BASE || 'https://apihub.agnes-ai.com').trim().replace(/\/+$/, '').replace(/\/v1$/, '');
const AGNES_VIDEO_MODEL = (process.env.AGNES_VIDEO_MODEL || 'agnes-video-2.5-flash').trim();
const AGNES_TIMEOUT_MS = parseInt(process.env.AGNES_TIMEOUT_MS) || 600_000;
const AGNES_DAILY_LIMIT = process.env.AGNES_DAILY_LIMIT === undefined ? 5 : (parseInt(process.env.AGNES_DAILY_LIMIT) || 0);
let agnesKeyIndex = 0;
const agnesUsage = new Map(); // deviceId -> { day, count }

function useAgnes(requestedModel) {
    if (AGNES_API_KEYS.length === 0) return false;
    // The app sends the Gemini Omni name with every generate-video request: treat it as "default" so the free providers run first.
    return !requestedModel || requestedModel === AGNES_VIDEO_MODEL || requestedModel === GEMINI_VIDEO_MODEL;
}

function agnesQuotaTake(deviceId) {
    if (!AGNES_DAILY_LIMIT) return true;
    const day = new Date().toISOString().slice(0, 10);
    const u = agnesUsage.get(deviceId);
    if (!u || u.day !== day) { agnesUsage.set(deviceId, { day, count: 1 }); return true; }
    if (u.count >= AGNES_DAILY_LIMIT) return false;
    u.count++;
    return true;
}
function agnesQuotaGiveBack(deviceId) {
    const u = agnesUsage.get(deviceId);
    if (u && u.count > 0) u.count--;
}

// Same license checks as deductCredits, but read-only (nothing is charged).
async function peekLicenseCredits(licenseKey, deviceId) {
    if (isFreeKey(licenseKey)) return 0; // free mode
    if (!firebaseReady) throw new Error('DB_NOT_READY');
    const doc = await db.collection('licenses').doc(licenseKey).get();
    if (!doc.exists) throw new Error('INVALID_LICENSE');
    const data = doc.data();
    if (data.deviceId && data.deviceId !== deviceId) throw new Error('LICENSE_BOUND_TO_OTHER_DEVICE');
    return data.credits || 0;
}

function agnesNextKey() {
    const k = AGNES_API_KEYS[agnesKeyIndex % AGNES_API_KEYS.length];
    agnesKeyIndex++;
    return k;
}

// Finds the first value stored under one of `names` anywhere in a JSON response.
function agnesDeepFind(obj, names, test, depth = 0) {
    if (!obj || typeof obj !== 'object' || depth > 6) return null;
    for (const n of names) {
        const v = obj[n];
        if (v !== undefined && v !== null && (!test || test(v))) return v;
    }
    for (const k of Object.keys(obj)) {
        const r = agnesDeepFind(obj[k], names, test, depth + 1);
        if (r !== null) return r;
    }
    return null;
}
const agnesIsHttp = (v) => typeof v === 'string' && /^https?:\/\//i.test(v);

function agnesParse(json) {
    const id = agnesDeepFind(json, ['video_id', 'task_id', 'id'], v => typeof v === 'string' || typeof v === 'number');
    const url = agnesDeepFind(json, ['video_url', 'videoUrl', 'download_url', 'url'], agnesIsHttp);
    const status = String(agnesDeepFind(json, ['status', 'state'], v => typeof v === 'string') || '').toLowerCase();
    const err = agnesDeepFind(json, ['error', 'message', 'fail_reason'], v => typeof v === 'string' || (v && typeof v === 'object'));
    return { id: id === null ? null : String(id), url, status, err };
}
const AGNES_DONE = ['completed', 'complete', 'succeeded', 'success', 'done', 'finished'];
const AGNES_FAILED = ['failed', 'failure', 'error', 'cancelled', 'canceled', 'rejected', 'expired'];

async function agnesJson(res, what) {
    const text = await res.text();
    if (!res.ok) throw new Error(`agnes ${what} HTTP ${res.status}: ${text.slice(0, 200)}`);
    try { return JSON.parse(text); }
    catch (_) { throw new Error(`agnes ${what}: response is not JSON: ${text.slice(0, 120)}`); }
}

async function agnesCreate(key, prompt) {
    let extra = {};
    try { extra = JSON.parse(process.env.AGNES_VIDEO_EXTRA || '{}'); } catch (_) {}
    const res = await fetchWithTimeout(`${AGNES_ROOT}/v1/videos`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
        // Agnes requires a "mode" ("mode is required" HTTP 400). Text-to-video = "text"; override with AGNES_VIDEO_MODE or AGNES_VIDEO_EXTRA.
        body: JSON.stringify({ model: AGNES_VIDEO_MODEL, prompt, mode: (process.env.AGNES_VIDEO_MODE || 'text').trim(), ...extra })
    }, 60_000);
    return agnesParse(await agnesJson(res, 'create'));
}

async function agnesPoll(key, videoId) {
    // The exact status route differs between Agnes docs/versions: try the known ones.
    const q = `video_id=${encodeURIComponent(videoId)}&model_name=${encodeURIComponent(AGNES_VIDEO_MODEL)}`;
    const urls = [
        `${AGNES_ROOT}/agnesapi?${q}`,
        `${AGNES_ROOT}/v1/agnesapi?${q}`,
        `${AGNES_ROOT}/v1/videos/${encodeURIComponent(videoId)}`
    ];
    let lastErr = null;
    for (const u of urls) {
        try {
            const res = await fetchWithTimeout(u, { headers: { 'Authorization': `Bearer ${key}` } }, 30_000);
            if (res.status === 404) { lastErr = new Error('agnes poll 404'); continue; }
            return agnesParse(await agnesJson(res, 'poll'));
        } catch (e) { lastErr = e; }
    }
    throw lastErr || new Error('agnes poll failed');
}

async function generateVideoWithAgnes(prompt, deviceId, jobId) {
    // Agnes answers HTTP 503 "video_queue_full" (or 429) when its free queue is busy: wait and retry a few times
    // (10s, 20s, 30s) before giving up and letting the next provider run.
    let key = null, created = null;
    for (let attempt = 0; ; attempt++) {
        key = agnesNextKey();
        try { created = await agnesCreate(key, prompt); break; }
        catch (e) {
            if (attempt >= 3 || !/HTTP (429|503)/.test(String(e.message || ''))) throw e;
            console.warn(`[agnes] queue busy, retry ${attempt + 1}/3 in ${10 * (attempt + 1)}s`);
            await omniSleep(10_000 * (attempt + 1));
        }
    }
    let result = created;
    const started = Date.now();
    const looksLikeVideo = (u) => /\.(mp4|webm|mov)(\?|$)/i.test(String(u || ''));
    while (!(result.url && (AGNES_DONE.includes(result.status) || (result.status === '' && looksLikeVideo(result.url))))) {
        if (AGNES_FAILED.includes(result.status)) {
            throw new Error(`agnes failed: ${typeof result.err === 'string' ? result.err : JSON.stringify(result.err || '').slice(0, 150)}`);
        }
        if (result.url && AGNES_DONE.includes(result.status)) break;
        if (Date.now() - started > AGNES_TIMEOUT_MS) throw new Error('agnes timeout');
        const id = (result.id || created.id);
        if (!id) throw new Error('agnes: no video id returned');
        await omniSleep(6000);
        result = await agnesPoll(key, id);
        if (!result.id) result.id = id;
    }
    const safe = await isSafeRemoteUrl(result.url);
    if (!safe.ok) throw new Error(`agnes unsafe url: ${safe.reason}`);
    const dl = await fetchWithTimeout(result.url, {}, 180_000);
    if (!dl.ok) throw new Error(`agnes download ${dl.status}`);
    const buffer = Buffer.from(await dl.arrayBuffer());
    if (buffer.length < 1024) throw new Error('agnes: downloaded file is too small');
    await omniSaveAndNotify(buffer, deviceId, jobId, prompt);
    console.log(`🚀 Agnes (${AGNES_VIDEO_MODEL}) video ready for ${deviceId}`);
}

// ----------------------------------------------------------------------------
// Hugging Face Space (free) through Gradio's plain HTTP API (no extra npm package).
// Works with any public Gradio Space that turns a text prompt into a video.
//   HF_TOKEN            your free Hugging Face token (raises the free quota)
//   HF_VIDEO_SPACE      "owner/space-name"  (required to enable this provider)
//   HF_VIDEO_API_NAME   endpoint shown on the Space's "Use via API" page (default /predict)
//   HF_VIDEO_INPUT      JSON array of inputs in order; "{prompt}" is replaced by the prompt,
//                       e.g. ["{prompt}", 5, 720]   (default ["{prompt}"])
//   HF_TIMEOUT_MS       max wait (default 600000)
// ----------------------------------------------------------------------------
const HF_TOKEN = (process.env.HF_TOKEN || '').trim();
const HF_TIMEOUT_MS = parseInt(process.env.HF_TIMEOUT_MS) || 600_000;
const HF_SPACE_RE = /^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/;

// Multi-model registry. Set HF_VIDEO_SPACES to a JSON array, one object per Space:
//   [{ "id":"minimax-h3", "label":"MiniMax H3 Turbo", "space":"MiniMaxAI/MiniMax-H3-Turbo-Lora",
//      "api":"/generate", "input":["{prompt}", 5, 6] }, ...]
//   id     = value the app sends as `model` in /api/generate-video (letters/digits/-/_)
//   api    = endpoint name from the Space's "Use via API" page
//   input  = inputs in order, "{prompt}" is replaced by the prompt
// The old single-Space variables (HF_VIDEO_SPACE / HF_VIDEO_API_NAME / HF_VIDEO_INPUT) still work as id "hf".
const HF_VIDEOS = (() => {
    const list = [];
    try {
        const arr = JSON.parse(process.env.HF_VIDEO_SPACES || '[]');
        if (Array.isArray(arr)) for (const e of arr) {
            if (!e || typeof e.id !== 'string' || !/^[A-Za-z0-9_-]{1,40}$/.test(e.id)) continue;
            if (typeof e.space !== 'string' || !HF_SPACE_RE.test(e.space)) continue;
            list.push({
                id: e.id, label: String(e.label || e.id).slice(0, 60), space: e.space,
                api: String(e.api || '/predict').trim().replace(/^\/+/, ''),
                input: Array.isArray(e.input) ? e.input : ['{prompt}']
            });
        }
    } catch (err) { console.warn('⚠️ HF_VIDEO_SPACES is not valid JSON:', err.message); }
    const legacy = (process.env.HF_VIDEO_SPACE || '').trim();
    if (HF_SPACE_RE.test(legacy) && !list.some(x => x.id === 'hf')) {
        let input = ['{prompt}'];
        try { const t = JSON.parse(process.env.HF_VIDEO_INPUT || '["{prompt}"]'); if (Array.isArray(t)) input = t; } catch (_) {}
        list.push({ id: 'hf', label: legacy, space: legacy, api: (process.env.HF_VIDEO_API_NAME || '/predict').trim().replace(/^\/+/, ''), input });
    }
    return list;
})();
const HF_SPACE_OK = HF_VIDEOS.length > 0;

// No model / default Omni name / "hf" -> try every Space in order. A specific id -> only that Space.
function hfSelect(requestedModel) {
    if (!HF_SPACE_OK) return [];
    if (!requestedModel || requestedModel === 'hf' || requestedModel === GEMINI_VIDEO_MODEL) return HF_VIDEOS;
    return HF_VIDEOS.filter(x => x.id === requestedModel);
}
function useHf(requestedModel) { return hfSelect(requestedModel).length > 0; }
function useFreeVideo(requestedModel) { return useAgnes(requestedModel) || useHf(requestedModel); }

function hfSpaceHost(space) {
    const fix = (x) => x.toLowerCase().replace(/[._]/g, '-');
    const [owner, name] = space.split('/');
    return `https://${fix(owner)}-${fix(name)}.hf.space`;
}

function hfBuildInput(entry, prompt) {
    return entry.input.map(v => typeof v === 'string' ? v.split('{prompt}').join(prompt) : v);
}

// Calls one Gradio endpoint and returns the parsed `data` array of the final result.
async function hfCallSpace(host, apiName, data, headers) {
    let lastErr = null;
    for (const prefix of ['/gradio_api', '']) {   // Gradio 5 uses /gradio_api, Gradio 4 does not
        try {
            const start = await fetchWithTimeout(`${host}${prefix}/call/${apiName}`, {
                method: 'POST',
                headers: { ...headers, 'Content-Type': 'application/json' },
                body: JSON.stringify({ data })
            }, 60_000);
            if (start.status === 404) { lastErr = new Error('hf 404'); continue; }
            if (!start.ok) throw new Error(`hf start HTTP ${start.status}: ${(await start.text()).slice(0, 150)}`);
            const { event_id } = await start.json();
            if (!event_id) throw new Error('hf: no event_id');
            const res = await fetchWithTimeout(`${host}${prefix}/call/${apiName}/${event_id}`, { headers }, HF_TIMEOUT_MS);
            if (!res.ok) throw new Error(`hf result HTTP ${res.status}`);
            const text = await res.text();          // the event stream ends after complete/error
            let ev = '', out = null;
            for (const line of text.split(/\r?\n/)) {
                if (line.startsWith('event:')) ev = line.slice(6).trim();
                else if (line.startsWith('data:')) {
                    const payload = line.slice(5).trim();
                    if (ev === 'error') throw new Error(`hf space error: ${payload.slice(0, 200)}`);
                    if (ev === 'complete') { try { out = JSON.parse(payload); } catch (_) {} }
                }
            }
            if (!out) throw new Error('hf: no result in event stream');
            return out;
        } catch (e) { lastErr = e; if (e.message !== 'hf 404') throw e; }
    }
    throw lastErr || new Error('hf call failed');
}

function hfFindVideoUrl(host, data) {
    const direct = agnesDeepFind(data, ['url'], agnesIsHttp);
    if (direct) return direct;
    if (Array.isArray(data)) for (const d of data) if (agnesIsHttp(d)) return d;
    const path = agnesDeepFind(data, ['path'], v => typeof v === 'string' && v.length > 0);
    if (path) return `${host}/gradio_api/file=${path}`;
    return null;
}

async function generateVideoWithHf(prompt, deviceId, jobId, entry) {
    const host = hfSpaceHost(entry.space);
    const headers = HF_TOKEN ? { 'Authorization': `Bearer ${HF_TOKEN}` } : {};
    const data = await hfCallSpace(host, entry.api, hfBuildInput(entry, prompt), headers);
    const url = hfFindVideoUrl(host, data);
    if (!url) throw new Error('hf: no video in result');
    const u = new URL(url);
    if (!u.hostname.endsWith('.hf.space') && !u.hostname.endsWith('.huggingface.co') && !u.hostname.endsWith('.hf.co')) {
        const safe = await isSafeRemoteUrl(url);
        if (!safe.ok) throw new Error(`hf unsafe url: ${safe.reason}`);
    }
    // The token is sent only to the Space's own host.
    const dl = await fetchWithTimeout(url, { headers: u.hostname === new URL(host).hostname ? headers : {} }, 180_000);
    if (!dl.ok) throw new Error(`hf download ${dl.status}`);
    const buffer = Buffer.from(await dl.arrayBuffer());
    if (buffer.length < 1024) throw new Error('hf: downloaded file is too small');
    await omniSaveAndNotify(buffer, deviceId, jobId, prompt);
    console.log(`🚀 Hugging Face Space (${entry.space}) video ready for ${deviceId}`);
}

// ----------------------------------------------------------------------------
// FREE video from IMAGE and/or AUDIO through Hugging Face Spaces (tried in turn, Gemini Omni last).
//   HF_VIDEO_REF_SPACES = JSON array, same shape as HF_VIDEO_SPACES, but "input" may use
//   "{prompt}", "{image}" and "{audio}" ({image}/{audio} become a Gradio file, or null when not sent), e.g.
//   [{"id":"fasth3","label":"FastH3-Omni","space":"FastVideo/FastH3-Omni","api":"/generate",
//     "input":["{prompt}","{image}","{audio}"]}]
// ----------------------------------------------------------------------------
// Built-in free Spaces (tried in turn). "input" is left out on purpose: the endpoint and its inputs are
// detected automatically from the Space's own /info page. Add or override with HF_VIDEO_REF_SPACES
// (an entry with the same id replaces the built-in one; give "api" and "input" to pin it by hand).
const HF_REF_DEFAULTS = [
    { id: 'fasth3-omni', space: 'FastVideo/FastH3-Omni' },
    { id: 'pika-h3-flex', space: 'Pika-Labs/pika-h3-flex' },
    { id: 'wan777', space: 'kulkas2pintu/wan777' },
    { id: 'wan2-aoti', space: 'aaaa33311/wan2-2-fp8da-aoti-preview-2c-finishing' }
];
const HF_REF_VIDEOS = (() => {
    const byId = new Map();
    const add = (e) => {
        if (!e || typeof e.space !== 'string' || !HF_SPACE_RE.test(e.space)) return;
        const id = String(e.id || e.space).slice(0, 40);
        byId.set(id, {
            id, space: e.space,
            api: e.api ? String(e.api).trim().replace(/^\/+/, '') : '',
            input: Array.isArray(e.input) ? e.input : null     // null = detect automatically
        });
    };
    HF_REF_DEFAULTS.forEach(add);
    try {
        const arr = JSON.parse(process.env.HF_VIDEO_REF_SPACES || '[]');
        if (Array.isArray(arr)) arr.forEach(add);
    } catch (err) { console.warn('⚠️ HF_VIDEO_REF_SPACES is not valid JSON:', err.message); }
    return [...byId.values()];
})();
let hfRefStart = 0;   // round-robin: each request starts with the next Space

// Uploads one file to the Space (Gradio /upload) and returns the FileData object the API expects.
async function hfUploadFile(host, file, headers) {
    let lastErr = null;
    for (const prefix of ['/gradio_api', '']) {
        try {
            const form = new FormData();
            form.append('files', new Blob([file.buffer], { type: file.mimetype }), file.originalname || 'input');
            const r = await fetchWithTimeout(`${host}${prefix}/upload`, { method: 'POST', headers, body: form }, 120_000);
            if (r.status === 404) { lastErr = new Error('hf upload 404'); continue; }
            if (!r.ok) throw new Error(`hf upload HTTP ${r.status}`);
            const paths = await r.json();
            if (!Array.isArray(paths) || !paths[0]) throw new Error('hf upload: no path');
            return { path: paths[0], orig_name: file.originalname || 'input', meta: { _type: 'gradio.FileData' } };
        } catch (e) { lastErr = e; if (e.message !== 'hf upload 404') throw e; }
    }
    throw lastErr || new Error('hf upload failed');
}

// Reads the Space's Gradio /info page and builds the input list by itself:
// image/audio components get the uploaded files, the prompt box gets the prompt, everything else its default value.
async function hfAutoCall(host, headers, imageData, audioData, prompt, pinnedApi) {
    let info = null;
    for (const prefix of ['/gradio_api', '']) {
        try {
            const r = await fetchWithTimeout(`${host}${prefix}/info`, { headers }, 30_000);
            if (r.ok) { info = await r.json(); break; }
        } catch (_) {}
    }
    const eps = info && info.named_endpoints;
    if (!eps || !Object.keys(eps).length) throw new Error('hf: no named API endpoints (custom UI?)');
    const kind = (p) => {
        const c = String(p.component || '').toLowerCase(), n = `${p.parameter_name || ''} ${p.label || ''}`.toLowerCase();
        if (c === 'image' || (c === 'file' && /image/.test(n))) return 'image';
        if (c === 'audio' || (c === 'file' && /audio/.test(n))) return 'audio';
        if (c === 'video') return 'video';
        if (c === 'textbox' || c === 'textarea') return /negative/.test(n) ? 'negative' : (/prompt|text|describe/.test(n) ? 'prompt' : 'text');
        return 'other';
    };
    // Endpoint: the pinned one, else the first that takes a file we have (best name match first).
    let names = Object.keys(eps);
    if (pinnedApi) names = names.filter(x => x.replace(/^\/+/, '') === pinnedApi);
    names.sort((a, b) => (/gen|video/i.test(b) ? 1 : 0) - (/gen|video/i.test(a) ? 1 : 0));
    let lastErr = new Error('hf: no suitable endpoint');
    for (const name of names) {
        const params = (eps[name].parameters || []);
        const kinds = params.map(kind);
        if (!kinds.includes('prompt') && !kinds.includes('text')) continue;
        if (imageData && !kinds.includes('image') && !(audioData && kinds.includes('audio'))) continue;
        if (!imageData && audioData && !kinds.includes('audio')) continue;
        let firstText = kinds.indexOf('prompt'); if (firstText < 0) firstText = kinds.indexOf('text');
        let ok = true;
        const data = params.map((p, i) => {
            const k = kinds[i];
            if (k === 'image') { if (imageData) return imageData; ok = ok && p.parameter_has_default; return p.parameter_default ?? null; }
            if (k === 'audio') { if (audioData) return audioData; return p.parameter_has_default ? p.parameter_default : null; }
            if (i === firstText) return prompt;
            return p.parameter_has_default ? p.parameter_default : (k === 'negative' || k === 'text' ? '' : null);
        });
        if (!ok) continue;
        try { return await hfCallSpace(host, name.replace(/^\/+/, ''), data, headers); }
        catch (e) { lastErr = e; }
    }
    throw lastErr;
}

async function generateVideoFromRefsWithHf(entry, image, audio, prompt, deviceId, jobId) {
    const host = hfSpaceHost(entry.space);
    const headers = HF_TOKEN ? { 'Authorization': `Bearer ${HF_TOKEN}` } : {};
    const imageData = image ? await hfUploadFile(host, image, headers) : null;
    const audioData = audio ? await hfUploadFile(host, audio, headers) : null;
    let out;
    if (entry.input) {
        const data = entry.input.map(v => {
            if (v === '{image}') return imageData;
            if (v === '{audio}') return audioData;
            return typeof v === 'string' ? v.split('{prompt}').join(prompt) : v;
        });
        out = await hfCallSpace(host, entry.api || 'predict', data, headers);
    } else {
        out = await hfAutoCall(host, headers, imageData, audioData, prompt, entry.api);
    }
    const url = hfFindVideoUrl(host, out);
    if (!url) throw new Error('hf: no video in result');
    const u = new URL(url);
    if (!u.hostname.endsWith('.hf.space') && !u.hostname.endsWith('.huggingface.co') && !u.hostname.endsWith('.hf.co')) {
        const safe = await isSafeRemoteUrl(url);
        if (!safe.ok) throw new Error(`hf unsafe url: ${safe.reason}`);
    }
    const dl = await fetchWithTimeout(url, { headers: u.hostname === new URL(host).hostname ? headers : {} }, 180_000);
    if (!dl.ok) throw new Error(`hf download ${dl.status}`);
    const buffer = Buffer.from(await dl.arrayBuffer());
    if (buffer.length < 1024) throw new Error('hf: downloaded file is too small');
    await omniSaveAndNotify(buffer, deviceId, jobId, prompt);
    console.log(`🚀 Hugging Face Space (${entry.space}) image/audio video ready for ${deviceId}`);
}

// Free Spaces first (rotating), then Gemini Omni. Credits are charged only when the free ones all fail.
async function runRefsFreeThenGemini({ image, audio, prompt, deviceId, licenseKey, cost }) {
    const n = HF_REF_VIDEOS.length;
    const first = hfRefStart++ % Math.max(n, 1);
    for (let i = 0; i < n; i++) {
        const entry = HF_REF_VIDEOS[(first + i) % n];
        // Skip a Space that needs a file the user did not send (e.g. an image-only Wan Space when only audio was sent).
        const inp = entry.input || [];
        if ((inp.includes('{image}') && !image && !inp.includes('{audio}')) ||
            (inp.includes('{image}') && !image && !audio) ||
            (inp.includes('{audio}') && !audio && !inp.includes('{image}'))) continue;
        try {
            await generateVideoFromRefsWithHf(entry, image, audio, prompt, deviceId, '');
            return;
        } catch (e) {
            console.error(`HF refs ${entry.id} failed, trying next:`, String(e.message || '').slice(0, 200));
        }
    }
    if (GEMINI_API_KEYS.length === 0) {
        return handleFailure('', deviceId, 'video', 'All free providers failed and Gemini is not configured', 'Generation failed');
    }
    let jobId = '';
    try {
        ({ jobId } = await deductCredits(licenseKey, deviceId, cost, 'video', prompt));
    } catch (e) {
        const msg = e.message === 'INSUFFICIENT_CREDITS' ? 'Insufficient credits' : 'Generation failed to start';
        return handleFailure('', deviceId, 'video', `Free providers failed; paid fallback not possible: ${e.message}`, msg);
    }
    try {
        await generateVideoFromRefsWithOmni(image, audio, prompt, deviceId, jobId);
    } catch (err) {
        console.error('Video-from-refs Error:', err.message);
        handleFailure(jobId, deviceId, 'video', `Image/audio video failed: ${err.message}`, 'Generation failed');
    }
}

console.log(`🎞️ Free image/audio video Spaces: [${HF_REF_VIDEOS.map(x => x.id).join(', ')}] then Gemini Omni${HF_TOKEN ? ' (HF token ✓)' : ' (HF token ✗)'}`);

// Startup summary (shows in the Render logs which free video providers are active; never prints secrets).
console.log(`🎬 Free video: Agnes=${AGNES_API_KEYS.length ? '✓ (' + AGNES_API_KEYS.length + ')' : '✗'} ` +
    `HuggingFace=${HF_SPACE_OK ? '✓ [' + HF_VIDEOS.map(x => x.id).join(', ') + ']' + (HF_TOKEN ? ' (token ✓)' : ' (token ✗)') : '✗'} ` +
    `daily-limit=${AGNES_DAILY_LIMIT || 'unlimited'}`);

// ----------------------------------------------------------------------------
// FREE IMAGE generation (same idea as the free video path): Agnes first, then a Hugging Face Space.
// Credits are charged only if every free provider fails and the Gemini/Imagen chain has to run.
//   AGNES_API_KEY (shared with video)  AGNES_IMAGE_MODEL  default agnes-image-2.1-flash
//   AGNES_IMAGE_EXTRA     JSON merged into the request body, e.g. {"size":"1024x1024"}
//   AGNES_IMAGE_DAILY_LIMIT   free images per device per day (default 20, 0 = unlimited)
//   HF_IMAGE_SPACE        "owner/space-name" of a public Gradio text-to-image Space (enables this provider)
//   HF_IMAGE_API_NAME     default /predict      HF_IMAGE_INPUT  JSON inputs, "{prompt}" is replaced, default ["{prompt}"]
//   (HF_TOKEN is shared with video.)  To turn the free image path off: remove AGNES_API_KEY and HF_IMAGE_SPACE.
// ----------------------------------------------------------------------------
const AGNES_IMAGE_MODEL = (process.env.AGNES_IMAGE_MODEL || 'agnes-image-2.1-flash').trim();
const AGNES_IMAGE_DAILY_LIMIT = process.env.AGNES_IMAGE_DAILY_LIMIT === undefined ? 20 : (parseInt(process.env.AGNES_IMAGE_DAILY_LIMIT) || 0);
const HF_IMAGE_SPACE = (process.env.HF_IMAGE_SPACE || '').trim();
const HF_IMAGE_API = (process.env.HF_IMAGE_API_NAME || '/predict').trim().replace(/^\/+/, '');
const HF_IMAGE_SPACE_OK = /^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(HF_IMAGE_SPACE);
const freeImageUsage = new Map(); // deviceId -> { day, count }
const FREE_IMAGE_MAX_BYTES = 12 * 1024 * 1024;

function freeImageAvailable() { return AGNES_API_KEYS.length > 0 || HF_IMAGE_SPACE_OK; }

function freeImageQuotaTake(deviceId) {
    if (!AGNES_IMAGE_DAILY_LIMIT) return true;
    const day = new Date().toISOString().slice(0, 10);
    const u = freeImageUsage.get(deviceId);
    if (!u || u.day !== day) { freeImageUsage.set(deviceId, { day, count: 1 }); return true; }
    if (u.count >= AGNES_IMAGE_DAILY_LIMIT) return false;
    u.count++;
    return true;
}
function freeImageQuotaGiveBack(deviceId) {
    const u = freeImageUsage.get(deviceId);
    if (u && u.count > 0) u.count--;
}

// Turns a remote image URL or a data: URL into { image: base64, mime }.
async function freeImageFromUrl(url, headers) {
    if (/^data:image\//i.test(url)) {
        const m = url.match(/^data:(image\/[A-Za-z0-9.+-]+);base64,(.+)$/i);
        if (!m) throw new Error('free image: bad data url');
        return { image: m[2], mime: m[1].toLowerCase() };
    }
    const u = new URL(url);
    const hfHost = u.hostname.endsWith('.hf.space') || u.hostname.endsWith('.huggingface.co') || u.hostname.endsWith('.hf.co');
    if (!hfHost) {
        const safe = await isSafeRemoteUrl(url);
        if (!safe.ok) throw new Error(`free image unsafe url: ${safe.reason}`);
    }
    const dl = await fetchWithTimeout(url, { headers: headers || {} }, 120_000);
    if (!dl.ok) throw new Error(`free image download ${dl.status}`);
    const buf = Buffer.from(await dl.arrayBuffer());
    if (buf.length < 512) throw new Error('free image: downloaded file is too small');
    if (buf.length > FREE_IMAGE_MAX_BYTES) throw new Error('free image: file too large');
    let mime = String(dl.headers.get('content-type') || '').split(';')[0].trim().toLowerCase();
    if (!/^image\//.test(mime)) mime = 'image/png';
    return { image: buf.toString('base64'), mime };
}

async function generateImageWithAgnes(prompt) {
    const key = agnesNextKey();
    let extra = {};
    try { extra = JSON.parse(process.env.AGNES_IMAGE_EXTRA || '{}'); } catch (_) {}
    const res = await fetchWithTimeout(`${AGNES_ROOT}/v1/images/generations`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ model: AGNES_IMAGE_MODEL, prompt, n: 1, ...extra })
    }, 120_000);
    const json = await agnesJson(res, 'image');
    const item = Array.isArray(json && json.data) ? json.data[0] : null;
    if (item && typeof item.b64_json === 'string' && item.b64_json.length > 100) {
        return { image: item.b64_json, mime: 'image/png' };
    }
    const url = (item && agnesIsHttp(item.url) && item.url) || agnesDeepFind(json, ['url', 'image_url'], agnesIsHttp);
    if (!url) throw new Error('agnes image: no image in response');
    return await freeImageFromUrl(url, {});
}

async function generateImageWithHf(prompt) {
    const host = hfSpaceHost(HF_IMAGE_SPACE);
    const headers = HF_TOKEN ? { 'Authorization': `Bearer ${HF_TOKEN}` } : {};
    let tpl;
    try { tpl = JSON.parse(process.env.HF_IMAGE_INPUT || '["{prompt}"]'); } catch (_) { tpl = ['{prompt}']; }
    if (!Array.isArray(tpl)) tpl = ['{prompt}'];
    const input = tpl.map(v => typeof v === 'string' ? v.split('{prompt}').join(prompt) : v);
    const data = await hfCallSpace(host, HF_IMAGE_API, input, headers);
    let url = null;
    if (Array.isArray(data)) for (const d of data) if (typeof d === 'string' && /^data:image\//i.test(d)) { url = d; break; }
    if (!url) url = hfFindVideoUrl(host, data);   // generic: finds a url / file path in the Gradio result
    if (!url) throw new Error('hf image: no image in result');
    const sameHost = !/^data:/i.test(url) && new URL(url).hostname === new URL(host).hostname;
    return await freeImageFromUrl(url, sameHost ? headers : {});
}

// Tries the free providers in order. Returns { image, mime } or null when all of them fail.
async function generateImageFree(prompt) {
    const chain = [];
    if (AGNES_API_KEYS.length > 0) chain.push(['Agnes', generateImageWithAgnes]);
    if (HF_IMAGE_SPACE_OK) chain.push(['HuggingFace', generateImageWithHf]);
    for (const [name, fn] of chain) {
        try {
            const out = await fn(prompt);
            console.log(`🖼️ Free image ready (${name})`);
            return out;
        } catch (e) {
            console.warn(`[image] ${name} failed, trying next:`, String(e.message || '').slice(0, 200));
        }
    }
    return null;
}

console.log(`🖌️ Image edit chain: ${GEMINI_API_KEYS.length ? '✓' : '✗'} ${GEMINI_EDIT_MODELS.join(' -> ')} -> ${AGNES_API_KEYS.length ? '✓' : '✗'} ${AGNES_EDIT_MODELS.join(' -> ')}`);
console.log(`🖼️ Free image: Agnes=${AGNES_API_KEYS.length ? '✓ ' + AGNES_IMAGE_MODEL : '✗'} ` +
    `HuggingFace=${HF_IMAGE_SPACE_OK ? '✓ ' + HF_IMAGE_SPACE : (HF_IMAGE_SPACE ? '✗ invalid HF_IMAGE_SPACE' : '✗')} ` +
    `daily-limit=${AGNES_IMAGE_DAILY_LIMIT || 'unlimited'}`);

// Free providers first (Agnes, then a Hugging Face Space); if all fail, the paid chain runs
// and credits are deducted only then.
async function runAgnesThenPaid({ prompt, deviceId, licenseKey, cost, model }) {
    const free = [];
    if (useAgnes(model)) free.push(['Agnes', generateVideoWithAgnes]);
    for (const entry of hfSelect(model)) free.push([`HF:${entry.id}`, (p, d, j) => generateVideoWithHf(p, d, j, entry)]);
    for (const [name, fn] of free) {
        try {
            await fn(prompt, deviceId, '');
            return;
        } catch (e) {
            console.error(`${name} failed, trying next:`, e.message);
        }
    }
    agnesQuotaGiveBack(deviceId);
    let jobId = '';
    try {
        ({ jobId } = await deductCredits(licenseKey, deviceId, cost, 'video', prompt));
    } catch (e) {
        const msg = e.message === 'INSUFFICIENT_CREDITS' ? 'Insufficient credits' : 'Generation failed to start';
        return handleFailure('', deviceId, 'video', `Free provider failed; paid fallback not possible: ${e.message}`, msg);
    }
    try {
        await generateVideoPaidChain(prompt, deviceId, jobId, model);
    } catch (err) {
        console.error('Background error (video fallback):', err.message);
        handleFailure(jobId, deviceId, 'video', `Start failed: ${err.message}`, 'Generation failed to start');
    }
}

// Lists the free video models the app can offer in its picker (value = `model` for /api/generate-video).
app.get('/api/video-models', (req, res) => {
    res.json({ models: HF_VIDEOS.map(x => ({ id: x.id, label: x.label })) });
});

app.post('/webhook/replicate', async (req, res) => {
    const { deviceId, type, prompt, token } = req.query;
    const jobId = typeof req.query.jobId === 'string' ? req.query.jobId : '';
    if (!isValidDeviceId(deviceId) || !['video', 'music'].includes(type)) return res.status(401).send('Unauthorized');
    if (jobId && !isValidJobId(jobId)) return res.status(401).send('Unauthorized');
    if (!safeEqual(token, webhookToken(deviceId, type, jobId))) return res.status(401).send('Unauthorized');

    const { output, status, error } = req.body || {};
    res.status(200).send('OK');
    if (status !== 'succeeded' || !output) {
        return handleFailure(jobId, deviceId, type, `Replicate status=${status}: ${error || 'no output'}`, 'Generation failed');
    }
    const remoteUrl = Array.isArray(output) ? output[0] : output;
    if (typeof remoteUrl !== 'string') {
        return handleFailure(jobId, deviceId, type, 'Invalid output type', 'Invalid output');
    }

    const safeCheck = await isSafeRemoteUrl(remoteUrl);
    if (!safeCheck.ok) {
        console.warn(`❌ SSRF blocked: ${remoteUrl} (${safeCheck.reason})`);
        return handleFailure(jobId, deviceId, type, `Unsafe URL: ${safeCheck.reason}`, 'Invalid output URL');
    }

    if (!firebaseReady || !bucket) return;
    const ext = type === 'video' ? 'mp4' : 'mp3';
    const fileName = `${type}s/${deviceId}/${Date.now()}.${ext}`;
    try {
        const download = await fetch(remoteUrl);
        if (!download.ok) throw new Error(`Download failed: HTTP ${download.status}`);
        const buffer = Buffer.from(await download.arrayBuffer());
        const bucketFile = bucket.file(fileName);
        await bucketFile.save(buffer, { contentType: type === 'video' ? 'video/mp4' : 'audio/mpeg' });
        const [signedUrl] = await bucketFile.getSignedUrl({
            version: 'v4', action: 'read', expires: Date.now() + 7 * 24 * 3_600_000 - 5 * 60_000
        });
        await db.collection(`${type}s`).doc(deviceId).collection('items').add({
            url: signedUrl, prompt: prompt || '', createdAt: admin.firestore.FieldValue.serverTimestamp()
        });
        if (jobId) await db.collection('jobs').doc(jobId).update({
            status: 'completed', completedAt: admin.firestore.FieldValue.serverTimestamp()
        }).catch(() => {});
        await sendNotification(deviceId, `${type}_ready`, { url: signedUrl, prompt: String(prompt || '') });
    } catch (err) {
        console.error(`❌ Upload failed for ${deviceId}:`, err.message);
        await handleFailure(jobId, deviceId, type, `Save failed: ${err.message}`, 'Failed to save file');
    }
});

// ============================================================================
// 15. FCM
// ============================================================================
async function sendNotification(deviceId, type, data) {
    if (!firebaseReady) return;
    try {
        await admin.messaging().send({
            data: { type, ...data },
            topic: `device_${deviceId}`,
            android: { priority: 'high', ttl: 24 * 60 * 60 * 1000 }
        });
        console.log(`📱 FCM (${type}) → device_${deviceId}`);
    } catch (e) { console.error('FCM error:', e.message); }
}

async function handleFailure(jobId, deviceId, type, reason, publicMessage) {
    let refunded = false;
    try { refunded = (await failJob(jobId, reason)).refunded; }
    catch (e) { console.error(`failJob (${jobId}):`, e.message); }
    await sendNotification(deviceId, `${type}_error`, { error: publicMessage, refunded: String(refunded) });
}

// ============================================================================
// 16. Google Play Billing (consumable credit packs) + AI content reports
// ============================================================================
let CREDITS_PRODUCTS = {
    'credits_100': 100,
    'credits_350': 350,
    'credits_800': 800,
    'credits_1800': 1800
};
// Optional override: PLAY_CREDITS_PRODUCTS='{"credits_100":100,"credits_500":500}'
try {
    const o = JSON.parse(process.env.PLAY_CREDITS_PRODUCTS || 'null');
    if (o && typeof o === 'object' && Object.values(o).every(n => Number.isInteger(n) && n > 0)) CREDITS_PRODUCTS = o;
} catch (_) {}
// Must equal the applicationId of the APK/AAB published on Google Play (Play rejects "com.example.*").
// Set PLAY_PACKAGE_NAME on the server when you change the applicationId.
const PACKAGE_NAME = (process.env.PLAY_PACKAGE_NAME || 'com.zevorix.assistant').trim();
// Apps that pay through Google Play (comma separated). Default: just PLAY_PACKAGE_NAME.
const PLAY_PACKAGES = (process.env.PLAY_PACKAGE_NAMES || PACKAGE_NAME).split(',').map(x => x.trim()).filter(Boolean);

// Non-fatal: the app also consumes the purchase, and an already-consumed item is fine.
async function consumePlayPurchase(productId, purchaseToken, pkg = PACKAGE_NAME) {
    try {
        await androidPublisher.purchases.products.consume({
            packageName: pkg, productId, token: purchaseToken
        });
        return true;
    } catch (e) {
        console.warn('[play] consume skipped:', e.message);
        return false;
    }
}

app.post('/api/play/credits', async (req, res) => {
    if (!firebaseReady) return res.status(503).json({ error: 'DB not ready' });
    if (!androidPublisher) return res.status(503).json({ error: 'Play API not configured' });

    const { purchaseToken, productId, deviceId, licenseKey } = req.body || {};
    // Which app is paying? Older app builds send no packageName -> the default package.
    const rawPkg = (req.body || {}).packageName;
    const pkg = (typeof rawPkg === 'string' && rawPkg.trim()) ? rawPkg.trim() : PACKAGE_NAME;
    if (!PLAY_PACKAGES.includes(pkg)) return res.status(400).json({ error: 'App does not use Google Play billing' });
    if (typeof purchaseToken !== 'string' || purchaseToken.length < 10 || purchaseToken.length > 4096 ||
        typeof productId !== 'string' || !isValidDeviceId(deviceId)) {
        return res.status(400).json({ error: 'Invalid request' });
    }
    if (!Object.prototype.hasOwnProperty.call(CREDITS_PRODUCTS, productId)) {
        return res.status(400).json({ error: 'Unknown product' });
    }
    const credits = CREDITS_PRODUCTS[productId];
    if (!playLimiter.check(deviceId).allowed) return res.status(429).json({ error: 'Too many requests' });

    const tokenRef = db.collection('play_tokens').doc(
        crypto.createHash('sha256').update(purchaseToken).digest('hex')
    );

    try {
        // Idempotent retry: credits were already granted for this token (e.g. the response was lost).
        const existing = await tokenRef.get();
        if (existing.exists) {
            const t = existing.data();
            if (t.deviceId !== deviceId) return res.status(409).json({ error: 'Already processed' });
            await consumePlayPurchase(t.productId, purchaseToken, t.packageName || pkg);
            return res.json({ status: 'ok', duplicate: true, licenseKey: t.licenseKey, credits: 0 });
        }

        // Verify the purchase with Google
        const purchase = await androidPublisher.purchases.products.get({
            packageName: pkg, productId, token: purchaseToken
        });
        const pd = purchase.data;
        if (pd.purchaseState !== 0) return res.status(400).json({ error: 'Purchase not completed' });
        if (pd.consumptionState === 1) return res.status(409).json({ error: 'Already consumed' });

        let grantedKey = null;
        let remaining = 0;

        await db.runTransaction(async (tx) => {
            grantedKey = null; remaining = 0;   // the transaction function may be retried
            const tokDoc = await tx.get(tokenRef);
            if (tokDoc.exists) throw new Error('ALREADY_PROCESSED');

            // 1) the license the app already uses (if it is valid and not bound to another device)
            let licRef = null, cur = 0;
            if (typeof licenseKey === 'string' && isValidLicenseKey(licenseKey)) {
                const ref = db.collection('licenses').doc(licenseKey);
                const snap = await tx.get(ref);
                if (snap.exists) {
                    const d = snap.data();
                    if (!d.deviceId || d.deviceId === deviceId) { licRef = ref; cur = d.credits || 0; }
                }
            }
            // 2) otherwise any license already bound to this device
            if (!licRef) {
                const snap = await tx.get(db.collection('licenses').where('deviceId', '==', deviceId).limit(1));
                if (!snap.empty) { licRef = snap.docs[0].ref; cur = snap.docs[0].data().credits || 0; }
            }

            if (licRef) {
                tx.update(licRef, {
                    deviceId,
                    credits: admin.firestore.FieldValue.increment(credits),
                    lastPurchaseAt: admin.firestore.FieldValue.serverTimestamp()
                });
                grantedKey = licRef.id;
                remaining = cur + credits;
            } else {
                // 3) new signed license (retry on the unlikely key collision)
                let candidate = null;
                for (let i = 0; i < 5; i++) {
                    const key = generateLicenseKey();
                    const check = await tx.get(db.collection('licenses').doc(key));
                    if (!check.exists) { candidate = key; break; }
                }
                if (!candidate) throw new Error('LICENSE_GEN_COLLISION');
                tx.create(db.collection('licenses').doc(candidate), {
                    deviceId,
                    credits,
                    createdAt: admin.firestore.FieldValue.serverTimestamp(),
                    lastPurchaseAt: admin.firestore.FieldValue.serverTimestamp()
                });
                grantedKey = candidate;
                remaining = credits;
            }

            tx.create(tokenRef, {
                deviceId, productId, credits, licenseKey: grantedKey, packageName: pkg,
                createdAt: admin.firestore.FieldValue.serverTimestamp()
            });
        });

        await consumePlayPurchase(productId, purchaseToken, pkg);
        console.log(`💳 Play credits +${credits} (${productId}) device=${deviceId}`);
        return res.json({ status: 'ok', licenseKey: grantedKey, credits, remaining });
    } catch (e) {
        if (e.message === 'ALREADY_PROCESSED') return res.status(409).json({ error: 'Already processed' });
        const code = Number(e.code || (e.response && e.response.status));
        if ([400, 404, 410].includes(code)) return res.status(400).json({ error: 'Invalid purchase' });
        console.error('Play credits error:', e.message);
        return res.status(502).json({ error: 'Verification failed' });
    }
});

// ============================================================================
// 16c. NOWPayments (crypto) — ONLY for the apps listed in NOWPAYMENTS_PACKAGE_NAMES
//   NOWPAYMENTS_API_KEY        your NOWPayments API key
//   NOWPAYMENTS_IPN_SECRET     IPN secret (several accounts: separate with commas)
//   NOWPAYMENTS_PACKAGE_NAMES  apps that pay by crypto, e.g. "com.zevorix.assistant,com.zevorix.two"
//   NOWPAYMENTS_PACKS          server-side price list (the app never sends the price).
//                              Optional "packages" limits a pack to specific apps (recommended with several apps):
//                              {"pack_10":{"usd":10,"credits":100,"packages":["com.example.voiceassistant"]},
//                               "unlock_10":{"usd":10,"credits":1,"packages":["com.example.gradiometer"]}}
//   BASE_URL                   public URL of this server (for the IPN callback)
// ============================================================================
const NOWPAYMENTS_API_KEY = (process.env.NOWPAYMENTS_API_KEY || '').trim();
const NOWPAYMENTS_IPN_SECRETS = (process.env.NOWPAYMENTS_IPN_SECRET || '').split(',').map(x => x.trim()).filter(Boolean);
const NOWPAYMENTS_PACKAGES = (process.env.NOWPAYMENTS_PACKAGE_NAMES || '').split(',').map(x => x.trim()).filter(Boolean);
let NOWPAYMENTS_PACKS = {};
try {
    const o = JSON.parse(process.env.NOWPAYMENTS_PACKS || '{}');
    for (const [id, v] of Object.entries(o || {})) {
        if (/^[A-Za-z0-9_-]{1,40}$/.test(id) && v && Number(v.usd) > 0 && Number.isInteger(v.credits) && v.credits > 0) {
            const only = Array.isArray(v.packages) ? v.packages.map(x => String(x).trim()).filter(Boolean) : null;
            NOWPAYMENTS_PACKS[id] = { usd: Number(v.usd), credits: v.credits, packages: only && only.length ? only : null };
        }
    }
} catch (_) {}
const nowLimiter = new RateLimiter(10, 60_000, 'nowpayments');

console.log(`💳 Payments: Play=[${PLAY_PACKAGES.join(', ')}] ${androidPublisher ? '✓' : '✗'} | NOWPayments=[${NOWPAYMENTS_PACKAGES.join(', ') || 'none'}] ` +
    `key=${NOWPAYMENTS_API_KEY ? '✓' : '✗'} ipn=${NOWPAYMENTS_IPN_SECRETS.length} packs=${Object.keys(NOWPAYMENTS_PACKS).length}`);
NOWPAYMENTS_PACKAGES.filter(x => PLAY_PACKAGES.includes(x)).forEach(x =>
    console.warn(`⚠️ ${x} is listed under BOTH Play and NOWPayments — each app should use only one.`));

app.post('/api/nowpayments/create-invoice', async (req, res) => {
    if (!firebaseReady) return res.status(503).json({ error: 'DB not ready' });
    if (!NOWPAYMENTS_API_KEY || !BASE_URL || Object.keys(NOWPAYMENTS_PACKS).length === 0) {
        return res.status(503).json({ error: 'NOWPayments not configured' });
    }
    const { deviceId, licenseKey, packageName, packId } = req.body || {};
    if (!isValidDeviceId(deviceId) || typeof packageName !== 'string' || typeof packId !== 'string') {
        return res.status(400).json({ error: 'Invalid request' });
    }
    if (!NOWPAYMENTS_PACKAGES.includes(packageName.trim())) return res.status(400).json({ error: 'App does not use crypto payments' });
    const pack = Object.prototype.hasOwnProperty.call(NOWPAYMENTS_PACKS, packId) ? NOWPAYMENTS_PACKS[packId] : null;
    if (!pack) return res.status(400).json({ error: 'Unknown pack' });
    // A pack with a "packages" list can only be bought from those apps (pack_* for one app, unlock_* for another).
    if (pack.packages && !pack.packages.includes(packageName.trim())) {
        console.warn(`[nowpayments] pack ${packId} is not allowed for package "${packageName.trim().slice(0, 80)}" (allowed: ${pack.packages.join(', ')})`);
        return res.status(400).json({ error: `Pack not available for this app (${packageName.trim().slice(0, 60)})` });
    }
    if (licenseKey && !isValidLicenseKey(licenseKey)) return res.status(400).json({ error: 'Invalid license' });
    if (!nowLimiter.check(deviceId).allowed) return res.status(429).json({ error: 'Too many requests' });

    try {
        const orderId = crypto.randomBytes(12).toString('hex');
        await db.collection('nowpayments_orders').doc(orderId).set({
            deviceId, packageName: packageName.trim(), packId, usd: pack.usd, credits: pack.credits,
            licenseKey: licenseKey || null, status: 'created',
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });
        const r = await fetchWithTimeout('https://api.nowpayments.io/v1/invoice', {
            method: 'POST',
            headers: { 'x-api-key': NOWPAYMENTS_API_KEY, 'Content-Type': 'application/json' },
            body: JSON.stringify({
                price_amount: pack.usd, price_currency: 'usd',
                order_id: orderId, order_description: `${pack.credits} credits`,
                ipn_callback_url: `${BASE_URL}/nowpayments/ipn`
            })
        }, 30_000);
        const data = await r.json().catch(() => ({}));
        if (!r.ok || !data.invoice_url) {
            console.warn('[nowpayments] invoice failed', r.status, JSON.stringify(data).slice(0, 200));
            return res.status(502).json({ error: 'Invoice failed' });
        }
        return res.json({ invoice_url: data.invoice_url, orderId, credits: pack.credits });
    } catch (e) {
        console.error('[nowpayments] create-invoice:', e.message);
        return res.status(500).json({ error: 'Failed' });
    }
});

// Instant Payment Notification: verifies the HMAC-SHA512 signature, then grants credits once per order.
app.post('/nowpayments/ipn', async (req, res) => {
    try {
        if (NOWPAYMENTS_IPN_SECRETS.length === 0 || !firebaseReady) return res.status(503).send('Not configured');
        const received = String(req.headers['x-nowpayments-sig'] || '');
        const sorted = JSON.stringify(deepSort(req.body || {}));
        const okSig = NOWPAYMENTS_IPN_SECRETS.some(sec =>
            safeEqual(received, crypto.createHmac('sha512', sec).update(sorted).digest('hex')));
        if (!okSig) return res.status(401).send('Invalid signature');

        const { payment_status, order_id, price_amount, price_currency, payment_id } = req.body || {};
        if (payment_status !== 'finished') return res.status(200).send('Not final yet');
        if (typeof order_id !== 'string' || !/^[a-f0-9]{24}$/.test(order_id)) return res.status(200).send('Ignored');

        const orderRef = db.collection('nowpayments_orders').doc(order_id);
        let result = null;
        await db.runTransaction(async (tx) => {
            result = null;
            const od = await tx.get(orderRef);
            if (!od.exists) return;
            const o = od.data();
            if (o.status === 'paid') return;                         // already credited
            if (String(price_currency || '').toLowerCase() !== 'usd' || !(Number(price_amount) + 1e-9 >= o.usd)) {
                tx.update(orderRef, { status: 'mismatch', paymentId: String(payment_id || '') });
                return;
            }
            // reads first
            let licRef = null, cur = 0;
            if (o.licenseKey && isValidLicenseKey(o.licenseKey)) {
                const ref = db.collection('licenses').doc(o.licenseKey);
                const snap = await tx.get(ref);
                if (snap.exists) {
                    const d = snap.data();
                    if (!d.deviceId || d.deviceId === o.deviceId) { licRef = ref; cur = d.credits || 0; }
                }
            }
            if (!licRef) {
                const snap = await tx.get(db.collection('licenses').where('deviceId', '==', o.deviceId).limit(1));
                if (!snap.empty) { licRef = snap.docs[0].ref; cur = snap.docs[0].data().credits || 0; }
            }
            let newKey = null;
            if (!licRef) {
                for (let i = 0; i < 5; i++) {
                    const key = generateLicenseKey();
                    const chk = await tx.get(db.collection('licenses').doc(key));
                    if (!chk.exists) { newKey = key; break; }
                }
                if (!newKey) throw new Error('LICENSE_GEN_COLLISION');
            }
            // writes
            let grantedKey, remaining;
            if (licRef) {
                tx.update(licRef, {
                    deviceId: o.deviceId,
                    credits: admin.firestore.FieldValue.increment(o.credits),
                    lastPurchaseAt: admin.firestore.FieldValue.serverTimestamp()
                });
                grantedKey = licRef.id; remaining = cur + o.credits;
            } else {
                tx.create(db.collection('licenses').doc(newKey), {
                    deviceId: o.deviceId, credits: o.credits,
                    createdAt: admin.firestore.FieldValue.serverTimestamp(),
                    lastPurchaseAt: admin.firestore.FieldValue.serverTimestamp()
                });
                grantedKey = newKey; remaining = o.credits;
            }
            tx.update(orderRef, {
                status: 'paid', licenseKey: grantedKey, paymentId: String(payment_id || ''),
                paidAt: admin.firestore.FieldValue.serverTimestamp()
            });
            result = { deviceId: o.deviceId, licenseKey: grantedKey, credits: o.credits, remaining };
        });
        if (result) {
            console.log(`💳 NOWPayments +${result.credits} device=${result.deviceId}`);
            sendNotification(result.deviceId, 'payment_done', {
                orderId: order_id, licenseKey: result.licenseKey, credits: String(result.credits)
            }).catch(() => {});
        }
        return res.status(200).send('OK');
    } catch (e) {
        console.error('[nowpayments] ipn:', e.message);
        return res.status(500).send('Error');
    }
});

// The app polls this after the user returns from the payment page.
app.post('/api/nowpayments/status', async (req, res) => {
    if (!firebaseReady) return res.status(503).json({ error: 'DB not ready' });
    const { deviceId, orderId } = req.body || {};
    if (!isValidDeviceId(deviceId) || typeof orderId !== 'string' || !/^[a-f0-9]{24}$/.test(orderId)) {
        return res.status(400).json({ error: 'Invalid request' });
    }
    if (!nowLimiter.check(deviceId).allowed) return res.status(429).json({ error: 'Too many requests' });
    try {
        const d = await db.collection('nowpayments_orders').doc(orderId).get();
        if (!d.exists || d.data().deviceId !== deviceId) return res.status(404).json({ error: 'Not found' });
        const o = d.data();
        if (o.status === 'paid') return res.json({ status: 'paid', licenseKey: o.licenseKey, credits: o.credits });
        return res.json({ status: o.status });
    } catch (e) { return res.status(500).json({ error: 'Failed' }); }
});

// AI-generated content reports (Google Play "AI-Generated Content" policy)
app.post('/api/report', async (req, res) => {
    try {
        const body = req.body || {};
        const { licenseKey, deviceId, messageId, reason, details } = body;
        if (!isValidLicenseKey(licenseKey) || !isValidDeviceId(deviceId)) {
            return res.status(401).json({ error: 'Invalid request' });
        }
        if (!firebaseReady) return res.status(503).json({ error: 'Service not ready' });
        if (!reportLimiter.check(licenseKey).allowed) return res.status(429).json({ error: 'Too many requests' });
        const reasonStr = String(reason || '').slice(0, 64);
        const detailsStr = String(details || '').slice(0, 2000);
        const messageStr = String(messageId == null ? '' : messageId).slice(0, 64);
        const reportRef = await db.collection('content_reports').add({
            licenseKey, deviceId,
            messageId: messageStr,
            reason: reasonStr,
            details: detailsStr,
            status: 'pending',
            createdAt: admin.firestore.FieldValue.serverTimestamp(),
        });
        console.log(`🚩 Report ${reportRef.id} from ${deviceId} reason=${reasonStr}`);
        return res.json({ status: 'received', reportId: reportRef.id });
    } catch (e) {
        console.error('[report] failed:', e.message);
        return res.status(500).json({ error: 'Report failed' });
    }
});

// ============================================================================
// 16b. Google Play pages & data deletion (privacy policy, deletion URL, API)
// ============================================================================
const APP_NAME = (process.env.APP_NAME || 'Zevorix').trim();
const SUPPORT_EMAIL = (process.env.SUPPORT_EMAIL || '').trim();
const deleteLimiter = new RateLimiter(3, 60_000, 'delete');

function escHtml(t) {
    return String(t).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function legalPage(title, bodyHtml) {
    return '<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">' +
        '<meta name="viewport" content="width=device-width, initial-scale=1">' +
        '<title>' + escHtml(title) + '</title>' +
        '<style>body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;max-width:760px;margin:0 auto;padding:20px;line-height:1.7;color:#1b1b1f}' +
        'h1{font-size:1.6rem}h2{font-size:1.15rem;margin-top:1.6rem}section.en{direction:ltr;text-align:left;border-top:1px solid #ccc;margin-top:2rem;padding-top:1rem}' +
        'code{background:#f0f0f4;padding:2px 5px;border-radius:4px}@media(prefers-color-scheme:dark){body{background:#121214;color:#e6e6ea}code{background:#26262c}}</style>' +
        '</head><body>' + bodyHtml + '</body></html>';
}

function sendLegal(res, html) {
    res.set({
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'public, max-age=3600',
        'X-Content-Type-Options': 'nosniff',
        'Content-Security-Policy': "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'"
    });
    res.send(html);
}

const CONTACT_AR = SUPPORT_EMAIL ? ('للتواصل: <a href="mailto:' + escHtml(SUPPORT_EMAIL) + '">' + escHtml(SUPPORT_EMAIL) + '</a>') : 'للتواصل: عبر صفحة التطبيق في Google Play.';
const CONTACT_EN = SUPPORT_EMAIL ? ('Contact: <a href="mailto:' + escHtml(SUPPORT_EMAIL) + '">' + escHtml(SUPPORT_EMAIL) + '</a>') : 'Contact: via the app listing on Google Play.';

// NOTE: review this text against what the app really does before publishing; adapt it to your legal needs.
app.get('/privacy', (req, res) => {
    const n = escHtml(APP_NAME);
    sendLegal(res, legalPage(n + ' — سياسة الخصوصية / Privacy Policy',
        '<h1>' + n + ' — سياسة الخصوصية</h1>' +
        '<p>آخر تحديث: نوفمبر 2026. ' + CONTACT_AR + '</p>' +
        '<h2>ما الذي نعالجه</h2><ul>' +
        '<li><b>محتوى الطلبات:</b> النصوص والصور والصوت التي ترسلها إلى المساعد تُرسَل إلى خوادمنا ثم إلى مزوّدي الذكاء الاصطناعي (Google Gemini وOpenAI وAnthropic حسب المحرك) لتوليد الرد. لا ترسل معلومات حساسة.</li>' +
        '<li><b>الردود مُنشأة بالذكاء الاصطناعي</b> وقد تحتوي أخطاء. يمكنك الإبلاغ عن أي رد من داخل التطبيق.</li>' +
        '<li><b>المعرّفات:</b> معرّف الجهاز ومفتاح الترخيص ورصيد النقاط لربط مشترياتك بجهازك.</li>' +
        '<li><b>المشتريات:</b> تتم عبر Google Play؛ نحتفظ برمز الشراء ومعرّف المنتج لمنع تكرار منح النقاط ولمكافحة الاحتيال. لا نرى بيانات بطاقتك.</li>' +
        '<li><b>الوسائط المولَّدة:</b> الفيديو والموسيقى والصور التي تطلب توليدها تُحفظ مرتبطة بمعرّف جهازك لتسليمها لك.</li>' +
        '<li><b>الإشعارات:</b> نستخدم Firebase Cloud Messaging لإعلامك باكتمال المهام.</li>' +
        '<li><b>البلاغات والدوائر المحفوظة:</b> البلاغات التي ترسلها، والدوائر التي تحفظها لمشاركتها بكود.</li></ul>' +
        '<h2>الأذونات على الجهاز</h2><p>يطلب التطبيق أذونات (مثل الميكروفون والكاميرا وجهات الاتصال والموقع والإشعارات) عند استخدام الميزة المرتبطة بها فقط، ويعرض إفصاحاً واضحاً قبل الطلب.</p>' +
        '<h2>المشاركة</h2><p>لا نبيع بياناتك ولا نعرض إعلانات. نشارك المحتوى اللازم فقط مع مزوّدي الذكاء الاصطناعي والاستضافة (Firebase/Google Cloud) لتقديم الخدمة.</p>' +
        '<h2>الاحتفاظ والحذف</h2><p>نحتفظ بالبيانات المرتبطة بجهازك حتى تطلب حذفها. لحذفها: <a href="/delete-data">صفحة حذف البيانات</a>. سجلات الشراء المطلوبة لمنع الاحتيال والالتزامات القانونية قد نحتفظ بها.</p>' +
        '<h2>الأطفال</h2><p>التطبيق غير موجّه للأطفال دون 13 عاماً.</p>' +
        '<section class="en" dir="ltr"><h1>' + n + ' — Privacy Policy</h1><p>Last updated: November 2026. ' + CONTACT_EN + '</p>' +
        '<h2>What we process</h2><ul>' +
        '<li><b>Request content:</b> text, images and audio you send to the assistant are sent to our servers and then to AI providers (Google Gemini, OpenAI, Anthropic, depending on the engine) to produce a reply. Do not send sensitive information.</li>' +
        '<li><b>Replies are AI-generated</b> and may contain mistakes. You can report any reply inside the app.</li>' +
        '<li><b>Identifiers:</b> device ID, license key and credit balance, to tie your purchases to your device.</li>' +
        '<li><b>Purchases:</b> handled by Google Play; we keep the purchase token and product ID to prevent duplicate credit grants and fraud. We never see your card details.</li>' +
        '<li><b>Generated media:</b> videos, music and images you request are stored against your device ID so we can deliver them.</li>' +
        '<li><b>Notifications:</b> Firebase Cloud Messaging tells you when jobs finish.</li>' +
        '<li><b>Reports and saved circuits:</b> reports you submit and circuits you save to share by code.</li></ul>' +
        '<h2>Device permissions</h2><p>The app asks for permissions (e.g. microphone, camera, contacts, location, notifications) only when you use the related feature, with a clear on-screen disclosure first.</p>' +
        '<h2>Sharing</h2><p>We do not sell your data and show no ads. We share only what is needed with AI providers and hosting (Firebase/Google Cloud) to run the service.</p>' +
        '<h2>Retention and deletion</h2><p>Data tied to your device is kept until you ask us to delete it: see the <a href="/delete-data">data deletion page</a>. Purchase records needed for fraud prevention and legal duties may be retained.</p>' +
        '<h2>Children</h2><p>The app is not directed to children under 13.</p></section>'));
});

app.get('/delete-data', (req, res) => {
    const n = escHtml(APP_NAME);
    sendLegal(res, legalPage(n + ' — حذف البيانات / Data deletion',
        '<h1>' + n + ' — حذف البيانات</h1>' +
        '<p>يمكنك طلب حذف البيانات المرتبطة بجهازك: الفيديو والموسيقى المولَّدة، وسجل المهام والطلبات، والبلاغات، والدوائر المحفوظة.</p>' +
        '<ol><li>أرسل طلب حذف إلى: ' + (SUPPORT_EMAIL ? '<a href="mailto:' + escHtml(SUPPORT_EMAIL) + '">' + escHtml(SUPPORT_EMAIL) + '</a>' : 'عنوان الدعم في صفحة التطبيق على Google Play') + ' مع <b>مفتاح الترخيص</b> و<b>معرّف الجهاز</b> من إعدادات التطبيق.</li>' +
        '<li>سنحذف البيانات خلال 30 يوماً كحد أقصى.</li></ol>' +
        '<p>حذف الترخيص نفسه يُلغي رصيد النقاط المتبقي ولا يمكن التراجع عنه. سجلات الشراء اللازمة لمنع الاحتيال والالتزامات القانونية قد نحتفظ بها.</p>' +
        '<section class="en" dir="ltr"><h1>' + n + ' — Data deletion</h1>' +
        '<p>You can ask us to delete the data tied to your device: generated videos and music, job and prompt history, reports and saved circuits.</p>' +
        '<ol><li>Send a deletion request to ' + (SUPPORT_EMAIL ? '<a href="mailto:' + escHtml(SUPPORT_EMAIL) + '">' + escHtml(SUPPORT_EMAIL) + '</a>' : 'the support address on the Google Play listing') + ' with your <b>license key</b> and <b>device ID</b> from the app settings.</li>' +
        '<li>We delete the data within 30 days at most.</li></ol>' +
        '<p>Deleting the license itself cancels any remaining credits and cannot be undone. Purchase records needed for fraud prevention and legal duties may be retained.</p></section>'));
});

async function deleteQueryDocs(query) {
    let total = 0;
    for (;;) {
        const snap = await query.limit(400).get();
        if (snap.empty) break;
        const batch = db.batch();
        snap.docs.forEach(d => batch.delete(d.ref));
        await batch.commit();
        total += snap.size;
        if (snap.size < 400) break;
    }
    return total;
}

// Authenticated by licenseKey + deviceId. Deletes content tied to the device.
// The license (and its credits) is deleted only with deleteLicense:true AND confirm:'DELETE_MY_LICENSE'.
app.post('/api/delete-data', async (req, res) => {
    if (!firebaseReady) return res.status(503).json({ error: 'Service not ready' });
    const { licenseKey, deviceId, deleteLicense, confirm } = req.body || {};
    if (!isValidLicenseKey(licenseKey) || !isValidDeviceId(deviceId)) return res.status(400).json({ error: 'Invalid request' });
    if (!deleteLimiter.check(deviceId).allowed) return res.status(429).json({ error: 'Too many requests' });
    try {
        const licRef = db.collection('licenses').doc(licenseKey);
        const lic = await licRef.get();
        if (!lic.exists) return res.status(404).json({ error: 'License not found' });
        const ld = lic.data();
        if (ld.deviceId && ld.deviceId !== deviceId) return res.status(403).json({ error: 'License used on another device' });

        const deleted = {};
        for (const col of ['videos', 'musics']) {
            deleted[col] = await deleteQueryDocs(db.collection(col).doc(deviceId).collection('items'));
        }
        deleted.jobs = await deleteQueryDocs(db.collection('jobs').where('deviceId', '==', deviceId));
        deleted.failures = await deleteQueryDocs(db.collection('failures').where('deviceId', '==', deviceId));
        deleted.reports = await deleteQueryDocs(db.collection('content_reports').where('deviceId', '==', deviceId));
        deleted.circuits = await deleteQueryDocs(db.collection('circuits').where('deviceId', '==', deviceId));
        if (bucket) {
            for (const prefix of ['videos', 'musics']) {
                await bucket.deleteFiles({ prefix: prefix + '/' + deviceId + '/' }).catch(e => console.warn('[delete] storage:', e.message));
            }
        }
        let licenseDeleted = false;
        if (deleteLicense === true && confirm === 'DELETE_MY_LICENSE') {
            await licRef.delete();
            licenseDeleted = true;
        }
        console.log('🗑️ Data deletion for device=' + deviceId + ' license=' + (licenseDeleted ? 'deleted' : 'kept'));
        return res.json({ status: 'ok', deleted, licenseDeleted });
    } catch (e) {
        console.error('[delete-data] failed:', e.message);
        return res.status(500).json({ error: 'Deletion failed' });
    }
});

// ============================================================================
// 17. Circuit Lab — AI endpoint (uses handleChatCore directly, no loopback)
// ============================================================================
// ✅ تم إضافة الأنواع الميكانيكية هنا
const CIRCUIT_MODES = new Set(['generate', 'explain', 'fix', 'arduino_code', 'generate_mechanical', 'explain_mechanical']);

function circuitSystemPrompt(mode, lang) {
    const language = lang === 'en' ? 'English' : 'Arabic';
    
    // ✅ إضافة برومبت المختبر الميكانيكي
    if (mode === 'generate_mechanical') {
        return 'You are a mechanical engineer designing 2D mechanical systems. ' +
               'Reply with ONE JSON object and nothing else (no markdown, no code fences). ' +
               'Schema: {"bodies":[{"type":"motor|gear|pulley|spring|ball|pendulum","x":100,"y":100,"size":30,"rpm":30,"k":60,"len":120}],"note":"short explanation in ' + language + '"}. ' +
               'x and y are screen coordinates (pixels). size is radius. rpm is motor speed. k is spring constant. len is pendulum or spring length.';
    }
    if (mode === 'explain_mechanical') {
        return 'You are a physics teacher. Explain the given mechanical design (JSON with bodies) in ' + language + ', ' +
               'in at most 5 short sentences: what it does, the physical principles (gravity, Hooke\'s law, gear ratios), and any issue. Plain text only.';
    }

    if (mode === 'generate') {
        return 'You design simple DC circuits for a circuit simulator. Reply with ONE JSON object and nothing else ' +
            '(no markdown, no code fences, no explanation). Schema: ' +
            '{"comps":[{"id":"B1","type":"battery","val":9},{"id":"S1","type":"switch","closed":true},' +
            '{"id":"R1","type":"resistor","val":330},{"id":"D1","type":"led","val":"red"}],' +
            '"wires":[["B1.a","S1.a"],["S1.b","R1.a"],["R1.b","D1.a"],["D1.b","B1.b"]]}. ' +
            'Allowed types: battery (1.5,3,4.5,5,9,12), resistor (10,47,100,220,330,470,1000,2200,4700,10000), ' +
            'capacitor (10,47,100,470,1000), diode (silicon,germanium), fuse (0.5,1,2,5), ' +
            'led (red,green,yellow,blue,white), bulb (25,50,100), switch (closed true or false). ' +
            'Every part has terminals a and b. Use ids B1,R1,D1,L1,S1,E1,C1,F1. ' +
            'Always include exactly one battery, close the loop, protect every LED with a series resistor, ' +
            'at most 12 parts, no positions.';
    }
    if (mode === 'fix') {
        return 'You are an electronics expert. The user sends a broken circuit as JSON. Fix it. ' +
            'Return ONLY the fixed JSON object with the same schema. ' +
            'Ensure all LEDs have series resistors, no short circuits, all loops closed.';
    }
    if (mode === 'arduino_code') {
        return 'You are an Arduino expert. The user sends a circuit as JSON. ' +
            'Write complete, compilable Arduino C++ code (setup + loop) that reproduces the circuit\'s behavior ' +
            'on an Arduino UNO. Infer pin mapping from wires: ' +
            'LEDs/buzzers/transistor bases → digital outputs, switches → INPUT_PULLUP, ' +
            'potentiometer wipers and LDR dividers → analog inputs, logic gates → boolean expressions. ' +
            'Start with a comment block listing the pin mapping. ' +
            'Write comments in ' + language + '. ' +
            'Return ONLY the code as plain text — no markdown fences, no explanations.';
    }
    return 'You are an electronics teacher. Explain the given circuit (JSON with parts, wires and simulated ' +
        'voltages and currents) in ' + language + ', in at most 8 short sentences: what it does, the ' +
        'current path, why each part is there, and any problem or improvement. Plain text only.';
}

function extractCircuitJson(text) {
    const a = text.indexOf('{'), b = text.lastIndexOf('}');
    if (a < 0 || b <= a) return null;
    try {
        const obj = JSON.parse(text.slice(a, b + 1));
        if (!Array.isArray(obj.comps) || obj.comps.length === 0 || obj.comps.length > 30) return null;
        if (!Array.isArray(obj.wires) || obj.wires.length > 70) return null;
        return obj;
    } catch (_) { return null; }
}

app.post('/api/ai/circuit', async (req, res) => {
    try {
        const b = req.body || {};
        const mode = typeof b.mode === 'string' ? b.mode : '';
        const prompt = typeof b.prompt === 'string' ? b.prompt.trim() : '';
        if (!CIRCUIT_MODES.has(mode)) return res.status(400).json({ error: 'bad mode' });
        if (!prompt || prompt.length > 20000) return res.status(400).json({ error: 'bad prompt' });
        if (typeof b.licenseKey !== 'string' || typeof b.deviceId !== 'string') {
            return res.status(400).json({ error: 'missing license or device' });
        }
        const lang = b.lang === 'en' ? 'en' : 'ar';

        // v8: call the core directly — no HTTP loopback, no double Express middleware
        const result = await handleChatCore({
            licenseKey: b.licenseKey,
            deviceId: b.deviceId,
            messages: [{ role: 'user', content: prompt }],
            systemPrompt: circuitSystemPrompt(mode, lang),
            provider: b.provider,
            providers: b.providers,
            attachments: [],
            cost: 1
        });

        if (!result.ok) return res.status(result.status).json(result.body);

        let text = String(result.body.text || '').trim();
        if (!text) return res.status(502).json({ error: 'empty reply' });

        // ✅ استخراج JSON يتم فقط للدوائر الكهربائية، وليس الميكانيكية
        if (mode === 'generate' || mode === 'fix') {
            const obj = extractCircuitJson(text);
            if (!obj) return res.status(422).json({ error: 'model did not return valid circuit JSON' });
            text = JSON.stringify(obj);
        }
        return res.json({ text, provider: result.body.provider });
    } catch (e) {
        console.error('[circuit] failed:', e && e.message ? e.message : e);
        return res.status(500).json({ error: 'circuit failed' });
    }
});

// ============================================================================
// 18. Circuit Lab — Cloud Save / Load
// ============================================================================
const CIRCUIT_CODE_RE = /^[A-Z2-9]{6}$/;
const CIRCUIT_CODE_CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
function newCircuitCode() {
    let code = '';
    for (let i = 0; i < 6; i++) code += CIRCUIT_CODE_CHARS.charAt(crypto.randomInt(CIRCUIT_CODE_CHARS.length));
    return code;
}

app.post('/api/circuit/save', async (req, res) => {
    if (!firebaseReady) return res.status(503).json({ error: 'DB not ready' });
    const { licenseKey, deviceId, circuit } = req.body || {};
    if (!isValidLicenseKey(licenseKey) || !isValidDeviceId(deviceId)) return res.status(401).json({ error: 'Invalid license' });
    if (typeof circuit !== 'string' || circuit.length === 0 || circuit.length > 200000) {
        return res.status(400).json({ error: 'bad circuit' });
    }

    const rl = saveLimiter.check(licenseKey);
    if (!rl.allowed) {
        return res.status(429).json({ error: 'RATE_LIMIT', retryAfter: Math.ceil((rl.resetAt - Date.now()) / 1000) });
    }

    try {
        const lic = await db.collection('licenses').doc(licenseKey).get();
        if (!lic.exists) return res.status(401).json({ error: 'Invalid license' });
        const ld = lic.data();
        if (ld.deviceId && ld.deviceId !== deviceId) return res.status(403).json({ error: 'LICENSE_BOUND' });
    } catch (_) { return res.status(500).json({ error: 'save failed' }); }

    for (let attempt = 0; attempt < 5; attempt++) {
        const code = newCircuitCode();
        try {
            await db.collection('circuits').doc(code).create({
                licenseKey, deviceId, circuit, createdAt: admin.firestore.FieldValue.serverTimestamp()
            });
            return res.json({ status: 'ok', code });
        } catch (e) {
            if (e && (e.code === 6 || /already exists/i.test(e.message || ''))) continue;
            console.error('Save circuit error:', e.message);
            return res.status(500).json({ error: 'save failed' });
        }
    }
    return res.status(500).json({ error: 'save failed' });
});

app.get('/api/circuit/load/:code', async (req, res) => {
    if (!firebaseReady) return res.status(503).json({ error: 'DB not ready' });
    const code = String(req.params.code || '').toUpperCase();
    if (!CIRCUIT_CODE_RE.test(code)) return res.status(400).json({ error: 'bad code' });
    try {
        const doc = await db.collection('circuits').doc(code).get();
        if (!doc.exists) return res.status(404).json({ error: 'Not found' });
        res.json({ status: 'ok', circuit: doc.data().circuit });
    } catch (e) {
        console.error('Load circuit error:', e.message);
        res.status(500).json({ error: 'load failed' });
    }
});

// ============================================================================
// 19. Start
// ============================================================================
const PORT = process.env.PORT || 10000;
// Startup self-test: proves the Firebase service-account key really works (init alone never fails on a wrong key).
if (firebaseReady) {
    db.collection('licenses').limit(1).get()
        .then(snap => console.log(`🗄️ Firestore OK (licenses readable, sample=${snap.size})`))
        .catch(e => console.error('❌ Firestore NOT usable — wrong/expired service-account key or project:', e.message));
}

app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Server on port ${PORT} (v8)`);
    console.log(`🔐 Ed25519 pub: ${Buffer.from(ED25519_PUBLIC_KEY).toString('hex').substring(0, 16)}…`);
    console.log(`✅ Streaming: unbuffered SSE (async partial refund)`);
    console.log(`🧪 Circuit Lab: /api/ai/circuit → handleChatCore directly (no loopback)`);
    console.log(`⚙️ Mechanical Lab: accepted generate_mechanical & explain_mechanical`);
    console.log(`🎙️ TTS: ${OPENAI_API_KEY ? 'OpenAI (PCM 24kHz)' : 'unavailable (app falls back to phone)'}`);
    console.log(`🛡️ Rate limits: AI=30/min, TTS=20/min, Save=20/min per license`);
    console.log(`🌐 Trust proxy: enabled (req.ip is real client IP)`);
    getPaymentEnabled().then(v => console.log(`🆓 Payment mode: ${v ? 'PAID (licenses + credits)' : 'FREE (no license needed for chat/image/tts)'} — read from Firestore config/app`));
});