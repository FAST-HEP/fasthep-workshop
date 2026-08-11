# Skims

> Part 1 of 3 in **Save Data**
>
> ▶ 01. Skims
> ○ 02. Column Selection
> ○ 03. Provenance

This tutorial creates the first analysis skim.

In many HEP analyses, the first step after obtaining experiment data is to create a smaller dataset containing only the events relevant for a particular study. Such a dataset is called a **skim**.

Skims reduce storage requirements, improve processing performance, and make it easier to work on local clusters or laptops.

FAST-HEP allows skims to be described declaratively alongside the rest of the analysis workflow.

## 1. Inspect the workflow

The workflow follows the same pattern as the earlier dimuon-selection examples:

```text
read data
    ↓
derive quantities
    ↓
select dimuon events
    ↓
write skim
```

The selection keeps candidate dimuon events:

```yaml
selection:
  dimuon_candidates:
    - "NIsolatedMuon >= 2"
    - "triggerIsoMu24 == 1"
    - "HasMuonAbove25"
```

The new part is the output sink, which writes the selected events to a ROOT file.

Each dataset is processed independently, producing one skim file per dataset.

## 2. Inspect the output stream

The skim is written from the event stream after the selection stage.

This means the output contains:

* source branches read from the input dataset
* derived quantities such as `Muon_Pt`
* event-level quantities such as `NIsolatedMuon`
* only events that pass the dimuon selection

By default, FAST-HEP writes the complete contents of the event stream.

Later tutorials show how to restrict which columns are written.

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/04-save-data/01-skims/workflow.yaml --outdir build/tutorials/04-save-data/01-skims
```

## 4. Inspect the outputs

Look at:

* `build/tutorials/04-save-data/01-skims/artifacts/files/`
* `build/tutorials/04-save-data/01-skims/artifacts/cutflows/`
* `build/tutorials/04-save-data/01-skims/reports/schema/`
* `build/tutorials/04-save-data/01-skims/run_summary.yaml`

The cutflow records how many events passed the selection.

The schema snapshot shows the structure of the event stream that is written to the skim.

The skim files themselves are standard ROOT files and can be inspected using ROOT, uproot, or used directly as inputs to later FAST-HEP workflows.

## Expected outputs

The expected outputs include:

* a skim file for each dataset
* the selection cutflow
* a schema snapshot of the saved event stream

The schema snapshot demonstrates that derived quantities are stored alongside the original dataset branches.

```{literalinclude} /_static/_generated/tutorials/04-save-data/01-skims/snippets/schema.summary.json
:language: json
```

The cutflow summary shows how many events survived the skim selection.

```{literalinclude} /_static/_generated/tutorials/04-save-data/01-skims/snippets/SelectDimuonEvents.summary.json
:language: json
```

Finally, the writer manifest shows you the files that have been written, their respective entries and sizes:

```{literalinclude} /_static/_generated/tutorials/04-save-data/01-skims/snippets/dimuon_candidates.manifest.json
:language: json
```

## What is written?

The writer saves the event stream after `SelectDimuonEvents`.

That stream contains the quantities that were read or created earlier in the workflow:

```python
>>> import uproot
>>> f = uproot.open("build/tutorials/04-save-data/01-skims/artifacts/files/dimuon_candidates/data/0_0.root")
>>> f["events"].keys()
['HasMuonAbove25', 'IsolatedMuon', 'Muon_Iso', 'Muon_Pt', 'Muon_Px', 'Muon_Py', 'NIsolatedMuon', 'triggerIsoMu24']
```
