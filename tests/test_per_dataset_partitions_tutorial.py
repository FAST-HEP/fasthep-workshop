from __future__ import annotations

import math
from pathlib import Path

import yaml

WORKSHOP_ROOT = Path(__file__).parents[1]
TUTORIAL = WORKSHOP_ROOT / "tutorials" / "99-extras" / "per-dataset-partitions"
EXPECTED_PARTITIONS = 5


def _datasets() -> list[dict]:
    payload = yaml.safe_load((TUTORIAL / "datasets.yaml").read_text())
    return payload["data"]["datasets"]


def test_per_dataset_chunk_sizes_give_five_partitions_each() -> None:
    datasets = _datasets()

    assert len(datasets) == 9
    for dataset in datasets:
        nevents = int(dataset["nevents"])
        chunk_size = dataset["chunk_size"]
        assert math.ceil(nevents / chunk_size) == EXPECTED_PARTITIONS, dataset["name"]


def test_workflow_enables_per_dataset_mode() -> None:
    workflow = yaml.safe_load((TUTORIAL / "workflow.yaml").read_text())

    assert workflow["execution"]["partitioning"]["per_dataset"] is True
    assert workflow["include"] == ["datasets.yaml"]
