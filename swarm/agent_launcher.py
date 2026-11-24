#!/usr/bin/env python3
"""
swarm/agent_launcher.py
Launches and manages the multi-agent bounty research swarm.
Each agent gets a role, a target, and a bounded toolset.
All actions are logged through session_logger for learn mode.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs" / "swarm"
REPORT_DIR = ROOT / "reports" / "swarm"
CONFIG_PATH = ROOT / "swarm" / "config.json"

ROLES = {
    "recon": {
        "description": "Maps attack surface from public sources only",
        "tools": ["web_search", "browse_page", "immunefi_api", "github_search"],
        "spawn_workers": True,
        "max_workers": 5,
    },
    "analysis": {
        "description": "Triages recon output, scores targets, spots patterns",
        "tools": ["rea_unified", "readelf_fallback", "objdump_fallback", "entropy_check"],
        "spawn_workers": True,
        "max_workers": 3,
    },
    "exploitation": {
        "description": "Develops PoCs against in-scope, authorized targets only",
        "tools": ["code_execution", "frida_hooks", "payload_gen"],
        "spawn_workers": False,
        "max_workers": 0,
        "requires_human_approval": True,
    },
    "reporting": {
        "description": "Drafts Immunefi/Bugcrowd-format submissions",
        "tools": ["markdown_gen", "poc_packager", "severity_calc"],
        "spawn_workers": False,
        "max_workers": 0,
    },
    "learner": {
        "description": "Digests session logs and writes durable corrections",
        "tools": ["session_learner", "instruction_updater"],
        "spawn_workers": False,
        "max_workers": 0,
    },
}


@dataclass
class AgentTask:
    agent_id: str
    role: str
    target: str
    started_at: str
    status: str = "queued"
    findings: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    finished_at: Optional[str] = None


def load_config() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {
        "max_parallel_agents": 4,
        "default_roles": ["recon", "analysis"],
        "log_level": "info",
        "headroom_proxy": "http://127.0.0.1:8787",
        "boundaries": {
            "public_data_only": True,
            "no_mainnet_interaction": True,
            "no_unauthorized_scanning": True,
            "human_approval_for_exploitation": True,
        },
    }


def log_action(agent_id: str, role: str, target: str, action: str, outcome: str):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "agent_id": agent_id,
        "role": role,
        "target": target,
        "action": action,
        "outcome": outcome,
    }
    with open(LOG_DIR / "actions.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")


def launch_agent(role: str, target: str, agent_id: str) -> AgentTask:
    if role not in ROLES:
        raise ValueError(f"Unknown role: {role}. Valid: {list(ROLES)}")
    spec = ROLES[role]
    task = AgentTask(
        agent_id=agent_id,
        role=role,
        target=target,
        started_at=datetime.now(timezone.utc).isoformat(),
    )
    log_action(agent_id, role, target, "launch", "started")
    # Bounded execution: recon/analysis can spawn workers; exploitation needs approval
    if spec.get("requires_human_approval"):
        task.status = "awaiting_human_approval"
        log_action(agent_id, role, target, "launch", "blocked_pending_approval")
        return task
    task.status = "running"
    # Simulate bounded work unit (real impl would dispatch to model/tools)
    task.findings.append(f"{role} pass on {target}: no active testing performed")
    task.status = "completed"
    task.finished_at = datetime.now(timezone.utc).isoformat()
    log_action(agent_id, role, target, "launch", "completed")
    return task


def run_swarm(targets: list[str], roles: list[str], max_parallel: int) -> list[AgentTask]:
    tasks: list[AgentTask] = []
    queue = [(r, t) for t in targets for r in roles]
    running = 0
    idx = 0
    while idx < len(queue) or running > 0:
        while running < max_parallel and idx < len(queue):
            role, target = queue[idx]
            idx += 1
            aid = f"{role}-{target.replace(' ', '_')[:24]}-{int(time.time())}"
            task = launch_agent(role, target, aid)
            tasks.append(task)
            if task.status == "running":
                running += 1
        # In real impl: await completions; here we just drain
        running = 0
        break
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORT_DIR / f"swarm-run-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.json"
    out.write_text(json.dumps([asdict(t) for t in tasks], indent=2))
    return tasks


def main():
    p = argparse.ArgumentParser(description="Launch the bounty research swarm")
    p.add_argument("--targets", required=True, help="Comma-separated targets or path to file")
    p.add_argument("--roles", default="recon,analysis", help="Comma-separated roles")
    p.add_argument("--max-parallel", type=int, default=4)
    args = p.parse_args()

    if Path(args.targets).exists():
        targets = [l.strip() for l in Path(args.targets).read_text().splitlines() if l.strip()]
    else:
        targets = [t.strip() for t in args.targets.split(",") if t.strip()]

    roles = [r.strip() for r in args.roles.split(",") if r.strip()]
    cfg = load_config()
    tasks = run_swarm(targets, roles, min(args.max_parallel, cfg["max_parallel_agents"]))
    print(f"Launched {len(tasks)} agent tasks. Report: {REPORT_DIR}")
    for t in tasks:
        print(f"  [{t.status}] {t.role} -> {t.target}")


if __name__ == "__main__":
    main()
