from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import awkward as ak  # type: ignore[import-untyped]
from hepflow.model.io import OutputResult
from prettytable import PrettyTable  # type: ignore[import-untyped]

CONSOLE_TABLE_SPEC = {
    "name": "workshop.console_table",
    "kind": "sink",
    "input": {"name": "target", "required": True},
    "params": {
        "path": {"required": False, "default": None},
        "fields": {"required": True},
        "columns": {"required": True},
        "sort_by": {"required": False, "default": []},
        "limit": {"required": False, "default": None},
    },
    "result": {"artifact": "artifact"},
    "requires": {
        "symbols": [
            {"from": "params.fields", "kind": "field_list"},
            {"from": "params.sort_by", "kind": "field_list"},
        ],
    },
}


def run_console_table(
    *,
    target: ak.Array,
    fields: list[str],
    columns: list[dict[str, Any]],
    path: str | None = None,
    sort_by: list[str] | None = None,
    limit: int | None = None,
    ctx: dict[str, Any] | None = None,
    **params: Any,
) -> OutputResult:
    column_specs = [_normalize_column(item) for item in columns]
    missing_columns = [
        item["field"]
        for item in column_specs
        if item.get("field") is not None and item["field"] not in fields
    ]
    if missing_columns:
        raise ValueError(
            "workshop.console_table columns must be listed in fields; "
            f"missing: {', '.join(missing_columns)}"
        )
    rows = _rows(target, column_specs)

    for field in reversed(sort_by or []):
        _sort_rows(rows, field=field)
    if limit is not None:
        rows = rows[: int(limit)]

    table = PrettyTable()
    table.field_names = [item["header"] for item in column_specs]
    table.align = "l"
    for row in rows:
        table.add_row([_format_value(row, item) for item in column_specs])

    text = table.get_string() + "\n"
    sys.stdout.write(text)

    output_path = Path(path) if path else None
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")

    return OutputResult(
        kind="table",
        path=str(output_path or ""),
        format="text",
        metadata={
            "rows": len(rows),
            "columns": [item["field"] for item in column_specs],
        },
    )


def _normalize_column(item: dict[str, Any]) -> dict[str, Any]:
    field = item.get("field")
    template = item.get("template")
    if not isinstance(field, str) and not isinstance(template, str):
        raise ValueError(
            "workshop.console_table column entries require a field or template"
        )
    return {
        "field": field if isinstance(field, str) else None,
        "header": str(item.get("header") or field),
        "format": item.get("format"),
        "missing": str(item.get("missing", "")),
        "template": template if isinstance(template, str) else None,
    }


def _rows(target: ak.Array, columns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = [
        item["field"]
        for item in columns
        if item.get("field") is not None and item["field"] not in target.fields
    ]
    if missing:
        raise KeyError(
            f"Cannot write table with missing field(s): {', '.join(missing)}"
        )

    data = ak.to_list(target)
    if not isinstance(data, list):
        raise TypeError("workshop.console_table expects a one-dimensional record array")
    return [dict(row) for row in data]


def _sort_key(value: Any) -> tuple[int, Any]:
    if value is None:
        return (1, "")
    return (0, value)


def _sort_rows(rows: list[dict[str, Any]], *, field: str) -> None:
    rows.sort(key=lambda row: _sort_key(row.get(field)))


def _format_value(row: dict[str, Any], spec: dict[str, Any]) -> str:
    if spec.get("template"):
        return str(spec["template"]).format_map(_FormatRow(row))

    value = row.get(spec["field"])
    if value is None:
        return spec["missing"]
    fmt = spec.get("format")
    if fmt:
        return format(value, str(fmt))
    return str(value)


class _FormatRow(dict[str, Any]):
    def __missing__(self, key: str) -> str:
        return ""
