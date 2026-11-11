"""Build branded Infinity Vision intro-guide PDFs (4–6 A4 pages) from courses_v4.py.

Writes HTML into a work directory, then prints PDFs with tools/print_guides.mjs
(Playwright Chromium). Called from tools/build.mjs after static assets exist.
"""
from __future__ import annotations
import html, os, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from courses_v4 import COURSES
from institute import ADDRESS

ROOT = Path(__file__).resolve().parents[1]
PHONE = '9098372445'
TEL = 'tel:+919098372445'
WA = 'https://wa.me/919098372445'
HONESTY = 'Placement assistance means support with the process, not a promised job. Employment is not guaranteed.'

# Official course names stay as in courses_v4.py. Cover titles can be a little warmer.
COVER_TITLE = {
    'data-analytics': 'Data Analytics',
    'performance-marketing': 'Performance Marketing & Analytics',
    'full-stack': 'Full Stack Web & App Development',
    'tally-gaap-ifrs': 'Tally with US GAAP & IFRS',
    'excel': 'Advanced Excel',
}

FIELD = {
    'data-analytics': (
        'Businesses collect more numbers than anyone can read by eye. Data analytics is the work of '
        'turning that raw information into a clear answer: clean the table, ask a precise question, '
        'check the totals, and explain what the numbers do — and do not — support.',
        'It is not machine learning, and it is not a promise that a dashboard will change a business on its own. '
        'It is a practical way to make everyday decisions with evidence rather than a guess.',
    ),
    'performance-marketing': (
        'Performance marketing is paid, measurable campaign work. You choose a channel (for example Google Ads or Meta Ads), '
        'spend a budget, track what happened, and improve the next round. The aim is to see which activity brought a lead or a sale, and at what cost.',
        'Results from real campaigns are never guaranteed. This guide explains the craft — planning, tracking and reading the numbers — not a formula for profit.',
    ),
    'full-stack': (
        'Full stack web and app development is the work of building both sides of a product: the pages and screens people see, '
        'and the server, database and APIs that sit behind them. A complete website or web app needs both.',
        'This is not a promise of a job title or a shipped commercial product. It is a path from a blank page to a small working application you can explain.',
    ),
    'tally-gaap-ifrs': (
        'Accounting records what a business owns, owes and earns. Tally Prime is widely used in Indian firms for day-to-day books, GST billing, inventory and payroll. '
        'US GAAP and IFRS are the reporting languages used when those accounts need to be understood in an international setting.',
        'The US GAAP and IFRS parts of this course are fundamentals. They are not a professional qualification or certification, and they do not replace tax, audit or professional advice.',
    ),
    'excel': (
        'Most workplace reporting still lives in a spreadsheet. Advanced Excel is about turning a raw table into a report someone else can trust: '
        'clean the data, summarise it with Pivot Tables, and present the result in a clear layout, with a check that the totals still match the source.',
        'It is a focused spreadsheet course. Data Analytics goes further with SQL, Power BI and business decisions. This guide stays with the Excel skills you will practise first.',
    ),
}

EXERCISE = {
    'data-analytics': {
        'title': 'Try this: a one-page sales question',
        'need': 'A spreadsheet program (Excel, Google Sheets or similar) and about 20 minutes. No special software.',
        'steps': [
            'Create a small table with these columns: Date, Product, Quantity, Unit price. Enter 8 to 10 rows for a local shop you know — for example tea, samosa, bottled water — using made-up but realistic numbers.',
            'Add a Revenue column with the formula Quantity × Unit price. Check one row by hand so the formula is doing what you think it is doing.',
            'Build a Pivot Table (or a simple SUMIF summary) of Revenue by Product. Write down which product brought in the most revenue.',
            'On the same page, write two sentences: (1) the decision this table could inform (for example, “which item should we stock more of next week?”), and (2) one thing the table cannot tell you (for example, cost, wastage, or whether a quiet item brings customers in).',
        ],
        'check': 'A complete attempt has a totals check (the sum of Revenue in the table matches the Pivot grand total) and an honest limitation, not just a ranking of products.',
    },
    'performance-marketing': {
        'title': 'Try this: a one-page campaign brief',
        'need': 'A notebook or a blank document. No ad account and no spend required.',
        'steps': [
            'Pick a local business you know (a tuition centre, a clinic, a shop). Write one sentence for the action you want someone to take — a WhatsApp message or a visit, not a vague goal like “awareness”.',
            'Write three search-ad headlines, each 30 characters or fewer, that name the offer and the place. Then write one line of description that says what happens after they click.',
            'Draft a UTM pattern you would add to the landing-page link, for example: utm_source=google, utm_medium=cpc, utm_campaign=whatsapp-leads-nov. Keep the names short and consistent.',
            'List two numbers you would look at after a week: spend, and the number of the action you chose. Write one sentence on why those two, and one sentence on a number you would not treat as success on its own (for example clicks without a lead).',
        ],
        'check': 'You should be able to read the page aloud in a minute and know the action, the message, how you would tag the link, and how you would judge the week. Live results are not part of this exercise.',
    },
    'full-stack': {
        'title': 'Try this: a one-page visiting card in HTML',
        'need': 'A text editor and a browser. No framework and no hosting account.',
        'steps': [
            'Create a file called index.html. Add a page for a local business: the name, a one-line offer, opening hours or an area they serve, and a “WhatsApp us” link (you can use a placeholder number).',
            'Style it with a simple CSS block in the same file: a max-width of about 40rem, comfortable padding, a clear heading, and a button-style link. Avoid position hacks and large background images.',
            'Open the file in your browser. Resize the window down to a phone width and fix anything that overflows or becomes hard to read.',
            'Write three short comments in the file: what the HTML is responsible for, what the CSS is responsible for, and one thing a real site would still need (for example a server to receive the enquiry).',
        ],
        'check': 'The page should remain readable on a narrow window, the WhatsApp link should be tappable, and your comments should show you can explain the split between structure, style and a back-end you have not built yet.',
    },
    'tally-gaap-ifrs': {
        'title': 'Try this: a six-entry thinking sheet',
        'need': 'A notebook or a blank spreadsheet. You do not need Tally installed for this exercise. This is practice thinking, not tax or audit advice.',
        'steps': [
            'Imagine a small stationery shop. List six everyday events: a cash sale, a credit purchase of stock, a cash deposit into the bank, owner drawings, a salary payment, and a GST invoice (only if you already know the idea of GST; otherwise swap this for “paid the electricity bill”).',
            'Next to each event, write the two accounts you would debit and credit, and a short reason. If you are unsure, write your best attempt and a question mark — that is useful, not a failure.',
            'Under the list, write which three of those events you would expect to see on a trial balance, and which report (profit and loss, or balance sheet) you would look at to check the salary and the bank balance.',
            'Bring the sheet to a counselling visit or to class. We will compare your reasoning with how Tally Prime records the same idea. Do not treat this as advice for a live set of books.',
        ],
        'check': 'A good attempt names both sides of each entry and includes at least one honest question. It does not need to be perfect, and it is not a filing or a return.',
    },
    'excel': {
        'title': 'Try this: clean a messy list and check the total',
        'need': 'Excel or Google Sheets and about 20 minutes.',
        'steps': [
            'Type (or paste) a 10-row list with these problems on purpose: names in mixed case, dates typed as text, two blank cells, and one category spelled two different ways (for example “Retail” and “retail ”).',
            'Clean the names with TRIM and PROPER (or Flash Fill). Turn the dates into real date values. Fill or clearly flag the blanks. Make the category spelling consistent.',
            'Insert a Pivot Table that counts rows by category. Write the grand total next to the number of data rows you started with.',
            'Add a two-line note: what you changed, and whether the Pivot total matches the source row count. If it does not, find the row that dropped out before you finish.',
        ],
        'check': 'The useful result is not a pretty sheet. It is a short cleaning note plus a totals check you can explain to someone else.',
    },
}

OFFLINE = [
    'Classes are offline only, in person at our centre — not a recorded-video course.',
    'A trainer is in the room, so you can ask when you are stuck and try the work yourself straight away.',
    'Parents are welcome to visit the classroom before you enrol. Please call or WhatsApp first so we can confirm a time. A request is not a confirmed appointment.',
    'Fees, batch dates, class timings, teaching language, and laptop or software needs differ by course. We share those with you directly rather than listing them here.',
    'Every course includes career support, described on the next pages. Employment is not guaranteed.',
]

SUPPORT = [
    ('CV help', 'Help presenting your skills and experience clearly, so your CV reflects work you can genuinely discuss.'),
    ('LinkedIn & Naukri profiles', 'Support shaping those profiles alongside your CV. Ask what is covered for your starting point.'),
    ('Mock interviews', 'Practice explaining your learning, projects and experience in an interview setting.'),
    ('Portfolio building', 'Support bringing your course work together in examples you can walk someone through.'),
    ('100% placement assistance', 'We help you prepare and apply. Ask how this process works for your course.'),
]

def faqs_for(c):
    common = [
        ('Is this an online course?', 'No. Classes are offline only, at our centre. Ask about attendance and available timings before you choose.'),
        ('When does the next batch start, and what are the fees?', 'Batch dates and fees differ by course. Call or WhatsApp 9098372445 and we will share the details for this course.'),
        ('Do you guarantee a job or a salary?', 'No. ' + HONESTY),
        ('Can I visit before I enrol?', 'Yes. Parents are welcome too. Call 9098372445 first so we can confirm a time.'),
        ('How do I ask a question?', 'Call or WhatsApp 9098372445, or send the enquiry form on our website. We will call you back at the time you choose.'),
    ]
    # Course-specific answers that do not invent fees, dates or guarantees.
    extra = {
        'data-analytics': [
            ('What spreadsheet level do I need?', 'Basic computer use and comfort entering data in a simple spreadsheet is the starting point. Python is not a prerequisite and is not part of this syllabus. If spreadsheets are new to you, ask about Advanced Excel first.'),
            ('Do I need to know coding or SQL already?', 'No. SQL is taught inside the course. You do not need prior programming.'),
        ],
        'performance-marketing': [
            ('Is ad spend required or included?', 'Live ad spend is not assumed. Ask which ad-account and tool access is arranged for practice in the next batch.'),
            ('Will you promise campaign results?', 'No. We teach you to plan, track and read a campaign. Results from real campaigns are never guaranteed.'),
        ],
        'full-stack': [
            ('Do I need previous programming experience?', 'No previous coding is assumed for the HTML and CSS start. Tell us what you have already tried so we can discuss the right starting point and device requirements.'),
            ('How much of the mobile app part is hands-on?', 'It is an introduction to how mobile apps are built and how web skills carry over. Ask the trainer how that module is taught in the next batch.'),
        ],
        'tally-gaap-ifrs': [
            ('Is previous accounting knowledge expected?', 'Basic accounting knowledge helps. Discuss your background with us and confirm the Tally version and practice access before you choose.'),
            ('How deep do the US GAAP and IFRS modules go?', 'They are fundamentals: an introduction to the ideas and common differences, not a professional qualification or certification.'),
        ],
        'excel': [
            ('What should I already know?', 'Basic computer and spreadsheet familiarity. Tell us which formulas, tables or reports you already use so we can discuss the right starting level.'),
            ('What is included in macros and automation?', 'That part of the course is confirmed with the trainer, including the Excel version used in class. Ask us when you enquire.'),
        ],
    }
    # Keep the list tight so FAQ + CTA fit one page.
    return extra[c['slug']] + common[:4]


def E(s):
    return html.escape(str(s), quote=True)


def font_faces(font_dir: Path) -> str:
    parts = []
    for weight in (400, 500, 600, 700):
        woff = font_dir / f'poppins-{weight}.woff2'
        fallback = ROOT / 'node_modules/@fontsource/poppins/files' / f'poppins-latin-{weight}-normal.woff2'
        src = woff if woff.exists() else fallback
        uri = src.resolve().as_uri()
        parts.append(
            f'@font-face{{font-family:"Poppins";font-style:normal;font-weight:{weight};'
            f'font-display:block;src:url("{uri}") format("woff2");}}'
        )
    return '\n'.join(parts)


def logo_img(mark: Path) -> str:
    svg = mark.read_text(encoding='utf-8') if mark.exists() else (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#2d4bff"/><stop offset="1" stop-color="#6a3bff"/></linearGradient></defs>'
        '<rect width="48" height="48" rx="14" fill="url(#g)"/>'
        '<path d="M24 24C16 8 4 14 4 24s12 16 20 0 20-10 20 0-12 16-20 0Z" fill="none" stroke="#fff" stroke-width="3"/></svg>'
    )
    import base64
    b64 = base64.b64encode(svg.encode('utf-8')).decode('ascii')
    return f'<img class="logo" src="data:image/svg+xml;base64,{b64}" alt="Infinity Vision" width="36" height="36">'


def css(font_dir: Path) -> str:
    return f'''
{font_faces(font_dir)}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
@page {{ size: A4; margin: 0; }}
html, body {{
  font-family: "Poppins", ui-sans-serif, sans-serif;
  color: #20263a;
  background: #fff;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}}
.page {{
  width: 210mm;
  height: 297mm;
  padding: 16mm 16mm 18mm;
  position: relative;
  page-break-after: always;
  overflow: hidden;
  background: #fff;
}}
.page:last-child {{ page-break-after: auto; }}
.topbar, .foot {{
  display: flex; align-items: center; justify-content: space-between;
  font-size: 9.5pt; color: #5d6680;
}}
.brand {{ display: flex; align-items: center; gap: 8px; font-weight: 600; color: #111a39; font-size: 12pt; }}
.brand b {{ color: #2d4bff; font-weight: 700; }}
.logo {{ width: 28px; height: 28px; border-radius: 8px; display: block; }}
.topbar {{ padding-bottom: 8px; border-bottom: 2px solid #2d4bff; margin-bottom: 11mm; }}
.kicker {{ font-size: 8.5pt; font-weight: 600; letter-spacing: .14em; text-transform: uppercase; color: #2d4bff; margin-bottom: 4px; }}
h1 {{ font-size: 26pt; line-height: 1.15; color: #111a39; font-weight: 700; }}
h1 .sub {{ display: block; font-size: 13pt; font-weight: 500; color: #2d4bff; margin-top: 6px; }}
h2 {{ font-size: 14pt; color: #111a39; margin: 0 0 6px; }}
h3 {{ font-size: 10.5pt; color: #111a39; margin: 0 0 2px; }}
p, li {{ font-size: 10pt; line-height: 1.45; color: #20263a; }}
.lead {{ font-size: 11pt; color: #3a4258; margin: 8px 0 14px; max-width: 42em; }}
.pill {{ display: inline-block; padding: 3px 10px; border-radius: 999px; background: #e8edff; color: #2d3fd6; font-size: 8.5pt; font-weight: 600; }}
.grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8mm; margin-top: 6mm; }}
.card {{
  background: #f6f8ff; border: 1px solid #dbe3ff; border-radius: 12px; padding: 4.5mm 5mm;
}}
.card p {{ font-size: 9.5pt; color: #3a4258; }}
ul.plain {{ padding-left: 1.1em; }}
ul.plain li {{ margin: 0 0 4px; }}
ol.steps {{ padding-left: 1.2em; }}
ol.steps li {{ margin: 0 0 6px; }}
.mod {{
  break-inside: avoid; border-left: 3px solid #2d4bff; padding: 1.2mm 0 1.2mm 3mm; margin: 0 0 2.2mm;
}}
.mod .num {{ font-size: 8pt; font-weight: 600; letter-spacing: .08em; color: #2d4bff; }}
.mod p {{ font-size: 8.7pt; color: #3a4258; line-height: 1.35; }}
.tools {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 3mm 0 6mm; }}
.tools span {{
  padding: 3px 9px; border-radius: 999px; background: #eef3ff; border: 1px solid #cfd8ff;
  font-size: 8.5pt; font-weight: 500; color: #111a39;
}}
.note {{
  background: #eefbf4; border: 1px solid #b7ebc9; border-radius: 10px; padding: 3.5mm 4.5mm; margin-top: 4mm;
  font-size: 9.5pt; color: #13532e;
}}
.roles {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2mm 6mm; margin: 2mm 0 0; }}
.roles li {{ list-style: none; padding-left: 14px; position: relative; font-weight: 500; }}
.roles li::before {{ content: ""; position: absolute; left: 0; top: 6px; width: 7px; height: 7px; border-radius: 50%; background: #2d4bff; }}
.foot {{
  position: absolute; left: 16mm; right: 16mm; bottom: 10mm;
  border-top: 1px solid #d6dff8; padding-top: 6px;
}}
.cta {{
  background: linear-gradient(135deg, #18203e, #2d4bff 70%, #6a3bff);
  color: #fff; border-radius: 14px; padding: 7mm 8mm; margin-top: 5mm;
}}
.cta h2, .cta p, .cta li, .cta address {{ color: #fff; }}
.cta h2 {{ font-size: 15pt; margin-bottom: 3px; }}
.cta p, .cta li, .cta address {{ font-size: 10pt; }}
.cta a {{ color: #8de3ff; text-decoration: none; font-weight: 600; }}
.cta .addr {{ margin-top: 3mm; font-style: normal; font-weight: 600; }}
.faq {{ margin: 0 0 3.5mm; }}
.faq h3 {{ font-size: 10pt; }}
.faq p {{ font-size: 9.5pt; color: #3a4258; }}
.support {{ margin: 0 0 4mm; }}
.cover-hero {{
  background: linear-gradient(135deg, #18203e 0%, #2d4bff 62%, #6a3bff 100%);
  color: #fff; border-radius: 16px; padding: 10mm 10mm 9mm; margin: -2mm 0 8mm;
}}
.cover-hero .kicker {{ color: #8de3ff; }}
.cover-hero h1 {{ color: #fff; font-size: 28pt; }}
.cover-hero h1 .sub {{ color: #c9d4ff; font-weight: 500; }}
.cover-hero .lead {{ color: #d7e0ff; margin-bottom: 0; }}
.cover-hero .pill {{ background: rgba(255,255,255,.14); color: #eaf1ff; border: 1px solid rgba(255,255,255,.28); margin-top: 8px; }}
.cover-brand {{ display:flex; align-items:center; gap:8px; margin-bottom:8mm; }}
.cover-hero .brand {{ color:#fff; font-size:13pt; }}
.cover-hero .brand b {{ color:#8de3ff; }}
.cover-hero .logo {{ width:32px; height:32px; }}
'''


def header(logo: str, section: str) -> str:
    return (
        f'<div class="topbar">{logo}<span class="brand">Infinity <b>Vision</b></span>'
        f'<span>Free intro guide · {E(section)}</span></div>'
    )


def footer(page: int, total: int, course: str) -> str:
    return (
        f'<div class="foot"><span>Infinity Vision · Call / WhatsApp {PHONE}</span>'
        f'<span>{E(course)} · {page} / {total}</span></div>'
    )


def page_wrap(inner: str, logo: str, section: str, course: str, num: int, total: int, cover=False) -> str:
    bar = '' if cover else header(logo, section)
    return f'<section class="page">{bar}{inner}{footer(num, total, course)}</section>'


def build_html(c: dict, logo: str, font_dir: Path) -> str:
    slug = c['slug']
    title = COVER_TITLE[slug]
    field_a, field_b = FIELD[slug]
    ex = EXERCISE[slug]
    modules = c['modules']
    mid = (len(modules) + 1) // 2
    col1, col2 = modules[:mid], modules[mid:]

    def mods(items, start=1):
        bits = []
        for i, (t, d, _flag) in enumerate(items, start):
            bits.append(
                f'<div class="mod"><div class="num">{i:02d}</div>'
                f'<h3>{E(t)}</h3><p>{E(d)}</p></div>'
            )
        return ''.join(bits)

    tools = ''.join(f'<span>{E(t)}</span>' for t in c['tools'])
    roles = ''.join(f'<li>{E(r)}</li>' for r in c['roles'])
    steps = ''.join(f'<li>{E(s)}</li>' for s in ex['steps'])
    offline = ''.join(f'<li>{E(s)}</li>' for s in OFFLINE)
    support = ''.join(
        f'<div class="support"><h3>{E(t)}</h3><p>{E(d)}</p></div>' for t, d in SUPPORT
    )
    faq_html = ''.join(f'<div class="faq"><h3>{E(q)}</h3><p>{E(a)}</p></div>' for q, a in faqs_for(c))

    p1 = page_wrap(
        f'''
        <div class="cover-hero">
          <div class="cover-brand">{logo}<span class="brand">Infinity <b>Vision</b></span></div>
          <p class="kicker">Free intro guide</p>
          <h1>{E(title)}<span class="sub">{E(c['tagline'])}</span></h1>
          <p class="lead">A short, honest introduction to the field, the classroom course, and a starter exercise you can try before you enrol.</p>
          <p class="pill">Offline classes at our centre</p>
        </div>
        <div class="grid-2">
          <div>
            <p class="kicker">The field</p>
            <h2>What this work is</h2>
            <p>{E(field_a)}</p>
            <p style="margin-top:3mm">{E(field_b)}</p>
          </div>
          <div class="card">
            <p class="kicker">Who it is for</p>
            <h2>Is this for you?</h2>
            <p>{E(c['audience'])}</p>
            <p style="margin-top:3mm"><strong>Before you join.</strong> {E(c['prereq'])}</p>
          </div>
        </div>
        ''',
        logo, title, title, 1, 5, cover=True,
    )

    p2 = page_wrap(
        f'''
        <p class="kicker">Careers</p>
        <h2>Roles this course can lead towards</h2>
        <p class="lead">These are common roles people prepare for with this kind of training. They are not a job offer, a salary figure, or a placement percentage. What you can apply for depends on your starting point, the work you produce, and the openings at the time.</p>
        <ul class="roles">{roles}</ul>
        <p style="margin:3mm 0 4mm;font-size:9pt;color:#5d6680">{E(c['difference'])} {E(HONESTY)}</p>
        <p class="kicker">The course</p>
        <h2>What you will learn</h2>
        <p class="lead">The topics below are the classroom modules for this course. Ask us about the exact order, depth and practical activities in the next batch.</p>
        <div class="grid-2"><div>{mods(col1, 1)}</div><div>{mods(col2, mid + 1)}</div></div>
        ''',
        logo, title, title, 2, 5,
    )

    p3 = page_wrap(
        f'''
        <p class="kicker">Tools</p>
        <h2>Tools you will practise</h2>
        <p class="lead">These are the tools named in the syllabus. Access, versions and how much time you spend on each one can differ by batch — please ask us.</p>
        <div class="tools">{tools}</div>
        <p class="kicker">A starter you can try now</p>
        <h2>{E(ex['title'])}</h2>
        <p class="lead">{E(ex['need'])}</p>
        <ol class="steps">{steps}</ol>
        <p class="note"><strong>What “done” looks like.</strong> {E(ex['check'])}</p>
        ''',
        logo, title, title, 3, 5,
    )

    p4 = page_wrap(
        f'''
        <p class="kicker">The classroom</p>
        <h2>How offline classes at our centre work</h2>
        <p class="lead">Infinity Vision teaches only in person. There is no recorded-video version of these courses.</p>
        <ul class="plain">{offline}</ul>
        <p class="kicker" style="margin-top:7mm">Career support</p>
        <h2>Support included with every course</h2>
        <p class="lead">100% placement assistance means we help you prepare and apply. It is not a job guarantee.</p>
        {support}
        <div class="card"><p>{E(HONESTY)}</p></div>
        ''',
        logo, title, title, 4, 5,
    )

    p5 = page_wrap(
        f'''
        <p class="kicker">Questions</p>
        <h2>Frequently asked questions</h2>
        {faq_html}
        <div class="cta">
          <p class="kicker">Next step</p>
          <h2>Come and talk to us</h2>
          <p>Call or WhatsApp <a href="{TEL}">9098372445</a> to book a free counselling. Parents are welcome. Ask us about fees, the next batch, and whether this course is the right starting point.</p>
          <p class="addr">Visit our centre<br>{E(ADDRESS)}</p>
          <p style="margin-top:3mm">Please call first so we can confirm a time. A message is not a confirmed appointment.</p>
        </div>
        ''',
        logo, title, title, 5, 5,
    )

    return (
        '<!DOCTYPE html><html lang="en-IN"><head><meta charset="utf-8">'
        f'<title>{E(title)} · Free intro guide · Infinity Vision</title>'
        f'<style>{css(font_dir)}</style></head><body>'
        f'{p1}{p2}{p3}{p4}{p5}'
        '</body></html>'
    )


def main():
    out_dir = Path(os.environ.get('GUIDE_OUT', ROOT / 'public' / 'guides'))
    work = Path(os.environ.get('GUIDE_HTML', ROOT / '.guides-html'))
    font_dir = Path(os.environ.get('GUIDE_FONTS', ROOT / 'public' / 'assets'))
    mark = font_dir / 'mark.svg'
    if not mark.exists():
        mark = ROOT / 'site' / 'assets' / 'mark.svg'
    logo = logo_img(mark)
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    for c in COURSES:
        html_path = work / f'{c["slug"]}.html'
        html_path.write_text(build_html(c, logo, font_dir), encoding='utf-8')
        print('HTML', html_path)
    env = os.environ.copy()
    env.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/workspace/qa-tools/browsers')
    node_paths = [
        '/workspace/qa-tools/node_modules',
        env.get('NODE_PATH', ''),
    ]
    env['NODE_PATH'] = os.pathsep.join(p for p in node_paths if p)
    # Playwright is not a dependency of the site repo; load it from qa-tools.
    cmd = [
        'node',
        '--input-type=module',
        '-e',
        "import {pathToFileURL} from 'node:url';"
        "import {register} from 'node:module';"
        "await import(pathToFileURL('/workspace/infyvision-site/tools/print_guides.mjs').href);",
        str(work),
        str(out_dir),
    ]
    # Simpler: run with cwd qa-tools so playwright resolves, passing paths
    printer = ROOT / 'tools' / 'print_guides.mjs'
    result = subprocess.run(
        ['node', str(printer), str(work), str(out_dir)],
        cwd='/workspace/qa-tools',
        env=env,
        check=False,
    )
    if result.returncode != 0:
        sys.exit(result.returncode)
    for c in COURSES:
        pdf = out_dir / f'{c["slug"]}.pdf'
        if not pdf.exists() or pdf.stat().st_size < 8000:
            raise SystemExit(f'Missing or tiny PDF: {pdf}')
    print('Guides written to', out_dir)


if __name__ == '__main__':
    main()
