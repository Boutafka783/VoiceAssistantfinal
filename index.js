#!/usr/bin/env node
// ══════════════════════════════════════════════════════════════════════════════
// Zevorix AI & Gradiometer — Backend v8
// Production-ready: rate limits · SSRF guard · fixed models · TTS credits
//                 · no-loopback circuit · trust proxy · async refund
// ══════════════════════════════════════════════════════════════════════════════

'use strict';

const express = require('express');
const sgMail = require('@sendgrid/mail');
const crypto = require('crypto');
const admin = require('firebase-admin');
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
const SENDGRID_KEY             = process.env.SENDGRID_KEY;
const NOWPAYMENTS_IPN_SECRET   = process.env.NOWPAYMENTS_IPN_SECRET;
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

if (SENDGRID_KEY) sgMail.setApiKey(SENDGRID_KEY);
console.log('🔐 Ed25519 loaded (pub: ' + Buffer.from(ED25519_PUBLIC_KEY).toString('hex').substring(0, 16) + '…)');
console.log('🤖 AI keys: Gemini=' + (GEMINI_API_KEYS.length > 0 ? `✓ (${GEMINI_API_KEYS.length})` : '✗') + ' OpenAI=' + (OPENAI_API_KEY ? '✓' : '✗') + ' Claude=' + (CLAUDE_API_KEY ? '✓' : '✗'));

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
const isValidJobId = (id) => typeof id === 'string' && /^[A-Za-z0-9]{10,40}$/.test(id);
const webhookToken = (d, t, j) => crypto.createHmac('sha256', LICENSE_SECRET).update(`WH|${d}|${t}|${j || ''}`).digest('hex').substring(0, 32);

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
const ttsLimiter    = new RateLimiter(20, 60_000, 'tts');
const saveLimiter   = new RateLimiter(20, 60_000, 'save');

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
    'gemini-3.8-flash',
    'gemini-3.1-flash-lite'
];
const OPENAI_MODEL = 'gpt-4o-mini';
const CLAUDE_MODEL = 'claude-3-5-sonnet-20241022';
const GEMINI_IMAGE_MODEL = 'gemini-3.1-flash-image';
const DEFAULT_TIMEOUT_MS = parseInt(process.env.AI_TIMEOUT_MS) || 300_000;

async function fetchWithTimeout(url, options = {}, timeoutMs = DEFAULT_TIMEOUT_MS) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
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

async function callGemini(apiKey, model, messages, systemPrompt, attachments) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`;
    const body = {
        system_instruction: { parts: [{ text: systemPrompt }] },
        contents: [
            ...messages.slice(0, -1).map(m => ({ role: toGeminiRole(m.role), parts: [{ text: m.content }] })),
            { role: 'user', parts: toGeminiParts(messages, attachments) }
        ],
        generationConfig: { maxOutputTokens: 16384 }
    };
    const res = await fetchWithTimeout(url, { method: 'POST', headers: { 'x-goog-api-key': apiKey, 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    const raw = await res.text();
    if (!res.ok) throw new Error(`gemini ${res.status}: ${raw.slice(0, 200)}`);
    const json = JSON.parse(raw);
    const text = (json.candidates?.[0]?.content?.parts || []).map(p => p.text || '').join('').trim();
    if (!text) throw new Error('gemini: empty');
    return { text, provider: 'gemini', model };
}

async function callOpenAI(apiKey, model, messages, systemPrompt) {
    const url = 'https://api.openai.com/v1/chat/completions';
    const normalized = messages.map(m => ({ role: normalizeRole(m.role), content: m.content }));
    const body = { model, messages: [{ role: 'system', content: systemPrompt }, ...normalized], max_tokens: 8192 };
    const res = await fetchWithTimeout(url, { method: 'POST', headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    const raw = await res.text();
    if (!res.ok) throw new Error(`openai ${res.status}: ${raw.slice(0, 200)}`);
    const json = JSON.parse(raw);
    const text = json.choices?.[0]?.message?.content?.trim();
    if (!text) throw new Error('openai: empty');
    return { text, provider: 'openai', model };
}

async function callClaude(apiKey, model, messages, systemPrompt, attachments) {
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
    const res = await fetchWithTimeout(url, { method: 'POST', headers: { 'x-api-key': apiKey, 'anthropic-version': '2023-06-01', 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    const raw = await res.text();
    if (!res.ok) throw new Error(`claude ${res.status}: ${raw.slice(0, 200)}`);
    const json = JSON.parse(raw);
    const text = (json.content || []).filter(b => b.type === 'text').map(b => b.text).join('').trim();
    if (!text) throw new Error('claude: empty');
    return { text, provider: 'claude', model };
}

async function tryProvider(provider, messages, systemPrompt, attachments) {
    if (provider === 'gemini') {
        let lastErr;
        const maxAttempts = Math.max(3, Math.min(GEMINI_API_KEYS.length * 2, 6));
        for (let attempt = 0; attempt < maxAttempts; attempt++) {
            const apiKey = getNextGeminiKey();
            if (!apiKey) throw new Error('gemini: no key');
            const model = GEMINI_MODELS[attempt % GEMINI_MODELS.length];
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
        return await callOpenAI(OPENAI_API_KEY, OPENAI_MODEL, messages, systemPrompt);
    }
    if (provider === 'claude') {
        if (!CLAUDE_API_KEY) throw new Error('claude: no key');
        return await callClaude(CLAUDE_API_KEY, CLAUDE_MODEL, messages, systemPrompt, attachments);
    }
    throw new Error('unknown provider: ' + provider);
}

// --- Streaming generators ---
async function* streamGemini(apiKey, model, messages, systemPrompt, attachments) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:streamGenerateContent?alt=sse`;
    const body = {
        system_instruction: { parts: [{ text: systemPrompt }] },
        contents: [
            ...messages.slice(0, -1).map(m => ({ role: toGeminiRole(m.role), parts: [{ text: m.content }] })),
            { role: 'user', parts: toGeminiParts(messages, attachments) }
        ],
        generationConfig: { maxOutputTokens: 16384 }
    };
    const res = await fetchWithTimeout(url, { method: 'POST', headers: { 'x-goog-api-key': apiKey, 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
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

async function* streamOpenAI(apiKey, model, messages, systemPrompt) {
    const url = 'https://api.openai.com/v1/chat/completions';
    const normalized = messages.map(m => ({ role: normalizeRole(m.role), content: m.content }));
    const body = { model, messages: [{ role: 'system', content: systemPrompt }, ...normalized], stream: true, max_tokens: 8192 };
    const res = await fetchWithTimeout(url, { method: 'POST', headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
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

async function* streamClaude(apiKey, model, messages, systemPrompt, attachments) {
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
    const res = await fetchWithTimeout(url, { method: 'POST', headers: { 'x-api-key': apiKey, 'anthropic-version': '2023-06-01', 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
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
            ai: { gemini: GEMINI_API_KEYS.length > 0, openai: !!OPENAI_API_KEY, claude: !!CLAUDE_API_KEY },
            license: 'ed25519',
            streaming: true,
            unbuffered_sse: true,
            circuit_lab: true,
            arduino_code: true,
            tts: !!OPENAI_API_KEY,
            rate_limited: true,
            circuit_no_loopback: true,
            async_partial_refund: true
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
    const { licenseKey, deviceId, messages, systemPrompt, provider, providers, attachments } = body;
    const cost = typeof body.cost === 'number' ? Math.max(1, Math.min(10, Math.floor(body.cost))) : 1;

    if (!isValidDeviceId(deviceId) || !isValidLicenseKey(licenseKey) || !Array.isArray(messages) || messages.length === 0) {
        return res.status(400).json({ error: 'Invalid request' });
    }
    if (!firebaseReady) return res.status(503).json({ error: 'Service not ready' });

    const rl = aiChatLimiter.check(licenseKey);
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
        return res.status(401).json({ error: 'INVALID_LICENSE' });
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

    let sentAnyChunk = false;
    let success = false;
    let usedProvider = null;

    for (const p of order) {
        if (clientDisconnected || sentAnyChunk) break;
        try {
            let stream;
            if (p === 'gemini') {
                const apiKey = getNextGeminiKey();
                if (apiKey) stream = streamGemini(apiKey, GEMINI_MODELS[0], messages, systemPrompt || '', attachments || []);
                else continue;
            } else if (p === 'openai' && OPENAI_API_KEY) {
                stream = streamOpenAI(OPENAI_API_KEY, OPENAI_MODEL, messages, systemPrompt || '');
            } else if (p === 'claude' && CLAUDE_API_KEY) {
                stream = streamClaude(CLAUDE_API_KEY, CLAUDE_MODEL, messages, systemPrompt || '', attachments || []);
            } else continue;

            let thisProviderSent = false;
            for await (const chunk of stream) {
                if (clientDisconnected) break;
                sendChunk(chunk);
                sentAnyChunk = true;
                thisProviderSent = true;
            }
            if (thisProviderSent) { success = true; usedProvider = p; break; }
        } catch (e) {
            console.warn(`Stream ${p} failed:`, e.message);
            if (sentAnyChunk) break;
        }
    }

    if (success) {
        if (jobId) db.collection('jobs').doc(jobId).update({
            status: 'completed', completedAt: admin.firestore.FieldValue.serverTimestamp(), provider: usedProvider
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
async function handleChatCore({ licenseKey, deviceId, messages, systemPrompt, provider, providers, attachments, cost }) {
    if (!isValidDeviceId(deviceId)) return { ok: false, status: 400, body: { error: 'Invalid device' } };
    if (!Array.isArray(messages) || messages.length === 0) return { ok: false, status: 400, body: { error: 'Invalid messages' } };
    if (!isValidLicenseKey(licenseKey)) return { ok: false, status: 401, body: { error: 'INVALID_LICENSE' } };
    if (!firebaseReady) return { ok: false, status: 503, body: { error: 'Service not ready' } };

    const rl = aiChatLimiter.check(licenseKey);
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
        if (e.message === 'INVALID_LICENSE') return { ok: false, status: 401, body: { error: 'INVALID_LICENSE' } };
        return { ok: false, status: 500, body: { error: 'Internal error' } };
    }

    const order = Array.isArray(providers) && providers.length > 0 ? providers : (provider ? [provider] : ['gemini', 'openai', 'claude']);
    let lastError = null;
    const started = Date.now();

    for (const p of order) {
        try {
            const result = await tryProvider(p, messages, systemPrompt || '', attachments || []);
            const latencyMs = Date.now() - started;
            if (jobId) db.collection('jobs').doc(jobId).update({
                status: 'completed', completedAt: admin.firestore.FieldValue.serverTimestamp(),
                provider: result.provider, model: result.model, latencyMs
            }).catch(() => {});
            return { ok: true, status: 200, body: { text: result.text, provider: result.provider, model: result.model, latencyMs } };
        } catch (e) {
            lastError = e;
            console.warn(`Provider ${p} failed: ${e.message}`);
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
        cost
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
    if (!isValidLicenseKey(licenseKey)) return res.status(401).json({ error: 'INVALID_LICENSE' });
    if (GEMINI_API_KEYS.length === 0) return res.status(503).json({ error: 'AI_NOT_CONFIGURED' });
    if (!firebaseReady) return res.status(503).json({ error: 'Service not ready' });

    let jobId = null;
    try {
        const r = await deductCredits(licenseKey, deviceId, cost, 'image', prompt);
        jobId = r.jobId;
    } catch (e) {
        if (e.message === 'INSUFFICIENT_CREDITS') return res.status(402).json({ error: 'INSUFFICIENT_CREDITS' });
        if (e.message === 'LICENSE_BOUND_TO_OTHER_DEVICE') return res.status(403).json({ error: 'LICENSE_BOUND' });
        return res.status(401).json({ error: 'INVALID_LICENSE' });
    }

    try {
        const apiKey = getNextGeminiKey();
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_IMAGE_MODEL}:predict`;
        const payload = {
            instances: [{ prompt }],
            parameters: { sampleCount: 1 }
        };
        const r = await fetchWithTimeout(url, {
            method: 'POST',
            headers: { 'x-goog-api-key': apiKey, 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        }, 90_000);
        const raw = await r.text();
        if (!r.ok) throw new Error(`imagen ${r.status}: ${raw.slice(0, 200)}`);
        const json = JSON.parse(raw);
        const preds = json.predictions || [];
        const b64 = preds[0]?.bytesBase64Encoded;
        if (!b64) throw new Error('imagen: no image in response');

        if (jobId) db.collection('jobs').doc(jobId).update({
            status: 'completed', completedAt: admin.firestore.FieldValue.serverTimestamp()
        }).catch(() => {});
        res.json({ image: b64, mime: 'image/png' });
    } catch (e) {
        try { await failJob(jobId, `image failed: ${e.message}`); } catch (_) {}
        return res.status(502).json({ error: 'AI_FAILED', message: String(e.message || '').slice(0, 300) });
    }
});

// ============================================================================
// 12. AI TTS — OpenAI (24kHz mono PCM)
// ============================================================================
const OPENAI_VOICE_MAP = {
    'Kore': 'nova', 'Aoede': 'shimmer', 'Leda': 'nova', 'Zephyr': 'shimmer', 'Sulafat': 'nova',
    'Charon': 'onyx', 'Puck': 'echo', 'Orus': 'onyx', 'Fenrir': 'echo', 'Achird': 'alloy'
};
const OPENAI_VOICES = new Set(['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']);

app.post('/api/ai/tts', async (req, res) => {
    const body = req.body || {};
    const { licenseKey, deviceId, text, voiceId } = body;
    const cleanText = typeof text === 'string' ? text.trim() : '';

    if (!isValidDeviceId(deviceId)) return res.status(400).json({ error: 'Invalid device' });
    if (!cleanText || cleanText.length > 5000) return res.status(400).json({ error: 'Invalid text' });
    if (!isValidLicenseKey(licenseKey)) return res.status(401).json({ error: 'INVALID_LICENSE' });
    if (!firebaseReady) return res.status(503).json({ error: 'Service not ready' });

    if (!OPENAI_API_KEY) {
        return res.status(503).json({ error: 'TTS_NOT_CONFIGURED', message: 'OpenAI TTS not configured. App will use phone TTS.' });
    }

    const rl = ttsLimiter.check(licenseKey);
    if (!rl.allowed) {
        return res.status(429).json({ error: 'RATE_LIMIT', retryAfter: Math.ceil((rl.resetAt - Date.now()) / 1000) });
    }

    let jobId = null;
    try {
        const r = await deductCredits(licenseKey, deviceId, 1, 'tts', cleanText.slice(0, 100));
        jobId = r.jobId;
    } catch (e) {
        if (e.message === 'INSUFFICIENT_CREDITS') return res.status(402).json({ error: 'INSUFFICIENT_CREDITS' });
        return res.status(401).json({ error: 'INVALID_LICENSE' });
    }

    try {
        const voice = OPENAI_VOICES.has(String(voiceId || '').toLowerCase())
            ? String(voiceId).toLowerCase()
            : (OPENAI_VOICE_MAP[voiceId] || 'nova');

        const url = 'https://api.openai.com/v1/audio/speech';
        const payload = {
            model: 'tts-1',
            voice,
            input: cleanText,
            response_format: 'pcm',
            speed: 1.0
        };
        const r = await fetchWithTimeout(url, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${OPENAI_API_KEY}`, 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        }, 60_000);
        if (!r.ok) throw new Error(`openai tts ${r.status}: ${await r.text()}`);

        const pcmBuffer = Buffer.from(await r.arrayBuffer());
        if (pcmBuffer.length === 0) throw new Error('tts: empty audio');
        if (pcmBuffer.length % 2 !== 0) throw new Error('tts: odd byte count');

        if (jobId) db.collection('jobs').doc(jobId).update({
            status: 'completed', completedAt: admin.firestore.FieldValue.serverTimestamp()
        }).catch(() => {});

        res.set('Content-Type', 'application/octet-stream');
        res.set('X-Sample-Rate', '24000');
        res.set('X-Channels', '1');
        res.send(pcmBuffer);
    } catch (e) {
        try { await failJob(jobId, `tts failed: ${e.message}`); } catch (_) {}
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
        const { remaining, jobId } = await deductCredits(licenseKey, deviceId, cost, type, prompt);
        res.status(200).json({ status: 'started', remaining });
        triggerReplicateAsync(prompt, deviceId, type, jobId).catch(err => {
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
        processVideoEdit(file, prompt, deviceId, jobId).catch(err => {
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
// 16. NOWPayments IPN — with create() retry
// ============================================================================
app.post('/nowpayments/ipn', async (req, res) => {
    try {
        const receivedSig = req.headers['x-nowpayments-sig'];
        const gradSecret = (process.env.GRADIOMETER_IPN_SECRET || '').trim();
        const zevSecret  = (NOWPAYMENTS_IPN_SECRET || '').trim();
        if (!gradSecret && !zevSecret) return res.status(500).send('Config error');

        const sortedBody = JSON.stringify(deepSort(req.body));
        const sigFor = (s) => crypto.createHmac('sha512', s).update(sortedBody).digest('hex');

        const matchGrad = !!gradSecret && safeEqual(receivedSig, sigFor(gradSecret));
        const matchZev  = !!zevSecret  && safeEqual(receivedSig, sigFor(zevSecret));
        if (!matchGrad && !matchZev) { console.warn('❌ Invalid IPN signature'); return res.status(401).send('Invalid signature'); }

        const { payment_status, order_id, customer_email, price_amount, payment_id } = req.body;
        const target = (matchGrad && matchZev) ? (order_id ? 'grad' : 'zev') : (matchGrad ? 'grad' : 'zev');

        if (payment_status !== 'finished' && payment_status !== 'confirmed') {
            return res.status(200).send('Not confirmed yet');
        }

        if (target === 'grad') {
            if (!order_id) return res.status(400).send('Missing order_id');
            if (!gradDb) return res.status(503).send('Gradiometer DB not ready');
            await gradDb.collection('purchases').doc(String(order_id)).set({
                paid: true, paymentId: String(payment_id),
                confirmedAt: admin.firestore.FieldValue.serverTimestamp()
            }, { merge: true });
            console.log(`✅ Gradiometer purchase confirmed: uid=${order_id}`);
            return res.status(200).send('OK');
        }

        if (!customer_email) return res.status(400).send('Missing customer_email');
        if (!firebaseReady || !payment_id) return res.status(500).send('Database not ready');
        if (!customer_email.includes('@')) return res.status(400).send('Invalid email');

        let creditsToAdd = 0;
        const amount = parseFloat(price_amount || 0);
        if (amount >= 130) creditsToAdd = 1800;
        else if (amount >= 65) creditsToAdd = 800;
        else if (amount >= 30) creditsToAdd = 350;
        else if (amount >= 10) creditsToAdd = 100;
        else return res.status(400).send('Amount too low');

        let licenseKey = null;
        let attempts = 0;
        while (attempts < 5) {
            try {
                await db.runTransaction(async (tx) => {
                    const orderRef = db.collection('orders').doc(String(payment_id));
                    const orderDoc = await tx.get(orderRef);
                    if (orderDoc.exists) throw new Error('ALREADY_PROCESSED');

                    const candidate = generateLicenseKey();
                    tx.create(db.collection('licenses').doc(candidate), {
                        credits: creditsToAdd,
                        email: customer_email,
                        createdAt: admin.firestore.FieldValue.serverTimestamp()
                    });
                    tx.set(orderRef, {
                        email: customer_email, licenseKey: candidate, amount, credits: creditsToAdd,
                        status: 'issued', createdAt: admin.firestore.FieldValue.serverTimestamp()
                    });
                    licenseKey = candidate;
                });
                break;
            } catch (e) {
                if (e.message === 'ALREADY_PROCESSED') throw e;
                if (e.code === 6) { attempts++; continue; }
                throw e;
            }
        }
        if (!licenseKey) throw new Error('LICENSE_GEN_COLLISION_5X');

        if (SENDGRID_KEY) {
            await sgMail.send({
                to: customer_email, from: 'tijara6@gmail.com',
                subject: 'تم تفعيل نسختك المدفوعة من Zevorix AI',
                html: `<h3>شكراً لشرائك!</h3>
                       <p>كود التفعيل: <strong>${licenseKey}</strong></p>
                       <p>تمت إضافة <strong>${creditsToAdd} نقطة</strong> لرصيدك.</p>`
            }).catch(e => console.error('Email:', e.message));
        }
        return res.status(200).send('License sent');
    } catch (error) {
        if (error.message === 'ALREADY_PROCESSED') return res.status(200).send('Already processed');
        console.error('IPN error:', error.message);
        res.status(500).send('Error');
    }
});

// ============================================================================
// 17. Circuit Lab — AI endpoint (uses handleChatCore directly, no loopback)
// ============================================================================
const CIRCUIT_MODES = new Set(['generate', 'explain', 'fix', 'arduino_code']);

function circuitSystemPrompt(mode, lang) {
    const language = lang === 'en' ? 'English' : 'Arabic';
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
app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Server on port ${PORT} (v8)`);
    console.log(`🔐 Ed25519 pub: ${Buffer.from(ED25519_PUBLIC_KEY).toString('hex').substring(0, 16)}…`);
    console.log(`✅ Streaming: unbuffered SSE (async partial refund)`);
    console.log(`🧪 Circuit Lab: /api/ai/circuit → handleChatCore directly (no loopback)`);
    console.log(`🎙️ TTS: ${OPENAI_API_KEY ? 'OpenAI (PCM 24kHz)' : 'unavailable (app falls back to phone)'}`);
    console.log(`🛡️ Rate limits: AI=30/min, TTS=20/min, Save=20/min per license`);
    console.log(`🌐 Trust proxy: enabled (req.ip is real client IP)`);
});