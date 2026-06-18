from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

import pytest
import yaml


def _load_sync_module() -> Any:
    script = Path(__file__).parents[2] / "scripts" / "sync_expected.py"
    spec = importlib.util.spec_from_file_location("sync_expected", script)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sync_expected = _load_sync_module()


def _write_manifest(tutorial: Path, items: list[dict[str, str]]) -> None:
    manifest = tutorial / "expected" / "manifest.yaml"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(yaml.safe_dump({"items": items}), encoding="utf-8")


def test_manifest_loading(tmp_path: Path) -> None:
    tutorial = tmp_path / "tutorial"
    _write_manifest(
        tutorial,
        [{"from": "artifacts/table.csv", "to": "tables/table.csv"}],
    )

    assert sync_expected.load_manifest(tutorial / "expected" / "manifest.yaml") == [
        {
            "from": "artifacts/table.csv",
            "to": "tables/table.csv",
            "mode": "copy",
        }
    ]


def test_copy_mode_creates_parent_directories(tmp_path: Path) -> None:
    tutorial = tmp_path / "tutorial"
    build = tmp_path / "build"
    source = build / "artifacts" / "plots" / "plot.png"
    source.parent.mkdir(parents=True)
    source.write_bytes(b"plot-bytes")
    _write_manifest(
        tutorial,
        [{"from": "artifacts/plots/plot.png", "to": "plots/plot.png"}],
    )

    sync_expected.sync_expected_outputs(tutorial=tutorial, build=build)

    assert (tutorial / "expected" / "plots" / "plot.png").read_bytes() == b"plot-bytes"


def test_cutflow_summary_writes_compact_json(tmp_path: Path) -> None:
    tutorial = tmp_path / "tutorial"
    build = tmp_path / "build"
    source = build / "artifacts" / "cutflows" / "Select.json"
    source.parent.mkdir(parents=True)
    source.write_text(
        json.dumps(
            {
                "nodes": [
                    {
                        "label": "NMuon >= 2",
                        "selection": "All",
                        "stats": {
                            "data": {
                                "n_in": 10,
                                "n_out": 5,
                            }
                        },
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    _write_manifest(
        tutorial,
        [
            {
                "from": "artifacts/cutflows/Select.json",
                "to": "snippets/Select.summary.json",
                "mode": "cutflow_summary",
            }
        ],
    )

    sync_expected.sync_expected_outputs(tutorial=tutorial, build=build)

    summary = json.loads(
        (tutorial / "expected" / "snippets" / "Select.summary.json").read_text(
            encoding="utf-8"
        )
    )
    assert summary == {
        "label": "NMuon >= 2",
        "selection": "All",
        "stats": [
            {
                "dataset": "data",
                "n_in": 10,
                "n_out": 5,
            }
        ],
    }


def test_missing_source_file_errors_clearly(tmp_path: Path) -> None:
    tutorial = tmp_path / "tutorial"
    _write_manifest(
        tutorial,
        [{"from": "artifacts/missing.txt", "to": "snippets/missing.txt"}],
    )

    with pytest.raises(FileNotFoundError, match="Missing expected-output source file"):
        sync_expected.sync_expected_outputs(tutorial=tutorial, build=tmp_path / "build")


def test_missing_manifest_errors_clearly(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Missing expected-output manifest"):
        sync_expected.sync_expected_outputs(
            tutorial=tmp_path / "tutorial",
            build=tmp_path / "build",
        )


def test_dry_run_does_not_write_files(tmp_path: Path) -> None:
    tutorial = tmp_path / "tutorial"
    _write_manifest(
        tutorial,
        [{"from": "artifacts/plots/plot.png", "to": "plots/plot.png"}],
    )

    sync_expected.sync_expected_outputs(
        tutorial=tutorial,
        build=tmp_path / "build",
        dry_run=True,
    )

    assert not (tutorial / "expected" / "plots" / "plot.png").exists()
