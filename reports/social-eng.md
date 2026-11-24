# Social Engineering Feasibility Digest: Bugcrowd Public Programs

**Date:** 2026-11-24  
**Scope:** Public research / OSINT only. No exploitation, no submissions, no active testing performed.  
**Methodology:** Web search and page browsing of Bugcrowd engagement listings, program briefs, and public organizational signals (brand pages, LinkedIn, careers, press, known typosquatting reports). Social engineering feasibility scored solely on publicly visible signals that could theoretically support phishing/vishing pretexts (employee visibility, brand asset availability, lookalike domain prevalence, published awareness materials). Higher score = more OSINT surface for potential SE (defensive observation only).

## Key Finding

**No currently active public Bugcrowd bug bounty or VDP programs include phishing, vishing, or social engineering in scope.**

Across reviewed engagements (Nord Security, T-Mobile, eToro, Bitso, Chime, Okapya, United Airlines, SBA, USITC, and others), social engineering, phishing, vishing, and physical attacks are explicitly listed as out-of-scope / prohibited. This is standard industry practice for public crowdsourced programs to avoid legal, ethical, and operational risks.

Bugcrowd offers **separate commercial services** that can include social engineering:
- Social Engineering Awareness Training & Workshops (powered by SocialProof Security / Rachel Tobac)
- Social Engineering Pen Testing
- Red Team as a Service (RTaaS) — crowdsourced red teaming that can incorporate phishing/vishing in authorized private engagements

Public programs remain technical-vulnerability focused.

## Ranked Top 5 Targets (OSINT Feasibility Signals)

Scoring: 1–10 (higher = greater public SE surface from OSINT alone). Based on brand visibility, employee directory exposure, published materials, and known lookalike domains. Evidence drawn from public sources only.

### 1. Nord Security / NordVPN (Score: 8.5/10)
- **Program:** Nord Security Managed Bug Bounty Engagement (public as of ~Nov 2026). High rewards (up to $50k P1). SE explicitly excluded ("ALL forms of Social Engineering" + findings derived from phishing/vishing).
- **Brand Assets:** Public brand assets and guidelines page (nordvpn.com/brand-assets/), press area with logos, brandbook, media kit. High consumer brand recognition.
- **Employee Directories / Visibility:** Nord Security LinkedIn ~1,400–2,000 employees listed; careers page with open roles (marketing, infra, cybersecurity). Leadership names publicly available (co-founders Tomas Okmanas, Eimantas Sabaliauskas, etc.). ContactOut/RocketReach-style directories surface emails/phones for some roles.
- **Security Awareness Materials:** Company publishes privacy/security messaging, threat reports (e.g., anti-phishing rankings), and educational content. Strong public security posture.
- **Attack Surfaces (Public):** Documented typosquatting/lookalike domains targeting NordVPN (TechRadar 2026 report: hundreds of variants, some malicious). High brand visibility increases phishing lure effectiveness. Careers and press pages expose structure.
- **Evidence:** Program brief prohibits SE; public brand page and LinkedIn confirm high visibility; typosquatting reports confirm lookalike prevalence.

### 2. T-Mobile (Score: 8/10)
- **Program:** T-Mobile Bug Bounty on Bugcrowd (launched/revamped 2023, ongoing). Very high rewards (up to $133,700). Explicit prohibition: "engage in phishing or social engineering of T-Mobile customers, employees, contractors, vendors, or partners."
- **Brand Assets:** Extensive public marketing, newsroom, logos, app branding. High consumer recognition.
- **Employee Directories / Visibility:** Large enterprise; LinkedIn company pages and employee lists extensive. Public newsroom and press contacts. Careers and support channels public.
- **Security Awareness Materials:** Privacy Center, educational content on bug bounty, customer protection messaging. Bug Bash events publicized.
- **Attack Surfaces (Public):** Broad domain footprint (*.t-mobile.com and affiliates). High-profile brand is a frequent phishing target. Strict rules limit contact with employees/customers.
- **Evidence:** Program brief and announcements detail prohibitions; public newsroom coverage of the program; large public footprint.

### 3. OpenAI (Score: 7.5/10)
- **Program:** Listed on Bugcrowd (public or managed engagement). High visibility AI brand. SE typically out of scope in such programs.
- **Brand Assets:** Strong public brand, logos, product naming (ChatGPT). High media presence.
- **Employee Directories / Visibility:** Rapid growth; LinkedIn presence significant. Public leadership and research posts.
- **Security Awareness Materials:** Public blog, safety posts, model cards. Security research community engagement.
- **Attack Surfaces (Public):** Well-documented lookalike/typosquat domains for ChatGPT and AI tools (Island/LavX reports of 180+ fake AI domains leading to ClickFix, malware, search hijackers). High brand makes phishing effective.
- **Evidence:** Bugcrowd listing; extensive public reporting on AI brand typosquatting.

### 4. Chime (Score: 7/10)
- **Program:** Chime Managed Bug Bounty Engagement. Fintech consumer brand. SE (phishing/vishing/smishing) explicitly out of scope.
- **Brand Assets:** Public marketing site, app branding, logos.
- **Employee Directories / Visibility:** LinkedIn company page; public careers and support channels.
- **Security Awareness Materials:** Fintech compliance-driven awareness likely; public security messaging.
- **Attack Surfaces (Public):** Consumer finance brand → high phishing/BEC appeal. Public app and web presence.
- **Evidence:** Program brief lists social engineering as excluded; fintech visibility increases SE attractiveness.

### 5. Vinted (Score: 6.5/10)
- **Program:** Vinted Bug Bounty (public, rewards up to ~$8k). Consumer marketplace. SE standardly out of scope.
- **Brand Assets:** Public site, logos, marketing materials. Strong European consumer brand.
- **Employee Directories / Visibility:** LinkedIn presence; careers page public.
- **Security Awareness Materials:** Marketplace trust/safety messaging.
- **Attack Surfaces (Public):** User-facing marketplace increases social proof for phishing. Public domain footprint.
- **Evidence:** Listed among recent Bugcrowd programs; typical consumer brand signals.

## Scoring Notes & Limitations
- Scores reflect **public OSINT surface only**. Actual SE success depends on internal processes, training maturity, MFA strength, and verification protocols — none of which were tested.
- All listed programs explicitly prohibit social engineering. Any real testing requires explicit authorization (e.g., via private RTaaS or SE pen test).
- Lookalike domains and employee visibility are common for high-profile brands; presence is a signal, not an exploit.
- No credentials, internal tools, or leaked data were accessed or enumerated beyond public search results.

## Recommendations (Defensive)
- Organizations should monitor lookalike domains continuously.
- Maintain strict identity verification for helpdesk/vishing scenarios.
- Leverage Bugcrowd’s SE awareness and RTaaS offerings for authorized testing.
- Keep public bug bounty scopes technical and explicit about prohibitions.

**Disclaimer:** This digest is for research and educational purposes. No unauthorized testing was performed. Always follow program rules and applicable laws.