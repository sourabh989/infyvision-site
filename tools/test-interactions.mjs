// DOM-only regression tests. This is not a browser, layout renderer, or visual audit.
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {Window} from 'happy-dom';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..');
const html=fs.readFileSync(path.join(root,'public/index.html'),'utf8');
const script=fs.readFileSync(path.join(root,'public/assets/site.js'),'utf8');
const checks=[];
function setup(reduced=false){
 const w=new Window({url:'http://localhost:8794/'});
 const animations=[];const observers=[];const warnings=[];const listeners=[];
 w.matchMedia=query=>({matches:query.includes('prefers-reduced-motion')?reduced:false,media:query,addEventListener:(type,cb)=>{if(query.includes('prefers-reduced-motion'))listeners.push(cb)},removeEventListener(){}});
 w.HTMLElement.prototype.animate=function(frames,options){animations.push({frames,options});return {finished:Promise.resolve(),cancel(){}}};
 w.IntersectionObserver=class{constructor(cb){this.cb=cb;observers.push(this)}observe(target){this.cb([{target,isIntersecting:true}])}unobserve(){}disconnect(){}};
 w.console.warn=(...args)=>warnings.push(args);
 w.document.write(html);
 // Avoid resource loading: scripts do not execute until this explicit local evaluation.
 w.eval(script);
 assert.equal(warnings.length,0,'Enhancement setup errors: '+JSON.stringify(warnings));
 return {w,d:w.document,animations,listeners};
}
const plain=new Window();plain.document.write(html);
assert.equal(plain.document.querySelectorAll('[data-course-card]:not([hidden])').length,9);
assert.equal(plain.document.querySelectorAll('.mini-course').length,4);
assert.equal(plain.document.querySelectorAll('[data-reveal][hidden]').length,0);
assert.deepEqual([...plain.document.querySelectorAll('[data-group=main] .course-card h3')].map(h=>h.textContent),['Data Analytics','Performance Marketing & Analytics','Web & App Development (Full Stack)','Tally with US GAAP & IFRS']);
checks.push('No-JS source: 9 course cards (4 main in owner order + Advanced Excel + 4 minis), 4 what’s-new cards and core copy remain available; only optional controls start hidden.');
const {w,d,animations,listeners}=setup();
const toggle=d.querySelector('.menu-toggle');const nav=d.querySelector('#navigation');
assert.equal(toggle.hidden,false);toggle.click();assert.equal(toggle.getAttribute('aria-expanded'),'true');assert(nav.classList.contains('is-open'));
d.dispatchEvent(new w.KeyboardEvent('keydown',{key:'Escape',bubbles:true}));assert.equal(toggle.getAttribute('aria-expanded'),'false');assert.equal(d.activeElement,toggle);
toggle.click();nav.querySelector('a').click();assert.equal(toggle.getAttribute('aria-expanded'),'false');
checks.push('Mobile-nav state: open, close on Escape with focus return, close on link activation.');
const sizes={all:9,main:4,short:5};
for(const button of d.querySelectorAll('[data-filter]')){
 button.click();const visible=[...d.querySelectorAll('[data-group]')].filter(g=>!g.hidden).flatMap(g=>[...g.querySelectorAll('.course-card')]);
 assert.equal(visible.length,sizes[button.dataset.filter]);
 assert.equal(button.getAttribute('aria-pressed'),'true');
 assert.equal(d.querySelectorAll('[data-filter][aria-pressed="true"]').length,1);
 assert.match(d.querySelector('#filter-status').textContent,/shown/);
}
d.querySelector('[data-filter="all"]').click();
checks.push('All three course tabs (9 cards: 4 main in owner order, 5 short): matching cards, aria-pressed and live result count.');
const expect={reporting:{starter:'excel',experienced:'data-analytics'},marketing:{starter:'performance-marketing',experienced:'performance-marketing'},web:{starter:'full-stack',experienced:'full-stack'},accounting:{starter:'tally-gaap-ifrs',experienced:'tally-gaap-ifrs'}};
for(const goal of Object.keys(expect))for(const level of ['starter','experienced']){
 const input=d.querySelector(`input[name="goal"][value="${goal}"]`);input.checked=true;
 d.querySelector(`input[name="level"][value="${level}"]`).checked=true;
 input.dispatchEvent(new w.Event('change',{bubbles:true}));
 const result=d.querySelector('#finder-result');const link=result.querySelector('a');
 assert.equal(link.getAttribute('href'),`courses/${expect[goal][level]}/index.html`);
 assert(result.textContent.includes('Enquire for next batch'));
 assert(fs.existsSync(path.join(root,'public',link.getAttribute('href'))));
}
checks.push('All eight goal/level combinations route to the new lineup pages with neutral next-batch labels.');
const motion=d.querySelector('.motion-control');assert(motion);assert.equal(motion.hidden,false);motion.click();assert.equal(motion.getAttribute('aria-pressed'),'true');assert(d.querySelector('.hero').classList.contains('motion-paused'));motion.click();assert.equal(motion.getAttribute('aria-pressed'),'false');
assert(animations.length>0);
assert(d.documentElement.classList.contains('js-motion'));
const form=d.querySelector('[data-enquiry-form]');assert(form);
assert.equal(form.querySelector('[data-source-page]').value,'/');
let opened='';w.open=(u)=>{opened=u;return {}};
const calls=[];let reply={status:200,body:{ok:true,id:1}};
w.fetch=async(url,opts)=>{calls.push({url,opts});return {ok:reply.status<300,status:reply.status,json:async()=>reply.body}};
const flush=()=>new Promise(r=>setTimeout(r,20));
const status=form.querySelector('[data-form-status]');
// invalid phone: no request, error state
form.querySelector('#c-name').value='Test Learner';form.querySelector('#c-phone').value='12345';
form.dispatchEvent(new w.Event('submit',{bubbles:true,cancelable:true}));await flush();
assert.equal(calls.length,0);assert.equal(status.hidden,false);assert.equal(status.dataset.state,'error');assert.equal(form.querySelector('#c-phone').getAttribute('aria-invalid'),'true');
// valid: posts JSON to /api/enquiry with normalised phone, success state
form.querySelector('#c-phone').value='+91 98765-43210';form.querySelector('#c-course').value='Data Analytics';
form.dispatchEvent(new w.Event('submit',{bubbles:true,cancelable:true}));await flush();
assert.equal(calls.length,1);assert.equal(calls[0].url,'/api/enquiry');assert.equal(calls[0].opts.method,'POST');
const sent=JSON.parse(calls[0].opts.body);assert.equal(sent.phone,'9876543210');assert.equal(sent.name,'Test Learner');assert.equal(sent.course,'Data Analytics');assert.equal(sent.website,'');assert.equal(sent.source_page,'/');
assert.equal(status.dataset.state,'success');assert(form.querySelector('[data-form-fields]').hidden);assert(status.textContent.includes('98765 43210'));
// WhatsApp fallback composes the prefilled message
form.querySelector('[data-wa-fallback]').click();
assert(opened.startsWith('https://wa.me/919098372445?text='));assert(decodeURIComponent(opened).includes('Name: Test Learner'));assert(decodeURIComponent(opened).includes('Mobile: +91 98765-43210'));
checks.push('Enquiry form: rejects invalid mobile without a request; POSTs JSON to /api/enquiry with normalised 10-digit phone, honeypot and source page; shows success state.');
// server error -> error state, fallback offered
{const e=setup();const f2=e.d.querySelector('[data-enquiry-form]');e.w.fetch=async()=>({ok:false,status:429,json:async()=>({ok:false,error:'Too many enquiries from this connection.'})});
f2.querySelector('#c-name').value='Test Learner';f2.querySelector('#c-phone').value='9876543210';f2.dispatchEvent(new e.w.Event('submit',{bubbles:true,cancelable:true}));await flush();
const st=f2.querySelector('[data-form-status]');assert.equal(st.dataset.state,'error');assert(st.textContent.includes('WhatsApp'));assert(!f2.querySelector('[data-form-fields]').hidden);assert(f2.classList.contains('is-error'));assert.equal(f2.querySelector('[data-submit]').disabled,false);
checks.push('Enquiry form: server rejection shows an error state, keeps the fields and points to the WhatsApp fallback.');await e.w.happyDOM.close();}
checks.push('Motion: genuine Web Animations calls, hero pause/resume state, static visible baseline.');
const reduce=setup(true);assert.equal(reduce.animations.length,0);assert(!reduce.d.documentElement.classList.contains('js-motion'));assert.equal(reduce.d.querySelectorAll('[data-reveal]:not(.is-in)').length,0);assert.equal(reduce.d.querySelector('.motion-control').hidden,true);assert(!reduce.d.querySelector('.hero').classList.contains('motion-active'));
checks.push('Reduced motion: zero scripted entrance animations, no ambient class, no unnecessary pause control.');
for(const details of d.querySelectorAll('.mini-course,.module,.faq-item,.comparison')){details.open=true;assert(details.open);assert(details.querySelector('summary'));details.open=false;assert(!details.open)}
checks.push('Expanders and comparison use native details/summary open state; keyboard behaviour requires browser verification.');
console.log(checks.map((x,i)=>`PASS ${i+1}: ${x}`).join('\n'));
fs.writeFileSync(path.join(root,'INTERACTION-TESTS.txt'),checks.map(x=>'PASS '+x).join('\n')+'\nDOM-only. No browser/visual verification.\n');
await w.happyDOM.close();await reduce.w.happyDOM.close();await plain.happyDOM.close();
