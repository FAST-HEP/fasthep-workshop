# NASA Exoplanets

This example is a small, domain-neutral Flow workflow built from capabilities
registered by `fasthep-workshop`.

It reads `data/NASA/exoplanets.parquet`, expands the list-valued planet columns
into one row per planet, selects Earth-sized planets with
`0.8 < planet_radius < 1.2`, and writes a deterministic text table with the
planet name, radius in Earth radii, and orbital period in days.

The Parquet schema does not include a discovery-year column, so this example does
not report discovery year. The selection is about measured planet size only; it
does not make habitability or Earth-like claims.

Run it from the `fasthep-workshop` repository root:

```bash
pixi run --environment dev fasthep run examples/NASA/exoplanets/workflow.yaml --outdir build/examples/NASA/exoplanets
```

The output table is written to:

```text
build/examples/NASA/exoplanets/artifacts/files/snippets/planets.txt
```

The useful shape of the workflow graph is:

```text
workshop.parquet
  -> workshop.tabular.explode
  -> workshop.tabular.filter
  -> workshop.tabular.project
  -> workshop.console_table
```
