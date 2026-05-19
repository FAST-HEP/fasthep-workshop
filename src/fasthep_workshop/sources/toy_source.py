from __future__ import annotations

from typing import Any, Literal

import awkward as ak  # type: ignore[import-untyped]
import numpy as np

EventType = Literal["data", "mc"]

DEFAULT_NEVENTS = 1_000_000
DEFAULT_DATASET = "toy"
DEFAULT_EVENT_WEIGHT = 1.0

TOY_SOURCE_SPEC = {
    "name": "workshop.toy_source",
    "kind": "source",
    "version": "1.0",
    "input": None,
    "params": {
        "nevents": {
            "type": "integer",
            "required": False,
            "default": DEFAULT_NEVENTS,
            "description": "Number of deterministic toy events to generate.",
        },
        "seed": {
            "type": "integer",
            "required": False,
            "default": 12345,
            "description": "NumPy random seed.",
        },
        "dataset": {
            "type": "string",
            "required": False,
            "default": DEFAULT_DATASET,
            "description": "Dataset label written to the Dataset event field.",
        },
        "event_type": {
            "type": "string",
            "required": False,
            "default": "mc",
            "description": "Toy event type: data or mc.",
        },
        "eventtype": {
            "type": "string",
            "required": False,
            "default": None,
            "description": "Alias for event_type, matching FAST-HEP dataset metadata.",
        },
        "event_weight": {
            "type": "number",
            "required": False,
            "default": DEFAULT_EVENT_WEIGHT,
            "description": "Flat MC event weight. Data events always use 1.0.",
        },
    },
    "result": {
        "kind": "event_stream",
        "description": "Deterministic Awkward toy event stream.",
    },
}


def run_toy_source(
    *,
    nevents: int | None = None,
    seed: int = 12345,
    dataset: str | None = None,
    event_type: EventType | str | None = None,
    eventtype: EventType | str | None = None,
    event_weight: float = DEFAULT_EVENT_WEIGHT,
    datasets: list[dict[str, Any]] | None = None,
    defaults: dict[str, Any] | None = None,
    ctx: dict[str, Any] | None = None,
    **params: Any,
) -> ak.Array:
    defaults = dict(defaults or {})
    dataset_cfg = _first_dataset_config(datasets)
    event_count = _event_count(nevents, dataset_cfg)
    dataset_name = _dataset_name(dataset, dataset_cfg, ctx)
    normalized_event_type = _event_type(
        event_type or eventtype,
        dataset_cfg,
        defaults,
        ctx,
    )

    rng = np.random.default_rng(seed)

    muon_counts = rng.choice(
        np.arange(4),
        size=event_count,
        p=[0.05, 0.80, 0.10, 0.05],
    )
    jet_counts = rng.choice(np.arange(3, 7), size=event_count, p=[0.10, 0.60, 0.20, 0.10])

    muon_pt = rng.gamma(shape=4.0, scale=8.0, size=int(np.sum(muon_counts)))
    muon_phi = rng.uniform(-np.pi, np.pi, size=muon_pt.size)
    muon_px = ak.unflatten(muon_pt * np.cos(muon_phi), muon_counts)
    muon_py = ak.unflatten(muon_pt * np.sin(muon_phi), muon_counts)
    muon_pz = ak.unflatten(rng.normal(0.0, 32.0, size=muon_pt.size), muon_counts)
    muon_iso = ak.unflatten(rng.beta(1.4, 28.0, size=muon_pt.size), muon_counts)
    muon_charge = ak.unflatten(rng.choice([-1, 1], size=muon_pt.size), muon_counts)

    jet_pt = rng.gamma(shape=8.0, scale=35.0, size=int(np.sum(jet_counts)))
    jet_phi = rng.uniform(-np.pi, np.pi, size=jet_pt.size)
    jet_px = ak.unflatten(jet_pt * np.cos(jet_phi), jet_counts)
    jet_py = ak.unflatten(jet_pt * np.sin(jet_phi), jet_counts)
    jet_pz = ak.unflatten(rng.normal(0.0, 100.0, size=jet_pt.size), jet_counts)

    visible_px = ak.sum(muon_px, axis=1) + ak.sum(jet_px, axis=1)
    visible_py = ak.sum(muon_py, axis=1) + ak.sum(jet_py, axis=1)
    met_px = -visible_px
    met_py = -visible_py

    return ak.Array(
        {
            "EventNumber": np.arange(event_count, dtype=np.int64),
            "RunNumber": rng.integers(300_000, 310_000, size=event_count, dtype=np.int32),
            "LumiBlock": rng.integers(1, 2_001, size=event_count, dtype=np.int32),
            "Dataset": np.full(event_count, dataset_name),
            "EventWeight": _event_weights(
                event_count,
                event_type=normalized_event_type,
                event_weight=event_weight,
            ),
            "Trigger": rng.random(event_count) < 0.98,
            "Muon_Px": muon_px,
            "Muon_Py": muon_py,
            "Muon_Pz": muon_pz,
            "Muon_Iso": muon_iso,
            "Muon_Charge": muon_charge,
            "Jet_Px": jet_px,
            "Jet_Py": jet_py,
            "Jet_Pz": jet_pz,
            "MET_Px": met_px,
            "MET_Py": met_py,
            "MET": np.sqrt(np.asarray(met_px) ** 2 + np.asarray(met_py) ** 2),
        }
    )


def _first_dataset_config(datasets: list[dict[str, Any]] | None) -> dict[str, Any]:
    if not datasets:
        return {}
    first = datasets[0]
    return dict(first) if isinstance(first, dict) else {}


def _event_count(nevents: int | None, dataset_cfg: dict[str, Any]) -> int:
    raw = nevents if nevents is not None else dataset_cfg.get("nevents", DEFAULT_NEVENTS)
    event_count = int(raw)
    if event_count < 0:
        raise ValueError("nevents must be non-negative")
    return event_count


def _dataset_name(
    dataset: str | None,
    dataset_cfg: dict[str, Any],
    ctx: dict[str, Any] | None,
) -> str:
    ctx = dict(ctx or {})
    return str(
        dataset
        or dataset_cfg.get("name")
        or ctx.get("dataset_name")
        or ctx.get("dataset")
        or DEFAULT_DATASET
    )


def _event_type(
    event_type: EventType | str | None,
    dataset_cfg: dict[str, Any],
    defaults: dict[str, Any],
    ctx: dict[str, Any] | None,
) -> EventType:
    ctx = dict(ctx or {})
    value = str(
        event_type
        or dataset_cfg.get("eventtype")
        or defaults.get("eventtype")
        or ctx.get("dataset_eventtype")
        or "mc"
    ).lower()
    if value not in {"data", "mc"}:
        raise ValueError("event_type must be 'data' or 'mc'")
    if value == "data":
        return "data"
    return "mc"


def _event_weights(
    event_count: int,
    *,
    event_type: EventType,
    event_weight: float,
) -> np.ndarray:
    if event_type == "data":
        return np.ones(event_count)
    return np.full(event_count, float(event_weight))
