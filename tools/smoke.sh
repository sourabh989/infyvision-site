#!/usr/bin/env bash
# Smoke test a running deployment: tools/smoke.sh https://infyvision-site.<subdomain>.workers.dev
# Reads the admin token from .secrets/admin_token (never printed). Creates ONE row marked TEST and prints its id.
set -uo pipefail
BASE="${1:?base url}"; TOKEN_FILE="${TOKEN_FILE:-.secrets/admin_token}"
C=(curl -s --noproxy '*' --max-time 20)
fail=0; ok(){ echo "PASS $*"; }; bad(){ echo "FAIL $*"; fail=1; }
code(){ "${C[@]}" -o /dev/null -w '%{http_code}' "$@"; }
for p in / /courses/ /placement/ /how-it-works/ /faculty/ /faq/ /contact/ /privacy/ /sitemap.xml /courses/data-analytics/ /courses/performance-marketing/ /courses/full-stack/ /courses/tally-gaap-ifrs/ /courses/excel/ /assets/site.css /assets/site.js /robots.txt; do
  c=$(code "$BASE$p"); [ "$c" = 200 ] && ok "GET $p 200" || bad "GET $p -> $c"; done
for pair in digital:performance-marketing marketing-analytics:performance-marketing web:full-stack data-business-analytics:data-analytics tally:tally-gaap-ifrs; do
  o=${pair%%:*}; n=${pair#*:}
  for src in "/courses/$o/" "/courses/$o" "/courses/$o/index.html"; do
    out=$("${C[@]}" -o /dev/null -w '%{http_code} %{redirect_url}' "$BASE$src")
    [[ "$out" == "301 "*"/courses/$n/" ]] && ok "redirect $src -> /courses/$n/" || bad "redirect $src -> $out"; done; done
c=$(code "$BASE/no-such-page/"); [ "$c" = 404 ] && ok "unknown page 404 (custom 404 page)" || bad "unknown page -> $c"
h=$("${C[@]}" -D - -o /dev/null "$BASE/"); echo "$h" | grep -qi "form-action 'self' https://wa.me" && echo "$h" | grep -qi "connect-src 'self'" && echo "$h" | grep -qi 'x-content-type-options: nosniff' && ok "security headers (CSP form-action 'self' + wa.me)" || bad "security headers"
c=$(code "$BASE/api/enquiries/unsynced"); [ "$c" = 401 ] && ok "unsynced without token 401" || bad "unsynced no token -> $c"
c=$(code -H 'authorization: Bearer wrong' "$BASE/api/enquiries/unsynced"); [ "$c" = 401 ] && ok "unsynced wrong token 401" || bad "wrong token -> $c"
c=$(code "$BASE/api/enquiry"); [ "$c" = 405 ] && ok "GET /api/enquiry 405" || bad "GET enquiry -> $c"
c=$(code -X POST -H 'content-type: application/json' -d '{"name":"TEST bad","phone":"12345","course":"Data Analytics","preferred_time":"Weekend"}' "$BASE/api/enquiry"); [ "$c" = 422 ] && ok "invalid phone 422" || bad "invalid phone -> $c"
c=$(code -X POST -H 'content-type: application/json' -d '{"name":"TEST bad","phone":"9876543210","course":"Hacking 101","preferred_time":"Weekend"}' "$BASE/api/enquiry"); [ "$c" = 422 ] && ok "unknown course 422" || bad "unknown course -> $c"
c=$(code -X POST -H 'content-type: application/json' -H 'origin: https://evil.example' -d '{}' "$BASE/api/enquiry"); [ "$c" = 403 ] && ok "cross-origin 403" || bad "cross-origin -> $c"
r=$("${C[@]}" -X POST -H 'content-type: application/json' -d '{"name":"TEST honeypot","phone":"9876543210","course":"Data Analytics","preferred_time":"Weekend","website":"spam"}' "$BASE/api/enquiry"); [[ "$r" == '{"ok":true}' ]] && ok "honeypot silently accepted, not stored" || bad "honeypot -> $r"
r=$("${C[@]}" -X POST -H 'content-type: application/json' -H "origin: $BASE" -d '{"name":"TEST - automated smoke test (delete me)","phone":"+91 90000 00000","course":"Data Analytics","level":"Complete beginner","preferred_time":"Weekday evening","message":"TEST entry from deployment smoke test. Not a real enquiry.","source_page":"/smoke-test"}' "$BASE/api/enquiry")
id=$(echo "$r" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("id",""))' 2>/dev/null)
[ -n "$id" ] && ok "TEST enquiry stored id=$id ($r)" || bad "TEST enquiry -> $r"
TOKEN=$(cat "$TOKEN_FILE")
u=$("${C[@]}" -H "authorization: Bearer $TOKEN" "$BASE/api/enquiries/unsynced?limit=500")
echo "$u" | python3 -c "import sys,json;d=json.load(sys.stdin);r=[e for e in d['enquiries'] if e['id']==$id];assert r and r[0]['phone']=='9000000000' and r[0]['created_at'].endswith('+05:30') and not any(e['name']=='TEST honeypot' for e in d['enquiries']);print('row',json.dumps(r[0]))" && ok "TEST row visible in unsynced (phone normalised, IST timestamp, honeypot absent)" || bad "unsynced listing"
m=$("${C[@]}" -X POST -H "authorization: Bearer $TOKEN" -H 'content-type: application/json' -d "{\"ids\":[$id]}" "$BASE/api/enquiries/mark-synced")
[[ "$m" == '{"ok":true,"updated":1}' ]] && ok "mark-synced updated 1" || bad "mark-synced -> $m"
u=$("${C[@]}" -H "authorization: Bearer $TOKEN" "$BASE/api/enquiries/unsynced?limit=500")
echo "$u" | python3 -c "import sys,json;d=json.load(sys.stdin);assert not [e for e in d['enquiries'] if e['id']==$id]" && ok "row no longer unsynced" || bad "still unsynced"
unset TOKEN
echo "TEST_ROW_ID=$id"
exit $fail
