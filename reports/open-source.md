# Ranked Digest: Top 5 Active Bugcrowd Open-Source / Public Code Scope Targets

**Generated:** 2026-11-24  
**Methodology:** Public web research (Bugcrowd engagement briefs, GitHub repos, NVD/advisories). Conceptual reverse-engineering unified approach applied: public repo inspection, static pattern analysis for common vuln classes (injection, XSS, auth/session, privilege escalation, deserialization, path traversal), stack-specific known issues. Scored on code quality signals (stars, commits, CI, SECURITY.md, activity) and dependency freshness (recent updates, lockfiles, known scanners). **No exploitation or submissions performed.**

Ranking factors: OSS purity + source accessibility, program activity/recent updates, reward potential, evidence of maintainership (patches, CVEs handled), relevance of vuln classes.

## Ranked Top 5

### 1. SecureDrop (Freedom of the Press Foundation)
- **Program:** https://bugcrowd.com/engagements/freedomofpress (active, last updated ~Nov 2026)
- **Repositories:** https://github.com/freedomofpress/securedrop (main), securedrop-workstation, securedrop-client
- **Languages:** Python (Flask/SQLAlchemy), some Rust (redwood), Ansible, Electron (client)
- **Linked CVEs / Advisories:** CVE-2025-24888 (client code exec via reply filename), GHSA-mp93-xwqc-7rm5 (Workstation USB auto-attach policy, high sev, Nov 2026), CVE-2026-50000 (API session token reuse vs web UI), others in history
- **Code Quality Signals:** ~3.9k stars, 14k+ commits, active develop branch, SECURITY.md, semgrep configs, extensive tests/CI, clear contribution guidelines. Score: 9/10
- **Dependency Freshness:** Active maintenance, PyUp sponsorship for Python deps, recent security patches, lockfiles present. Score: 8/10
- **Conceptual Analysis:** Mature Flask app with Tor isolation. Static patterns: focus on session/auth boundaries (recent token reuse), SQLAlchemy usage (injection less likely but check raw queries), file upload/handling in source/journalist interfaces, workstation Qubes policy. Known classes: auth bypass, XSS (CSP strict), privilege issues in multi-VM setup. High-quality target due to privacy impact and open setup (Docker/Vagrant for local).

### 2. Mattermost Public Bug Bounty
- **Program:** https://bugcrowd.com/engagements/mattermost-mbb-public (transitioned from HackerOne, active)
- **Repositories:** https://github.com/mattermost/mattermost (core, monorepo), plus plugins, desktop, etc.
- **Languages:** Go (server), React/TypeScript (web), React Native, Electron
- **Linked CVEs:** Historical (many self-disclosed); check recent for active hunting
- **Code Quality Signals:** ~40k stars, massive activity (Nov 2026 updates), strong CI, security policy, open-core model with clear self-host. Score: 9/10
- **Dependency Freshness:** Monthly releases, active Dependabot-style management implied by frequency. Score: 9/10
- **Conceptual Analysis:** Collaboration platform. Static: Go concurrency/race conditions, React XSS/DOM, auth/SSO, plugin sandboxing, API IDOR. Known classes: privilege escalation via plugins, message injection, config exposure. Excellent for source review given full public monorepo.

### 3. Zendesk Managed Bug Bounty (Public Repositories scope)
- **Program:** https://bugcrowd.com/engagements/zendesk (active, ongoing since Dec 2025, high rewards up to $50k)
- **Repositories:** https://github.com/zendesk, ultimateai, others (hundreds; many explicit out-of-scope lists)
- **Languages:** Ruby, TypeScript/JavaScript, Java, Python, etc.
- **Linked CVEs:** Public ones out of scope; focus novel in non-excluded repos
- **Code Quality Signals:** Large org, mixed maturity across repos; many active. Score: 7/10 (volume dilutes)
- **Dependency Freshness:** Varies; some modern, some older libraries excluded. Score: 6/10
- **Conceptual Analysis:** Explicit code review encouraged for public repos. Static patterns: Ruby Rails injection/mass assignment, TS XSS, API auth flaws. Known classes: cross-tenant, AI/LLM injection (separate scope), supply-chain in clients. Strong reward potential for concrete impact in realistic scenarios.

### 4. AXIS OS
- **Program:** https://bugcrowd.com/engagements/axis-os-public (active, recent updates Nov 2026, 90+ rewarded, $250k+ historical payouts)
- **Repositories / Source:** Linux-based embedded OS for cameras/devices; components and VAPIX API public; not full open source but OSS parts (kernel, libs) relevant. No single public full repo.
- **Languages:** C/C++ (embedded), Lua?, web interfaces
- **Linked CVEs:** Dozens attributed to bounty (Axis is CNA); recent program notes high volume from AI-assisted research
- **Code Quality Signals:** Mature product security process, frequent patches, public advisories. Score: 7/10 (proprietary core)
- **Dependency Freshness:** Regular OS updates; 3rd-party vulns often out of scope. Score: 7/10
- **Conceptual Analysis:** IoT/embedded. Static/API: VAPIX endpoint authz, privilege escalation (viewer to admin/root), config injection. Known classes: auth bypass, command injection in CGI, firmware issues. High payout for criticals; device access limited but API testing viable.

### 5. OWASP Java HTML Sanitizer
- **Program:** https://bugcrowd.com/engagements/owaspjavasanitizer (VDP/bounty focused on XSS bypasses)
- **Repositories:** https://github.com/OWASP/java-html-sanitizer, test apps in OWASPBugBounty
- **Languages:** Java
- **Linked CVEs:** Historical XSS bypasses; project designed with security review
- **Code Quality Signals:** Security-focused, extensive tests, adversarial reviews mentioned. Score: 8/10
- **Dependency Freshness:** Relies on Guava; maintained but narrower scope. Score: 7/10
- **Conceptual Analysis:** Pure security library. Static: policy parsing, HTML tokenization, attribute handling. Known classes: XSS via malformed/encoded input, policy bypass. Ideal for focused reverse-engineering of sanitizer logic; local war-file testing available.

## Summary Scoring Table

| Rank | Program          | OSS Purity | Activity | Reward Potential | Code Quality | Dep Freshness | Overall |
|------|------------------|------------|----------|------------------|--------------|---------------|---------|
| 1    | SecureDrop      | High      | High    | Medium ($2.5k)  | 9            | 8             | High   |
| 2    | Mattermost      | High      | High    | Medium-High     | 9            | 9             | High   |
| 3    | Zendesk (repos) | Medium    | High    | Very High ($50k)| 7            | 6             | High   |
| 4    | AXIS OS         | Medium    | High    | High ($20k+)    | 7            | 7             | Medium-High |
| 5    | OWASP Sanitizer | High      | Medium  | Low-Medium      | 8            | 7             | Medium |

**Notes:** Block Open Source program on Bugcrowd ceased new submissions ~Sept 2026 (moved to private HackerOne). Code.org program paused. Prioritize SecureDrop and Mattermost for pure source-based hunting. All data from public sources as of Nov 24, 2026. Verify current briefs before any research.
