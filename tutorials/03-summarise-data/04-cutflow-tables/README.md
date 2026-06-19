# Cutflow tables

> Part 4 of 4 in **Summarise Data**
>
> ✓ 01. Histograms  
> ✓ 02. Render Histograms  
> ✓ 03. Two-Dimensional Histograms  
> ▶ 04. Cutflow Tables

This tutorial turns the dimuon event selection into a cutflow product and a
rendered table.

It uses the same selection ideas introduced in
`tutorials/02-transform-data/02-object-selections`, now with `EventWeight` so the
cutflow tracks weighted data/MC yields.

## 1. Inspect the selection

The selection keeps candidate dimuon events:

```yaml
selection:
  dimuon_candidates:
    - "NIsolatedMuon >= 2"
    - "triggerIsoMu24 == 1"
    - "HasMuonAbove25"
```

Each requirement is evaluated in sequence. FAST-HEP records how many events pass each step, producing a cutflow artifact.

Unlike the earlier object-selection tutorial, this workflow applies EventWeight, so the cutflow tracks weighted data and Monte Carlo yields as well as simple event counts.

## 2. Inspect the style file

`styles.yaml` keeps visual presentation separate from analysis logic. For this
tutorial the style is tiny because the renderer writes a CSV-style cutflow
table:

```yaml
styles:
  event_selection_cutflow:
    op: hep.render.cutflow_csv
```

Just as histogram renderers convert histogram products into plots, the cutflow renderer converts a machine-readable cutflow artifact into a table that can be inspected directly or imported into other tools.

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/03-summarise-data/04-cutflow-tables/author.yaml --outdir build/tutorials/03-summarise-data/04-cutflow-tables
```

## 4. Inspect the outputs

Look at:

- `build/tutorials/03-summarise-data/04-cutflow-tables/artifacts/cutflows/`
- `build/tutorials/03-summarise-data/04-cutflow-tables/artifacts/tables/`
- `build/tutorials/03-summarise-data/04-cutflow-tables/render/`
- `build/tutorials/03-summarise-data/04-cutflow-tables/run_summary.yaml`

The cutflow artifact records the full machine-readable selection history, including the order of cuts and the event yields after each step.

The rendered table is a human-readable view of the same information.

As with histogram rendering, the cutflow and its presentation are kept separate. This allows the same cutflow artifact to be rendered in different formats without rerunning the analysis.

## Expected outputs

The compact cutflow snippet shows the selection logic and weighted yields recorded in the machine-readable artifact.

```{literalinclude} /_static/_generated/tutorials/03-summarise-data/04-cutflow-tables/snippets/SelectDimuonEvents.summary.json
:language: json
```

The CSV table is rendered from the same cutflow artifact:

```{literalinclude} /_static/_generated/tutorials/03-summarise-data/04-cutflow-tables/tables/SelectDimuonEvents.csv
:language: text
```
