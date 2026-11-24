# Grok Bug Bounty Research Toolkit

Passive research coordination tools for authorized bug bounty work.

## Components
- `swarm/` — Passive orchestrator that ranks public Immunefi programs and generates digests
- `headroom/` — Optional output compression / session learning helpers (install headroom-ai locally if desired)

## Important Boundaries
This repository contains **passive public-data tools only**. It does not include:
- Active scanners
- Exploit code
- Mainnet interaction scripts
- Automated submission tooling

All research must stay within the published rules of the specific bounty program you are authorized to test. Out-of-scope activity is unauthorized and can create legal risk.

## Quick Start
```bash
python swarm/orchestrator.py
```

Review the generated `reports/passive-digest.md`, then perform any further analysis manually or via scheduled Grok Automations under the target program's rules.
