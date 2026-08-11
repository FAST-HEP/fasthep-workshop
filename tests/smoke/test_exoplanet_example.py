from __future__ import annotations

from pathlib import Path

import awkward as ak  # type: ignore[import-untyped]
import pytest
from hepflow.api import compile_workflow_file, run_workflow_file

from fasthep_workshop.sinks.table import run_console_table
from fasthep_workshop.sources.parquet import run_parquet_source
from fasthep_workshop.transforms.tabular import (
    run_tabular_explode,
    run_tabular_filter,
    run_tabular_project,
)

WORKSHOP_ROOT = Path(__file__).parents[2]
EXAMPLE = WORKSHOP_ROOT / "examples" / "NASA" / "exoplanets"


def test_parquet_source_reads_real_exoplanet_schema(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(WORKSHOP_ROOT)

    events = run_parquet_source(
        path="data/NASA/exoplanets.parquet",
        columns=["name", "planet_name", "planet_radius", "planet_period"],
    )

    assert len(events) == 2935
    assert events.fields == ["name", "planet_name", "planet_radius", "planet_period"]
    assert ak.all(
        ak.num(events.planet_name, axis=1) == ak.num(events.planet_radius, axis=1)
    )


def test_tabular_components_select_earth_sized_planets() -> None:
    stream = ak.Array(
        {
            "name": ["System A", "System B"],
            "planet_name": [["b", "c"], ["b"]],
            "planet_radius": [[0.75, 1.0], [1.25]],
            "planet_period": [[3.0, 5.0], [7.0]],
        }
    )

    exploded = run_tabular_explode(
        stream=stream,
        fields=["planet_name", "planet_radius", "planet_period"],
        keep_fields=["name"],
    )["stream"]
    selected = run_tabular_filter(
        stream=exploded,
        expr="(planet_radius > 0.8) & (planet_radius < 1.2)",
    )["stream"]
    projected = run_tabular_project(
        stream=selected,
        fields=["name", "planet_name", "planet_radius", "planet_period"],
    )["stream"]

    assert ak.to_list(projected) == [
        {
            "name": "System A",
            "planet_name": "c",
            "planet_radius": 1.0,
            "planet_period": 5.0,
        }
    ]


def test_explode_rejects_misaligned_list_columns() -> None:
    stream = ak.Array(
        {
            "planet_name": [["b", "c"]],
            "planet_radius": [[1.0]],
        }
    )

    with pytest.raises(ValueError, match="aligned list fields"):
        run_tabular_explode(
            stream=stream,
            fields=["planet_name", "planet_radius"],
        )


def test_console_table_writes_deterministic_text(tmp_path: Path) -> None:
    path = tmp_path / "planets.txt"

    run_console_table(
        target=ak.Array(
            {
                "name": ["System B", "System A"],
                "planet_name": ["b", "c"],
                "planet_radius": [1.1, 0.9],
                "planet_period": [7.0, 5.0],
            }
        ),
        path=str(path),
        fields=["name", "planet_name", "planet_radius", "planet_period"],
        columns=[
            {"template": "{name} {planet_name}", "header": "Planet"},
            {"field": "planet_radius", "header": "Radius", "format": ".2f"},
            {"field": "planet_period", "header": "Period", "format": ".1f"},
        ],
        sort_by=["planet_radius", "name", "planet_name"],
    )

    assert path.read_text(encoding="utf-8") == (
        "+------------+--------+--------+\n"
        "| Planet     | Radius | Period |\n"
        "+------------+--------+--------+\n"
        "| System A c | 0.90   | 5.0    |\n"
        "| System B b | 1.10   | 7.0    |\n"
        "+------------+--------+--------+\n"
    )


def test_exoplanet_example_compiles_to_workshop_only_graph(tmp_path: Path) -> None:
    plan = compile_workflow_file(EXAMPLE / "workflow.yaml", outdir=tmp_path / "plan")

    assert [f"{node.id}:{node.impl}" for node in plan.nodes] == [
        "read.planets:workshop.parquet",
        "stage.PlanetRows:workshop.tabular.explode",
        "stage.EarthSizedPlanets:workshop.tabular.filter",
        "stage.PlanetTable:workshop.tabular.project",
        "write.PlanetTable.0:workshop.console_table",
    ]
    assert "hep.define" not in plan.registry["transforms"]
    assert plan.data_flow["required_sources"]["planets"]["branches"] == [
        "name",
        "planet_name",
        "planet_period",
        "planet_radius",
    ]


def test_exoplanet_example_runs_and_matches_expected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(WORKSHOP_ROOT)
    outdir = tmp_path / "exoplanets"

    result = run_workflow_file(EXAMPLE / "workflow.yaml", outdir=outdir)

    assert result.success
    actual = outdir / "artifacts" / "files" / "snippets" / "planets.txt"
    expected = EXAMPLE / "expected" / "snippets" / "planets.txt"
    assert actual.read_text(encoding="utf-8") == expected.read_text(encoding="utf-8")
