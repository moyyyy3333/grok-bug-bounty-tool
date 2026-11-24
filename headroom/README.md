# Headroom Integration

Token compression layer for the bug bounty swarm. Headroom runs locally on
your machine — nothing leaves your host to be compressed.

## Install (on your machine, not the sandbox)

```bash
pip install "headroom-ai[all]"
```

## Three ways to use it

**1. Library mode** — import in any agent script:

```python
from headroom.compress_outputs import compress_tool_output

raw = scanner.run(target)          # big verbose output
slim = compress_tool_output(raw)  # 21-57% fewer tokens
```

**2. Proxy mode** — zero code changes for every agent:

```bash
headroom proxy --host 127.0.0.1 --port 8787
```

Then set `OPENAI_BASE_URL=http://127.0.0.1:8787/v1` (see `proxy_config.py`
for the full env block). Recon, analysis, exploit, and report agents all
route through it automatically.

**3. Agent wrap** — for CLI coding agents:

```bash
headroom wrap grok
```

## What gets compressed

- Tool outputs (scanner results, recon dumps, decompile output)
- Logs and repeated JSON arrays (90%+ savings)
- Conversation history between swarm agents
- Model output verbosity (optional, off by default)

User messages are never touched. Originals are cached locally and
retrievable via `headroom_retrieve` if an agent needs the full text.

## Measured savings

| Scenario | Before | After | Saved |
|---|---:|---:|---:|
| Code search (100 results) | 17,199 | 13,597 | 21% |
| SRE incident debugging | 55,957 | 24,340 | 57% |
| Codebase exploration | 58,801 | 33,895 | 42% |
| GitHub issue triage | 46,067 | 32,429 | 30% |

On a long bounty session with heavy recon output, that compounds into real
money and real context window.
