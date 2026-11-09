// Unit tests for the Worker's pure validation helpers (no network, no D1).
import assert from 'node:assert/strict';
import { normalisePhone, validateEnquiry, istIso } from '../src/worker.js';
import OPTIONS from '../src/form-options.json' with { type: 'json' };
for (const [raw, want] of [['9876543210','9876543210'],['+91 98765 43210','9876543210'],['91-98765-43210','9876543210'],['09876543210','9876543210'],['(987) 654-3210','9876543210'],['5876543210',''],['987654321',''],['98765432100',''],['abcdefghij',''],['','']]) assert.equal(normalisePhone(raw), want, raw);
assert.equal(istIso(new Date('2026-11-09T18:45:30Z')), '2026-11-10T00:15:30+05:30');
const good = { name: 'Riya Sharma', phone: '98765 43210', course: OPTIONS.courses[0], preferred_time: OPTIONS.times[2], message: 'Hello' };
let r = validateEnquiry(good); assert(r.ok); assert.equal(r.value.phone, '9876543210'); assert.equal(r.value.level, null);
for (const c of OPTIONS.courses) assert(validateEnquiry({ ...good, course: c }).ok, c);
assert(!validateEnquiry({ ...good, course: 'Something else' }).ok);
assert(!validateEnquiry({ ...good, preferred_time: 'midnight' }).ok);
assert(!validateEnquiry({ ...good, name: '1' }).ok);
assert(!validateEnquiry({ ...good, level: 'Expert hacker' }).ok);
assert.equal(validateEnquiry({ ...good, message: 'x'.repeat(900) }).value.message.length, 600);
assert.equal(validateEnquiry({ ...good, source_page: 'https://evil' }).value.source_page, null);
console.log('PASS worker: phone normalisation, IST timestamps, course/time/level allow-lists, length limits');
