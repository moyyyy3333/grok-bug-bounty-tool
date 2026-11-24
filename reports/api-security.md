# Ranked Digest: Top 5 Bugcrowd Programs with API Scope

**Date:** 2026-11-24  
**Method:** Public web search, program briefs, API documentation review, and safe read-only unauthenticated GET probes only. No exploitation, no authentication bypass attempts, no write operations, no submissions.

## Scoring Methodology
Scores (0-10) based on public signals for:
- **Auth weakness signals** (clear error messages revealing scheme, weak/default auth patterns, potential for IDOR/mass assignment on documented endpoints)
- **Missing / weak rate limiting** (absent headers or documented high limits)
- **Verbose error leakage** (detailed JSON/text errors on unauth or invalid requests)

Higher score = more interesting for further authorized research (not a vulnerability finding).

## Top 5 Ranked Targets

### 1. PlanetHoster Bug Bounty (Score: 8.2)
- **Program:** https://bugcrowd.com/engagements/planethosterinc
- **Base URLs:** `https://api.planethoster.net/v4` (Domain/Reseller), World API endpoints
- **Auth scheme:** API user + API key in HTTP headers + mandatory IP whitelist
- **Rate limits:** Not publicly documented; requires IP whitelist for access
- **Endpoint patterns:** Extensive REST (GET/POST/PUT/PATCH/DELETE) for domains (`/domain/*`), hostings (`/hosting/*`), DNS, SSL, SSH keys, N0C storage. Public OpenAPI-style docs at https://apidoc.planethoster.com/v4/en/
- **Safe probe evidence:** Unauthenticated requests to `/v4/hello` timed out (consistent with IP whitelist / restrictive access). Documented endpoints support resource ID parameters → high IDOR/mass assignment surface once authenticated.
- **Signals:** Strong auth (IP + keys) but rich documented attack surface for BOLA/IDOR and mass assignment on account/domain/hosting objects. Verbose docs aid reconnaissance.

### 2. Gearset Managed Bug Bounty (Score: 7.5)
- **Program:** https://bugcrowd.com/engagements/gearset-mbb
- **Base URLs:** `https://api.gearset.com` and staging `https://staging-api.gearset.com`
- **Auth scheme:** `Authorization: token <APIToken>` header (plus optional `api-version` header)
- **Rate limits:** Not publicly documented in snippets
- **Endpoint patterns:** Public Automation, Reporting, Auditing APIs (e.g. `/public/automation/continuous-integration-jobs/{id}/status`, reporting DORA metrics). Documented in Gearset Help Center.
- **Safe probe evidence:** Unauthenticated GET returned `401 Missing or badly formatted Authorization header.` — clear scheme leakage.
- **Signals:** Explicit token scheme in errors; staging environment available; endpoints take resource IDs → IDOR potential. Good candidate for auth bypass / token validation testing under program rules.

### 3. Bugcrowd Platform API (own program) (Score: 6.8)
- **Program:** https://bugcrowd.com/engagements/bugcrowd (api.bugcrowd.com explicitly in scope)
- **Base URL:** `https://api.bugcrowd.com`
- **Auth scheme:** `Authorization: Token <key:secret>` + `Accept: application/vnd.bugcrowd+json`
- **Rate limits:** 60 requests/minute per IP (confirmed via `x-ratelimit-limit: 60` / `x-ratelimit-remaining` headers)
- **Endpoint patterns:** JSON:API style (`/programs`, `/submissions`, `/engagements`, etc.) with sparse fieldsets and includes.
- **Safe probe evidence:** Unauthenticated GET `/programs` → `401` with JSON `{"errors":[{"detail":"Invalid or missing authentication credentials.","title":"Unauthorized","status":"401"}]}`. Rate-limit headers present and decrementing. Invalid path still returns same 401 (no extra leakage).
- **Signals:** Proper rate limiting and consistent auth errors. Moderate verbose leakage (reveals expected format). Lower interest due to strong controls, but useful as a reference for JSON:API patterns.

### 4. Rapyd Bug Bounty (Score: 6.4)
- **Program:** https://bugcrowd.com/engagements/rapyd
- **Base URLs:** `api.rapyd.net` (explicitly in scope), plus dashboard/verify/checkout hosts
- **Auth scheme:** Not fully public in brief snippets; fintech API typically uses access keys / signatures (common for Rapyd)
- **Rate limits:** Program requires `X-Bugcrowd` header with username on all requests
- **Endpoint patterns:** Core payment/fintech APIs (high reward for critical API findings). Docs.rapyd.net is out of scope.
- **Safe probe evidence:** Unauthenticated GET to root returned `404 Not Found` (Cloudflare). No verbose stack traces.
- **Signals:** High-value fintech surface, program explicitly prioritizes API findings with potential increased rewards. Auth scheme not leaked in root probe. Good for authenticated IDOR/mass assignment once credentials obtained under rules.

### 5. USAA Bug Bounty (Score: 5.9)
- **Program:** https://bugcrowd.com/engagements/usaa
- **Base URLs:** `api.usaa.com`, `api-a.usaa.com`, `b2bapi.usaa.com`, `mapi.usaa.com`, `vlapi.usaa.com`, `ws.usaa.com` and others (Akamai CDN)
- **Auth scheme:** Not detailed in public brief excerpts; typical enterprise (likely OAuth/JWT/session)
- **Rate limits:** Not publicly documented
- **Endpoint patterns:** Multiple dedicated API hosts tagged "API Testing"
- **Safe probe evidence:** Unauthenticated GET to `https://api.usaa.com/` returned `403` (Akamai/Honesty server). Minimal body leakage.
- **Signals:** Broad API surface across several hosts. Strong edge protection (403). Lower immediate leakage; higher interest once authenticated testing is allowed.

## Summary Observations
- Most programs enforce authentication before meaningful responses (good).
- PlanetHoster and Gearset provide the richest public documentation of endpoint patterns, making them the highest priority for structured IDOR / mass-assignment / auth-bypass research under safe-harbor rules.
- Rate-limit signals were strongest (and positive) on the Bugcrowd platform API itself.
- No clear unauthenticated data exposure or missing rate limits observed in the limited safe probes performed.
- All testing was strictly read-only and unauthenticated. Further work requires program enrollment and adherence to each brief’s rules.

**Disclaimer:** This is reconnaissance and scoring only. No vulnerabilities were confirmed or exploited. Researchers must follow each program’s scope, safe harbor, and testing guidelines.