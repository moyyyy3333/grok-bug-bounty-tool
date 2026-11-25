# Bug Bounty Research Toolkit

Research coordination tools for authorized bug bounty work.

## Layout
- `swarm/` — agent launcher, orchestrator, RE pipeline, runner
- `headroom/` — session logging, learn mode, output compaction
- `reports/` — generated digests and run summaries

## Quick start
```bash
python swarm/run_swarm.py          # coordinate roles over existing reports
python swarm/orchestrator.py       # refresh public Immunefi ranking
python swarm/re_unified.py --help  # static RE pipeline on a local binary
```

## Limits
Coordinates research over public data and previously generated digests. Does not autonomously discover novel vulnerabilities, generate exploits, or submit reports. Exploitation role is defined but gated.
