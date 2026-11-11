# Infinity Vision website (Cloudflare Workers)

Offline-first institute site for **Infinity Vision**, Bhopal (call/WhatsApp 9098372445). The current centre address is in `tools/institute.py` so a move is a one-file change.
Static pages are generated from Python content files, styled with locally compiled Tailwind v4, and served by a
Cloudflare **Worker with static assets**. A small API stores enquiries in **D1**.

- Preview URL: https://infyvision-site.sourabhpurohit86.workers.dev (workers.dev only, `noindex`)
- No custom domain or route is attached. `infyvision.xyz` is still served by the old Pages project `infyvision`.

## Layout
| Path | What |
| --- | --- |
| `tools/courses_v4.py`, `tools/content.py` | Course lineup and all copy (edit content here) |
| `tools/generate.py` | HTML templates. Also writes `_redirects`, `_headers`, `404.html` and `src/form-options.json` |
| `src/input.css`, `src/site.js` | Design system and browser JS (particles, typed hero, reveals, course tabs, enquiry form) |
| `src/worker.js` | Worker: `/api/*` handlers, all other requests go to static assets |
| `src/form-options.json` | Allowed course / time / level values (generated, committed so the Worker always has it) |
| `migrations/` | D1 schema |
| `wrangler.jsonc` | Worker config (assets dir `./public`, `run_worker_first: ["/api/*"]`, 404 page) |
| `tools/validate.py`, `tools/test-interactions.mjs`, `tools/test-worker.mjs` | Content rules, DOM tests, Worker unit tests |
| `tools/smoke.sh` | End-to-end check of a deployed URL (creates 1 TEST row; delete it afterwards) |

`public/` (the build output) is **not committed**; `npm run build` recreates it.

## Build and test
```sh
npm ci
npm run build      # -> ./public
npm run validate   # content/claim rules, JS syntax, DOM + Worker tests, html-validate
npm run dev        # local Worker + local D1 at http://localhost:8787 (needs .dev.vars with ADMIN_TOKEN, IP_HASH_SALT)
```

## Deploy (workers.dev)
```sh
export CLOUDFLARE_ACCOUNT_ID=c54b2aac75854ed1ee968d78ace982c3
npm run deploy     # build + validate + D1 migrations (remote) + wrangler deploy
tools/smoke.sh https://infyvision-site.sourabhpurohit86.workers.dev
npx wrangler d1 execute infyvision-enquiries --remote --command "DELETE FROM enquiries WHERE name LIKE 'TEST%' AND phone='9000000000'"
```
Secrets (already set; set again only to rotate): `npx wrangler secret put ADMIN_TOKEN`, `npx wrangler secret put IP_HASH_SALT`.

## Redirects and headers
`public/_redirects` and `public/_headers` are applied by Workers static assets (same format as Pages). Old course
URLs (`/courses/digital/`, `/courses/marketing-analytics/`, `/courses/web/`, `/courses/data-business-analytics/`,
`/courses/tally/`, with or without trailing slash or `index.html`) return 301 to the new pages. `_headers` sets CSP
(`connect-src 'self'`, `form-action 'self' https://wa.me`), nosniff, referrer and permissions policies, and `noindex`
while this is a preview. `_headers` does not apply to Worker responses, so the Worker sets its own headers on `/api/*`.

## Enquiry API
**`POST /api/enquiry`** (JSON or form-encoded; no-JS form posts get a small HTML reply)
fields: `name` (2-80 chars), `phone` (Indian mobile, 10 digits starting 6-9; `+91`/`0` prefixes and spaces ok),
`course` (one of `src/form-options.json` courses), `preferred_time` (one of the listed times), optional `level`, `message` (600 chars), `source_page` (a page path, or `guide:<slug>` when someone requests the free intro PDF).
Course pages also have a compact name-and-phone form for the printable intro guide; those rows use `source_page` like `guide:data-analytics` and appear in `/api/enquiries/unsynced` with the other enquiries.
PDFs are generated at build time by `tools/build_guides.py` into `public/guides/<slug>.pdf`.
Protection: same-origin check, hidden honeypot field `website` (filled = silently dropped), 8 KB body cap, and a rate limit of
5 enquiries per hashed IP per 10 minutes (`RATE_LIMIT_MAX`, `RATE_LIMIT_WINDOW_MINUTES`). IPs are stored only as a salted SHA-256 hash.
Turnstile is not used (it would add a third-party script and a widget to manage); add it if spam appears.

Stored in D1 `infyvision-enquiries`, table `enquiries`; `created_at` is ISO 8601 in IST (`…+05:30`).

**Admin endpoints** (Bearer token = `ADMIN_TOKEN` secret; local copy in `.secrets/admin_token`, never committed):
```sh
TOKEN=$(cat .secrets/admin_token)
curl -H "Authorization: Bearer $TOKEN" "https://infyvision-site.sourabhpurohit86.workers.dev/api/enquiries/unsynced?limit=100"
curl -X POST -H "Authorization: Bearer $TOKEN" -H 'content-type: application/json' \
  -d '{"ids":[1,2,3]}' https://infyvision-site.sourabhpurohit86.workers.dev/api/enquiries/mark-synced
```
Use these to copy new enquiries into the Google Sheet, then mark them synced.

## CI
`.github/workflows/deploy.yml` builds and validates on every push/PR. It deploys only when the repository has a
`CLOUDFLARE_API_TOKEN` secret (a Cloudflare API token with *Workers Scripts: Edit* and *D1: Edit* on this account). Not set yet.
