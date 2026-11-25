# Swarm

Multi-role research coordinator for authorized bug bounty work.

## Roles
- recon — public-source mapping
- analysis — triage and scoring
- reporting — draft structured notes
- learner — digests session logs
- exploitation — defined but gated; requires explicit human approval and is not auto-executed

## Run
```bash
python swarm/run_swarm.py
```

It reads targets from the existing `reports/*.md` digests, launches the non-gated roles, and writes `reports/swarm-last-run.json` plus logs under `logs/swarm/`.

## Limits
This coordinates research agents over public data and previously generated digests. It does not autonomously discover novel vulnerabilities, generate exploits, or submit reports.
