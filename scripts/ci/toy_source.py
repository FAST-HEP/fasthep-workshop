from __future__ import annotations

from typing import Any

import awkward as ak

TOY_SOURCE_SPEC = {
    "name": "root_tree",
    "params": {},
    "outputs": {"stream": "event_stream"},
}


def run_toy_source(*, ctx: dict[str, Any] | None = None, **params: Any) -> ak.Array:
    return ak.Array(
        {
            "pt": [12.0, 18.0, 21.0, 28.0, 34.0, 47.0, 52.0, 66.0, 72.0, 84.0, 93.0, 105.0]
        }
    )
