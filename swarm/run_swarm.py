#!/usr/bin/env python3
"""
Entry point for the research swarm.
Coordinates the roles defined in agent_launcher.py against targets
drawn from the reports/ directory (public digests already generated).

Roles executed: recon, analysis, reporting, learner.
Exploitation role remains gated and is not auto-run.
All actions logged to logs/swarm/actions.jsonl.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
LOG_DIR = ROOT / "logs" / "swarm"

# Import the role definitions and launcher helpers
sys.path.insert(0, str(ROOT / "swarm"))
from agent_launcher import ROLES, launch_agent, log_action, AgentTask  # type: ignore


def collect_targets() -> list[str]:
    targets = []
    if REPORTS.exists():
        for md in sorted(REPORTS.glob("*.md")):
            if md.name.startswith("deploy-"):
                continue
            targets.append(md.stem.replace("-", " "))
    return targets or ["web apps", "api security", "blockchain"]


def run():
    targets = collect_targets()
    roles = ["recon", "analysis", "reporting", "learner"]
    tasks: list[AgentTask] = []
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Swarm run started: {datetime.now(timezone.utc).isoformat()}")
    print(f"Targets from reports/: {targets}")
    print(f"Roles: {roles}\n")

    for target in targets:
        for role in roles:
            aid = f"{role}-{target.replace(' ', '_')[:20]}-{int(datetime.now(timezone.utc).timestamp())}"
            task = launch_agent(role, target, aid)
            tasks.append(task)
            print(f"[{task.status}] {role:12} → {target}")

    summary = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "targets": targets,
        "roles": roles,
        "tasks": [
            {
                "agent_id": t.agent_id,
                "role": t.role,
                "target": t.target,
                "status": t.status,
                "findings": t.findings,
            }
            for t in tasks
        ],
    }
    out = REPORTS / "swarm-last-run.json"
    out.write_text(json.dumps(summary, indent=2))
    print(f"\nWrote {out}")
    print(f"Total tasks: {len(tasks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
