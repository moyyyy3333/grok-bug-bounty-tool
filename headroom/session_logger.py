"""Structured session logger for bug bounty swarm agents.

Every agent action gets logged as a JSONL event with timestamps, role,
target, action type, inputs, outputs, and outcome. Learn mode reads these
clean structured logs instead of scraping raw text.

Usage:
    from headroom.session_logger import SessionLogger

    log = SessionLogger(role="recon", target="example.com")
    log.event("scan_start", {"tool": "unified_re", "flags": ["--json"]})
    log.event("finding", {"type": "cors", "severity": "medium", "url": "..."})
    log.event("scan_end", {"duration_s": 42, "findings": 3})
    log.close()
"""

from __future__ import annotations

import json
import logging
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class SessionEvent:
    """One atomic action in a swarm session."""
    ts: str
    session_id: str
    role: str
    target: str
    action: str
    data: dict[str, Any] = field(default_factory=dict)
    duration_ms: float | None = None
    outcome: str = "ok"  # ok | error | blocked | timeout


class SessionLogger:
    """Thread-safe JSONL logger. One file per session."""

    def __init__(
        self,
        role: str,
        target: str,
        sessions_dir: str | Path = "swarm/sessions",
        session_id: str | None = None,
    ):
        self.role = role
        self.target = target
        self.session_id = session_id or uuid.uuid4().hex[:12]
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.sessions_dir / f"{self.session_id}.jsonl"
        self._lock = threading.Lock()
        self._fh = open(self.path, "a", encoding="utf-8")
        self._start = time.monotonic()
        self.event("session_start", {"role": role, "target": target})

    def event(
        self,
        action: str,
        data: dict[str, Any] | None = None,
        outcome: str = "ok",
        duration_ms: float | None = None,
    ) -> SessionEvent:
        ev = SessionEvent(
            ts=datetime.now(timezone.utc).isoformat(),
            session_id=self.session_id,
            role=self.role,
            target=self.target,
            action=action,
            data=data or {},
            duration_ms=duration_ms,
            outcome=outcome,
        )
        line = json.dumps(asdict(ev), default=str)
        with self._lock:
            self._fh.write(line + "\n")
            self._fh.flush()
        return ev

    def timed(self, action: str, data: dict[str, Any] | None = None):
        """Context manager that logs start/end with duration."""
        return _TimedEvent(self, action, data)

    def close(self) -> None:
        total = (time.monotonic() - self._start) * 1000
        self.event("session_end", {"total_duration_ms": round(total, 1)})
        with self._lock:
            self._fh.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


class _TimedEvent:
    def __init__(self, log: SessionLogger, action: str, data: dict[str, Any] | None):
        self.log = log
        self.action = action
        self.data = data or {}
        self.t0 = time.monotonic()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        ms = (time.monotonic() - self.t0) * 1000
        outcome = "error" if exc_type else "ok"
        self.log.event(self.action, self.data, outcome=outcome, duration_ms=round(ms, 1))
        return False


def load_session(path: str | Path) -> list[SessionEvent]:
    """Load a JSONL session file back into events."""
    events = []
    for line in Path(path).read_text().splitlines():
        if line.strip():
            events.append(SessionEvent(**json.loads(line)))
    return events


def load_all_sessions(sessions_dir: str | Path = "swarm/sessions") -> list[SessionEvent]:
    """Load every session in the directory."""
    d = Path(sessions_dir)
    if not d.exists():
        return []
    events = []
    for f in sorted(d.glob("*.jsonl")):
        events.extend(load_session(f))
    return events
