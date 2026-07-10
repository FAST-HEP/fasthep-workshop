from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Literal, cast
from urllib.parse import urlparse

import awkward as ak  # type: ignore[import-untyped]
import numpy as np
from numpy.typing import NDArray

EventType = Literal["data", "mc"]
ToyProcess = Literal["dy", "ttbar", "qcd", "data"]

DEFAULT_NEVENTS = 1_000_000
DEFAULT_DATASET = "toy"
DEFAULT_EVENT_WEIGHT = 1.0
DEFAULT_SEED = 12345
DEFAULT_PROCESS: ToyProcess = "dy"

SUPPORTED_TOY_PROCESSES = frozenset({"dy", "ttbar", "qcd", "data"})

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
            "default": DEFAULT_SEED,
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
        "weight": {
            "type": "number",
            "required": False,
            "default": None,
            "description": "Alias for event_weight, matching dataset-style weights.",
        },
        "process": {
            "type": "string",
            "required": False,
            "default": DEFAULT_PROCESS,
            "description": "Toy process: dy, ttbar, qcd, or data.",
        },
    },
    "result": {
        "kind": "event_stream",
        "description": "Deterministic Awkward toy event stream.",
    },
}


@dataclass(frozen=True)
class ToyDatasetConfig:
    name: str = DEFAULT_DATASET
    event_type: EventType = "mc"
    process: ToyProcess = DEFAULT_PROCESS
    nevents: int = DEFAULT_NEVENTS
    seed: int = DEFAULT_SEED
    event_weight: float = DEFAULT_EVENT_WEIGHT


@dataclass(frozen=True)
class ToyObjects:
    px: ak.Array
    py: ak.Array
    pz: ak.Array
    extra: ak.Array | None = None


def parse_toy_uri(uri: str) -> str:
    parsed = urlparse(uri)
    if parsed.scheme != "toy":
        raise ValueError(f"Unsupported toy source URI scheme {parsed.scheme!r}: {uri!r}")

    process = (parsed.netloc or parsed.path.lstrip("/")).lower()
    if process not in SUPPORTED_TOY_PROCESSES:
        allowed = ", ".join(sorted(SUPPORTED_TOY_PROCESSES))
        raise ValueError(f"Unsupported toy process {process!r}; expected one of: {allowed}")
    return process


def dataset_config_from_ctx(ctx: dict[str, Any] | None) -> ToyDatasetConfig:
    ctx = dict(ctx or {})
    dataset = _active_dataset(ctx)
    metadata = _dataset_metadata(dataset)
    process = _process_from_dataset(dataset) or _normalize_process(
        ctx.get("process"),
        default=DEFAULT_PROCESS,
    )
    event_type = _normalize_event_type(
        dataset.get("eventtype")
        or dataset.get("event_type")
        or metadata.get("eventtype")
        or metadata.get("event_type")
        or ctx.get("dataset_eventtype")
        or ctx.get("eventtype")
        or ctx.get("event_type")
        or ("data" if process == "data" else "mc")
    )

    return ToyDatasetConfig(
        name=str(dataset.get("name") or ctx.get("dataset_name") or DEFAULT_DATASET),
        event_type=event_type,
        process=process,
        nevents=_normalize_nevents(
            dataset.get("nevents") or metadata.get("nevents") or ctx.get("nevents")
        ),
        seed=_normalize_seed(dataset.get("seed") or metadata.get("seed") or ctx.get("seed")),
        event_weight=_normalize_weight(
            dataset.get("weight")
            or dataset.get("event_weight")
            or metadata.get("weight")
            or metadata.get("event_weight")
            or ctx.get("dataset_weight")
            or ctx.get("weight")
            or ctx.get("event_weight")
        ),
    )


def generate_muons(
    rng: np.random.Generator,
    event_count: int,
    *,
    process: ToyProcess,
) -> tuple[ToyObjects, ak.Array]:
    count_probabilities = {
        "dy": [0.05, 0.80, 0.10, 0.05],
        "ttbar": [0.10, 0.35, 0.45, 0.10],
        "qcd": [0.70, 0.25, 0.04, 0.01],
        "data": [0.06, 0.78, 0.11, 0.05],
    }[process]
    counts = rng.choice(np.arange(4), size=event_count, p=count_probabilities)

    pt = rng.gamma(shape=4.0, scale=_muon_scale(process), size=int(np.sum(counts)))
    phi = rng.uniform(-np.pi, np.pi, size=pt.size)
    muons = ToyObjects(
        px=ak.unflatten(pt * np.cos(phi), counts),
        py=ak.unflatten(pt * np.sin(phi), counts),
        pz=ak.unflatten(rng.normal(0.0, 32.0, size=pt.size), counts),
        extra=ak.unflatten(rng.beta(1.4, 28.0, size=pt.size), counts),
    )
    charges = ak.unflatten(rng.choice([-1, 1], size=pt.size), counts)
    return muons, charges


def generate_jets(
    rng: np.random.Generator,
    event_count: int,
    *,
    process: ToyProcess,
) -> ToyObjects:
    count_probabilities = {
        "dy": [0.10, 0.60, 0.20, 0.10],
        "ttbar": [0.03, 0.17, 0.45, 0.35],
        "qcd": [0.15, 0.45, 0.25, 0.15],
        "data": [0.10, 0.59, 0.21, 0.10],
    }[process]
    counts = rng.choice(np.arange(3, 7), size=event_count, p=count_probabilities)

    pt = rng.gamma(shape=8.0, scale=_jet_scale(process), size=int(np.sum(counts)))
    phi = rng.uniform(-np.pi, np.pi, size=pt.size)
    return ToyObjects(
        px=ak.unflatten(pt * np.cos(phi), counts),
        py=ak.unflatten(pt * np.sin(phi), counts),
        pz=ak.unflatten(rng.normal(0.0, 100.0, size=pt.size), counts),
    )


def compute_met(
    muons: ToyObjects,
    jets: ToyObjects,
) -> tuple[ak.Array, ak.Array, NDArray[np.float64]]:
    met_px = -(ak.sum(muons.px, axis=1) + ak.sum(jets.px, axis=1))
    met_py = -(ak.sum(muons.py, axis=1) + ak.sum(jets.py, axis=1))
    met = np.sqrt(np.asarray(met_px) ** 2 + np.asarray(met_py) ** 2)
    return met_px, met_py, met


def build_event_record(
    *,
    cfg: ToyDatasetConfig,
    rng: np.random.Generator,
    muons: ToyObjects,
    muon_charge: ak.Array,
    jets: ToyObjects,
    met_px: ak.Array,
    met_py: ak.Array,
    met: NDArray[np.float64],
) -> ak.Array:
    event_count = cfg.nevents
    record = {
        "EventNumber": np.arange(event_count, dtype=np.int64),
        "RunNumber": rng.integers(300_000, 310_000, size=event_count, dtype=np.int32),
        "LumiBlock": rng.integers(1, 2_001, size=event_count, dtype=np.int32),
        "Dataset": np.full(event_count, cfg.name),
        "EventWeight": _event_weights(cfg),
        "Trigger": rng.random(event_count) < 0.98,
        "Muon_Px": muons.px,
        "Muon_Py": muons.py,
        "Muon_Pz": muons.pz,
        "Muon_Iso": muons.extra,
        "Muon_Charge": muon_charge,
        "Jet_Px": jets.px,
        "Jet_Py": jets.py,
        "Jet_Pz": jets.pz,
        "MET_Px": met_px,
        "MET_Py": met_py,
        "MET": met,
    }
    if cfg.event_type == "mc":
        record["MCLepton_Px"] = muons.px
        record["MCLepton_Py"] = muons.py
    return ak.Array(record)


def run_toy_source(
    *,
    nevents: int | None = None,
    seed: int | None = None,
    dataset: str | None = None,
    event_type: EventType | str | None = None,
    eventtype: EventType | str | None = None,
    event_weight: float | None = None,
    weight: float | None = None,
    process: str | None = None,
    datasets: list[dict[str, Any]] | None = None,
    defaults: dict[str, Any] | None = None,
    ctx: dict[str, Any] | None = None,
    **params: Any,
) -> ak.Array:
    del params
    runtime_ctx = _ctx_with_explicit_datasets(ctx, datasets, defaults)
    cfg = _merge_source_params(
        dataset_config_from_ctx(runtime_ctx),
        ctx=runtime_ctx,
        nevents=nevents,
        seed=seed,
        dataset=dataset,
        event_type=event_type or eventtype,
        event_weight=event_weight if event_weight is not None else weight,
        process=process,
    )

    rng = np.random.default_rng(cfg.seed)
    muons, muon_charge = generate_muons(rng, cfg.nevents, process=cfg.process)
    jets = generate_jets(rng, cfg.nevents, process=cfg.process)
    met_px, met_py, met = compute_met(muons, jets)
    return build_event_record(
        cfg=cfg,
        rng=rng,
        muons=muons,
        muon_charge=muon_charge,
        jets=jets,
        met_px=met_px,
        met_py=met_py,
        met=met,
    )


def _active_dataset(ctx: dict[str, Any]) -> dict[str, Any]:
    dataset = ctx.get("dataset")
    if isinstance(dataset, dict):
        return dict(dataset)

    for key in ("current_dataset", "active_dataset"):
        candidate = ctx.get(key)
        if isinstance(candidate, dict):
            return dict(candidate)

    dataset_name = ctx.get("dataset_name")
    datasets = ctx.get("datasets")
    if isinstance(datasets, dict):
        if dataset_name in datasets and isinstance(datasets[dataset_name], dict):
            return dict(datasets[dataset_name])
        if len(datasets) == 1:
            only = next(iter(datasets.values()))
            if isinstance(only, dict):
                return dict(only)

    if isinstance(datasets, list):
        for candidate in datasets:
            if not isinstance(candidate, dict):
                continue
            if dataset_name is None or candidate.get("name") == dataset_name:
                return dict(candidate)

    if dataset_name is not None:
        return {"name": str(dataset_name)}
    return {}


def _ctx_with_explicit_datasets(
    ctx: dict[str, Any] | None,
    datasets: list[dict[str, Any]] | None,
    defaults: dict[str, Any] | None,
) -> dict[str, Any] | None:
    merged = dict(ctx or {})
    if datasets is not None and "datasets" not in merged:
        merged["datasets"] = datasets
    if defaults:
        for key, value in defaults.items():
            merged.setdefault(key, value)
    return merged


def _process_from_dataset(dataset: dict[str, Any]) -> ToyProcess | None:
    for uri in dataset.get("files") or ():
        if not isinstance(uri, str):
            continue
        return _normalize_process(parse_toy_uri(uri), default=DEFAULT_PROCESS)
    metadata = _dataset_metadata(dataset)
    if metadata.get("process") is not None:
        return _normalize_process(metadata["process"], default=DEFAULT_PROCESS)
    if dataset.get("process") is not None:
        return _normalize_process(dataset["process"], default=DEFAULT_PROCESS)
    return None


def _dataset_metadata(dataset: dict[str, Any]) -> dict[str, Any]:
    metadata = dataset.get("metadata") or dataset.get("meta") or {}
    return dict(metadata) if isinstance(metadata, dict) else {}


def _merge_source_params(
    cfg: ToyDatasetConfig,
    *,
    ctx: dict[str, Any] | None,
    nevents: int | None,
    seed: int | None,
    dataset: str | None,
    event_type: EventType | str | None,
    event_weight: float | None,
    process: str | None,
) -> ToyDatasetConfig:
    ctx = dict(ctx or {})
    dataset_cfg = _active_dataset(ctx)
    metadata = _dataset_metadata(dataset_cfg)
    updates: dict[str, Any] = {}
    if nevents is not None and not _has_any(dataset_cfg, metadata, ctx, "nevents"):
        updates["nevents"] = _normalize_nevents(nevents)
    if seed is not None and not _has_any(dataset_cfg, metadata, ctx, "seed"):
        updates["seed"] = _normalize_seed(seed)
    if dataset is not None and "name" not in dataset_cfg and "dataset_name" not in ctx:
        updates["name"] = str(dataset)
    if process is not None and not _has_process(dataset_cfg, metadata, ctx):
        updates["process"] = _normalize_process(process, default=cfg.process)
    if event_type is not None and not _has_event_type(dataset_cfg, metadata, ctx):
        updates["event_type"] = _normalize_event_type(event_type)
    elif updates.get("process") == "data":
        updates["event_type"] = "data"
    if event_weight is not None and not _has_weight(dataset_cfg, metadata, ctx):
        updates["event_weight"] = _normalize_weight(event_weight)
    return replace(cfg, **updates)


def _normalize_process(value: Any, *, default: ToyProcess) -> ToyProcess:
    if value is None:
        return default
    process = str(value).lower()
    if process not in SUPPORTED_TOY_PROCESSES:
        allowed = ", ".join(sorted(SUPPORTED_TOY_PROCESSES))
        raise ValueError(f"Unsupported toy process {process!r}; expected one of: {allowed}")
    return cast(ToyProcess, process)


def _has_any(
    dataset: dict[str, Any],
    metadata: dict[str, Any],
    ctx: dict[str, Any],
    key: str,
) -> bool:
    return key in dataset or key in metadata or key in ctx


def _has_event_type(
    dataset: dict[str, Any],
    metadata: dict[str, Any],
    ctx: dict[str, Any],
) -> bool:
    keys = {"eventtype", "event_type"}
    return bool(keys & dataset.keys() or keys & metadata.keys() or keys & ctx.keys()) or (
        "dataset_eventtype" in ctx
    )


def _has_weight(
    dataset: dict[str, Any],
    metadata: dict[str, Any],
    ctx: dict[str, Any],
) -> bool:
    keys = {"weight", "event_weight"}
    return bool(keys & dataset.keys() or keys & metadata.keys() or keys & ctx.keys()) or (
        "dataset_weight" in ctx
    )


def _has_process(
    dataset: dict[str, Any],
    metadata: dict[str, Any],
    ctx: dict[str, Any],
) -> bool:
    return (
        bool(dataset.get("files"))
        or "process" in dataset
        or "process" in metadata
        or "process" in ctx
    )


def _normalize_event_type(value: Any) -> EventType:
    event_type = str(value or "mc").lower()
    if event_type not in {"data", "mc"}:
        raise ValueError("event_type must be 'data' or 'mc'")
    return "data" if event_type == "data" else "mc"


def _normalize_nevents(value: Any) -> int:
    event_count = int(DEFAULT_NEVENTS if value is None else value)
    if event_count < 0:
        raise ValueError("nevents must be non-negative")
    return event_count


def _normalize_seed(value: Any) -> int:
    return int(DEFAULT_SEED if value is None else value)


def _normalize_weight(value: Any) -> float:
    return float(DEFAULT_EVENT_WEIGHT if value is None else value)


def _event_weights(cfg: ToyDatasetConfig) -> NDArray[np.float64]:
    if cfg.event_type == "data" or cfg.process == "data":
        return np.ones(cfg.nevents)
    return np.full(cfg.nevents, cfg.event_weight)


def _muon_scale(process: ToyProcess) -> float:
    return {"dy": 8.0, "ttbar": 10.0, "qcd": 5.5, "data": 8.0}[process]


def _jet_scale(process: ToyProcess) -> float:
    return {"dy": 35.0, "ttbar": 42.0, "qcd": 28.0, "data": 35.0}[process]
