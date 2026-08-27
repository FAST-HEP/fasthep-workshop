from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import yaml  # type: ignore[import-untyped]
from hepflow.api import compile_workflow_file, run_workflow_file
from hepflow.backends._dask._htcondor import normalize_dask_htcondor_config

WORKSHOP_ROOT = Path(__file__).parents[1]
LOCAL_DASK = WORKSHOP_ROOT / "tutorials/07-scale-execution/01-local-dask/workflow.yaml"
HTCONDOR = WORKSHOP_ROOT / "tutorials/07-scale-execution/02-dask-condor/workflow.yaml"
CHUNK_SIZE = 3000


def test_scale_execution_tutorial_structure_exists() -> None:
    root = WORKSHOP_ROOT / "tutorials/07-scale-execution"

    assert [
        path.name
        for path in sorted(item for item in root.iterdir() if item.is_dir())
    ] == [
        "01-local-dask",
        "02-dask-condor",
        "03-forward-data",
        "04-worker-resources",
        "05-slurm",
    ]
    for name in [
        "01-local-dask",
        "02-dask-condor",
        "03-forward-data",
        "04-worker-resources",
        "05-slurm",
    ]:
        assert (root / name / "README.md").exists()


def test_local_dask_tutorial_compiles_to_many_partitions(tmp_path: Path) -> None:
    plan = compile_workflow_file(
        LOCAL_DASK,
        outdir=tmp_path / "compile-local-dask",
        chunk_size=CHUNK_SIZE,
    )

    assert plan.execution["backend"] == "dask"
    assert plan.execution["strategy"] == "local"
    assert plan.execution["config"]["workers"] == 4
    assert plan.execution["config"]["threads_per_worker"] == 1
    assert len(plan.partitions) == 24
    assert {partition.dataset for partition in plan.partitions} == {
        "dy",
        "qcd",
        "ttbar",
    }


def test_htcondor_tutorial_compiles_and_requests_ten_workers(
    tmp_path: Path,
) -> None:
    plan = compile_workflow_file(
        HTCONDOR,
        outdir=tmp_path / "compile-htcondor",
        chunk_size=CHUNK_SIZE,
    )
    htcondor_config = normalize_dask_htcondor_config(plan.execution)

    assert plan.execution["backend"] == "dask"
    assert plan.execution["strategy"] == "htcondor"
    assert len(plan.partitions) == 24
    assert htcondor_config["workers"] == 10
    assert htcondor_config["scale"] == {"default": 10}
    assert htcondor_config["cluster_options"]["cores"] == 1
    assert htcondor_config["cluster_options"]["memory"] == "2GB"
    assert htcondor_config["cluster_options"]["disk"] == "2GB"
    assert "walltime" not in htcondor_config["cluster_options"]


def test_local_dask_result_matches_ordinary_local_backend(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(WORKSHOP_ROOT)
    dask_out = tmp_path / "local-dask"
    local_out = tmp_path / "local-backend"

    dask_result = run_workflow_file(
        LOCAL_DASK,
        outdir=dask_out,
        chunk_size=CHUNK_SIZE,
    )
    local_result = run_workflow_file(
        LOCAL_DASK,
        outdir=local_out,
        chunk_size=CHUNK_SIZE,
        backend="local",
    )

    assert dask_result.success
    assert local_result.success
    assert _histogram_payloads(dask_out) == _histogram_payloads(local_out)

    summary = yaml.safe_load((dask_out / "run_summary.yaml").read_text())
    assert summary["backend"]["name"] == "dask"
    assert summary["backend"]["strategy"] == "local"
    assert summary["backend"]["n_workers"] == 4
    assert summary["npartitions"] == 24


def _histogram_payloads(root: Path) -> dict[str, Any]:
    return {
        path.name: json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((root / "artifacts" / "histograms").glob("*.json"))
    }
