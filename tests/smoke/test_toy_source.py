from __future__ import annotations

import awkward as ak  # type: ignore[import-untyped]
import numpy as np

import fasthep_workshop.sources.toy_source as toy_source
from fasthep_workshop.sources.toy_source import run_toy_source

EXPECTED_FIELDS = {
    "EventNumber",
    "RunNumber",
    "LumiBlock",
    "Dataset",
    "EventWeight",
    "Trigger",
    "Muon_Px",
    "Muon_Py",
    "Muon_Pz",
    "Muon_Iso",
    "Muon_Charge",
    "Jet_Px",
    "Jet_Py",
    "Jet_Pz",
    "MET_Px",
    "MET_Py",
    "MET",
}


def test_toy_source_imports() -> None:
    assert toy_source.TOY_SOURCE_SPEC["name"] == "workshop.toy_source"


def test_toy_source_generates_expected_fields_and_shapes() -> None:
    events = run_toy_source(nevents=1000, seed=7, dataset="unit", event_type="data")

    assert len(events) == 1000
    assert set(events.fields) == EXPECTED_FIELDS
    assert set(ak.to_list(events.Dataset)) == {"unit"}

    muon_counts = ak.num(events.Muon_Px, axis=1)
    jet_counts = ak.num(events.Jet_Px, axis=1)

    assert set(ak.to_list(muon_counts)).issubset({0, 1, 2, 3})
    assert set(ak.to_list(jet_counts)).issubset({3, 4, 5, 6})
    assert ak.all(ak.num(events.Muon_Py, axis=1) == muon_counts)
    assert ak.all(ak.num(events.Muon_Pz, axis=1) == muon_counts)
    assert ak.all(ak.num(events.Muon_Iso, axis=1) == muon_counts)
    assert ak.all(ak.num(events.Muon_Charge, axis=1) == muon_counts)
    assert ak.all(ak.num(events.Jet_Py, axis=1) == jet_counts)
    assert ak.all(ak.num(events.Jet_Pz, axis=1) == jet_counts)


def test_toy_source_data_weights_trigger_and_met() -> None:
    events = run_toy_source(nevents=1000, seed=11, event_type="data")

    assert np.all(np.asarray(events.EventWeight) == 1.0)
    assert abs(float(np.mean(np.asarray(events.Trigger))) - 0.98) < 0.03
    assert np.all(np.isfinite(np.asarray(events.MET)))
    assert np.all(np.asarray(events.MET) >= 0.0)


def test_toy_source_is_deterministic_for_same_seed() -> None:
    first = run_toy_source(nevents=1000, seed=123, dataset="same", event_type="mc")
    second = run_toy_source(nevents=1000, seed=123, dataset="same", event_type="mc")

    assert ak.almost_equal(first, second)
