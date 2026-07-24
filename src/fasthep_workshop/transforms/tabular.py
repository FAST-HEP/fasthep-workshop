from __future__ import annotations

from typing import Any

import awkward as ak  # type: ignore[import-untyped]
import numpy as np
from hepflow.runtime.engine import eval_expr

TABULAR_EXPLODE_SPEC = {
    "name": "workshop.tabular.explode",
    "kind": "transform",
    "input": {"name": "stream", "required": True},
    "params": {
        "fields": {"required": True},
        "keep_fields": {"required": False, "default": []},
    },
    "result": {"stream": "event_stream"},
    "requires": {
        "symbols": [
            {"from": "params.fields", "kind": "field_list"},
            {"from": "params.keep_fields", "kind": "field_list"},
        ],
    },
    "provides": {
        "symbols": [
            {"from": "params.fields", "kind": "field_list"},
            {"from": "params.keep_fields", "kind": "field_list"},
        ],
    },
}

TABULAR_FILTER_SPEC = {
    "name": "workshop.tabular.filter",
    "kind": "transform",
    "input": {"name": "stream", "required": True},
    "params": {
        "expr": {"required": True},
    },
    "result": {"stream": "event_stream"},
    "requires": {
        "symbols": [
            {"from": "params.expr", "kind": "expr_or_field"},
        ],
    },
}

TABULAR_PROJECT_SPEC = {
    "name": "workshop.tabular.project",
    "kind": "transform",
    "input": {"name": "stream", "required": True},
    "params": {
        "fields": {"required": True},
    },
    "result": {"stream": "event_stream"},
    "requires": {
        "symbols": [
            {"from": "params.fields", "kind": "field_list"},
        ],
    },
    "provides": {
        "symbols": [
            {"from": "params.fields", "kind": "field_list"},
        ],
    },
}


def run_tabular_explode(
    *,
    stream: ak.Array,
    fields: list[str],
    keep_fields: list[str] | None = None,
    ctx: dict[str, Any] | None = None,
    **params: Any,
) -> dict[str, ak.Array]:
    if not fields:
        raise ValueError("workshop.tabular.explode requires at least one field")

    missing = [
        field for field in [*fields, *(keep_fields or [])] if field not in stream.fields
    ]
    if missing:
        raise KeyError(f"Cannot explode missing field(s): {', '.join(missing)}")

    counts = ak.num(stream[fields[0]], axis=1)
    for field in fields[1:]:
        if not bool(ak.all(ak.num(stream[field], axis=1) == counts)):
            raise ValueError(
                "workshop.tabular.explode requires aligned list fields; "
                f"field {field!r} does not match {fields[0]!r}"
            )

    exploded: dict[str, Any] = {
        field: ak.flatten(stream[field], axis=1) for field in fields
    }
    for field in keep_fields or []:
        exploded[field] = ak.flatten(
            ak.broadcast_arrays(stream[field], stream[fields[0]])[0]
        )

    return {"stream": ak.Array(exploded)}


def run_tabular_filter(
    *,
    stream: ak.Array,
    expr: str,
    ctx: dict[str, Any] | None = None,
    **params: Any,
) -> dict[str, ak.Array]:
    mask = eval_expr(stream, expr, ctx=ctx)
    return {"stream": stream[np.asarray(mask, dtype=bool)]}


def run_tabular_project(
    *,
    stream: ak.Array,
    fields: list[str],
    ctx: dict[str, Any] | None = None,
    **params: Any,
) -> dict[str, ak.Array]:
    missing = [field for field in fields if field not in stream.fields]
    if missing:
        raise KeyError(f"Cannot project missing field(s): {', '.join(missing)}")
    return {"stream": ak.Array({field: stream[field] for field in fields})}
