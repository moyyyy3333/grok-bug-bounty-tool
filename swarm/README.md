# Passive Swarm Orchestrator

Legitimate automation layer for authorized bug bounty research.

## What it does
- Fetches public Immunefi program metadata via the official public API
- Ranks high-ceiling programs (≥ $1M max bounty by default)
- Generates markdown digests for human review
- Designed to feed into scheduled Grok Automations for deeper (still passive) analysis

## Usage
```bash
python swarm/orchestrator.py
```

Output is written to `reports/passive-digest.md`.

## Integration with Grok Automations
The digests produced here can be used as input for scheduled Grok analysis runs (via the Automations connector) that perform additional public-source research and ranking. All findings remain subject to manual human verification before any report is submitted.

## Legal & Platform Notes
- Always read the target program's full policy before any research.
- Many platforms (including Immunefi) restrict or prohibit automated scanning that generates significant traffic and prohibit mainnet testing.
- Stay strictly in scope. Out-of-scope activity is unauthorized access.
- This tool is for passive public-data coordination only.

## Requirements
- Python 3.8+
- Network access to immunefi.com (public API)
