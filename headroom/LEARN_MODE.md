# Learn Mode

Closes the loop between sessions. Every failed recon pass, blocked request,
and dead-end exploit attempt becomes a permanent instruction for the swarm.

## How it works

1. Each agent session writes a log to `swarm/sessions/`.
2. `SessionLearner.ingest_session()` scans the log against known failure
   patterns (403s, rate limits, WAF blocks, missed CORS chains, etc.).
3. Matching patterns become `LearnedCorrection` objects stored in
   `swarm/instructions/learned_corrections.json`.
4. `write_corrections()` appends a "Learned Lessons" block to every role
   instruction file (recon, analysis, exploit, report) so the next campaign
   starts with scar tissue instead of amnesia.

## Run it

```python
from headroom.learn_mode import SessionLearner

learner = SessionLearner()
for log in Path("swarm/sessions").glob("*.log"):
    learner.ingest_session(log)
learner.write_corrections()
print(learner.summary())
```

Or as a one-liner after any campaign:

```bash
python -m headroom.learn_mode swarm/sessions/
```

## Why it matters for bounties

Top hunters on Bugcrowd don't just find more bugs — they stop making the
same mistakes. A subdomain takeover attempt that 403'd last week shouldn't
be retried identically this week. Learn mode makes that automatic.

Combined with Headroom's token compression, the swarm gets both cheaper
and smarter per session. That's the compounding edge.
