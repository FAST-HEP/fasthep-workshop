# Cutflow tables

This tutorial turns the dimuon event selection into a cutflow product and a
rendered table.

It uses the same selection ideas introduced in
`tutorials/02-transform-data/object-selections`, now with `EventWeight` so the
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

## 2. Inspect the style file

`styles.yaml` keeps visual presentation separate from analysis logic. For this
tutorial the style is tiny because the renderer writes a CSV-style cutflow
table:

```yaml
styles:
  event_selection_cutflow:
    op: hep.render.cutflow_csv
```

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/03-summarise-data/cutflow-tables/author.yaml --outdir build/tutorials/03-summarise-data/cutflow-tables
```

## 4. Inspect the outputs

Look at:

- `build/tutorials/03-summarise-data/cutflow-tables/artifacts/cutflows/`
- `build/tutorials/03-summarise-data/cutflow-tables/artifacts/tables/`
- `build/tutorials/03-summarise-data/cutflow-tables/render/`
- `build/tutorials/03-summarise-data/cutflow-tables/run_summary.yaml`

The JSON representation, such as `SelectDimuonEvents.json`, is intended for
machines and automation. Later tutorials will show alternative human-readable
presentations.
