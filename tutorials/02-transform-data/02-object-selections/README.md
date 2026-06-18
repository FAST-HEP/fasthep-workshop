# Object selections

> Part 2 of 3 in **Transform Data**
>
> ✓ 01. Derived Columns  
> ▶ 02. Object Selections  
> ○ 03. Project Fields

This tutorial reads the small local Z &rarr; $\mu\mu$ ROOT files and applies a
compact event selection.

It shows how object-level quantities can feed an event-level requirement. It
does not make histograms, skim files, run systematics, or use distributed
execution.

## 1. Inspect the dataset file

Datasets live in `datasets.yaml`, separate from the workflow:

```yaml
datasets:
  data:
    files:
      - data/CMS/Zmumu/data.root
  dy:
    files:
      - data/CMS/Zmumu/dy.root
```

## 2. Inspect the workflow

The first stage derives object and event flags:

```yaml
- id: MuonObjectFlags
  op: hep.define
```

The second stage applies a small cutflow:

```yaml
- id: SelectDimuonEvents
  op: hep.selection.cutflow
```

The selection keeps events with at least two isolated muons, the single-muon
trigger, and at least one muon above 25 GeV.

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/02-transform-data/02-object-selections/author.yaml --outdir build/tutorials/02-transform-data/02-object-selections
```

## 4. Inspect the outputs

Look at:

- `build/tutorials/02-transform-data/02-object-selections/artifacts/cutflows/SelectDimuonEvents.json`
- `build/tutorials/02-transform-data/02-object-selections/reports/schema/`
- `build/tutorials/02-transform-data/02-object-selections/run_summary.yaml`

The schema snapshots show the stream before derived flags, after derived flags,
and after the selection.

`SelectDimuonEvents.json` has the full information about the order of cuts as well as the number of events going into and out of a cut.
Later we will see how to make these more human-readable.
