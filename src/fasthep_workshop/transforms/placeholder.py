from __future__ import annotations

from typing import Any

PLACEHOLDER_STAGE_SPEC = {
    "name": "workshop.placeholder_stage",
    "kind": "transform",
    "input": {"name": "stream", "required": True},
    "params": {
        "notes": {"required": False},
    },
    "result": {"stream": "event_stream"},
}


def run_placeholder_stage(
    *,
    stream: Any,
    notes: str | None = None,
    ctx: dict[str, Any] | None = None,
    **params: Any,
) -> dict[str, Any]:
    """Pass the stream through unchanged; stands in for a not-yet-ported analysis stage."""
    del notes, ctx, params
    return {"stream": stream}


__all__ = ["PLACEHOLDER_STAGE_SPEC", "run_placeholder_stage"]
