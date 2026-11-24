#!/usr/bin/env python3
"""
Passive Swarm Orchestrator for authorized bug bounty research.

- Pulls public Immunefi bounty data
- Ranks programs by published max bounty and metadata
- Outputs structured digests for human review
- Does NOT perform active scanning, mainnet interaction, exploitation, or automated submissions
- Designed to feed into Grok Automations for further analysis

Use only on programs where you are authorized to research under their published rules.
"""

import json
import urllib.request
from datetime import datetime, timezone
from typing import List, Dict, Any

IMMUNEFI_API = "https://immunefi.com/public-api/bounties.json"

def fetch_immunefi_bounties() -> List[Dict[str, Any]]:
    try:
        with urllib.request.urlopen(IMMUNEFI_API, timeout=30) as resp:
            data = json.load(resp)
            return data if isinstance(data, list) else []
    except Exception as e:
        print(f"Failed to fetch Immunefi data: {e}")
        return []

def rank_programs(programs: List[Dict[str, Any]], min_max_bounty: int = 1_000_000) -> List[Dict[str, Any]]:
    ranked = []
    for p in programs:
        max_bounty = p.get("maxBounty") or 0
        if max_bounty < min_max_bounty:
            continue
        ranked.append({
            "project": p.get("project"),
            "slug": p.get("slug"),
            "max_bounty": max_bounty,
            "launch_date": p.get("launchDate"),
            "updated": p.get("updatedDate"),
            "kyc": p.get("kyc"),
            "language": p.get("language"),
            "ecosystem": p.get("ecosystem"),
            "program_type": p.get("programType"),
            "url": f"https://immunefi.com/bug-bounty/{p.get('slug')}/information/" if p.get("slug") else None,
        })
    ranked.sort(key=lambda x: x["max_bounty"], reverse=True)
    return ranked

def generate_digest(ranked: List[Dict[str, Any]]) -> str:
    lines = [
        f"# Passive Bounty Digest ({datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')})",
        "",
        "**Source**: Public Immunefi API only. No active testing performed.",
        "**Purpose**: Ranked list for human review under authorized program rules.",
        "",
        "## High-Ceiling Programs (≥ $1M max)",
        "",
    ]
    for i, p in enumerate(ranked[:20], 1):
        lines.append(
            f"{i}. **{p['project']}** — ${p['max_bounty']:,} max"
            f" | KYC: {p['kyc']} | Updated: {str(p['updated'])[:10] if p['updated'] else 'n/a'}"
        )
        if p["url"]:
            lines.append(f"   {p['url']}")
        lines.append("")
    lines.append("\n---\n*This digest is passive public data only. Manual verification and compliance with each program's rules are required before any research activity.*")
    return "\n".join(lines)

def main():
    print("Fetching public Immunefi bounty data...")
    programs = fetch_immunefi_bounties()
    if not programs:
        print("No data retrieved.")
        return
    ranked = rank_programs(programs)
    digest = generate_digest(ranked)
    print(digest)
    # Optionally write to file
    with open("reports/passive-digest.md", "w") as f:
        f.write(digest)
    print("\nDigest written to reports/passive-digest.md")

if __name__ == "__main__":
    main()
