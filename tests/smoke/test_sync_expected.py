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


def test_schema_summary_keeps_compact_schema_fields() -> None:
    summary = sync_expected.schema_summary(
        {
            "node_id": "read.events",
            "metadata": {"dataset_name": "DoubleMuon"},
            "awkward_type": {
                "Muon_pt": "float[]",
                "run": "uint32_t",
            },
            "inspected_python_type": "RootTreeSchema",
            "fields": ["run", "Muon_pt"],
        }
    )

    assert summary == {
        "node_id": "read.events",
        "metadata": {"dataset_name": "DoubleMuon"},
        "awkward_type": {
            "Muon_pt": "float[]",
            "run": "uint32_t",
        },
        "inspected_python_type": "RootTreeSchema",
    }


def test_schema_summary_limits_awkward_type_entries() -> None:
    summary = sync_expected.schema_summary(
        {
            "awkward_type": {
                "f": "int",
                "a": "int",
                "e": "int",
                "b": "int",
                "d": "int",
                "c": "int",
            }
        },
        limit=5,
    )

    assert list(summary["awkward_type"]) == ["a", "b", "c", "d", "e"]


def test_schema_summary_invalid_top_level_errors_clearly() -> None:
    with pytest.raises(ValueError, match="schema_summary expects a JSON object"):
        sync_expected.schema_summary([])


def test_schema_summary_invalid_mapping_field_errors_clearly() -> None:
    with pytest.raises(ValueError, match="awkward_type to be a mapping"):
        sync_expected.schema_summary({"awkward_type": []})


def test_schema_summary_invalid_inspected_python_type_errors_clearly() -> None:
    with pytest.raises(ValueError, match="inspected_python_type to be a string"):
        sync_expected.schema_summary({"inspected_python_type": {}})


def test_write_schema_summary_writes_pretty_json(tmp_path: Path) -> None:
    source = tmp_path / "build" / "reports" / "schema.json"
    target = tmp_path / "tutorial" / "expected" / "snippets" / "schema.summary.json"
    source.parent.mkdir(parents=True)
    source.write_text(
        json.dumps(
            {
                "node_id": "read.events",
                "metadata": {"dataset_name": "DoubleMuon"},
                "awkward_type": {
                    "b": "float",
                    "a": "int",
                },
                "inspected_python_type": "RootTreeSchema",
            }
        ),
        encoding="utf-8",
    )

    sync_expected.write_schema_summary(source, target)

    assert target.exists()
    assert target.read_text(encoding="utf-8").endswith("\n")
    assert json.loads(target.read_text(encoding="utf-8")) == {
        "node_id": "read.events",
        "metadata": {"dataset_name": "DoubleMuon"},
        "awkward_type": {
            "a": "int",
            "b": "float",
        },
        "inspected_python_type": "RootTreeSchema",
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
