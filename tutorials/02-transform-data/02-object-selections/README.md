# Object selections

> Part 2 of 3 in **Transform Data**
>
> ✓ 01. Derived Columns  
> ▶ 02. Object Selections  
> ○ 03. Field Mapping

This tutorial reads the small local Z &rarr; $\mu\mu$ ROOT files and applies a
compact event selection.

It shows how object-level quantities be used to filter events.

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
- id: DerivedMuonColumns
  op: hep.define
  params:
    variables:
      - name: Muon_Pt
        expr: "sqrt(Muon_Px ** 2 + Muon_Py ** 2)"
      - name: IsolatedMuon
        expr: "(Muon_Iso / Muon_Pt) < 0.10"
      - name: NIsolatedMuon
        reduce:
          op: count_nonzero
          over: IsolatedMuon
      - name: HasMuonAbove25
        reduce:
          op: any
          over: "Muon_Pt > 25"
```

This stage creates variables such as:

- `NIsolatedMuon`
- `HasMuonAbove25`
- `triggerIsoMu24`

The second stage applies a cutflow:

```yaml
- id: SelectDimuonEvents
  op: hep.selection.cutflow
  params:
    selection:
      dimuon_candidates:
        - "NIsolatedMuon >= 2"
        - "triggerIsoMu24 == 1"
        - "HasMuonAbove25"
```

A cutflow is an ordered sequence of selections. FAST-HEP evaluates each selection in turn and records how many events pass each step.

The dimuon_candidates selection requires:

1. at least two isolated muons (`NIsolatedMuon >= 2`)
2. the single-muon trigger to have fired (`triggerIsoMu24 == 1`)
3. at least one muon with transverse momentum above 25 GeV (`HasMuonAbove25`)

All three conditions must be satisfied for an event to pass the final selection.

This pattern is common in HEP analyses: first derive useful quantities, then use them to select the events of interest.


## 3. Run the workflow

```bash
pixi run fasthep run tutorials/02-transform-data/02-object-selections/workflow.yaml --outdir build/tutorials/02-transform-data/02-object-selections
```

## 4. Inspect the outputs

This tutorial introduces a new user-facing artifact: a cutflow.

Look at:

- `build/tutorials/02-transform-data/02-object-selections/artifacts/cutflows/SelectDimuonEvents.json`
- `build/tutorials/02-transform-data/02-object-selections/run_summary.yaml`

`SelectDimuonEvents.json` records each cut in order, together with the number of events before and after the cut.

This is useful for checking that a selection behaves as expected. For example, you can see how many events pass the isolated-muon requirement, then how many remain after the trigger requirement, and finally how many pass the full dimuon-candidate selection.

The JSON file is machine-readable and intended for automation. Later tutorials show how to turn this information into more human-readable tables and reports.

## Expected outputs

The curated expected snippet keeps one compact summary from the full cutflow artifact.

```{literalinclude} /_static/_generated/tutorials/02-transform-data/02-object-selections/snippets/SelectDimuonEvents.summary.json
:language: json
```

The full output is available in:

```
build/tutorials/02-transform-data/02-object-selections/artifacts/cutflows/SelectDimuonEvents.json
```
