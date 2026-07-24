from __future__ import annotations

from pathlib import Path
from typing import Any

import awkward as ak  # type: ignore[import-untyped]
import pyarrow.parquet as pq

PARQUET_SOURCE_SPEC = {
    "name": "workshop.parquet",
    "kind": "source",
    "version": "1.0",
    "input": None,
    "params": {
        "path": {
            "type": "string",
            "required": False,
            "default": None,
            "description": "Parquet file path. Defaults to the active dataset file.",
        },
        "columns": {
            "type": "array",
            "required": False,
            "default": None,
            "description": "Optional list of Parquet columns to read.",
        },
    },
    "result": {
        "kind": "event_stream",
        "description": "Awkward event stream read from a Parquet file.",
    },
    "provides": {
        "symbols": [
            {"from": "params.columns", "kind": "field_list"},
        ],
    },
}


def run_parquet_source(
    *,
    path: str | None = None,
    columns: list[str] | None = None,
    ctx: dict[str, Any] | None = None,
    **params: Any,
) -> ak.Array:
    source_path = _resolve_source_path(path, ctx=ctx)
    table = pq.read_table(source_path, columns=columns)
    return ak.Array(table.to_pydict())


def _resolve_source_path(path: str | None, *, ctx: dict[str, Any] | None) -> Path:
    if path:
        return _existing_path(Path(path))

    dataset = _active_dataset(ctx)
    files = dataset.get("files") or []
    if not isinstance(files, list) or not files:
        raise ValueError(
            "workshop.parquet requires a path parameter or an active dataset file"
        )
    if len(files) != 1:
        raise ValueError(
            "workshop.parquet reads one file per source invocation; "
            f"got {len(files)} active dataset files"
        )
    return _existing_path(Path(str(files[0])))


def _active_dataset(ctx: dict[str, Any] | None) -> dict[str, Any]:
    ctx = dict(ctx or {})
    dataset = ctx.get("dataset")
    if isinstance(dataset, dict):
        return dict(dataset)

    dataset_name = ctx.get("dataset_name")
    datasets = ctx.get("datasets")
    if isinstance(datasets, dict) and dataset_name in datasets:
        value = datasets[dataset_name]
        if isinstance(value, dict):
            return dict(value)

    return {}


def _existing_path(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(f"Parquet source file does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"Parquet source path is not a file: {path}")
    return path
