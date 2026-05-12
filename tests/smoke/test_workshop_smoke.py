from __future__ import annotations

import importlib.resources as resources
from pathlib import Path

import pytest
import yaml

from hepflow.api import compile_author_file, run_author_file


WORKSHOP_ROOT = Path(__file__).parents[2]

AUTHOR_PATHS = [
    WORKSHOP_ROOT / "examples" / "CMS" / "Zmumu" / "author.yaml",
    WORKSHOP_ROOT / "examples" / "CMS" / "L1Trigger" / "author.yaml",
    WORKSHOP_ROOT / "examples" / "LZ" / "mssi" / "author.yaml",
    WORKSHOP_ROOT / "examples" / "tutorial" / "split-packages" / "author.yaml",
    WORKSHOP_ROOT / "examples" / "tutorial" / "runtime-smoke" / "author.yaml",
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
    ]


def test_package_profiles_are_installed_resources() -> None:
    profile_refs = [
        ("fasthep_carpenter.profiles", "registry.yaml"),
        ("fasthep_curator.profiles", "registry.yaml"),
        ("fasthep_curator.profiles", "default_context.yaml"),
        ("fasthep_curator.profiles", "runtime_diagnostics.yaml"),
        ("fasthep_render.profiles", "registry.yaml"),
    ]

    for package, name in profile_refs:
        text = resources.files(package).joinpath(name).read_text(encoding="utf-8")
        assert text.strip()


@pytest.mark.parametrize("author_path", AUTHOR_PATHS)
def test_examples_compile(author_path: Path, tmp_path: Path) -> None:
    plan = compile_author_file(
        author_path,
        outdir=tmp_path / author_path.parent.name,
    )

    source_impl = plan.registry["sources"]["root_tree"]["impl"]
    assert source_impl.startswith("fasthep_carpenter.") or source_impl.startswith(
        "scripts.ci.toy_source:"
    )
    assert "hep.schema_snapshot" in plan.registry["observers"]
    assert "hep.render.hist1d" in plan.registry["sinks"]


def test_tutorial_runs_end_to_end(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(WORKSHOP_ROOT)
    monkeypatch.setenv("MPLCONFIGDIR", str(tmp_path / "mplconfig"))

    outdir = tmp_path / "tutorial-run"
    result = run_author_file(
        WORKSHOP_ROOT / "examples" / "tutorial" / "runtime-smoke" / "author.yaml",
        outdir=outdir,
    )

    assert result.success
    assert (outdir / "normalized.yaml").exists()
    assert (outdir / "plan.yaml").exists()
    assert (outdir / "run_summary.yaml").exists()
    assert any((outdir / "artifacts").rglob("*.png"))
