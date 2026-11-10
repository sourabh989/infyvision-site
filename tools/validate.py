from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'public'
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=True);self.ids=set();self.refs=[];self.tags=[];self.text=[];self.duplicate=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  d=dict(attrs);self.tags.append((tag,d))
  if 'id' in d:
   if d['id'] in self.ids:self.duplicate.append(d['id'])
   self.ids.add(d['id'])
  for k in ['href','src']:
   if k in d:self.refs.append((tag,k,d[k]))
 def handle_data(self,d):self.text.append(d)
pages={p:Page(p.read_text()) for p in OUT.rglob('*.html') if p.name!='404.html'};assert len(pages)==13,len(pages)
nf=(OUT/'404.html').read_text();assert 'href="/assets/site.css"' in nf and 'tel:+919098372445' in nf and 'href="/courses/"' in nf,'404 page'
issues=[];links=0;wa=0;tel=0
for p,page in pages.items():
 text=p.read_text();rel=str(p.relative_to(OUT));visible=' '.join(page.text)
 if page.duplicate:issues.append((rel,'Duplicate IDs',page.duplicate))
 if len([1 for t,a in page.tags if t=='h1'])!=1:issues.append((rel,'Expected one h1'))
 for number in ['7898338899','6266771665','917898338899']:
  if number in text:issues.append((rel,'Old contact',number))
 for forbidden in ['92%','1500+','guaranteed salary','guaranteed job','limited seats','small batches','QUB','Queen’s','mailto:','cdn.tailwindcss.com','@tailwindcss/browser']:
  if forbidden.lower() in text.lower():issues.append((rel,'Forbidden claim/runtime',forbidden))
 if re.search(r'100%\s+placement(?!\s+assistance)', text, re.I):issues.append((rel,'Forbidden claim/runtime','100% placement'))
 if 'Employment is not guaranteed.' not in visible:issues.append((rel,'Missing disclaimer'))
 if "Infinity Vision is not affiliated with Queen's University Belfast." not in visible:issues.append((rel,'Missing QUB footer line'))
 if visible.count("Queen's")!=(2 if rel=='courses/data-analytics/index.html' else 1):issues.append((rel,'Queen\'s mentioned outside the disclaimer'))
 if rel.startswith('courses/') and rel!='courses/index.html' and 'Placement assistance means support with the process, not a promised job. Employment is not guaranteed.' not in visible:issues.append((rel,'Missing honesty line'))
 if f'<link rel="canonical" href="https://infyvision.xyz/{rel[:-10]}">' not in text:issues.append((rel,'Canonical'))
 for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text):
  try:
   g=json.loads(blk)['@graph'];types=[x['@type'] for x in g]
   if 'EducationalOrganization' not in types:issues.append((rel,'Org schema'))
   if rel!='index.html' and 'BreadcrumbList' not in types:issues.append((rel,'Breadcrumb schema'))
   if rel.startswith('courses/') and rel!='courses/index.html' and 'Course' not in types:issues.append((rel,'Course schema'))
   if 'timeRequired' in blk:issues.append((rel,'timeRequired'))
  except Exception as e:issues.append((rel,'Bad JSON-LD',str(e)))
 if 'E-2, 359 Arera Colony Bhopal' not in visible:issues.append((rel,'Address'))
 for t,a in page.tags:
  if t=='form' and (a.get('action')!='/api/enquiry' or a.get('method')!='post'):issues.append((rel,'Form must POST to /api/enquiry',a.get('action')))
  if t=='form' and 'data-enquiry-form' not in a:issues.append((rel,'Form missing enhancement hook'))
 for tag,key,url in page.refs:
  if url.startswith('tel:'):
   tel+=1
   if url!='tel:+919098372445':issues.append((rel,'Bad phone link',url))
   continue
  u=urlsplit(url)
  if u.scheme in ['https','http']:
   if u.netloc=='www.google.com' and u.path.startswith('/maps'):continue
   if tag=='link' and u.netloc=='infyvision.xyz':continue
   if u.netloc=='wa.me':
    wa+=1
    if u.path!='/919098372445':issues.append((rel,'Wrong WhatsApp',url))
   else:issues.append((rel,'Unexpected external dependency/link',url))
   continue
  if u.scheme:continue
  if u.path.startswith('/api/'):continue
  target=((OUT/unquote(u.path).lstrip('/')) if u.path.startswith('/') else (p.parent/unquote(u.path))).resolve() if u.path else p
  if target.is_dir():target=target/'index.html'
  if not target.is_relative_to(OUT):issues.append((rel,'Outside publish',url));continue
  links+=1
  if not target.exists():issues.append((rel,'Missing route/asset',url))
  elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:issues.append((rel,'Missing fragment',url))
 for tag,attrs in page.tags:
  if tag=='a' and attrs.get('target')=='_blank' and 'noopener' not in attrs.get('rel',''):issues.append((rel,'Unsafe blank target'))
  if tag=='button' and attrs.get('type') not in ('button','submit'):issues.append((rel,'Unspecified button type'))
  if tag=='img' and 'alt' not in attrs:issues.append((rel,'Missing alt'))
 # Every new programme page and homepage labels development.
 if rel=='index.html' and 'In development' not in visible:issues.append((rel,'Missing mini-course development label'))
 if (rel=='index.html' or rel.startswith('courses/')) and 'New' not in visible and 'excel' not in rel:issues.append((rel,'Missing New label'))
 for old in ['courses/digital/','courses/web/','courses/marketing-analytics/','courses/data-business-analytics/','courses/tally/']:
  if old in text:issues.append((rel,'Link to retired slug',old))
 if 'Currently advertised' in visible or 'Running now' in visible:issues.append((rel,'Running-status claim'))
css=(OUT/'assets/site.css').read_text();js=(OUT/'assets/site.js').read_text()
for name in re.findall(r'url\([\'\"]?([^\)\'\"]+)',css):
 if not name.startswith(('data:','%23','#')) and not (OUT/'assets'/name).exists():issues.append(('CSS','Missing asset',name))
assert 'tailwindcss v4.3.5' in css,'Tailwind compilation banner missing'
assert 'prefers-reduced-motion' in css and 'rv-failsafe' in css
assert 'backdrop-filter' not in css and 'perspective' not in css and 'rotateX' not in css,'No blur/tilt'
assert 'IntersectionObserver' in js and 'requestAnimationFrame' in js
assert 'eval(' not in js and 'localStorage' not in js and 'fetch("/api/enquiry"' in js
home=pages[OUT/'index.html'];hometext=(OUT/'index.html').read_text()
assert len([1 for t,a in home.tags if 'data-course-card' in a])==5
assert hometext.count('class="card mini-card"')==4
order=[hometext.index('class="card course-card" id="'+s+'"') for s in ['data-analytics','performance-marketing','full-stack','tally-gaap-ifrs','excel']]
assert order==sorted(order),'Main course order wrong'
for needle in ['Excel Reporting Clinic','SQL Foundations','Power BI/DAX Foundations','GA4 Basics','Performance Marketing &amp; Analytics','Web &amp; App Development (Full Stack)','Tally with US GAAP &amp; IFRS','Roles you can apply for','Tools you practise in our Bhopal classroom include Excel, SQL, Power BI, Google Ads, Meta Ads, GA4, Tally Prime, HTML, CSS and React.']:
 assert needle in hometext,needle
assert hometext.count('WhatsApp us')>=5 and hometext.count('View syllabus')>=5
for pth in pages:
  if 'courses' in str(pth): assert 'Roles you can apply for' in pth.read_text() and 'Key topics' in pth.read_text(), pth
red=(OUT/'_redirects').read_text()
hdr=(OUT/'_headers').read_text();assert "form-action 'self' https://wa.me" in hdr and "connect-src 'self'" in hdr,'CSP'
import json as _j;opts=_j.loads((ROOT/'src/form-options.json').read_text())
assert opts['courses'][:4]==['Data Analytics','Performance Marketing & Analytics','Web & App Development (Full Stack)','Tally with US GAAP & IFRS'] and len(opts['courses'])==10,opts
for c in opts['courses']:assert 'value="'+c.replace('&','&amp;')+'"' in hometext,c
for pth in pages:
  if 'privacy' in str(pth):continue
  t=pth.read_text();assert t.count('data-enquiry-form')==1 and 'name="consent"' in t and ' required' in t.split('name="consent"')[1][:40] and all(f'name="{f}"' in t for f in ['name','phone','course','level','preferred_time','message','website','source_page']) and 'data-wa-fallback' in t,pth
for o,n in [('digital','performance-marketing'),('marketing-analytics','performance-marketing'),('web','full-stack'),('data-business-analytics','data-analytics'),('tally','tally-gaap-ifrs')]:
  assert f'/courses/{o}/ /courses/{n}/ 301' in red and (OUT/'courses'/n/'index.html').exists()
assert (OUT/'robots.txt').read_text()=='User-agent: *\nAllow: /\n\nSitemap: https://infyvision.xyz/sitemap.xml\n'
sm=(OUT/'sitemap.xml').read_text();assert sm.count('<loc>')==len(pages),sm
for o,n in [('advanced-excel','excel'),('tally-erp-gst','tally-gaap-ifrs'),('us-gaap-ifrs-xero','tally-gaap-ifrs'),('digital-marketing','performance-marketing'),('front-end-development','full-stack'),('full-stack-development','full-stack'),('data-analytics','data-analytics'),('business-analytics','data-analytics'),('app-development','full-stack')]:
  pass  # /programs/* redirects live in src/worker.js, tested in tools/test-worker.mjs
assert 'FAQPage' in (OUT/'faq/index.html').read_text()
for pg in ['placement','how-it-works','faculty','faq','contact','courses','privacy']:assert (OUT/pg/'index.html').exists(),pg
faculty=(OUT/'faculty/index.html').read_text()
for bad in ['IIT','CA ','years of experience','Queen']:assert bad not in faculty.split('<footer')[0],bad
files=list(OUT.rglob('*'));assert not any(p.name in ['package.json','package-lock.json','node_modules','BUILD-REVIEW.md'] for p in files)
report={'pages':len(pages),'local_references_checked':links,'telephone_links':tel,'whatsapp_links':wa,'issues':issues,'html_word_counts':{str(p.relative_to(OUT)):len(' '.join(v.text).split()) for p,v in pages.items()},'assets_bytes':{str(p.relative_to(OUT)):p.stat().st_size for p in (OUT/'assets').iterdir()}}
(ROOT/'VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert not issues,issues
