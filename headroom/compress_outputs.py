"""Compress tool outputs and agent messages through Headroom.

Headroom must be installed on the host: pip install "headroom-ai[all]"
If it's missing, these functions pass data through unchanged so the
pipeline never breaks.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

_headroom = None
try:
    from headroom import compress as _hr_compress
    _headroom = _hr_compress
except ImportError:
    logger.warning("headroom-ai not installed; compression disabled, passing through")


def compress_tool_output(output: str, model: str = "gpt-4o") -> str:
    """Compress a single tool output string."""
    if _headroom is None or not output:
        return output
    try:
        result = _headroom([{"role": "tool", "content": output}], model=model)
        return result.messages[0]["content"]
    except Exception as exc:
        logger.warning("Headroom compression failed: %s", exc)
        return output


def compress_messages(messages: list[dict[str, Any]], model: str = "gpt-4o") -> list[dict[str, Any]]:
    """Compress a full message list, leaving user turns untouched."""
    if _headroom is None:
        return messages
    try:
        result = _headroom(messages, model=model)
        return result.messages
    except Exception as exc:
        logger.warning("Headroom message compression failed: %s", exc)
        return messages
