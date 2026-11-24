# Ranked Digest: Top 5 Active Bugcrowd Public AI/ML Security Programs

**Research-only pipeline output.** No exploitation, probing, or submissions were performed. Data drawn from public Bugcrowd engagement briefs (as of late November 2026), Bugcrowd blog/docs, and related public materials.

## Scoring Methodology
AI-specific weakness indicators scored 0–10:
- Documented prompt-injection / indirect-injection / RAG / agent / tool-calling scope openness
- Reward size and clarity for AI findings
- Multi-tenancy, action surface, or data-access depth
- Publicly documented vectors (system-prompt leaks, jailbreaks, data-leak / extraction signals, research papers)
- Model/API transparency and guardrail documentation depth

Higher scores indicate stronger public signals of a testable AI attack surface.

## Ranked Top 5

### 1. Zendesk Managed Bug Bounty — Score: 9.2/10
- **Engagement**: https://bugcrowd.com/engagements/zendesk (active, public)
- **Model types**: LLM-powered AI Agents & Advanced AI Agents, AI Agent Builder, Copilot, App Builder (explicit Large Language Model scope).
- **API / endpoints**: `https://{subdomain}.zendesk.com/` (agent workspace, knowledge, admin, messaging, etc.). Self-signup trial instances using `@bugcrowdninja.com` emails.
- **Guardrail documentation**: Explicit in-scope AI list. Low-agency features (AI Ticket Summary, AI Intelligence Triage) and pure alignment/jailbreak without secondary exploit are out of scope. Valid submissions require tangible security impact (unauthorized data access, privilege escalation, cross-tenant leakage, state changes).
- **Publicly documented vectors / signals**: Indirect & exploitable prompt injection (nested, encoded, third-party data), RAG poisoning, response data leakage (backend API keys/credentials), model extraction / membership inference / training-pipeline poisoning, action & automation abuse, privilege escalation via AI interface. Strong multi-tenant SaaS surface.
- **Evidence**: Brief lists concrete attack classes; Zendesk AI target rewards P1 $5,000–$50,000. High average payouts and fast triage. Aligns with OWASP LLM Top 10 patterns for agent + RAG + multi-tenant systems.

### 2. OpenAI Security Bug Bounty — Score: 8.7/10
- **Engagement**: https://bugcrowd.com/engagements/openai (ongoing since 2023; major reward increases Nov 2026)
- **Model types**: GPT-series and other OpenAI models powering ChatGPT, API, Codex, Atlas Browser, Operator, Connectors.
- **API / endpoints**: ChatGPT services, OpenAI API, API-key exposure program, related product surfaces.
- **Guardrail documentation**: Model safety issues (jailbreaks, DAN, hallucinations, pure prompt-based safety bypasses) are explicitly out of scope. Application-layer prompt injection is in-scope only when it exploits a separate product control or OpenAI-controlled integration flaw.
- **Publicly documented vectors / signals**: Historical system-prompt extraction (Sydney-era), known jailbreaks, private/unreleased model access (accepted if product controls are bypassed). High-reward structure with quality/loyalty/campaign multipliers (exceptional criticals + bonuses up to ~$172k).
- **Evidence**: Brief section 3 clearly distinguishes model behavior from product controls. Recent announcements and disclosed reports confirm active high-value AI product surface.

### 3. OpenAI Safety Bug Bounty — Score: 8.4/10
- **Engagement**: https://bugcrowd.com/engagements/openai-safety (public since ~March 2026)
- **Model types**: Same OpenAI models, focused on agentic products.
- **API / endpoints**: Agentic tools (Atlas Browser, Codex, Operator, Connectors, MCP integrations).
- **Guardrail documentation**: Material-harm design/implementation flaws. Indirect / third-party prompt injection causing an agent to misuse a Connector or MCP tool for data exfiltration or harmful actions is in-scope (PII from chat history counts as sensitive). Realism/feasibility required; pure content issues out of scope. Test-account only.
- **Publicly documented vectors / signals**: Explicit MCP/Connector + indirect injection language; Chain-of-Thought / proprietary reasoning leakage also listed.
- **Evidence**: Brief enumerates precise in-scope agentic scenarios (authorization bypasses, missing confirmations, tool misuse). P1 rewards $5,500–$7,500. Complements the main Security program.

### 4. Indeed (Career Scout AI target) — Score: 7.6/10
- **Engagement**: https://bugcrowd.com/engagements/indeed (Career Scout added as primary scope)
- **Model types**: LLM career coach / agent (publicly confirmed to use OpenAI APIs).
- **API / endpoints**: Indeed mobile app (iOS via TestFlight noted); Career Scout chat interface.
- **Guardrail documentation**: Explicit focus on prompt injection and insecure output handling. Also interested in authorization, authentication, sensitive data exposure, stored/reflected XSS. Out of scope: pure AI safety, algorithmic/data biases, non-reproducible multi-turn, volumetric DoS against AI features. Reward examples include P1 up to $10,000 for prompt injection leading to authorization bypass / highly sensitive data.
- **Publicly documented vectors / signals**: Indeed-published research on resume-based prompt injection against LLM feature extractors; public marketing of Career Scout as conversational AI coach.
- **Evidence**: Brief announcements and focus table specifically list Career Scout + prompt injection. OpenAI partnership confirms API usage.

### 5. Optus Managed Bug Bounty – AI Search — Score: 6.8/10
- **Engagement**: https://bugcrowd.com/engagements/optus-mbb-og
- **Model types**: Generative-AI search capability (summary, article suggestion, quick links).
- **API / endpoints**: `https://gateway.optus.com.au/api/ai-search/search/v1`
- **Guardrail documentation**: Focus areas explicitly include prompt injection, insecure output handling, and sensitive information disclosure. Rate-limit/scanning caution and DoS out of scope.
- **Publicly documented vectors / signals**: Direct LLM attack-surface call-outs; customer-facing generative search is a classic indirect-injection and output-handling target.
- **Evidence**: Dedicated “Optus – AI Search” target with matching reward chart and listed focus areas.

## Additional Notes
- Other programs (Sunrun `*.ai.sunrun.com` surfaces, various chatbots, Mattermost MCP mentions, NASA LiteLLM VDP disclosure) showed AI surface but lacked the combination of explicit LLM/prompt-injection language, high rewards, and clear active scope required for top ranking.
- Bugcrowd platform AI features (Global Control of LLMs, AI Connect MCP server, AI Triage Assistant) are documented with architectural mitigations assuming prompt-injection bypass is possible; these are not customer bounty targets.
- All information is based solely on publicly available scope, rewards, and known vectors. No testing was performed.

*Generated 2026-11-24 via research pipeline.*
