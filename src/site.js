// Infinity Vision V5 front-end: native JS (no libraries). Particles, typed text, reveals, counters,
// nav state, mobile menu, cursor glow and the enquiry form (POST /api/enquiry with WhatsApp fallback).
const doc = document.documentElement;
doc.classList.add('js');
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
const WA = '919098372445';

// Navbar background on scroll + mobile menu
const nav = document.querySelector('[data-nav]');
const onScroll = () => { if (nav) nav.classList.toggle('scrolled', window.scrollY > 30); document.body.classList.toggle('fab-on', window.scrollY > 280); };
onScroll();
window.addEventListener('scroll', onScroll, { passive: true });
const menuBtn = document.querySelector('[data-menu]');
const menu = document.getElementById('site-nav');
if (menuBtn && menu) {
  const setOpen = open => { menu.classList.toggle('open', open); menuBtn.setAttribute('aria-expanded', String(open)); };
  menuBtn.addEventListener('click', () => setOpen(menuBtn.getAttribute('aria-expanded') !== 'true'));
  menu.addEventListener('click', e => { if (e.target.closest('a')) setOpen(false); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && menuBtn.getAttribute('aria-expanded') === 'true') { setOpen(false); menuBtn.focus(); } });
}

// Reveal on scroll. Always ends visible: observer, plus a timed failsafe, plus a CSS failsafe.
const items = [...document.querySelectorAll('[data-rv]')];
const showAll = () => items.forEach(el => el.classList.add('in'));
if (reduce.matches || !('IntersectionObserver' in window)) showAll();
else {
  const io = new IntersectionObserver(entries => {
    for (const en of entries) if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
  }, { rootMargin: '0px 0px -6% 0px', threshold: 0.01 });
  items.forEach(el => io.observe(el));
  setTimeout(showAll, 3000);
}

// Counters
const counters = document.querySelectorAll('[data-count]');
const runCount = el => {
  const target = Number(el.dataset.count) || 0;
  if (reduce.matches || target < 2) { el.textContent = String(target); return; }
  const start = performance.now(), dur = 1200;
  const step = now => { const t = Math.min(1, (now - start) / dur); el.textContent = String(Math.round(target * (1 - Math.pow(1 - t, 3)))); if (t < 1) requestAnimationFrame(step); };
  el.textContent = '0';
  requestAnimationFrame(step);
};
if ('IntersectionObserver' in window) {
  const co = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { runCount(e.target); co.unobserve(e.target); } }), { threshold: 0.5 });
  counters.forEach(el => co.observe(el));
}

// Typed text (85ms type, 45ms delete, 1300ms hold)
const typed = document.querySelector('[data-typed]');
if (typed && !reduce.matches) {
  const words = (typed.dataset.words || '').split('|').filter(Boolean);
  let w = 0, i = words[0] ? words[0].length : 0, deleting = true;
  const tick = () => {
    const word = words[w];
    if (deleting) { i--; if (i <= 0) { deleting = false; w = (w + 1) % words.length; } }
    else { i++; if (i >= words[w].length) { typed.textContent = words[w]; deleting = true; return setTimeout(tick, 1300); } }
    typed.textContent = (deleting ? word : words[w]).slice(0, Math.max(0, i));
    setTimeout(tick, deleting ? 45 : 85);
  };
  if (words.length > 1) setTimeout(tick, 1600);
}

// Particles (particles.js look: dots, link lines, grab on hover, push on click)
function particles(canvas) {
  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  const colors = ['#ffffff', '#8de3ff', '#9fafff'];
  let w = 0, h = 0, dpr = 1, pts = [], mouse = null, raf = 0, visible = true;
  const make = (x, y) => ({ x: x ?? Math.random() * w, y: y ?? Math.random() * h, vx: (Math.random() - .5) * .9, vy: (Math.random() - .5) * .9, r: Math.random() * 2.2 + .8, c: colors[(Math.random() * 3) | 0], a: Math.random() * .4 + .35 });
  const resize = () => {
    const box = canvas.getBoundingClientRect();
    dpr = Math.min(window.devicePixelRatio || 1, 2); w = box.width; h = box.height;
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const n = Math.max(24, Math.min(80, Math.round(w * h / 14000)));
    while (pts.length < n) pts.push(make());
    pts.length = n;
  };
  const frame = () => {
    ctx.clearRect(0, 0, w, h);
    for (const p of pts) {
      p.x += p.vx; p.y += p.vy;
      if (p.x < -10) p.x = w + 10; else if (p.x > w + 10) p.x = -10;
      if (p.y < -10) p.y = h + 10; else if (p.y > h + 10) p.y = -10;
    }
    ctx.lineWidth = 1;
    for (let i = 0; i < pts.length; i++) {
      const a = pts[i];
      for (let j = i + 1; j < pts.length; j++) {
        const b = pts[j], dx = a.x - b.x, dy = a.y - b.y, d = dx * dx + dy * dy;
        if (d < 19600) { ctx.strokeStyle = `rgba(212,227,255,${.28 * (1 - Math.sqrt(d) / 140)})`; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
      }
      if (mouse) {
        const dx = a.x - mouse.x, dy = a.y - mouse.y, d = Math.sqrt(dx * dx + dy * dy);
        if (d < 170) { ctx.strokeStyle = `rgba(141,227,255,${.5 * (1 - d / 170)})`; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke(); }
      }
    }
    for (const p of pts) { ctx.globalAlpha = p.a; ctx.fillStyle = p.c; ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill(); }
    ctx.globalAlpha = 1;
    raf = visible ? requestAnimationFrame(frame) : 0;
  };
  resize();
  if ('ResizeObserver' in window) new ResizeObserver(resize).observe(canvas); else window.addEventListener('resize', resize);
  const host = canvas.closest('.hero') || canvas.parentElement;
  host.addEventListener('pointermove', e => { const b = canvas.getBoundingClientRect(); mouse = { x: e.clientX - b.left, y: e.clientY - b.top }; });
  host.addEventListener('pointerleave', () => { mouse = null; });
  host.addEventListener('click', e => { if (e.target.closest('a,button,input,select')) return; const b = canvas.getBoundingClientRect(); for (let k = 0; k < 4; k++) pts.push(make(e.clientX - b.left, e.clientY - b.top)); if (pts.length > 120) pts.splice(0, pts.length - 120); });
  if ('IntersectionObserver' in window) new IntersectionObserver(es => { visible = es[0].isIntersecting; if (visible && !raf) raf = requestAnimationFrame(frame); }).observe(canvas);
  raf = requestAnimationFrame(frame);
}
if (!reduce.matches) document.querySelectorAll('[data-particles]').forEach(particles);

// Cursor glow (fine pointers only)
const glow = document.querySelector('.cursor-glow');
if (glow && !reduce.matches && window.matchMedia('(pointer: fine)').matches) {
  window.addEventListener('pointermove', e => { glow.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`; glow.classList.add('on'); }, { passive: true });
  document.addEventListener('pointerleave', () => glow.classList.remove('on'));
}

// Enquiry form
const waText = data => `Hello Infinity Vision, I would like to enquire about offline classes in Bhopal.\nName: ${data.name || '-'}\nMobile: ${data.phone || '-'}\nCourse: ${data.course || 'Not sure yet'}\nStarting level: ${data.level || '-'}\nBest time: ${data.preferred_time || '-'}\nMessage: ${data.message || '-'}`;
for (const form of document.querySelectorAll('[data-enquiry-form]')) {
  const source = form.querySelector('[data-source-page]');
  if (source) source.value = location.pathname;
  const error = form.querySelector('[data-form-error]');
  const fields = form.querySelector('[data-form-fields]');
  const status = form.querySelector('[data-form-status]');
  const submit = form.querySelector('[data-submit]');
  const label = form.querySelector('[data-submit-label]');
  const read = () => Object.fromEntries(new FormData(form).entries());
  const fail = (msg, name) => {
    error.textContent = msg; error.hidden = false;
    form.querySelectorAll('[aria-invalid]').forEach(el => el.removeAttribute('aria-invalid'));
    const el = name && form.elements[name];
    if (el) { el.setAttribute('aria-invalid', 'true'); el.focus(); }
  };
  const check = d => {
    if (!d.name || d.name.trim().length < 2) return ['Please enter your name.', 'name'];
    const digits = String(d.phone || '').replace(/[\s\-().+]/g, '').replace(/^(91|0)(?=\d{10}$)/, '');
    if (!/^[6-9]\d{9}$/.test(digits)) return ['Please enter a valid 10-digit Indian mobile number.', 'phone'];
    if (!d.course) return ['Please choose a course.', 'course'];
    if (!d.preferred_time) return ['Please choose a preferred time.', 'preferred_time'];
    if (!d.consent) return ['Please tick the box to agree to be contacted about courses.', 'consent'];
    return null;
  };
  form.querySelector('[data-wa-fallback]')?.addEventListener('click', () => {
    window.open(`https://wa.me/${WA}?text=${encodeURIComponent(waText(read()))}`, '_blank', 'noopener');
  });
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const data = read();
    const bad = check(data);
    if (bad) return fail(bad[0], bad[1]);
    error.hidden = true;
    submit.disabled = true; label.textContent = 'Sending…';
    try {
      const res = await fetch("/api/enquiry", { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(data) });
      const out = await res.json().catch(() => ({}));
      if (!res.ok || !out.ok) {
        const name = out.fields ? Object.keys(out.fields)[0] : null;
        fail(out.error || 'Your enquiry was not sent. Please try again or use WhatsApp.', name);
      } else {
        fields.hidden = true; status.hidden = false; status.focus();
      }
    } catch {
      fail('No connection. Please try again, or tap “Send on WhatsApp”.');
    } finally {
      submit.disabled = false; label.textContent = 'Send enquiry';
    }
  });
}
