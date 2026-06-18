from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

import yaml


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    sync_expected_outputs(
        tutorial=Path(args.tutorial),
        build=Path(args.build),
        dry_run=args.dry_run,
    )
    return 0


def sync_expected_outputs(*, tutorial: Path, build: Path, dry_run: bool = False) -> None:
    manifest_path = tutorial / "expected" / "manifest.yaml"
    manifest = load_manifest(manifest_path)
    expected_dir = tutorial / "expected"

    print(f"sync expected outputs for {tutorial}")  # noqa: T201
    for item in manifest:
        source_rel = Path(item["from"])
        target_rel = Path(item["to"])
        mode = item.get("mode", "copy")
        source = build / source_rel
        target = expected_dir / target_rel

        print(  # noqa: T201
            f"{mode} {source_rel.as_posix()} -> expected/{target_rel.as_posix()}"
        )
        if dry_run:
            continue

        if mode == "copy":
            copy_item(source, target)
        elif mode == "cutflow_summary":
            write_cutflow_summary(source, target)
        else:
            raise ValueError(f"Unsupported expected-output sync mode: {mode!r}")


def load_manifest(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing expected-output manifest: {path}")

    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError(f"Expected-output manifest must be a mapping: {path}")

    items = raw.get("items")
    if not isinstance(items, list):
        raise ValueError(f"Expected-output manifest must define an items list: {path}")

    normalized: list[dict[str, str]] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"manifest items[{index}] must be a mapping")
        source = item.get("from")
        target = item.get("to")
        mode = item.get("mode", "copy")
        if not isinstance(source, str) or not source.strip():
            raise ValueError(f"manifest items[{index}].from must be a non-empty string")
        if not isinstance(target, str) or not target.strip():
            raise ValueError(f"manifest items[{index}].to must be a non-empty string")
        if not isinstance(mode, str) or not mode.strip():
            raise ValueError(f"manifest items[{index}].mode must be a non-empty string")
        normalized.append({"from": source, "to": target, "mode": mode})

    return normalized


def copy_item(source: Path, target: Path) -> None:
    _require_source(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def write_cutflow_summary(source: Path, target: Path) -> None:
    _require_source(source)
    cutflow = json.loads(source.read_text(encoding="utf-8"))
    summary = cutflow_summary(cutflow)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def cutflow_summary(cutflow: Any) -> dict[str, Any]:
    if not isinstance(cutflow, dict):
        raise ValueError("cutflow_summary expects a JSON object")

    nodes = cutflow.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise ValueError("cutflow_summary requires a non-empty nodes list")

    first_node = nodes[0]
    if not isinstance(first_node, dict):
        raise ValueError("cutflow_summary requires nodes[0] to be an object")

    stats = _first_stat(first_node.get("stats"))
    return {
        "label": first_node.get("label"),
        "selection": first_node.get("selection"),
        "stats": [stats],
    }


def _first_stat(stats: Any) -> dict[str, Any]:
    if isinstance(stats, list):
        if not stats:
            raise ValueError("cutflow_summary requires nodes[0].stats to be non-empty")
        first = stats[0]
        if not isinstance(first, dict):
            raise ValueError("cutflow_summary requires stats entries to be objects")
        return dict(first)

    if isinstance(stats, dict):
        if not stats:
            raise ValueError("cutflow_summary requires nodes[0].stats to be non-empty")
        dataset, values = next(iter(stats.items()))
        if not isinstance(values, dict):
            raise ValueError("cutflow_summary requires dataset stats to be objects")
        return {"dataset": dataset, **values}

    raise ValueError("cutflow_summary requires nodes[0].stats to be a list or mapping")


def _require_source(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing expected-output source file: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Expected-output source is not a file: {path}")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sync curated tutorial expected-output fixtures."
    )
    parser.add_argument(
        "tutorial",
        help="Tutorial directory containing expected/manifest.yaml.",
    )
    parser.add_argument(
        "--build",
        required=True,
        help="Build directory to sync outputs from.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print sync actions without writing files.",
    )
    return parser


if __name__ == "__main__":
    raise SystemExit(main())
