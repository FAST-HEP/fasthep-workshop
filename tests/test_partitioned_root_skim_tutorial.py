from __future__ import annotations

from collections import Counter
from pathlib import Path

from hepflow.api import compile_workflow_file

WORKSHOP_ROOT = Path(__file__).parents[1]
TUTORIAL = WORKSHOP_ROOT / "tutorials" / "99-extras" / "partitioned-root-skim"
WORKFLOW = TUTORIAL / "workflow.yaml"
CHUNK_SIZE = 40
EXPECTED_DATASETS = {
    "data",
    "dy",
    "qcd",
    "single_top",
    "ttbar",
    "wjets",
    "ww",
    "wz",
    "zz",
}


def test_partitioned_root_skim_tutorial_compiles_and_branches(tmp_path: Path) -> None:
    plan = compile_workflow_file(
        WORKFLOW,
        outdir=tmp_path / "partitioned-root-skim",
        chunk_size=CHUNK_SIZE,
    )

    assert set(plan.context["datasets"]) == EXPECTED_DATASETS
    partitions_by_dataset = Counter(partition.dataset for partition in plan.partitions)
    assert set(partitions_by_dataset) == EXPECTED_DATASETS
    assert all(count > 1 for count in partitions_by_dataset.values())
    assert all(count == 3 for count in partitions_by_dataset.values())

    writer = plan.get_node("write.SelectDimuonEvents.0")
    hist = plan.get_node("stage.DiMuonMass")
    selection = plan.get_node("stage.SelectDimuonEvents")

    assert writer.impl == "root_tree"
    assert writer.params["when"] == "partition_end"
    assert writer.params["tree"] == "events"
    assert writer.params["path"] == "dimuon_partition_skim.root"
    assert writer.outputs == {"artifact": "artifact"}
    assert writer.params["keep"] == [
        "EventWeight",
        "triggerIsoMu24",
        "NMuon",
        "Muon_Pt",
        "Muon_Charge",
        "NIsolatedMuon",
        "HasMuonAbove25",
        "DiMuon_Mass",
    ]

    writer_input = writer.inputs[0]
    hist_input = hist.inputs[0]
    assert writer_input.node_id == selection.id
    assert writer_input.output_name == "stream"
    assert hist_input.node_id == selection.id
    assert hist_input.output_name == "stream"
    assert hist.impl == "hep.hist"
