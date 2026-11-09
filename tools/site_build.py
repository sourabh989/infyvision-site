"""Infinity Vision V5 generator: fresh front-end in the live infyvision.xyz style (blue/violet glass,
particles, typed text, reveals, counters), upgraded. Content: courses_v4.py + content.py."""
import sys, json, shutil
from pathlib import Path
from urllib.parse import quote
sys.path.insert(0, str(Path(__file__).resolve().parent))
from content import E, clean_html, MINIS, CAREER  # noqa
from courses_v4 import COURSES, MAIN, REDIRECTS, FAQ

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'site'
shutil.rmtree(OUT, ignore_errors=True)
(OUT / 'assets').mkdir(parents=True)

PHONE = '9098372445'
TEL = 'tel:+919098372445'
ADDRESS = 'E-2, 359 Arera Colony Bhopal'
MAP_Q = 'E-2, 359 Arera Colony, Bhopal, Madhya Pradesh'
MAP_EMBED = 'https://www.google.com/maps?q=' + quote(MAP_Q) + '&output=embed'
MAP_LINK = 'https://www.google.com/maps/search/?api=1&query=' + quote(MAP_Q)
TOOLS_NOTE = 'Tools across our current courses and the proposed analytics programmes. SQL, Power BI, DAX, GA4 and UTM work belong to programmes in development.'
TOOLS = ['Advanced Excel', 'Pivot Tables', 'Power Query', 'Dashboards', 'Tally ERP', 'GST billing', 'Inventory', 'Payroll', 'SQL', 'Power BI', 'DAX', 'GA4', 'UTM tracking', 'SEO', 'Google Ads', 'Meta Ads', 'Social media', 'HTML', 'CSS', 'JavaScript', 'Responsive design']
TIMES = ['Weekday morning', 'Weekday afternoon', 'Weekday evening', 'Weekend', 'Any time, please call me']
LEVELS = ['Complete beginner', 'I know the basics', 'Working professional', 'Business owner']
COURSE_OPTIONS = [(c['name'], c['name'] + (' (new)' if c['new'] else '')) for c in COURSES] + [(m[0], m[0] + ' (in development)') for m in MINIS] + [('Not sure yet', 'Not sure yet, please guide me')]

P = {
 'infinity': '<path d="M12 12C8 4 2 7 2 12s6 8 10 0 10-5 10 0-6 8-10 0Z"/>',
 'arrow': '<path d="M5 12h14m-6-6 6 6-6 6"/>',
 'sheet': '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M4 9h16M4 15h16M10 9v12"/>',
 'ledger': '<path d="M5 3h14v18l-3-2-4 2-4-2-3 2V3ZM9 8h6M9 12h6"/>',
 'code': '<path d="m8 6-6 6 6 6m8-12 6 6-6 6m-3-16-2 20"/>',
 'target': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
 'chart': '<path d="M3 3v18h18M7 16v-5m5 5V7m5 9V4"/>',
 'pin': '<path d="M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="10" r="2.5"/>',
 'check': '<path d="m5 12 4 4L19 6"/>',
 'phone': '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2Z"/>',
 'chat': '<path d="M20 12a8 8 0 0 1-11.6 7.1L4 20l1-4.2A8 8 0 1 1 20 12Z"/>',
 'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6"/>',
 'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'file': '<path d="M14 3H6v18h12V7l-4-4Z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
 'brief': '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V4h6v3M3 12h18"/>',
 'mic': '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
 'folder': '<path d="M3 6h6l2 2h10v11H3z"/><path d="m9 14 2 2 4-4"/>',
 'hand': '<path d="M7 11V5a1.5 1.5 0 0 1 3 0v5m0-1V3.5a1.5 1.5 0 0 1 3 0V10m0-5a1.5 1.5 0 0 1 3 0v5m0-2a1.5 1.5 0 0 1 3 0v6a7 7 0 0 1-7 7h-1a7 7 0 0 1-6-3.4L3 14a1.5 1.5 0 0 1 2.5-1.6L7 14"/>',
 'eye': '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
 'map': '<path d="m9 4-6 2v14l6-2 6 2 6-2V4l-6 2-6-2Zm0 0v14m6-12v14"/>',
 'send': '<path d="m3 11 18-8-8 18-2-8-8-2Z"/>',
 'board': '<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M12 16v4m-4 0h8M7 12l3-3 2 2 4-4"/>',
 'cap': '<path d="m2 9 10-5 10 5-10 5L2 9Z"/><path d="M6 11v5c3 2 9 2 12 0v-5M22 9v6"/>',
 'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
 'star': '<path d="m12 3 2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.4 6.7 19.4l1.2-6L3.4 9.3l6-.7L12 3Z"/>',
 'flask': '<path d="M9 3h6M10 3v6L4.5 18.5A1.7 1.7 0 0 0 6 21h12a1.7 1.7 0 0 0 1.5-2.5L14 9V3"/><path d="M7 15h10"/>',
 'quote': '<path d="M9 7H5v6h4v-2a4 4 0 0 1-4 4m14-8h-4v6h4v-2a4 4 0 0 1-4 4"/>',
}
def icon(kind, cls='ic'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[kind]}</svg>'
WA_SVG = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.8-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.2-.2-.5-.3Z"/></svg>'

def wa_href(context):
    return 'https://wa.me/919098372445?text=' + quote('Hello Infinity Vision, I would like to ask about ' + context + '. Please help me understand the next step for offline classes in Bhopal.')
def wa_btn(label, context, cls='btn btn-wa'):
    return f'<a class="{cls}" href="{wa_href(context)}" target="_blank" rel="noopener noreferrer">{WA_SVG}<span>{E(label)}</span><span class="sr-only"> (opens WhatsApp in a new tab)</span></a>'
def call_btn(cls='btn btn-ghost'):
    return f'<a class="{cls}" href="{TEL}">{icon("phone")}<span>Call&nbsp;{PHONE}</span></a>'

GRADS = {'g-blue': 'grad-blue', 'g-violet': 'grad-violet', 'g-cyan': 'grad-cyan', 'g-pink': 'grad-pink', 'g-green': 'grad-green'}

def head(title, desc, path):
    return f'''<!DOCTYPE html><html lang="en-IN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#0b1122"><title>{E(title)}</title><link rel="icon" href="/assets/mark.svg" type="image/svg+xml"><link rel="preload" href="/assets/poppins-600.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/assets/site.css"><script defer src="/assets/site.js"></script></head><body data-page="{E(path)}"><a class="skip" href="#main">Skip to content</a><div class="cursor-glow" aria-hidden="true"></div>'''

NAV = [('Courses', '/#courses'), ('Why offline', '/#why-offline'), ('Career support', '/#career'), ('FAQ', '/#faq'), ('Contact', '/#contact')]
def header():
    links = ''.join(f'<li><a href="{h}">{E(t)}</a></li>' for t, h in NAV)
    return f'''<header class="nav" data-nav><div class="wrap nav-in"><a class="brand" href="/" aria-label="Infinity Vision home"><img src="/assets/mark.svg" alt="" width="36" height="36"><span>Infinity <b>Vision</b></span></a><nav aria-label="Main" id="site-nav" class="nav-links"><ul>{links}</ul><a class="btn btn-glow btn-sm nav-call" href="{TEL}">{icon("phone")}<span>Call&nbsp;{PHONE}</span></a></nav><button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav" data-menu>{icon("menu")}<span class="sr-only">Menu</span></button></div></header>'''

def footer():
    clinks = ''.join(f'<li><a href="/courses/{c["slug"]}/">{E(c["name"])}</a></li>' for c in COURSES)
    return f'''<footer class="footer"><div class="wrap foot-grid"><div><a class="brand" href="/"><img src="/assets/mark.svg" alt="" width="36" height="36"><span>Infinity <b>Vision</b></span></a><p>Offline, practical, career-focused training in Bhopal. Classes run only in person at our centre.</p><p class="foot-note">Career support includes CV help, LinkedIn &amp; Naukri profiles, mock interviews, portfolio building and placement assistance. Employment is not guaranteed.</p></div><div><h2>Courses</h2><ul>{clinks}</ul></div><div><h2>Quick links</h2><ul>{''.join(f'<li><a href="{h}">{E(t)}</a></li>' for t, h in NAV)}</ul></div><div><h2>Visit us</h2><address>{ADDRESS}</address><p><a href="{TEL}">Call&nbsp;{PHONE}</a><br><a href="{wa_href('courses')}" target="_blank" rel="noopener noreferrer">WhatsApp&nbsp;{PHONE}<span class="sr-only"> (opens WhatsApp in a new tab)</span></a></p></div></div><div class="wrap foot-base"><span>© 2026 Infinity Vision, Bhopal.</span><span>Fees, timings and batch dates: please ask us. <span class="preview-tag">Preview build</span></span></div></footer><a class="wa-fab" href="{wa_href('courses')}" target="_blank" rel="noopener noreferrer" aria-label="Chat on WhatsApp with 9098372445 (opens in a new tab)">{WA_SVG}</a></body></html>'''

def particles():
    return '<div class="hero-bg" aria-hidden="true"><canvas class="particles" data-particles></canvas><span class="shape s1"></span><span class="shape s2"></span><span class="shape s3"></span></div>'

def tools_strip():
    row = ''.join(f'<li>{E(t)}</li>' for t in TOOLS)
    return f'''<section class="tools" aria-label="Tools across current and proposed pathways"><div class="tools-mask"><ul class="tools-track">{row}</ul><ul class="tools-track" aria-hidden="true">{row}</ul></div><p class="tools-note">{TOOLS_NOTE}</p></section>'''

def sec_head(kicker, title, sub='', center=True):
    return f'''<div class="sec-head{' center' if center else ''}" data-rv><p class="kicker">{E(kicker)}</p><h2>{title}</h2>{f'<p class="sub">{sub}</p>' if sub else ''}</div>'''

def badge(c):
    if c['newness'] == 'new': return '<span class="badge badge-new">New course</span>'
    if c['newness'] == 'expanded': return '<span class="badge badge-exp">Expanded course</span>'
    return '<span class="badge badge-short">Short course</span>'

def course_card(c, i):
    chips = ''.join(f'<li>{E(t)}</li>' for t in c['tools'])
    roles = ', '.join(E(r) for r in c['roles'])
    return f'''<article class="card course-card" id="{c['slug']}" data-course-card data-rv style="--d:{i*70}ms"><div class="cc-top"><span class="ic-tile {GRADS[c['grad']]}">{icon(c['ic'])}</span>{badge(c)}</div><h3><a href="/courses/{c['slug']}/">{E(c['name'])}</a></h3><p class="tagline">{E(c['tagline'])}</p><p class="mini-label">Key topics</p><ul class="chips">{chips}</ul><p class="mini-label">Roles this prepares you for</p><p class="roles">{roles}</p><div class="cc-actions">{wa_btn('Enquire on WhatsApp', c['name'], 'btn btn-wa btn-sm')}<a class="btn btn-line btn-sm" href="/courses/{c['slug']}/"><span>View syllabus</span>{icon("arrow")}</a></div></article>'''

def mini_card(m, i):
    name, num, tag, who, practice, output, note, ic = m
    return f'''<article class="card mini-card" data-rv style="--d:{i*70}ms"><div class="cc-top"><span class="num">{num}</span><span class="badge badge-dev">In development</span></div><h3>{E(name)}</h3><p class="tagline">{E(tag)}</p><p class="small">{E(practice)}</p><p class="small muted">{E(note)}</p>{wa_btn('Register interest', name + ' (in development)', 'btn btn-wa btn-sm')}</article>'''

def courses_section():
    excel = next(c for c in COURSES if c['slug'] == 'excel')
    return f'''<section class="section" id="courses"><div class="wrap">{sec_head('OUR COURSES', 'Choose your <span class="grad-text">career path</span>', 'Four main courses, taught offline in our Bhopal classroom. Every course shows its key topics and the roles it prepares you for. Ask us about the next batch.')}<div class="grid-courses">{''.join(course_card(c, i) for i, c in enumerate(MAIN))}</div><div class="sub-block"><h3 class="block-title" data-rv>Short course</h3><div class="grid-courses">{course_card(excel, 0)}<div class="card note-card" data-rv><span class="ic-tile grad-violet">{icon("flask")}</span><h3>Mini-courses in development</h3><p>Four short, focused courses are being prepared. Launch details and enrolment are not announced yet. You can ask about their scope and register interest on WhatsApp.</p><a class="btn btn-line btn-sm" href="#mini-courses"><span>See mini-courses</span>{icon("arrow")}</a></div></div></div><div class="sub-block" id="mini-courses"><h3 class="block-title" data-rv>Mini-courses <span class="badge badge-dev">In development</span></h3><div class="grid-minis">{''.join(mini_card(m, i) for i, m in enumerate(MINIS))}</div></div></div></section>'''

OFFLINE = [('chat', 'Doubts cleared face to face', 'Ask when you are stuck, see it solved on screen, try it yourself straight away.'), ('users', 'Learn alongside others', 'Classmates keep you going, and explaining work out loud builds confidence.'), ('clock', 'A routine you will keep', 'A set class time and place makes it easier to finish what you start.'), ('eye', 'Visit before you decide', 'See the centre and talk to us in person before choosing a course.'), ('board', 'Practical, hands-on sessions', 'Work on real tools in class, with a trainer checking your work as you go.'), ('brief', 'Career support in person', 'CV help, LinkedIn and Naukri profiles, mock interviews, portfolio building and placement assistance, face to face.')]
def why_section():
    tiles = ''.join(f'<div class="card feat" data-rv style="--d:{i*60}ms"><span class="ic-tile {g}">{icon(k)}</span><div><h3>{E(t)}</h3><p>{E(d)}</p></div></div>' for i, ((k, t, d), g) in enumerate(zip(OFFLINE, ['grad-blue', 'grad-violet', 'grad-cyan', 'grad-pink', 'grad-green', 'grad-blue'])))
    stats = [(4, 'Main courses'), (5, 'Short courses'), (5, 'Career-support services'), (1, 'Offline centre in Bhopal')]
    st = ''.join(f'<div class="stat" data-rv style="--d:{i*80}ms"><strong data-count="{n}">{n}</strong><span>{E(l)}</span></div>' for i, (n, l) in enumerate(stats))
    return f'''<section class="section alt" id="why-offline"><div class="wrap">{sec_head('OFFLINE IS OUR USP', 'Why learn in a <span class="grad-text">real classroom?</span>', 'We teach only offline, at our centre in Arera Colony, Bhopal. No recorded-video course. Just a trainer, a classroom and people learning alongside you.')}<div class="grid-feat">{tiles}</div><div class="stats">{st}</div></div></section>'''

CAREER_ICONS = ['folder', 'file', 'brief', 'mic', 'hand']
def career_section(compact=False):
    tiles = ''.join(f'<div class="card career" data-rv style="--d:{i*60}ms"><span class="ic-tile {g}">{icon(k)}</span><p class="kick-sm">{E(a)}</p><h3>{E(b)}</h3>{"" if compact else f"<p>{E(c)}</p>"}</div>' for i, ((a, b, c), k, g) in enumerate(zip(CAREER, CAREER_ICONS, ['grad-blue', 'grad-violet', 'grad-cyan', 'grad-pink', 'grad-green'])))
    return f'''<section class="section" id="career"><div class="wrap">{sec_head('FULL CAREER SUPPORT', 'Learn it. Build it. <span class="grad-text">Present it with confidence.</span>', 'Every course comes with career support. Ask us how each service applies to your course and starting point.')}<div class="grid-career">{tiles}</div><p class="disclaimer" data-rv>Placement assistance is available. Employment is not guaranteed.</p></div></section>'''

def cta_band():
    return f'''<section class="cta-band"><div class="wrap cta-in" data-rv><div><h2>Start your career journey with Infinity Vision</h2><p>Free counselling: tell us your goal and we will help you pick the right course. Visit, call or WhatsApp.</p></div><div class="cta-actions">{wa_btn('WhatsApp us', 'free counselling', 'btn btn-white')}{call_btn('btn btn-outline-w')}</div></div></section>'''

def faq_section():
    items = ''.join(f'<details class="faq" data-rv><summary>{E(q)}<span class="plus" aria-hidden="true"></span></summary><p>{E(a)}</p></details>' for q, a in FAQ)
    return f'''<section class="section alt" id="faq"><div class="wrap">{sec_head('FAQ', 'Questions people <span class="grad-text">ask us</span>')}<div class="faq-grid">{items}</div></div></section>'''

def enquiry_form(pre, default_course=''):
    opts = '<option value="">Choose a course</option>' + ''.join(f'<option value="{E(v)}"{" selected" if v == default_course else ""}>{E(t)}</option>' for v, t in COURSE_OPTIONS)
    times = '<option value="">Choose a time</option>' + ''.join(f'<option value="{E(t)}">{E(t)}</option>' for t in TIMES)
    levels = '<option value="">Optional</option>' + ''.join(f'<option value="{E(t)}">{E(t)}</option>' for t in LEVELS)
    return f'''<form class="enq" action="/api/enquiry" method="post" data-enquiry-form novalidate><div class="enq-fields" data-form-fields><div class="f"><label for="{pre}-name">Your name</label><input type="text" id="{pre}-name" name="name" autocomplete="name" required minlength="2" maxlength="80" placeholder="e.g. Riya Sharma"></div><div class="f"><label for="{pre}-phone">Mobile number</label><input type="tel" id="{pre}-phone" name="phone" autocomplete="tel" inputmode="numeric" required maxlength="16" placeholder="10-digit mobile"></div><div class="f"><label for="{pre}-course">Course</label><select id="{pre}-course" name="course" required>{opts}</select></div><div class="f"><label for="{pre}-time">Best time to call</label><select id="{pre}-time" name="preferred_time" required>{times}</select></div><div class="f"><label for="{pre}-level">Where are you starting?</label><select id="{pre}-level" name="level">{levels}</select></div><div class="f"><label for="{pre}-message">Message <small>(optional)</small></label><input type="text" id="{pre}-message" name="message" maxlength="600" placeholder="Your goal or question"></div><div class="hp" aria-hidden="true"><label for="{pre}-website">Leave this field empty</label><input type="text" id="{pre}-website" name="website" tabindex="-1" autocomplete="off"></div><input type="hidden" name="source_page" value="" data-source-page><p class="form-error" data-form-error role="alert" hidden></p><div class="enq-actions"><button class="btn btn-primary" type="submit" data-submit>{icon("send")}<span data-submit-label>Send enquiry</span></button><button class="btn btn-wa" type="button" data-wa-fallback>{WA_SVG}<span>Send on WhatsApp</span></button></div><p class="fine">We save your enquiry only to call you back about courses.</p></div><div class="form-status" data-form-status role="status" aria-live="polite" tabindex="-1" hidden><span class="ic-tile grad-green">{icon("check")}</span><h3 data-status-title>Enquiry received</h3><p data-status-text>Thank you. Our team will call you back soon.</p></div></form>'''

def contact_section(default_course=''):
    return f'''<section class="section" id="contact"><div class="wrap">{sec_head('VISIT · CALL · WHATSAPP', 'Come and see the classroom. <span class="grad-text">Talk to us first.</span>', 'Classes are offline only, at our centre in Arera Colony, Bhopal. Tell us your goal and when you can attend.')}<div class="contact-grid"><div class="card form-card" data-rv><h3>Send a quick enquiry</h3>{enquiry_form('enq', default_course)}</div><div class="contact-side" data-rv style="--d:80ms"><div class="card map-card"><iframe title="Map showing E-2, 359 Arera Colony, Bhopal" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe><a class="map-open" href="{MAP_LINK}" target="_blank" rel="noopener noreferrer">{icon("map")}<span>Open in Google Maps</span><span class="sr-only"> (opens in a new tab)</span></a></div><div class="card contact-rows"><a class="crow" href="{TEL}"><span class="ic-tile sm grad-blue">{icon("phone")}</span><span><small>Call</small><strong>{PHONE}</strong></span></a><a class="crow" href="{wa_href('course suitability')}" target="_blank" rel="noopener noreferrer"><span class="ic-tile sm grad-green">{WA_SVG}</span><span><small>WhatsApp</small><strong>{PHONE}</strong></span><span class="sr-only"> (opens WhatsApp in a new tab)</span></a><div class="crow"><span class="ic-tile sm grad-violet">{icon("pin")}</span><div><small>Address</small><address>{ADDRESS}</address></div></div><p class="fine">Offline only. Please call before travelling; a visit request is not a confirmed appointment.</p></div></div></div></div></section>'''

def home():
    words = '|'.join(['Data Analytics', 'Performance Marketing', 'Full-Stack Development', 'Tally + US GAAP & IFRS'])
    hero = f'''<section class="hero home-hero" id="top">{particles()}<div class="wrap hero-grid"><div class="hero-copy"><p class="pill">{icon("pin")}<span>100% offline classes · Arera Colony, Bhopal</span></p><h1>Empowering skills.<br><span class="grad-light">Building careers.</span></h1><p class="typed-line">Learn <span class="typed" data-typed data-words="{E(words)}">Data Analytics</span><span class="caret" aria-hidden="true"></span></p><p class="lead">Practical, classroom-based training with full career support: CV help, LinkedIn &amp; Naukri profiles, mock interviews, portfolio building and placement assistance.</p><div class="hero-actions"><a class="btn btn-glow" href="#courses"><span>Explore courses</span>{icon("arrow")}</a>{wa_btn('Chat on WhatsApp', 'free counselling', 'btn btn-wa')}</div><ul class="trust"><li>{icon("check")}Offline only</li><li>{icon("check")}Practical projects</li><li>{icon("check")}Placement assistance</li></ul></div><aside class="glass hero-card" aria-label="Free counselling"><p class="kick-sm">FREE COUNSELLING</p><h2>Not sure which course fits?</h2><p>Tell us your goal. We will suggest the right starting point.</p><ul class="hc-list">{''.join(f'<li><a href="/courses/{c["slug"]}/"><span class="dot {GRADS[c["grad"]]}"></span>{E(c["short"])}{icon("arrow")}</a></li>' for c in MAIN)}</ul><div class="hc-actions">{call_btn('btn btn-glow btn-sm')}<a class="btn btn-ghost btn-sm" href="#contact">Request a call back</a></div></aside></div>{tools_strip()}</section>'''
    body = hero + courses_section() + why_section() + career_section() + cta_band() + faq_section() + contact_section()
    return head('Infinity Vision | Offline Career Courses in Bhopal', 'Offline career courses in Bhopal: Data Analytics, Performance Marketing & Analytics, Full Stack Web & App Development, Tally with US GAAP & IFRS and Advanced Excel. Call 9098372445.', '/') + header() + f'<main id="main">{body}</main>' + footer()

def course_page(c):
    mods = ''.join(f'''<div class="card module" data-rv style="--d:{(i%3)*60}ms"><div class="mod-top"><span class="num">{i+1:02d}</span>{'<span class="badge badge-new">New</span>' if f == 'new' else ('<span class="badge badge-exp">Expanded</span>' if f == 'expanded' else '')}</div><h3>{E(t)}</h3><p>{E(d)}</p></div>''' for i, (t, d, f) in enumerate(c['modules']))
    roles = ''.join(f'<li>{icon("check")}{E(r)}</li>' for r in c['roles'])
    chips = ''.join(f'<li>{E(t)}</li>' for t in c['tools'])
    outs = ''.join(f'<li>{icon("check")}{E(o)}</li>' for o in c['outputs'])
    qs = ''.join(f'<li>{E(q)}</li>' for q in c['questions'])
    others = ''.join(f'<a class="card other" href="/courses/{o["slug"]}/" data-rv><span class="ic-tile sm {GRADS[o["grad"]]}">{icon(o["ic"])}</span><span>{E(o["name"])}</span>{icon("arrow")}</a>' for o in COURSES if o['slug'] != c['slug'])
    newnote = {'new': 'A new course at Infinity Vision.', 'expanded': 'Builds on our earlier course with new modules, marked “New” or “Expanded” below.'}.get(c['newness'], 'A focused short course.')
    hero = f'''<section class="hero course-hero">{particles()}<div class="wrap hero-grid"><div class="hero-copy"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/#courses">Courses</a><span aria-hidden="true">/</span><span aria-current="page">{E(c['short'])}</span></nav><p class="pill">{badge(c)}<span>Offline · Arera Colony, Bhopal</span></p><h1>{E(c['name'])}</h1><p class="lead">{E(c['tagline'])} {E(newnote)}</p><ul class="chips chips-dark">{chips}</ul><div class="hero-actions">{wa_btn('Enquire on WhatsApp', c['name'])}{call_btn()}<a class="btn btn-ghost" href="#contact">Send enquiry</a></div></div><aside class="glass hero-card roles-card"><p class="kick-sm">CAREER OUTCOMES</p><h2>Roles this prepares you for</h2><ul class="role-list">{roles}</ul><p class="fine-w">Full career support included. Employment is not guaranteed.</p></aside></div></section>'''
    topics = f'''<section class="section" id="topics"><div class="wrap">{sec_head('SYLLABUS', 'Key topics', 'What you will cover in class. Ask us about the exact order, depth and practical activities in the next batch.')}<div class="grid-mods">{mods}</div></div></section>'''
    fit = f'''<section class="section alt" id="fit"><div class="wrap">{sec_head('IS IT FOR YOU?', 'Who this course <span class="grad-text">is for</span>')}<div class="grid-3"><div class="card info" data-rv><span class="ic-tile grad-blue">{icon("users")}</span><h3>Who it is for</h3><p>{E(c['audience'])}</p></div><div class="card info" data-rv style="--d:70ms"><span class="ic-tile grad-violet">{icon("cap")}</span><h3>Before you join</h3><p>{E(c['prereq'])}</p></div><div class="card info" data-rv style="--d:140ms"><span class="ic-tile grad-cyan">{icon("star")}</span><h3>How it is different</h3><p>{E(c['difference'])}</p></div></div><div class="grid-2"><div class="card info" data-rv><span class="ic-tile grad-pink">{icon("folder")}</span><h3>Course project</h3><p>{E(c['project'])}</p><ul class="out-list">{outs}</ul></div><div class="card info" data-rv style="--d:70ms"><span class="ic-tile grad-green">{icon("chat")}</span><h3>Good questions to ask us</h3><ul class="q-list">{qs}</ul><p class="small muted">Fees, timings, language and software requirements: please ask us. They differ by course.</p><div class="cc-actions">{wa_btn('Ask on WhatsApp', c['name'], 'btn btn-wa btn-sm')}{call_btn('btn btn-line btn-sm')}</div></div></div></div></section>'''
    other = f'''<section class="section" id="other-courses"><div class="wrap">{sec_head('EXPLORE MORE', 'Other courses')}<div class="grid-other">{others}</div></div></section>'''
    body = hero + topics + fit + career_section(compact=True) + other + contact_section(c['name'])
    return head(f'{c["short"]} course, Bhopal | Infinity Vision', f'{c["name"]} offline course at Infinity Vision, Arera Colony, Bhopal: {", ".join(c["tools"])}. Roles: {", ".join(c["roles"][:3])}. Call 9098372445.', f'/courses/{c["slug"]}/') + header() + f'<main id="main">{body}</main>' + footer()

def write(rel, html):
    p = OUT / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(clean_html(html))

write('index.html', home())
for c in COURSES: write(f'courses/{c["slug"]}/index.html', course_page(c))
nf = head('Page not found | Infinity Vision', 'This page could not be found.', '/404') + header() + f'''<main id="main"><section class="hero course-hero">{particles()}<div class="wrap"><div class="hero-copy"><h1>This page has moved.</h1><p class="lead">Browse all courses or ask us on WhatsApp.</p><div class="hero-actions"><a class="btn btn-glow" href="/#courses">See all courses</a>{wa_btn('Ask on WhatsApp', 'courses')}{call_btn()}</div></div></div></section></main>''' + footer()
write('404.html', nf)
(OUT / 'robots.txt').write_text('User-agent: *\nAllow: /\n')
(OUT / '_redirects').write_text(''.join(f'/courses/{o}/ /courses/{n}/ 301\n/courses/{o}/index.html /courses/{n}/ 301\n/courses/{o} /courses/{n}/ 301\n' for o, n in REDIRECTS.items()))
(OUT / '_headers').write_text("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:; frame-src https://www.google.com https://maps.google.com; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self' https://wa.me\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n")
(OUT / 'assets' / 'mark.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2d4bff"/><stop offset="1" stop-color="#6a3bff"/></linearGradient></defs><rect width="48" height="48" rx="14" fill="url(#g)"/><path d="M24 24C16 8 4 14 4 24s12 16 20 0 20-10 20 0-12 16-20 0Z" fill="none" stroke="#fff" stroke-width="3"/></svg>')
(ROOT / 'src' / 'form-options.json').write_text(json.dumps({'courses': [v for v, _ in COURSE_OPTIONS], 'times': TIMES, 'levels': LEVELS}, indent=2) + '\n')
print('Generated', len(list(OUT.rglob('*.html'))), 'pages into', OUT)
