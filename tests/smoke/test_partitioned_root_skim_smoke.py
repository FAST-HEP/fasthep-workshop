from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import pytest
import uproot  # type: ignore[import-untyped]
import yaml  # type: ignore[import-untyped]
from hepflow.api import run_workflow_file

pytestmark = pytest.mark.smoke

WORKSHOP_ROOT = Path(__file__).parents[2]
WORKFLOW = (
    WORKSHOP_ROOT / "tutorials" / "99-extras" / "partitioned-root-skim" / "workflow.yaml"
)
EXPECTED_BRANCHES = {
    "DiMuon_Mass",
    "EventWeight",
    "HasMuonAbove25",
    "Muon_Charge",
    "Muon_Pt",
    "NIsolatedMuon",
    "NMuon",
    "triggerIsoMu24",
}


def test_partitioned_root_skim_tutorial_runs_and_writes_valid_parts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    if not (WORKSHOP_ROOT / "data" / "CMS" / "Zmumu" / "qcd.root").exists():
        pytest.skip("local CMS/Zmumu tutorial data is not installed")

    monkeypatch.chdir(WORKSHOP_ROOT)
    outdir = tmp_path / "partitioned-root-skim"

    result = run_workflow_file(WORKFLOW, outdir=outdir, chunk_size=40)

    assert result.success
    plan = yaml.safe_load((outdir / "compile" / "plan.yaml").read_text())
    expected_parts = len(plan["partitions"])
    assert expected_parts == 27

    parts = sorted((outdir / "artifacts" / "files" / "dimuon_partition_skim").glob("*/*.root"))
    assert len(parts) == expected_parts
    assert len({part.relative_to(outdir).as_posix() for part in parts}) == expected_parts
    assert Counter(part.parent.name for part in parts) == dict.fromkeys(
        plan["context"]["datasets"],
        3,
    )

    entries_by_dataset: dict[str, int] = defaultdict(int)
    for part in parts:
        with uproot.open(part) as handle:
            tree = handle["events"]
            assert set(tree.keys()) == EXPECTED_BRANCHES
            entries_by_dataset[part.parent.name] += int(tree.num_entries)

    cutflow = json.loads(
        (outdir / "artifacts" / "cutflows" / "SelectDimuonEvents.json").read_text()
    )
    selected_by_dataset = {
        dataset: int(cutflow["nodes"][-1]["stats"][dataset]["n_unweighted_out"])
        for dataset in cutflow["datasets"]
    }
    assert dict(entries_by_dataset) == selected_by_dataset

    writer_manifest = json.loads(
        (
            outdir
            / "artifacts"
            / "files"
            / "dimuon_partition_skim"
            / "manifest.json"
        ).read_text()
    )
    manifest_file_count = sum(
        len(dataset["files"]) for dataset in writer_manifest["datasets"].values()
    )
    assert manifest_file_count == expected_parts

    histogram_files = sorted((outdir / "artifacts" / "histograms").glob("*.pkl"))
    assert [path.name for path in histogram_files] == ["DiMuonMass.pkl"]
    assert (outdir / "artifacts" / "cutflows" / "SelectDimuonEvents.json").exists()
