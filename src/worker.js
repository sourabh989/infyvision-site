// Infinity Vision Worker: serves static assets and handles the enquiry API.
// Routes (only /api/* runs the Worker first, see wrangler.jsonc):
//   POST /api/enquiry                 public form submission (JSON or form-encoded)
//   GET  /api/enquiries/unsynced      admin, Bearer ADMIN_TOKEN, ?limit=1..500
//   POST /api/enquiries/mark-synced   admin, Bearer ADMIN_TOKEN, body {"ids":[1,2]}
import OPTIONS from './form-options.json' with { type: 'json' };

const MAX_BODY = 8 * 1024;
const API_HEADERS = {
  'content-type': 'application/json; charset=utf-8',
  'cache-control': 'no-store',
  'x-content-type-options': 'nosniff',
  'x-robots-tag': 'noindex, nofollow',
  'referrer-policy': 'strict-origin-when-cross-origin',
};

const json = (data, status = 200, extra = {}) => new Response(JSON.stringify(data), { status, headers: { ...API_HEADERS, ...extra } });

export function normalisePhone(raw) {
  let d = String(raw ?? '').replace(/[\s\-().]/g, '');
  if (d.startsWith('+')) d = d.slice(1);
  if (d.length === 12 && d.startsWith('91')) d = d.slice(2);
  else if (d.length === 11 && d.startsWith('0')) d = d.slice(1);
  return /^[6-9]\d{9}$/.test(d) ? d : '';
}

const clean = (v, max) => String(v ?? '').replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, '').replace(/\s+/g, ' ').trim().slice(0, max);
const cleanMessage = (v, max) => String(v ?? '').replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, '').replace(/\r\n?/g, '\n').trim().slice(0, max);

/** ISO 8601 in India Standard Time, e.g. 2026-11-09T22:30:05+05:30 */
export function istIso(date = new Date()) {
  return new Date(date.getTime() + 330 * 60000).toISOString().slice(0, 19) + '+05:30';
}

export function validateEnquiry(input) {
  const errors = {};
  const name = clean(input.name, 80);
  const phone = normalisePhone(input.phone);
  const course = clean(input.course, 80);
  const preferred_time = clean(input.preferred_time ?? input.time, 60);
  const level = clean(input.level, 40);
  const message = cleanMessage(input.message, 600);
  const source_page = clean(input.source_page, 120);
  if (name.length < 2 || !/\p{L}/u.test(name)) errors.name = 'Please enter your name.';
  if (!phone) errors.phone = 'Please enter a valid 10-digit Indian mobile number.';
  if (!OPTIONS.courses.includes(course)) errors.course = 'Please choose a course from the list.';
  if (!OPTIONS.times.includes(preferred_time)) errors.preferred_time = 'Please choose a preferred time.';
  if (level && !OPTIONS.levels.includes(level)) errors.level = 'Please choose your starting level from the list.';
  if (String(input.message ?? '').length > 2000) errors.message = 'Please keep the message under 600 characters.';
  return {
    ok: Object.keys(errors).length === 0,
    errors,
    value: { name, phone, course, level: level || null, preferred_time, message: message || null, source_page: source_page.startsWith('/') ? source_page : null },
  };
}

async function sha256Hex(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}

async function readBody(request) {
  const len = Number(request.headers.get('content-length') || 0);
  if (len > MAX_BODY) throw Object.assign(new Error('Request too large.'), { status: 413 });
  const text = await request.text();
  if (text.length > MAX_BODY) throw Object.assign(new Error('Request too large.'), { status: 413 });
  const type = (request.headers.get('content-type') || '').toLowerCase();
  if (type.includes('application/json')) {
    try { const data = JSON.parse(text); if (data && typeof data === 'object' && !Array.isArray(data)) return { data, isJson: true }; } catch {}
    throw Object.assign(new Error('Invalid JSON.'), { status: 400 });
  }
  if (type.includes('application/x-www-form-urlencoded')) return { data: Object.fromEntries(new URLSearchParams(text)), isJson: false };
  throw Object.assign(new Error('Unsupported content type.'), { status: 415 });
}

function htmlResult(ok, text, back, status = ok ? 200 : 400) {
  const safe = s => s.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const href = back && back.startsWith('/') && !back.startsWith('//') ? back : '/';
  const body = `<!DOCTYPE html><html lang="en-IN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${ok ? 'Enquiry received' : 'Enquiry not sent'} | Infinity Vision</title><link rel="stylesheet" href="/assets/site.css"></head><body><main id="main" style="max-width:640px;margin:12vh auto;padding:24px"><h1>${ok ? 'Thank you, we have your enquiry.' : 'Your enquiry was not sent.'}</h1><p>${safe(text)}</p><p><a class="btn btn-primary" href="${safe(href)}#contact">Back to the website</a> <a class="btn btn-wa" href="https://wa.me/919098372445" rel="noopener noreferrer">WhatsApp 9098372445</a> <a class="btn btn-ghost" href="tel:+919098372445">Call 9098372445</a></p></main></body></html>`;
  return new Response(body, { status, headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store', 'x-content-type-options': 'nosniff', 'x-robots-tag': 'noindex, nofollow', 'content-security-policy': "default-src 'none'; style-src 'self' 'unsafe-inline'; font-src 'self'; form-action 'none'; frame-ancestors 'none'; base-uri 'none'" } });
}

async function handleEnquiry(request, env) {
  const url = new URL(request.url);
  const origin = request.headers.get('origin');
  if (origin && origin !== url.origin) return json({ ok: false, error: 'Cross-site submissions are not accepted.' }, 403);
  let parsed;
  try { parsed = await readBody(request); } catch (e) { return json({ ok: false, error: e.message }, e.status || 400); }
  const { data, isJson } = parsed;
  const respond = (ok, status, payload, text) => (isJson ? json(payload, status) : htmlResult(ok, text, clean(data.source_page, 120), ok ? 200 : status));

  // Honeypot: real visitors never fill this hidden field. Pretend success, store nothing.
  if (clean(data.website, 200)) return respond(true, 200, { ok: true }, 'Thank you. Our team will call you back soon.');

  const result = validateEnquiry(data);
  if (!result.ok) {
    const first = Object.values(result.errors)[0];
    return respond(false, 422, { ok: false, error: first, fields: result.errors }, first);
  }

  const ip = request.headers.get('cf-connecting-ip') || 'unknown';
  const ipHash = (await sha256Hex(`${env.IP_HASH_SALT || 'infyvision'}|${ip}`)).slice(0, 32);
  const max = Number(env.RATE_LIMIT_MAX || 5);
  const windowMin = Number(env.RATE_LIMIT_WINDOW_MINUTES || 10);
  const since = istIso(new Date(Date.now() - windowMin * 60000));
  const recent = await env.DB.prepare('SELECT COUNT(*) AS n FROM enquiries WHERE ip_hash = ?1 AND created_at > ?2').bind(ipHash, since).first('n');
  if (recent >= max) {
    const msg = 'Too many enquiries from this connection. Please try again in a few minutes.';
    return isJson ? json({ ok: false, error: msg }, 429, { 'retry-after': String(windowMin * 60) }) : htmlResult(false, msg, clean(data.source_page, 120), 429);
  }

  const v = result.value;
  const createdAt = istIso();
  const ua = clean(request.headers.get('user-agent'), 300);
  const row = await env.DB.prepare('INSERT INTO enquiries (created_at, name, phone, course, level, preferred_time, message, source_page, user_agent, ip_hash) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10) RETURNING id')
    .bind(createdAt, v.name, v.phone, v.course, v.level, v.preferred_time, v.message, v.source_page, ua, ipHash).first();
  return respond(true, 201, { ok: true, id: row?.id, created_at: createdAt }, 'Our team will call you back on the number you gave. For a faster reply, message us on WhatsApp.');
}

async function isAdmin(request, env) {
  const header = request.headers.get('authorization') || '';
  const token = header.startsWith('Bearer ') ? header.slice(7).trim() : '';
  if (!env.ADMIN_TOKEN || !token) return false;
  const [a, b] = await Promise.all([sha256Hex(token), sha256Hex(env.ADMIN_TOKEN)]);
  const enc = new TextEncoder();
  return crypto.subtle.timingSafeEqual(enc.encode(a), enc.encode(b));
}

async function handleUnsynced(request, env) {
  const url = new URL(request.url);
  const limit = Math.min(500, Math.max(1, Number.parseInt(url.searchParams.get('limit') || '100', 10) || 100));
  const { results } = await env.DB.prepare('SELECT id, created_at, name, phone, course, level, preferred_time, message, source_page, user_agent FROM enquiries WHERE synced_to_sheet = 0 ORDER BY id LIMIT ?1').bind(limit).all();
  return json({ ok: true, count: results.length, enquiries: results });
}

async function handleMarkSynced(request, env) {
  let data;
  try { ({ data } = await readBody(request)); } catch (e) { return json({ ok: false, error: e.message }, e.status || 400); }
  const ids = Array.isArray(data.ids) ? [...new Set(data.ids.map(Number))].filter(n => Number.isInteger(n) && n > 0) : [];
  if (!ids.length || ids.length > 500) return json({ ok: false, error: 'Provide "ids": an array of 1 to 500 enquiry ids.' }, 400);
  const placeholders = ids.map((_, i) => `?${i + 1}`).join(',');
  const res = await env.DB.prepare(`UPDATE enquiries SET synced_to_sheet = 1 WHERE synced_to_sheet = 0 AND id IN (${placeholders})`).bind(...ids).run();
  return json({ ok: true, updated: res.meta?.changes ?? 0 });
}

const ROUTES = {
  '/api/enquiry': { POST: handleEnquiry },
  '/api/enquiries/unsynced': { GET: handleUnsynced, admin: true },
  '/api/enquiries/mark-synced': { POST: handleMarkSynced, admin: true },
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (!url.pathname.startsWith('/api/')) return env.ASSETS.fetch(request);
    const route = ROUTES[url.pathname.replace(/\/+$/, '')];
    if (!route) return json({ ok: false, error: 'Not found.' }, 404);
    const handler = route[request.method];
    if (!handler) return json({ ok: false, error: 'Method not allowed.' }, 405, { allow: Object.keys(route).filter(k => k !== 'admin').join(', ') });
    if (route.admin && !(await isAdmin(request, env))) return json({ ok: false, error: 'Unauthorised.' }, 401, { 'www-authenticate': 'Bearer' });
    try {
      return await handler(request, env);
    } catch (err) {
      console.error('api error', url.pathname, err && err.message);
      return json({ ok: false, error: 'Something went wrong on our side.' }, 500);
    }
  },
};
