# Swarm

Research coordinator.

## Modules
- `run_swarm.py` — launches non-gated roles against targets from `reports/`
- `agent_launcher.py` — role definitions and task runner
- `orchestrator.py` — public Immunefi ranking
- `re_unified.py` — static RE pipeline with fallbacks
- `scanner.py` — offline text/header scorer
- `deploy.py` — writes a deployment manifest

## Run
```bash
python swarm/run_swarm.py
```

Exploitation role is defined in the launcher but gated and not auto-executed.
