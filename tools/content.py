"""Original standalone Infinity Vision V2 page generator. No repository/source checkout."""
from pathlib import Path
import html,json,re,shutil
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'site'
OUT.mkdir(exist_ok=True)
E=html.escape
def clean_html(text):
    text=re.sub(r'&(?!#[0-9]+;|#x[0-9a-fA-F]+;|[A-Za-z][A-Za-z0-9]+;)', '&amp;',text)
    # Keep phone-action labels together without changing accessible text or hrefs.
    def phone_label(match):
        parts=re.split(r'(<[^>]+>)',match.group(2))
        return match.group(1)+''.join(t if t.startswith('<') else t.replace(' ','&nbsp;') for t in parts)+match.group(3)
    return re.sub(r'(<a\b[^>]*href="tel:[^>]+>)(.*?)(</a>)',phone_label,text,flags=re.S)

PHONE='9098372445'
ARROW='<span aria-hidden="true">↗</span>'
def wa(label,context='course suitability',cls='btn btn-lime'):
    href='https://wa.me/919098372445?text='+quote('Hello Infinity Vision, I would like to ask about '+context+'. Please help me understand the next step for offline classes at your centre.')
    return f'<a class="{cls}" href="{href}" target="_blank" rel="noopener noreferrer">{E(label)} {ARROW}<span class="sr-only"> (opens WhatsApp in a new tab)</span></a>'
def btn(label,href,cls='btn btn-dark'):
    return f'<a class="{cls}" href="{href}">{E(label)} {ARROW}</a>'
def course(slug,name,category,tagline,tools,audience,prereq,difference,modules,project,outputs,questions,new=False):
    return dict(slug=slug,name=name,category=category,tagline=tagline,tools=tools,audience=audience,prereq=prereq,difference=difference,modules=modules,project=project,outputs=outputs,questions=questions,new=new)
COURSES=[
course('excel','Advanced Excel','Reporting','Make the spreadsheet work for you.',['Pivot Tables','Power Query','Dashboards','Macros'],
'For spreadsheet users, students and professionals who want to organise data, summarise performance and understand repeatable business reporting.',
'Bring basic computer and spreadsheet familiarity to the conversation. Tell us which formulas, tables or reports you already use so we can discuss the right starting level.',
'The broader Excel pathway includes advertised macros and automation. The proposed Excel Reporting Clinic is a focused introduction; the proposed analytics flagship adds SQL, Power BI and business decisions.',[
('Pivot Tables','Summarise spreadsheet data into useful comparisons. Explore how categories and filters change a report, and why a total should be checked against its source.'),
('Power Query','Explore preparing and transforming data for analysis. Discuss the cleaning and refresh workflows covered, and how to document important changes to source fields.'),
('Dashboards','Bring useful summaries together. A good reporting layout helps a reader identify the question, understand the comparison and trace the numbers back to the underlying data.'),
('Data analysis','Examine patterns and explain what a result means. Ask about the types of business questions and analysis exercises included in the current syllabus.'),
('Macros and automation','Explore the advertised automation component. Confirm the exact macro scope, software version and starting knowledge with the trainer; advanced VBA coverage is not assumed.')],
'A reporting workbook connecting a source table, cleaning steps, a Pivot Table and a dashboard. A short explanation would document what changed and how the report totals were checked.',
['A structured reporting table','A pivot summary and clear dashboard','A source-to-report checking note'],
['Which Excel version and device do I need?','What formulas or spreadsheet knowledge should I already have?','What is included in macros and automation?','Which exercises are part of the current course?']),
course('tally','Tally ERP','Accounting','Understand the records behind a business.',['Accounting','GST billing','Inventory','Payroll'],
'For learners exploring accounting workflows and people who want a clearer view of the records behind everyday business transactions, stock and reporting.',
'Discuss your accounting knowledge and computer confidence with the team. Confirm the Tally software version, access arrangements and entry requirements before choosing.',
'Tally ERP is the accounting pathway, not an analytics bootcamp. Excel can support reporting, but it does not replace the accounting records and workflows covered here.',[
('Accounting records','Explore the accounting component of the published course. Ask which transaction and record workflows are included and how the trainer checks the examples.'),
('GST billing','Understand the advertised billing area. Software version and examples need to be current and validated by a qualified trainer; training does not replace professional tax advice.'),
('Inventory','Explore records for stock movements and how inventory information relates to business transactions. Confirm the particular inventory workflows in the syllabus.'),
('Payroll','Discuss the payroll processes covered and the starting knowledge expected. Do not assume every statutory or advanced payroll scenario is included.'),
('Financial reporting','Connect records to financial reporting. Ask which reports are explored, how source entries are checked and how examples are explained in class.')],
'A sample-business exercise linking illustrative transactions, inventory records and financial reports. A qualified trainer must review the software version, accounting treatment and GST examples before this is offered.',
['An illustrative transaction trail','A stock-record walkthrough','A financial-report checking note'],
['Which Tally version is used?','Is previous accounting knowledge expected?','Who reviews the GST examples?','Which reports and practice activities are included?']),
course('web','Web Development','Development','Go from a blank page to a real interface.',['HTML','CSS','JavaScript','Responsive design'],
'For learners curious about how websites are structured, styled and made interactive, and people who want a practical starting point in frontend development.',
'Ask what computer skills, device and software are expected. Tell the team about any HTML, CSS or coding you have tried so the starting point is appropriate.',
'This is the advertised frontend pathway. Backend systems, full-stack engineering, hosting and deployment should not be assumed to be included.',[
('HTML foundations','Explore the structure of a web page and the relationship between headings, paragraphs, links and other content. Ask how the course introduces page structure.'),
('CSS and layout','Learn about styling and presentation within the published scope. Discuss which layout techniques and visual exercises are included in the current syllabus.'),
('JavaScript foundations','Explore the language that adds behaviour to web pages. Ask what interactions are built and which JavaScript fundamentals are covered before choosing.'),
('Responsive design','Understand adapting a frontend across screen sizes. Ask how different layouts are checked and which device requirements apply to classroom practice.'),
('Frontend project development','The published course includes real project development. Confirm the exact brief, expected output and review arrangements rather than assuming a specific production application.')],
'A responsive small-business website bringing page structure, styling and a simple interaction together. The accompanying explanation could describe design choices and checks across screen widths. The exact project needs teaching approval.',
['A responsive frontend concept','A purposeful interface interaction','A design and testing explanation'],
['What frontend project is currently taught?','Do I need previous programming experience?','Which device and software should I use?','Is any backend or deployment coverage included?']),
course('digital','Digital Marketing','Marketing','Understand the channels. Connect the plan.',['SEO','Google Ads','Meta Ads','Social media'],
'For learners exploring digital marketing, and business owners who want to understand the channels used to reach potential customers and evaluate activity.',
'Discuss your digital familiarity and goals. Ask which practical tools and access arrangements apply; live advertising spend or client campaign access should not be assumed.',
'Digital Marketing covers channels and execution. The proposed Marketing Analytics with GA4 flagship focuses more deeply on measurement, interpretation and what to test next.',[
('Search engine optimisation','Explore the SEO area of the published syllabus. Ask how search visibility, website content and practical exercises are approached in the current course.'),
('Google Ads','Understand the advertised Google Ads component. Confirm tool access and the nature of exercises; a live advertising budget is not a promised inclusion.'),
('Meta Ads','Explore the Meta advertising area and discuss how campaign objectives and audiences are introduced. No specific lead volume or campaign result is promised.'),
('Social media marketing','Consider how social channels support business communication. Ask which planning and content activities are included rather than assuming every platform is taught.'),
('Lead generation and analytics','Connect channel activity with measurement questions. This is already part of the advertised scope, not an entirely new addition to Digital Marketing.')],
'A sample campaign brief connecting a business objective, audience, channel choice, landing-page requirements and measurement questions. This does not promise live client work, paid media spend or guaranteed leads.',
['A sample campaign brief','A channel and landing-page plan','A measurement-question checklist'],
['Which activities and tools are included?','Are exercises simulated or based on permitted examples?','Is ad spend required or included?','How does this differ from Marketing Analytics?']),
course('data-business-analytics','Data & Business Analytics','Analytics','Raw data. Clear thinking. Better decisions.',['Excel','SQL','Power BI','Business decisions'],
'Proposed for beginners with basic spreadsheet comfort, people handling recurring reports and professionals who want stronger reporting and decision-making skills.',
'Basic computer use and comfort entering data in simple spreadsheets. No Python prerequisite is proposed. Discuss prior learning before repeating foundations; the Excel Reporting Clinic may be a starting point.',
'This flagship combines data preparation, querying, dashboards and business reasoning. It is not an advanced machine-learning programme or a substitute for professional experience.',[
('Business questions and data literacy','Define the decision, useful metrics and data-quality checks. Proposed practice: turn a vague sales question into a focused analysis brief with explicit assumptions.'),
('Excel and Power Query','Organise tables, summarise with pivots, clean inconsistent fields and reconcile totals. Proposed practice: produce a documented reporting table and cleaning log.'),
('SQL for analysis','Filter, group and join related tables using readable queries. Proposed practice: answer product and monthly-sales questions while checking row counts, duplicate records and totals.'),
('Data modelling','Explore relationships and a simple star schema. Proposed practice: separate transaction and reference tables, then check the effect of joins and filters on a result.'),
('Power BI and DAX foundations','Build basic measures, understand filter effects and choose readable visuals. Proposed practice: validate dashboard totals against independent source calculations.'),
('Business statistics and decisions','Use descriptive measures, uncertainty literacy, simple forecast baselines, break-even and scenario comparisons. Proposed practice: compare options with visible assumptions, not false precision.'),
('Communicating analysis','Write a short decision memo explaining evidence, trade-offs and limitations. Proposed practice: distinguish a measured result from a judgement or recommendation.')],
'An integrated retail capstone using original synthetic or appropriately licensed data: clean and query the data, build a simple model, check a sales/margin dashboard, compare a business scenario and explain the recommendation.',
['Cleaning log and SQL analysis','Validated model and retail dashboard','Scenario workbook','One-page decision memo'],
['When will the proposed programme be available?','What spreadsheet level is needed?','What Windows, Power BI and software access will be required?','How will the proposed exercises be reviewed?'],True),
course('marketing-analytics','Marketing Analytics with GA4','Analytics','Don’t just report a campaign. Question it.',['GA4','Funnels','Campaign economics','Measurement'],
'Proposed for marketers, business owners and analysts who want to evaluate acquisition, conversion and retention rather than only report traffic.',
'Basic spreadsheets and common business metrics. A GA4 introduction may help first-time users. Data & Business Analytics is not a mandatory proposed purchase. Exercise access will be confirmed before launch.',
'This is a measurement specialisation, not a second name for Digital Marketing. It focuses on report interpretation and decisions rather than SEO execution, content production or ad operation.',[
('Measurement planning','Connect goals, funnels, KPIs, events and key events. Proposed practice: write an event and KPI specification for a sample business question.'),
('GA4 report interpretation','Interpret users, acquisition and conversion context. Proposed practice: explain a report without mixing scopes or using inconsistent denominators.'),
('Campaign consistency','Use clear UTM naming and fair comparisons. Proposed practice: prepare a naming guide and spot inconsistent campaign labels before interpreting performance.'),
('Funnels, cohorts and segments','Inspect conversion drop-off and retention patterns. Proposed practice: describe a potential issue and identify the additional evidence needed before acting.'),
('Marketing economics','Consider CAC, ROAS, margin and LTV assumptions. Proposed practice: compare campaigns without treating revenue as profit or a higher ROAS as an automatic business win.'),
('Tests, attribution and privacy','Interpret evidence cautiously and recognise attribution limits. Proposed practice: write a test recommendation with limitations while minimising personal data.')],
'A permitted GA4 example or demo analysis combined with synthetic campaign data: create an event specification, UTM guide and funnel/campaign report, then write a qualified budget or testing recommendation. No real customer personal data is planned.',
['Event and KPI specification','UTM naming guide','Funnel and campaign report','Evidence-qualified test recommendation'],
['When will launch details be announced?','Will a personal GA4 property be needed?','What example data and access will be arranged?','How does GA4 Basics differ from this flagship?'],True)
]
MINIS=[('Excel Reporting Clinic','01','Start with a table. Finish with a report.','For learners needing a focused introduction to structured reporting.','Organise a messy table, check key fields and build a Pivot Table summary.','A clean table, pivot summary and short reporting sheet.','A starter, not a replacement for Advanced Excel or its macros and automation.','sheet'),('SQL Foundations','02','Ask better questions of a database.','For beginners curious about queries and business data.','Filter rows, group results and join two related tables while checking totals.','Readable queries with explanation notes and join checks.','A focused introduction, not the full analytics flagship.','code'),('Power BI/DAX Foundations','03','Build a model. Check the measure.','For spreadsheet users starting with dashboards and modelling.','Relate simple tables, build basic DAX measures and reconcile results.','A small model and report with a validation checklist.','Foundations only; no advanced Power BI promise.','chart'),('GA4 Basics','04','Know what the report is really saying.','For first-time learners of web measurement.','Connect a business goal to events and KPIs; interpret a permitted example.','An event/KPI worksheet and a short report explanation.','Report reading, not a promise of production tracking implementation.','target')]

CAREER=[('Build the evidence','Portfolio building','Get support bringing your skills together in work you can explain. Ask how portfolio support applies to your chosen course.'),('Put it into words','CV help','Get help presenting your skills and experience clearly. Your CV should reflect work you can genuinely discuss.'),('Make your profile clearer','LinkedIn & Naukri','Profile support for LinkedIn and Naukri, alongside your CV. Discuss what is covered for your starting point.'),('Practise the conversation','Mock interviews','Practise explaining your learning, projects and experience through mock interviews.'),('Discuss your next step','Placement assistance','Placement assistance is available. Ask about the process, eligibility and scope. Employment is not guaranteed.')]
FAQ=[('Is this an online course platform?','No. Classes are offline only, at our centre. Discuss attendance and available timings before choosing a course.'),('Which courses are currently advertised?','Advanced Excel, Tally ERP, Web Development and Digital Marketing. Ask about current availability, exact syllabus and your starting level; a course listing is not confirmation of an open batch.'),('Can I join the new analytics programmes now?','The two proposed flagship programmes and four mini-courses are in development. Launch details and enrolment are not announced. You can ask about their scope and express interest without assuming a batch is available.'),('What does full career support include?','CV help, LinkedIn and Naukri profile support, mock interviews, portfolio building and placement assistance. Ask about eligibility and how these services apply to your chosen course. Employment is not guaranteed.'),('What are the fees, timings and software requirements?','Contact the institute for course-specific fees, available timings, teaching language, equipment and software requirements, practice arrangements and relevant policies. These details are not assumed to be the same for every course.'),('Do I need coding for the proposed analytics flagship?','Basic computer and spreadsheet comfort is the proposed starting point. SQL is introduced within Data & Business Analytics; Python is not a proposed prerequisite. Marketing Analytics starts from spreadsheet and KPI basics and does not require purchasing the other flagship.'),('How do I arrange a visit?','Call 9098372445 or open WhatsApp to request a suitable time. Wait for the team to confirm the arrangements before travelling; a request is not a confirmed appointment.')]
