"""Headroom proxy configuration for swarm agents.

Drop-in proxy on loopback port 8787. Any OpenAI-compatible client
(recon agents, exploit engine, report writer) routes through it with
zero code changes by setting the base URL.
"""

PROXY_PORT = 8787
PROXY_HOST = "127.0.0.1"


def build_proxy_env() -> dict[str, str]:
    """Environment variables that point agents at the local Headroom proxy."""
    base = f"http://{PROXY_HOST}:{PROXY_PORT}/v1"
    return {
        "OPENAI_BASE_URL": base,
        "OPENAI_API_BASE": base,
        "GROK_MODELS_BASE_URL": base,
        "HEADROOM_OUTPUT_SHAPER": "1",  # trim verbose model output too
    }


PROXY_LAUNCH_CMD = (
    f"headroom proxy --host {PROXY_HOST} --port {PROXY_PORT}"
)
