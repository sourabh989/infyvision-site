/* Infinity Vision V3 — progressive enhancements. No analytics, no data collection, no network calls. */
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const motionAllowed = () => !reducedMotion.matches;
const finePointer = () => window.matchMedia('(hover: hover) and (pointer: fine)').matches;

function setupNavigation() {
  const toggle = $('.menu-toggle');
  const nav = $('#navigation');
  if (!toggle || !nav) return;
  const setOpen = open => { toggle.setAttribute('aria-expanded', String(open)); nav.classList.toggle('is-open', open); };
  toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
  nav.addEventListener('click', event => { if (event.target.closest('a')) setOpen(false); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') { setOpen(false); toggle.focus(); }
  });
  document.addEventListener('click', event => { if (!event.target.closest('.site-header')) setOpen(false); });
  window.matchMedia('(min-width: 901px)').addEventListener?.('change', () => setOpen(false));
  let lastY = window.scrollY;
  window.addEventListener('scroll', () => { if (Math.abs(window.scrollY - lastY) > 120 && toggle.getAttribute('aria-expanded') === 'true') setOpen(false); }, { passive: true });
  toggle.addEventListener('click', () => { lastY = window.scrollY; });
  toggle.hidden = false;
  document.documentElement.classList.add('nav-enhanced');
}

function pop(element, delay = 0) {
  if (!motionAllowed() || !element.animate) return;
  element.animate([{ opacity: 0, transform: 'translateY(14px) scale(.98)' }, { opacity: 1, transform: 'none' }], { duration: 480, delay, easing: 'cubic-bezier(.2,.7,.2,1)', fill: 'backwards' });
}

function setupReveals() {
  const items = $$('[data-reveal]');
  if (!('IntersectionObserver' in window) || !motionAllowed()) { items.forEach(el => el.classList.add('is-in')); return; }
  document.documentElement.classList.add('js-motion');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-in');
      $$('.draw', entry.target).forEach(path => path.classList.add('is-in'));
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  items.forEach(element => observer.observe(element));
  // Safety net: never leave content hidden.
  setTimeout(() => items.forEach(el => { const r = el.getBoundingClientRect(); if (r.top < innerHeight) el.classList.add('is-in'); }), 1800);
  reducedMotion.addEventListener?.('change', event => {
    if (event.matches) { observer.disconnect(); items.forEach(el => el.classList.add('is-in')); document.documentElement.classList.remove('js-motion'); }
  });
}

/* Particle network: cursor-reactive, linked nodes, click to add.
   The canvas follows its container's CSS box (ResizeObserver), never the window, and its bitmap is always
   cssSize x devicePixelRatio (capped at 2) so it is never stretched. Dot size, speed and link distance are in CSS px. */
function particleField(canvas) {
  const ctx = canvas.getContext && canvas.getContext('2d');
  if (!ctx) return null;
  const host = canvas.parentElement;
  const colours = ['255,255,255', '141,227,255', '170,160,255'];
  const cap = Number(canvas.dataset.count) || 80;
  const EDGE = 24, MAX_POINTS = 220;
  let w = 0, h = 0, dpr = 1, points = [], raf = 0, running = false, redistTimer = 0, pending = null;
  const mouse = { x: -9999, y: -9999 };
  const targetCount = () => {
    const perDot = w < 640 ? 9000 : 13000; // CSS px² per dot: phones stay airy but not empty
    return Math.max(18, Math.min(cap, Math.round((w * h) / perDot)));
  };
  const makePoint = (x, y, speed = .5) => ({ x, y, vx: (Math.random() - .5) * speed, vy: (Math.random() - .5) * speed, r: Math.random() * 1.5 + .9, c: colours[(Math.random() * 3) | 0] });
  const seed = () => { points = Array.from({ length: targetCount() }, () => makePoint(Math.random() * w, Math.random() * h)); };
  // Spread the existing dots over the new box (positions only; dots keep their CSS px size) and top up / trim by area.
  const redistribute = (ow, oh) => {
    const sx = w / ow, sy = h / oh;
    points.forEach(p => { p.x *= sx; p.y *= sy; });
    const n = targetCount();
    while (points.length < n) points.push(makePoint(Math.random() * w, Math.random() * h));
    if (points.length > n) points.length = n;
  };
  const step = () => {
    for (const p of points) {
      p.x += p.vx; p.y += p.vy;
      if (p.x < -EDGE) p.x = w + EDGE; else if (p.x > w + EDGE) p.x = -EDGE;
      if (p.y < -EDGE) p.y = h + EDGE; else if (p.y > h + EDGE) p.y = -EDGE;
      const dx = p.x - mouse.x, dy = p.y - mouse.y, d = Math.hypot(dx, dy);
      if (d < 120 && d > 0) { p.x += dx / d * 1.2; p.y += dy / d * 1.2; }
    }
  };
  const draw = () => {
    ctx.clearRect(0, 0, w, h);
    const link = w < 640 ? 105 : 145;
    for (let i = 0; i < points.length; i++) {
      const a = points[i];
      for (let j = i + 1; j < points.length; j++) {
        const b = points[j], d = Math.hypot(a.x - b.x, a.y - b.y);
        if (d < link) { ctx.strokeStyle = `rgba(190,215,255,${(1 - d / link) * .32})`; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
      }
      const md = Math.hypot(a.x - mouse.x, a.y - mouse.y);
      if (md < 190) { ctx.strokeStyle = `rgba(92,225,255,${(1 - md / 190) * .7})`; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke(); }
      ctx.fillStyle = `rgba(${a.c},.85)`; ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, Math.PI * 2); ctx.fill();
    }
  };
  const frame = () => { step(); draw(); raf = running ? requestAnimationFrame(frame) : 0; };
  // Match the bitmap to the container's layout size (clientWidth/Height ignore transforms, so no parent scale leaks in).
  const fit = () => {
    const nw = host.clientWidth, nh = host.clientHeight, nd = Math.min(window.devicePixelRatio || 1, 2);
    if (!nw || !nh || (nw === w && nh === h && nd === dpr)) return;
    const ow = w, oh = h;
    w = nw; h = nh; dpr = nd;
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    ctx.setTransform(canvas.width / w, 0, 0, canvas.height / h, 0, 0);
    if (!ow || !points.length) seed();
    else if (Math.abs(w - ow) > 1 || Math.abs(h - oh) > 120) {
      // Real layout change (rotation, window resize): debounce the respread so dragging a window doesn't churn.
      // Positions are respread against the size they were laid out for, so chained resizes stay consistent.
      clearTimeout(redistTimer);
      if (!pending) pending = { w: ow, h: oh };
      const run = () => { redistTimer = 0; if (pending) { redistribute(pending.w, pending.h); pending = null; } };
      if (Math.abs(w - pending.w) > pending.w * .25) run(); else redistTimer = setTimeout(run, 180);
    }
    // Small height-only changes (mobile address bar, text reflow) keep every dot where it is; edge wrap handles the rest.
    draw(); // resizing clears the bitmap: repaint now so there is no blank frame
  };
  if ('ResizeObserver' in window) new ResizeObserver(() => fit()).observe(host);
  let resizeTimer;
  window.addEventListener('resize', () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(fit, 120); });
  // Browser zoom or moving to another screen changes devicePixelRatio without a size change.
  const watchDpr = () => {
    if (!window.matchMedia) return;
    const mq = matchMedia(`(resolution: ${window.devicePixelRatio || 1}dppx)`);
    const on = () => { fit(); watchDpr(); };
    mq.addEventListener ? mq.addEventListener('change', on, { once: true }) : mq.addListener?.(on);
  };
  watchDpr();
  const section = canvas.closest('section');
  const toLocal = e => { const r = canvas.getBoundingClientRect(); return { x: (e.clientX - r.left) * (w / (r.width || w)), y: (e.clientY - r.top) * (h / (r.height || h)) }; };
  section.addEventListener('pointermove', e => { if (e.pointerType === 'touch') return; const q = toLocal(e); mouse.x = q.x; mouse.y = q.y; });
  section.addEventListener('pointerleave', () => { mouse.x = mouse.y = -9999; });
  section.addEventListener('click', e => {
    if (e.target.closest('a,button,input,select,label,summary')) return;
    const q = toLocal(e);
    for (let k = 0; k < 4; k++) points.push({ ...makePoint(q.x, q.y, 1.4), c: colours[k % 3] });
    if (points.length > MAX_POINTS) points.splice(0, 4);
  });
  fit();
  return {
    start() { running = true; if (!raf) raf = requestAnimationFrame(frame); },
    stop() { running = false; cancelAnimationFrame(raf); raf = 0; },
    still() { running = false; cancelAnimationFrame(raf); raf = 0; draw(); }
  };
}

function setupHeroMotion() {
  const hero = $('.hero');
  if (!hero) return;
  const canvas = $('.particles', hero);
  let field = null;
  try { field = canvas ? particleField(canvas) : null; } catch (e) { field = null; }
  let manuallyPaused = false, inView = true;
  const control = document.createElement('button');
  control.type = 'button'; control.className = 'motion-control'; control.setAttribute('aria-pressed', 'false');
  (hero.querySelector('.marquee-band') || hero).append(control);
  const update = () => {
    const enabled = motionAllowed();
    const paused = manuallyPaused || !inView || document.hidden;
    hero.classList.toggle('motion-active', enabled);
    hero.classList.toggle('motion-paused', !enabled || paused);
    control.hidden = !enabled;
    control.innerHTML = manuallyPaused
      ? '<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>'
      : '<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true" focusable="false"><path d="M7 5h4v14H7zM13 5h4v14h-4z" fill="currentColor"/></svg>';
    control.title = manuallyPaused ? 'Resume background motion' : 'Pause background motion';
    control.setAttribute('aria-pressed', String(manuallyPaused));
    control.setAttribute('aria-label', (manuallyPaused ? 'Resume' : 'Pause') + ' decorative background motion');
    if (field) { if (enabled && !paused) field.start(); else if (!enabled) field.still(); else field.stop(); }
    typer && (enabled && !manuallyPaused ? typer.play() : typer.pause());
  };
  const typer = setupTyped(hero);
  control.addEventListener('click', () => { manuallyPaused = !manuallyPaused; update(); });
  reducedMotion.addEventListener?.('change', update);
  document.addEventListener('visibilitychange', update);
  if ('IntersectionObserver' in window) new IntersectionObserver(entries => { inView = entries[0].isIntersecting; update(); }, { threshold: 0 }).observe(hero);
  update();
}

function setupTyped(root) {
  const el = $('.typed', root);
  if (!el) return null;
  const words = (el.dataset.words || '').split('|').filter(Boolean);
  if (words.length < 2) return null;
  let wi = 0, ci = words[0].length, deleting = false, timer = 0, playing = false;
  const tick = () => {
    const word = words[wi];
    if (!deleting) {
      ci++; el.textContent = word.slice(0, ci);
      if (ci >= word.length) { deleting = true; timer = setTimeout(tick, 1700); return; }
      timer = setTimeout(tick, 80);
    } else {
      ci--; el.textContent = word.slice(0, Math.max(ci, 0));
      if (ci <= 0) { deleting = false; wi = (wi + 1) % words.length; timer = setTimeout(tick, 260); return; }
      timer = setTimeout(tick, 42);
    }
  };
  return {
    play() { if (playing) return; playing = true; ci = el.textContent.length; deleting = ci >= words[wi].length; timer = setTimeout(tick, 1400); },
    pause() { playing = false; clearTimeout(timer); }
  };
}

function setupCounters() {
  const nums = $$('[data-count]');
  if (!nums.length || !('IntersectionObserver' in window) || !motionAllowed()) return;
  const io = new IntersectionObserver(entries => entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    io.unobserve(entry.target);
    const el = entry.target, target = Number(el.dataset.count), t0 = performance.now(), dur = 1400;
    const step = now => { const k = Math.min(1, (now - t0) / dur); el.textContent = String(Math.round(target * (1 - Math.pow(1 - k, 3)))); if (k < 1) requestAnimationFrame(step); };
    el.textContent = '0'; requestAnimationFrame(step);
  }), { threshold: .5 });
  nums.forEach(n => io.observe(n));
}

function setupTilt() {
  if (!finePointer()) return;
  $$('.tilt').forEach(card => {
    let raf = 0;
    card.addEventListener('pointermove', e => {
      const r = card.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      card.style.setProperty('--mx', (x * 100) + '%'); card.style.setProperty('--my', (y * 100) + '%');
      if (!motionAllowed()) return;
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => { card.style.transform = `perspective(900px) rotateX(${(.5 - y) * 6}deg) rotateY(${(x - .5) * 7}deg) translateY(-8px)`; });
    });
    card.addEventListener('pointerleave', () => { cancelAnimationFrame(raf); card.style.transform = ''; });
  });
}

function setupCursorGlow() {
  const glow = $('.cursor-glow');
  if (!glow || !finePointer() || !motionAllowed()) return;
  let x = 0, y = 0, queued = false;
  window.addEventListener('pointermove', e => {
    x = e.clientX; y = e.clientY;
    if (!queued) { queued = true; requestAnimationFrame(() => { glow.style.transform = `translate(${x}px,${y}px)`; queued = false; }); }
    document.documentElement.classList.add('has-glow');
  }, { passive: true });
}

function setupScrollEffects() {
  const header = $('.site-header');
  const parallax = $$('[data-parallax]');
  const journey = $('[data-progress]');
  const spyLinks = $$('.nav-link[data-spy]');
  const onHome = !!$('#top');
  const sections = onHome ? spyLinks.map(a => document.getElementById(a.dataset.spy)).filter(Boolean) : [];
  let queued = false, maxP = 0;
  const update = () => {
    queued = false;
    const y = window.scrollY;
    header && header.classList.toggle('is-scrolled', y > 30);
    if (motionAllowed()) parallax.forEach(el => { const r = el.parentElement.getBoundingClientRect(); el.style.translate = `0 ${(r.top + r.height / 2 - innerHeight / 2) * Number(el.dataset.parallax) * -1}px`; });
    if (journey) {
      const r = journey.getBoundingClientRect();
      maxP = motionAllowed() ? Math.max(maxP, Math.max(0, Math.min(1, (innerHeight * .75 - r.top) / (r.height || 1)))) : 1;
      const p = maxP;
      journey.style.setProperty('--p', p.toFixed(3));
    }
    if (sections.length) {
      let current = '';
      sections.forEach(s => { if (s.getBoundingClientRect().top < innerHeight * .35) current = s.id; });
      spyLinks.forEach(a => a.classList.toggle('is-active', a.dataset.spy === current));
    }
  };
  window.addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(update); } }, { passive: true });
  window.addEventListener('resize', update);
  update();
  // Expose the un-collapsed header height (preview strip + nav row) so the first view can fit below it exactly.
  const strip = header && $('.preview-strip', header), nav = header && $('.nav-row', header);
  if (strip && nav) {
    const setHdr = () => {
      const cs = getComputedStyle(strip);
      const text = strip.scrollHeight - (parseFloat(cs.paddingTop) || 0) - (parseFloat(cs.paddingBottom) || 0);
      document.documentElement.style.setProperty('--hdr', Math.ceil(nav.offsetHeight + text + 10) + 'px');
    };
    setHdr();
    window.addEventListener('resize', setHdr);
    document.fonts?.ready?.then(setHdr);
  }
}

function setupCourseFilters() {
  const controls = $('.filter-controls');
  const groups = $$('[data-group]');
  const status = $('#filter-status');
  if (!controls || !groups.length) return;
  const buttons = $$('[data-filter]', controls);
  const apply = button => {
    const filter = button.dataset.filter;
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    let count = 0;
    groups.forEach(group => {
      group.hidden = filter !== 'all' && group.dataset.group !== filter;
      if (!group.hidden) $$('.course-card', group).forEach(card => { card.classList.add('is-in'); pop(card, Math.min(count, 8) * 50); count++; });
    });
    if (status) status.textContent = `${count} ${count === 1 ? 'course' : 'courses'} shown.`;
  };
  buttons.forEach(button => button.addEventListener('click', () => apply(button)));
  controls.hidden = false;
}

function setupDetailsLinks() {
  const openTarget = hash => {
    const target = hash && document.getElementById(hash.slice(1));
    if (target && target.tagName === 'DETAILS') { target.open = true; target.classList.add('is-in'); }
  };
  $$('[data-open-details]').forEach(link => link.addEventListener('click', () => openTarget(link.getAttribute('href'))));
  openTarget(location.hash);
}

function setupDetailsFeedback() {
  $$('details').forEach(details => details.addEventListener('toggle', () => {
    if (!details.open || !motionAllowed()) return;
    const content = [...details.children].find(child => child.tagName !== 'SUMMARY');
    if (content?.animate) content.animate([{ opacity: 0, transform: 'translateY(-6px)' }, { opacity: 1, transform: 'none' }], { duration: 260, easing: 'ease-out' });
  }));
}

const WA_NUMBER = '919098372445';
function normalisePhone(raw) {
  let d = String(raw || '').replace(/[\s\-().]/g, '');
  if (d.startsWith('+')) d = d.slice(1);
  if (d.length === 12 && d.startsWith('91')) d = d.slice(2);
  else if (d.length === 11 && d.startsWith('0')) d = d.slice(1);
  return /^[6-9]\d{9}$/.test(d) ? d : '';
}

function enquiryMessage(form) {
  const get = name => (form.elements[name]?.value || '').trim();
  return ['Hello Infinity Vision, I would like to enquire about offline classes in Bhopal.', get('name') && `Name: ${get('name')}`, get('phone') && `Mobile: ${get('phone')}`, get('course') && `Course: ${get('course')}`, get('level') && `My level: ${get('level')}`, get('preferred_time') && `Preferred time: ${get('preferred_time')}`, get('message') && `Message: ${get('message')}`].filter(Boolean).join('\n');
}

function openWhatsApp(form) {
  const url = `https://wa.me/${WA_NUMBER}?text=` + encodeURIComponent(enquiryMessage(form));
  const win = window.open(url, '_blank', 'noopener');
  if (!win) location.href = url;
}

function setupEnquiryForm() {
  $$('[data-enquiry-form]').forEach(form => {
    const source = form.querySelector('[data-source-page]');
    if (source) source.value = location.pathname;
    const fields = form.querySelector('[data-form-fields]');
    const status = form.querySelector('[data-form-status]');
    const button = form.querySelector('[data-submit]');
    const label = form.querySelector('[data-submit-label]');
    const fallback = form.querySelector('[data-wa-fallback]');
    const showStatus = (kind, title, text) => {
      status.hidden = false; status.dataset.state = kind;
      status.querySelector('[data-status-title]').textContent = title;
      status.querySelector('[data-status-text]').textContent = text;
      form.classList.toggle('is-sent', kind === 'success');
      form.classList.toggle('is-error', kind === 'error');
      if (status.animate && !matchMedia('(prefers-reduced-motion: reduce)').matches) status.animate([{ opacity: 0, transform: 'translateY(8px)' }, { opacity: 1, transform: 'none' }], { duration: 320, easing: 'ease-out' });
      status.focus?.({ preventScroll: true });
    };
    const fieldError = (el, msg) => { el.setCustomValidity?.(msg); el.setAttribute('aria-invalid', msg ? 'true' : 'false'); };
    fallback?.addEventListener('click', () => openWhatsApp(form));
    form.addEventListener('submit', async event => {
      event.preventDefault();
      const nameEl = form.elements.name, phoneEl = form.elements.phone;
      const name = nameEl.value.trim(), phone = normalisePhone(phoneEl.value);
      fieldError(nameEl, name.length >= 2 ? '' : 'Please enter your name.');
      fieldError(phoneEl, phone ? '' : 'Please enter a valid 10-digit Indian mobile number.');
      if (name.length < 2 || !phone) {
        showStatus('error', 'Please check your details', name.length < 2 ? 'Please enter your name.' : 'Please enter a valid 10-digit Indian mobile number, for example 98765 43210.');
        (name.length < 2 ? nameEl : phoneEl).focus();
        return;
      }
      const data = Object.fromEntries(new FormData(form).entries());
      data.phone = phone;
      button.disabled = true; label.textContent = 'Sending…'; form.classList.add('is-busy');
      try {
        const res = await fetch('/api/enquiry', { method: 'POST', headers: { 'content-type': 'application/json', accept: 'application/json' }, body: JSON.stringify(data) });
        const body = await res.json().catch(() => ({}));
        if (!res.ok || !body.ok) throw new Error(body.error || 'We could not save your enquiry right now.');
        fields.hidden = true;
        showStatus('success', `Thank you, ${name.split(' ')[0]}!`, `We have received your enquiry and will call you on ${phone.slice(0, 5)} ${phone.slice(5)}. For a faster reply, you can also send it on WhatsApp.`);
      } catch (err) {
        showStatus('error', 'Your enquiry was not sent', `${err.message} Please send it on WhatsApp instead, or call 9098372445.`);
      } finally {
        button.disabled = false; label.textContent = 'Send enquiry'; form.classList.remove('is-busy');
      }
    });
  });
}

const RECOMMENDATIONS = {
  reporting: {
    starter: ['Advanced Excel', 'New to reporting? Start with Advanced Excel, or ask about the Excel Reporting Clinic mini-course (in development). Ask about the next batch.', 'excel', 'Short course · Enquire for next batch'],
    experienced: ['Data Analytics', 'Ready to go beyond spreadsheets? Data Analytics adds Power Query, SQL, Power BI, dashboards and business case projects. It is a new course: ask about the next batch.', 'data-analytics', 'New course · Enquire for next batch']
  },
  marketing: {
    starter: ['Performance Marketing & Analytics', 'Learn Google Ads, Meta Ads, SEO and social basics, then how to track results with GA4. Ask which practice accounts are used; ad spend is not assumed.', 'performance-marketing', 'New modules · Enquire for next batch'],
    experienced: ['Performance Marketing & Analytics', 'Already running ads? Focus on the new modules: bidding strategies, GTM, Meta Pixel, conversion tracking, A/B tests and reporting dashboards.', 'performance-marketing', 'New modules · Enquire for next batch']
  },
  web: {
    starter: ['Web & App Development (Full Stack)', 'Start with HTML, CSS and JavaScript, then move to React, Node and Express, databases and APIs. Ask about device requirements.', 'full-stack', 'New modules · Enquire for next batch'],
    experienced: ['Web & App Development (Full Stack)', 'Know the front-end basics? Discuss joining for the new back-end, API, Git, deployment and mobile app introduction modules.', 'full-stack', 'New modules · Enquire for next batch']
  },
  accounting: {
    starter: ['Tally with US GAAP & IFRS', 'Learn Tally Prime accounting, GST, inventory, payroll and financial statements, plus new US GAAP and IFRS fundamentals.', 'tally-gaap-ifrs', 'New modules · Enquire for next batch'],
    experienced: ['Tally with US GAAP & IFRS', 'Already use Tally? Ask about the new US GAAP and IFRS fundamentals modules used by international and KPO firms. They are not a professional qualification.', 'tally-gaap-ifrs', 'New modules · Enquire for next batch']
  }
};
function setupCourseFinder() {
  const controls = $('.finder-controls');
  const result = $('#finder-result');
  if (!controls || !result) return;
  const update = () => {
    const goal = $$('input[name="goal"]', controls).find(input => input.checked)?.value || 'reporting';
    const level = $$('input[name="level"]', controls).find(input => input.checked)?.value || 'starter';
    const [name, description, slug, statusLabel] = RECOMMENDATIONS[goal][level];
    // Only developer-authored constant strings enter this fragment; user values never become HTML.
    result.innerHTML = `<span class="micro">A STARTING POINT TO DISCUSS</span><h3>${name}</h3><span class="result-status">${statusLabel}</span><p>${description}</p><a class="text-link" href="courses/${slug}/index.html">View syllabus <span aria-hidden="true">↗</span></a>`;
    pop(result);
  };
  controls.addEventListener('change', update);
  controls.hidden = false;
  update();
}
// Independent enhancements: a failure in one decorative feature must not disable content or navigation.
[setupNavigation, setupReveals, setupCourseFilters, setupCourseFinder, setupHeroMotion, setupCounters, setupTilt, setupCursorGlow, setupScrollEffects, setupDetailsLinks, setupDetailsFeedback, setupEnquiryForm].forEach(setup => {
  try { setup(); } catch (error) { console.warn('Optional website enhancement unavailable:', setup.name, error); }
});
