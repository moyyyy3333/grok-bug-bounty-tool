#!/usr/bin/env python3
"""Fetch and rank public Immunefi programs."""

from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

API = "https://immunefi.com/public-api/bounties.json"
OUT = Path(__file__).resolve().parents[1] / "reports" / "passive-digest.md"


def fetch() -> list[dict[str, Any]]:
    try:
        with urllib.request.urlopen(API, timeout=30) as resp:
            data = json.load(resp)
            return data if isinstance(data, list) else []
    except Exception as exc:
        print(f"fetch failed: {exc}", file=sys.stderr)
        return []


def rank(programs: list[dict[str, Any]], min_bounty: int = 1_000_000) -> list[dict[str, Any]]:
    ranked = []
    for p in programs:
        mb = p.get("maxBounty") or 0
        if mb < min_bounty:
            continue
        ranked.append({
            "project": p.get("project"),
            "slug": p.get("slug"),
            "max_bounty": mb,
            "updated": p.get("updatedDate"),
            "kyc": p.get("kyc"),
            "url": f"https://immunefi.com/bug-bounty/{p.get('slug')}/information/" if p.get("slug") else None,
        })
    ranked.sort(key=lambda x: x["max_bounty"], reverse=True)
    return ranked


def to_md(ranked: list[dict[str, Any]]) -> str:
    lines = [
        f"# Passive Bounty Digest ({datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')})",
        "",
        "Source: public Immunefi API. No active testing.",
        "",
        "## High-ceiling programs (≥ $1M)",
        "",
    ]
    for i, p in enumerate(ranked[:25], 1):
        lines.append(f"{i}. **{p['project']}** — ${p['max_bounty']:,}")
        if p["url"]:
            lines.append(f"   {p['url']}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    programs = fetch()
    if not programs:
        return 1
    ranked = rank(programs)
    md = to_md(ranked)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(md)
    print(md)
    print(f"\nWrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
