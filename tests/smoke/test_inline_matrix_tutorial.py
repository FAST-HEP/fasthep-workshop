from __future__ import annotations

import json
from pathlib import Path

import awkward as ak  # type: ignore[import-untyped]
import numpy as np
import pytest
import uproot  # type: ignore[import-untyped]
import yaml  # type: ignore[import-untyped]
from hepflow.api import run_workflow_file

pytestmark = pytest.mark.smoke

WORKSHOP_ROOT = Path(__file__).parents[2]
WORKFLOW = (
    WORKSHOP_ROOT
    / "tutorials"
    / "05-systematics"
    / "02-variation-matrix-inline"
    / "workflow.yaml"
)
FACTORS = {
    "scale_up": 1.02,
    "scale_down": 0.98,
    "alignment_up": 1.05,
    "alignment_down": 0.95,
}


def test_inline_matrix_shares_prefix_and_writes_all_variations(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(WORKSHOP_ROOT)
    outdir = tmp_path / "matrix"
    result = run_workflow_file(WORKFLOW, outdir=outdir)
    assert result.success
    assert list(outdir.rglob("plan.yaml")) == [outdir / "compile" / "plan.yaml"]
    assert list(outdir.rglob("graph.json")) == [outdir / "graph" / "graph.json"]
    assert not (outdir / "compile" / "systematics.yaml").exists()
    for extension in ("mmd", "dot", "json", "d2"):
        assert (outdir / "graph" / f"graph.{extension}").is_file()

    plan = yaml.safe_load((outdir / "compile" / "plan.yaml").read_text())
    nodes = {node["id"]: node for node in plan["nodes"]}
    expected_nodes = {
        "read.events",
        "stage.BasicVars",
        "stage.CalibrateMuon",
        "stage.MuonKinematics",
        "collect.stage.Output",
        "stage.Output",
        "write.Output.0",
    }
    for variation in FACTORS:
        expected_nodes.update(
            {
                f"stage.CalibrateMuon@{variation}",
                f"stage.MuonKinematics@{variation}",
                f"export.stage.MuonKinematics@{variation}",
            }
        )
        anchor = nodes[f"stage.CalibrateMuon@{variation}"]
        assert anchor["inputs"][0]["node_id"] == "stage.BasicVars"
        source, direction = variation.rsplit("_", 1)
        assert anchor["meta"]["variation"]["matrix_values"] == {
            "source": source,
            "direction": direction,
        }
        assert anchor["params"]["variables"][0]["expr"] == (
            f"RawMuonPt * (1 + {source} * {direction})"
        )
        downstream = nodes[f"stage.MuonKinematics@{variation}"]
        assert downstream["inputs"][0]["node_id"] == anchor["id"]
    assert set(nodes) == expected_nodes
    graph = json.loads((outdir / "graph" / "graph.json").read_text())
    assert {node["id"] for node in graph["nodes"]} == expected_nodes
    assert len(nodes["collect.stage.Output"]["inputs"]) == 5
    assert nodes["stage.Output"]["inputs"][0]["node_id"] == "collect.stage.Output"

    files = list((outdir / "artifacts" / "files" / "momenta").rglob("*.root"))
    assert len(files) == 1
    with uproot.open(files[0]) as root_file:
        arrays = root_file["events"].arrays(library="ak")
    assert len(arrays) == 1000
    nominal = ak.to_numpy(ak.flatten(arrays["MuonPt_nominal"]))
    assert len(nominal) > 0
    for variation, factor in FACTORS.items():
        varied = arrays[f"MuonPt_{variation}"]
        assert ak.to_list(ak.num(varied)) == ak.to_list(
            ak.num(arrays["MuonPt_nominal"])
        )
        values = ak.to_numpy(ak.flatten(varied))
        np.testing.assert_allclose(values, nominal * factor)
        assert not np.array_equal(values, nominal)
