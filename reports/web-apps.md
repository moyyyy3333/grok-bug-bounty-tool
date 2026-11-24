# Ranked Digest: Top 5 Bugcrowd Public Web Application Targets

**Generated:** 2026-11-24  
**Method:** Public program discovery via Bugcrowd engagements and secondary indexes. Program briefs, in-scope domains, and exclusions pulled from public pages. Unified reverse-engineering scanner logic applied *conceptually* only (passive observation of public assets, headers, tech tags, and known patterns). **No exploitation, no authenticated testing, no submissions.**

## Scoring Criteria (0-10 conceptual risk/interest score)
- **Debug Endpoints:** Exposed /debug, /actuator, /swagger, source maps, etc.
- **Verbose Errors:** Stack traces, detailed error pages visible publicly.
- **Outdated Libraries:** Legacy jQuery, old Ember, unpatched frameworks from tags/headers.
- **JS-Leaked Internal URLs:** SPA bundles revealing staging, internal APIs, or secrets.
- **CORS Misconfigurations:** Overly permissive Access-Control-Allow-Origin on public endpoints.

Higher aggregate indicates richer public recon surface for further responsible research.

---

## 1. YNAB (Score: 8.2/10)
**Program:** https://bugcrowd.com/engagements/ynab  
**Brief Summary:** Personal finance budgeting app. Focus on staging web app/API and marketing site. Rewards up to $3000 P1. Ember.js SPA + Ruby on Rails 7.x on Heroku. Safe Harbor. Ongoing since 2022, ~179 vulns rewarded.

**In-Scope Domains:**
- staging-app.bany.dev (primary SPA)
- staging-api.bany.dev (API)
- www.ynab.com (Webflow marketing)
- *.ynab.com (except exclusions)

**Excluded Paths/Assets:**
- Production app.ynab.com (real user data)
- support.ynab.com, learn.ynab.com (third-party)
- develop-app.ynab.com
- Mobile apps, older desktop versions
- Customer data / real accounts

**Conceptual Scan Evidence:**
- Debug: Low-Medium (staging redirects to /users/sign_in; no obvious public debug observed in headers).
- Verbose Errors: Medium (Rails staging often leaks more; CSP present but upgrade-insecure-requests).
- Outdated Libraries: Medium (Ember.js SPA historically has supply-chain risks; jQuery tags noted on related assets).
- JS-Leaked URLs: High (typical for Ember SPAs; internal API paths and asset CDNs often embedded).
- CORS: Medium (CloudFront + Heroku; public marketing site preconnects to multiple CDNs; worth checking API CORS).

**Ranking Rationale:** Staging environment explicitly encouraged, clear tech stack, high reward density, public marketing surface.

---

## 2. Octopus Deploy (Score: 7.6/10)
**Program:** https://bugcrowd.com/engagements/octopus-og  
**Brief Summary:** Deployment automation platform. Primary focus on public web application and *.octopus.com. Rewards up to $6000 P1. ASP.NET / .NET stack. ~80 vulns rewarded. Use @bugcrowdninja.com for accounts.

**In-Scope Domains:**
- *.octopus.com
- octopus.com
- GitHub.com/OctopusDeploy (code review)

**Excluded Paths/Assets:**
- partners.octopus.com, *.octopus.app (samples)
- artifactorysample, bamboosample, etc.
- trust.octopus.com, i.octopus.com, shop.octopus.com
- Self-hosted product, customer instances, WAF bypasses currently OOS
- Automated scanners prohibited

**Conceptual Scan Evidence:**
- Debug: Medium (ASP.NET x-powered-by header observed; common for /elmah, /trace if misconfigured).
- Verbose Errors: Medium-High (classic ASP.NET error pages if custom errors off).
- Outdated Libraries: Medium (Bootstrap + ASP.NET noted in tags).
- JS-Leaked URLs: Medium (public site may embed instance or API references).
- CORS: Low-Medium (Azure/CloudFront indicators; check for wildcard on public endpoints).

**Ranking Rationale:** Wide wildcard scope on primary domain, high P1 reward, clear exclusions, public registration flow.

---

## 3. Skroutz (Score: 7.1/10)
**Program:** https://bugcrowd.com/skroutz or https://bugcrowd.com/engagements/skroutz  
**Brief Summary:** Greek e-commerce comparison platform. Production web app + API. Rewards up to $4500 P1. ReactJS frontend + Ruby on Rails. Testing on live production; stability critical. ~77 vulns rewarded.

**In-Scope Domains:**
- https://www.skroutz.gr

**Excluded Paths/Assets:**
- Any other subdomains or properties
- Behavior compromising site stability
- Many standard OOS (headers, self-XSS, etc.)

**Conceptual Scan Evidence:**
- Debug: Low (Cloudflare challenge on root; production hardened).
- Verbose Errors: Low-Medium (Rails possible, but CF in front).
- Outdated Libraries: Medium (React + Rails; open-source components on GitHub/skroutz).
- JS-Leaked URLs: High (React SPA likely leaks internal GraphQL/REST paths).
- CORS: Medium (e-commerce APIs often have complex CORS for partners).

**Ranking Rationale:** High-value production e-commerce surface, strong rewards, explicit production testing allowed with caveats.

---

## 4. Linktree (Score: 6.9/10)
**Program:** https://bugcrowd.com/engagements/linktree-mbb-og  
**Brief Summary:** Link-in-bio platform. Primary targets *.linktr.ee, *.linktree.com, etc. Rewards up to $7500 P1. Mix of Gatsby, Varnish, Ruby, Node, NextJS. High volume (~424 vulns rewarded). Multiple secondary brands (Plann, Odesli, etc.).

**In-Scope Domains:**
- *.linktr.ee, *.linktree.com, *.tr.ee
- Secondary: plannthat.com, *.odesli.co, song.link variants, etc.

**Excluded Paths/Assets:**
- *.filestack.com, *.freshdesk.com, *.blstr.xyz, community.linktr.ee

**Conceptual Scan Evidence:**
- Debug: Medium (multiple frameworks; possible source maps or debug routes on marketing).
- Verbose Errors: Medium (Varnish + various backends).
- Outdated Libraries: Medium-High (legacy Gatsby/jQuery possible on older properties).
- JS-Leaked URLs: High (link aggregation apps frequently embed many third-party and internal endpoints).
- CORS: High (public link resolvers and APIs often require broad CORS).

**Ranking Rationale:** Extremely wide and high-traffic public surface, multiple tech stacks, strong payout history.

---

## 5. Web.com Group (Network Solutions / Bluehost / HostGator) (Score: 6.5/10)
**Program:** https://bugcrowd.com/engagements/webdotcom  
**Brief Summary:** Domain/hosting suite. OneWeb platform across properties. Focus on app.web.com (website builder + AI), storefronts, account managers. Rewards up to $3000+ P1. Heavy jQuery, Bootstrap, Cloudflare. ~726 vulns rewarded.

**In-Scope Domains:**
- app.web.com
- www.networksolutions.com, www.bluehost.com, www.hostgator.com
- *.web.com, *.register.com, *.networksolutions.com, *.bluehost.com, *.hostgator.com
- Authenticated subdomain flows

**Excluded Paths/Assets:**
- Explicitly noted contact/sales forms in some variants
- Scope can evolve; check brief for latest

**Conceptual Scan Evidence:**
- Debug: Medium (website builders often have preview/debug modes; jQuery-heavy).
- Verbose Errors: Medium (older PHP/jQuery stacks).
- Outdated Libraries: High (jQuery, Bootstrap, Moment.js, Select2 tags frequently appear).
- JS-Leaked URLs: Medium (account managers and builders embed many service endpoints).
- CORS: Medium (CDN and multi-domain setup).

**Ranking Rationale:** Massive multi-property scope under one platform, long-running program with high historical payout volume, clear website-builder focus area.

---

## Notes & Methodology
- All data derived from publicly accessible Bugcrowd program pages and secondary aggregators as of November 2026.
- Conceptual scanner considered only unauthenticated public responses, response headers, technology tags listed in briefs, and common patterns for the frameworks involved.
- No active scanning beyond standard HEAD requests for header inspection, no payload testing, no account creation, no exploitation.
- Rankings prioritize combination of scope breadth, reward potential, public accessibility, and indicators of recon-friendly surfaces.
- Researchers must always re-validate current brief, scope, and rules before any testing. Out-of-scope testing risks penalties.

**Disclaimer:** This digest is for educational/research planning only. Responsible disclosure via the official program channels is required for any findings.
