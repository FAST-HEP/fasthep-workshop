from __future__ import annotations

import importlib.resources as resources
from pathlib import Path

import pytest
import yaml  # type: ignore[import-untyped]
from hepflow.api import compile_author_file, run_author_file
from hepflow.compiler.profiles import load_profile_config

import fasthep_workshop

WORKSHOP_ROOT = Path(__file__).parents[2]

AUTHOR_PATHS = [
    WORKSHOP_ROOT / "examples" / "CMS" / "Zmumu" / "author.yaml",
    WORKSHOP_ROOT / "examples" / "CMS" / "L1Trigger" / "author.yaml",
    WORKSHOP_ROOT / "examples" / "LZ" / "mssi" / "author.yaml",
    WORKSHOP_ROOT / "examples" / "testing" / "split-packages" / "author.yaml",
    WORKSHOP_ROOT / "examples" / "testing" / "runtime-smoke" / "author.yaml",
]

DOMAIN_NEUTRAL_AUTHOR_PATHS = [
    WORKSHOP_ROOT / "examples" / "NASA" / "exoplanets" / "author.yaml",
]

READ_DATA_TUTORIAL_AUTHOR_PATHS = [
    WORKSHOP_ROOT / "tutorials" / "01-read-data" / "01-root-files" / "author.yaml",
    WORKSHOP_ROOT / "tutorials" / "01-read-data" / "02-datasets" / "author.yaml",
    WORKSHOP_ROOT / "tutorials" / "01-read-data" / "03-remote-data" / "author.yaml",
]

TRANSFORM_DATA_TUTORIAL_AUTHOR_PATHS = [
    WORKSHOP_ROOT
    / "tutorials"
    / "02-transform-data"
    / "01-derived-columns"
    / "author.yaml",
    WORKSHOP_ROOT
    / "tutorials"
    / "02-transform-data"
    / "02-object-selections"
    / "author.yaml",
    WORKSHOP_ROOT
    / "tutorials"
    / "02-transform-data"
    / "03-field-mapping"
    / "author.yaml",
]

SUMMARISE_DATA_TUTORIAL_AUTHOR_PATHS = [
    WORKSHOP_ROOT / "tutorials" / "03-summarise-data" / "01-histograms" / "author.yaml",
    WORKSHOP_ROOT
    / "tutorials"
    / "03-summarise-data"
    / "02-render-histograms"
    / "author.yaml",
    WORKSHOP_ROOT
    / "tutorials"
    / "03-summarise-data"
    / "03-two-dimensional-histograms"
    / "author.yaml",
    WORKSHOP_ROOT
    / "tutorials"
    / "03-summarise-data"
    / "04-cutflow-tables"
    / "author.yaml",
]


@pytest.mark.parametrize("author_path", AUTHOR_PATHS)
def test_author_yaml_parses(author_path: Path) -> None:
    doc = yaml.safe_load(author_path.read_text(encoding="utf-8"))

    assert isinstance(doc, dict)
    assert doc["use"]["profiles"] == [
        "registry",
        "fasthep_carpenter:registry",
        "fasthep_curator:registry",
        "fasthep_curator:default_context",
        "fasthep_curator:runtime_diagnostics",
        "fasthep_render:registry",
        "fasthep_workshop:registry",
    ]


@pytest.mark.parametrize("author_path", DOMAIN_NEUTRAL_AUTHOR_PATHS)
def test_domain_neutral_author_yaml_parses(author_path: Path) -> None:
    doc = yaml.safe_load(author_path.read_text(encoding="utf-8"))

    assert isinstance(doc, dict)
    assert doc["use"]["profiles"] == [
        "registry",
        "fasthep_workshop:registry",
    ]


def test_fasthep_workshop_imports() -> None:
    assert fasthep_workshop.__version__


def test_package_profiles_are_installed_resources() -> None:
    profile_refs = [
        ("fasthep_carpenter.profiles", "registry.yaml"),
        ("fasthep_curator.profiles", "registry.yaml"),
        ("fasthep_curator.profiles", "default_context.yaml"),
        ("fasthep_curator.profiles", "runtime_diagnostics.yaml"),
        ("fasthep_render.profiles", "registry.yaml"),
        ("fasthep_workshop.profiles", "registry.yaml"),
    ]

    for package, name in profile_refs:
        text = resources.files(package).joinpath(name).read_text(encoding="utf-8")
        assert text.strip()


def test_workshop_registry_profile_loads() -> None:
    config = load_profile_config(
        "fasthep_workshop:registry", project_root=WORKSHOP_ROOT
    )

    assert (
        config["registry"]["sources"]["workshop.toy_source"]["impl"]
        == "fasthep_workshop.sources.toy_source:run_toy_source"
    )


@pytest.mark.parametrize("author_path", AUTHOR_PATHS)
def test_examples_compile(author_path: Path, tmp_path: Path) -> None:
    plan = compile_author_file(
        author_path,
        outdir=tmp_path / author_path.parent.name,
    )

    registry_text = yaml.safe_dump(plan.registry)
    assert "scripts." not in registry_text
    assert (
        plan.registry["sources"]["workshop.toy_source"]["impl"]
        == "fasthep_workshop.sources.toy_source:run_toy_source"
    )
    assert "hep.schema_snapshot" in plan.registry["observers"]
    assert "hep.render.hist1d" in plan.registry["sinks"]


@pytest.mark.parametrize("author_path", DOMAIN_NEUTRAL_AUTHOR_PATHS)
def test_domain_neutral_examples_compile(author_path: Path, tmp_path: Path) -> None:
    plan = compile_author_file(
        author_path,
        outdir=tmp_path / author_path.parent.name,
    )

    assert plan.nodes[0].impl == "workshop.parquet"
    assert "workshop.tabular.filter" in plan.registry["transforms"]
    assert "workshop.console_table" in plan.registry["sinks"]
    assert "hep.hist" not in plan.registry["transforms"]


@pytest.mark.parametrize("author_path", READ_DATA_TUTORIAL_AUTHOR_PATHS)
def test_read_data_tutorials_compile(author_path: Path, tmp_path: Path) -> None:
    plan = compile_author_file(
        author_path,
        outdir=tmp_path / author_path.parent.name,
    )

    read_node = next(node for node in plan.nodes if node.id == "read.events")
    assert read_node.impl == "root_tree"
    assert "hep.schema_snapshot" in plan.registry["observers"]


@pytest.mark.parametrize("author_path", TRANSFORM_DATA_TUTORIAL_AUTHOR_PATHS)
def test_transform_data_tutorials_compile(author_path: Path, tmp_path: Path) -> None:
    plan = compile_author_file(
        author_path,
        outdir=tmp_path / author_path.parent.name,
    )

    read_node = next(node for node in plan.nodes if node.id == "read.events")
    assert read_node.impl == "root_tree"
    assert "hep.schema_snapshot" in plan.registry["observers"]


@pytest.mark.parametrize("author_path", SUMMARISE_DATA_TUTORIAL_AUTHOR_PATHS)
def test_summarise_data_tutorials_compile(author_path: Path, tmp_path: Path) -> None:
    plan = compile_author_file(
        author_path,
        outdir=tmp_path / author_path.parent.name,
    )

    read_node = next(node for node in plan.nodes if node.id == "read.events")
    assert read_node.impl == "root_tree"
    assert "hep.hist" in plan.registry["transforms"]


def test_runtime_smoke_runs_end_to_end(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(WORKSHOP_ROOT)
    monkeypatch.setenv("MPLCONFIGDIR", str(tmp_path / "mplconfig"))

    outdir = tmp_path / "runtime-smoke"
    result = run_author_file(
        WORKSHOP_ROOT / "examples" / "testing" / "runtime-smoke" / "author.yaml",
        outdir=outdir,
    )

    assert result.success
    assert (outdir / "compile" / "normalized.yaml").exists()
    assert (outdir / "compile" / "plan.yaml").exists()
    assert (outdir / "run_summary.yaml").exists()
    assert any((outdir / "artifacts" / "plots").rglob("*.png"))


def test_transform_derived_columns_tutorial_runs_with_event_arrays(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    if not (WORKSHOP_ROOT / "data" / "CMS" / "Zmumu" / "data.root").exists():
        pytest.skip("local CMS/Zmumu tutorial data is not installed")

    monkeypatch.chdir(WORKSHOP_ROOT)

    outdir = tmp_path / "02-transform-data" / "01-derived-columns"
    result = run_author_file(
        WORKSHOP_ROOT
        / "tutorials"
        / "02-transform-data"
        / "01-derived-columns"
        / "author.yaml",
        outdir=outdir,
    )

    assert result.success
    summary = yaml.safe_load((outdir / "run_summary.yaml").read_text(encoding="utf-8"))
    output_types = {
        item["type"]
        for partition in summary["partitions"]
        for item in partition["outputs"]
        if item["node"] == "read.events"
    }
    assert output_types == {"Array"}
