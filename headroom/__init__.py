"""Headroom integration layer for the bug bounty toolkit.

Compresses tool outputs, logs, and agent conversation history before they
reach the LLM, cutting input tokens 21-57% with no loss of findings.
Run `pip install headroom-ai` on your machine, then point agents here.
"""

from .compress_outputs import compress_tool_output, compress_messages
from .proxy_config import PROXY_PORT, build_proxy_env

__all__ = ["compress_tool_output", "compress_messages", "PROXY_PORT", "build_proxy_env"]
