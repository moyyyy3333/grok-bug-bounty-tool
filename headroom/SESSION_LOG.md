# Structured Session Logger

Gives learn mode clean, typed input instead of raw text scraping.

## What it captures

Every event is one JSON line with:

- `ts` — UTC timestamp
- `session_id` — ties events to one campaign run
- `role` — recon / analysis / exploit / report
- `target` — the bounty target
- `action` — what happened (scan_start, finding, blocked, etc.)
- `data` — arbitrary structured payload
- `duration_ms` — how long it took
- `outcome` — ok / error / blocked / timeout

## Usage in an agent

```python
from headroom.session_logger import SessionLogger

with SessionLogger(role="recon", target="example.com") as log:
    with log.timed("subdomain_enum", {"tool": "subfinder"}):
        results = run_subfinder("example.com")
    for r in results:
        log.event("subdomain_found", {"host": r})
    log.event("finding", {"type": "cors", "url": "https://api.example.com"})
```

## Why structured beats raw logs

Learn mode's failure patterns match on action names and outcomes, not
keyword soup. A 403 becomes `outcome: "blocked"` with `action: "http_get"`
instead of a wall of text that might say "access denied" or "HTTP 403"
or "forbidden by policy." Precise matching means precise lessons.

## Pipeline

```
Agent action → SessionLogger (JSONL) → SessionLearner → role instructions
```

The logger writes; the learner reads. Neither blocks the other, so a
crashed agent still leaves a partial but valid log behind.
