#!/usr/bin/env python3
"""Deploy script: chains swarm agent launcher to scheduled automations.

Reads swarm/agent_launcher.py role definitions, verifies the ten Bugcrowd
category automations exist and are active, and writes a deployment manifest
(reports/deploy-manifest.md) summarizing the full pipeline state.

This is a coordination/verification tool — it does not launch attacks.
"""

from __future__ import annotations

import ast
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SWARM_DIR = REPO_ROOT / "swarm"
REPORTS_DIR = REPO_ROOT / "reports"

EXPECTED_AUTOMATIONS = [
    "bb-web-apps", "bb-mobile-apps", "bb-api-security", "bb-iot-hardware",
    "bb-cloud-infra", "bb-blockchain", "bb-ai-ml", "bb-social-eng",
    "bb-platform-infra", "bb-open-source",
]

SWARM_FILES = [
    "agent_launcher.py", "orchestrator.py", "re_unified.py", "scanner.py", "README.md",
]

HEADROOM_FILES = [
    "__init__.py", "compress_outputs.py", "proxy_config.py", "session_logger.py",
    "learn_mode.py", "LEARN_MODE.md", "README.md", "SESSION_LOG.md",
]


def extract_roles(launcher_path: Path) -> list[str]:
    """Pull role names from agent_launcher.py via AST."""
    roles: list[str] = []
    try:
        tree = ast.parse(launcher_path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError) as e:
        return [f"ERROR reading {launcher_path.name}: {e}"]
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.upper() in ("ROLES", "AGENT_ROLES", "SWARM_ROLES"):
                    if isinstance(node.value, (ast.List, ast.Tuple)):
                        for elt in node.value.elts:
                            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                roles.append(elt.value)
    # Fallback: regex-ish scan for quoted role-like strings near 'role'
    if not roles:
        text = launcher_path.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            l = line.strip().lower()
            if "role" in l and any(r in l for r in ("recon", "analysis", "exploit", "report", "learn")):
                for r in ("recon", "analysis", "exploitation", "reporting", "learner"):
                    if r in l and r not in roles:
                        roles.append(r)
    return roles or ["(no roles detected)"]


def check_files(directory: Path, names: list[str]) -> dict[str, bool]:
    return {n: (directory / n).is_file() for n in names}


def build_manifest(roles: list[str], swarm_status: dict[str, bool], headroom_status: dict[str, bool], automations: list[str]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Deployment Manifest",
        "",
        f"Generated: {now}",
        "",
        "## Swarm layer",
        "",
    ]
    for name, ok in swarm_status.items():
        lines.append(f"- [{'x' if ok else ' '}] swarm/{name}")
    lines.append("")
    lines.append("## Detected agent roles")
    lines.append("")
    for r in roles:
        lines.append(f"- {r}")
    lines.append("")
    lines.append("## Headroom layer")
    lines.append("")
    for name, ok in headroom_status.items():
        lines.append(f"- [{'x' if ok else ' '}] headroom/{name}")
    lines.append("")
    lines.append("## Scheduled automations (expected)")
    lines.append("")
    found = set(automations)
    for name in EXPECTED_AUTOMATIONS:
        lines.append(f"- [{'x' if name in found else ' '}] {name}")
    missing = [n for n in EXPECTED_AUTOMATIONS if n not in found]
    lines.append("")
    if missing:
        lines.append(f"**Missing automations: {', '.join(missing)}**")
    else:
        lines.append("All ten expected automations present.")
    lines.append("")
    lines.append("## Pipeline chain")
    lines.append("")
    lines.append("1. Automations fire at 07:16 CT → public recon per category")
    lines.append("2. Results land in reports/*.md")
    lines.append("3. scanner.py scores any pasted public text or headers")
    lines.append("4. re_unified.py does binary-side static analysis with fallbacks")
    lines.append("5. agent_launcher.py coordinates roles; learn_mode.py digests failures")
    lines.append("6. headroom/ compresses outputs and runs the learn loop")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    launcher = SWARM_DIR / "agent_launcher.py"
    roles = extract_roles(launcher) if launcher.is_file() else ["(agent_launcher.py missing)"]
    swarm_status = check_files(SWARM_DIR, SWARM_FILES)
    headroom_status = check_files(SWARM_DIR.parent / "headroom", HEADROOM_FILES)

    # Automations: try the Automations connector if available; else accept CLI list
    automations: list[str] = []
    if argv and argv[0] == "--automations":
        automations = argv[1:]
    else:
        # Best-effort: look for a local cache file
        cache = REPO_ROOT / "reports" / "automations-cache.json"
        if cache.is_file():
            try:
                data = json.loads(cache.read_text(encoding="utf-8"))
                automations = [a.get("name", "") for a in data if a.get("isActive")]
            except (json.JSONDecodeError, OSError):
                pass

    manifest = build_manifest(roles, swarm_status, headroom_status, automations)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORTS_DIR / "deploy-manifest.md"
    out.write_text(manifest, encoding="utf-8")
    print(manifest)
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
