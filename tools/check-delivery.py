"""HTTP/asset checks, gzip budgets and a small declared-token contrast audit (not a visual audit)."""
from pathlib import Path
from urllib.request import urlopen
import json,gzip,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'public'
http=[]
for p in OUT.rglob('*'):
 if not p.is_file() or p.name.startswith('_'):continue
 route='/'+str(p.relative_to(OUT))
 with urlopen('http://127.0.0.1:8794'+route,timeout=5) as r:
  assert r.status==200;body=r.read();assert body==p.read_bytes();http.append({'route':route,'status':r.status,'mime':r.headers.get_content_type()})
def luminance(s):
 vals=[int(s[i:i+2],16)/255 for i in (1,3,5)];vals=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in vals]
 return sum(v*w for v,w in zip(vals,[.2126,.7152,.0722]))
def contrast(a,b):
 x,y=sorted([luminance(a),luminance(b)]);return (y+.05)/(x+.05)
pairs=[('Primary body','#12131b','#f6f5f1'),('Muted body','#575965','#f6f5f1'),('White cards body','#575965','#ffffff'),('Violet text','#6542cf','#f6f5f1'),('Dark hero body','#b9b8c8','#12131b'),('Lime CTA text','#12131b','#d5fb73'),('Lavender finder body','#574b6a','#e9e3f5'),('Career body','#c3bece','#14151d'),('Mini course body','#cbc3d8','#22202b'),('New-programme copy','#c7c0d5','#24222f')]
checks=[{'token':name,'foreground':a,'background':b,'ratio':round(contrast(a,b),2),'AA_normal':contrast(a,b)>=4.5} for name,a,b in pairs]
assert all(c['AA_normal'] for c in checks)
report={'http':http,'declared_contrast_tokens':checks,'gzip_bytes':{p.name:len(gzip.compress(p.read_bytes())) for p in [OUT/'assets/site.css',OUT/'assets/site.js']},'limitations':'No rendered layout, actual computed-style, screen-reader, browser or Core Web Vitals verification.'}
(ROOT/'DELIVERY-CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
