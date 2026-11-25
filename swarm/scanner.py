#!/usr/bin/env python3
"""Lightweight public-text scorer for weakness signals.

Reads text or HTTP response bodies and scores common indicators.
Does not make network requests.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable

SIGNALS = {
    "debug_endpoint": re.compile(r"/debug|/actuator|/console|/phpinfo", re.I),
    "verbose_error": re.compile(r"stack trace|exception|traceback|debug=true", re.I),
    "outdated_lib": re.compile(r"jquery-1\.|angularjs-1\.|lodash-4\.1", re.I),
    "js_leak": re.compile(r"api[_-]?key|secret|password|token", re.I),
    "cors_misconfig": re.compile(r"access-control-allow-origin:\s*\*", re.I),
    "open_s3": re.compile(r"s3\.amazonaws\.com|\.s3\.", re.I),
    "exposed_git": re.compile(r"\.git/config|\.svn", re.I),
    "swagger": re.compile(r"swagger|openapi\.json", re.I),
    "phpinfo": re.compile(r"phpinfo\(\)", re.I),
}


def score(text: str) -> dict[str, int]:
    hits = {}
    for name, pat in SIGNALS.items():
        hits[name] = len(pat.findall(text))
    return hits


def rank(hits: dict[str, int]) -> str:
    total = sum(hits.values())
    if total >= 5:
        return "GO"
    if total >= 2:
        return "MAYBE"
    if total >= 1:
        return "LOW"
    return "SKIP"


def main(argv: Iterable[str] | None = None) -> int:
    args = list(argv or sys.argv[1:])
    if not args:
        print("usage: scanner.py <file-or-text>", file=sys.stderr)
        return 1
    target = args[0]
    path = Path(target)
    text = path.read_text(errors="ignore") if path.exists() else target
    hits = score(text)
    rating = rank(hits)
    print(f"rating: {rating}")
    for k, v in hits.items():
        if v:
            print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
