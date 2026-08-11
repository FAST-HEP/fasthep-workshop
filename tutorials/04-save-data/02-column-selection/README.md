# Column selection

> Part 2 of 3 in **Save Data**
>
> ✓ 01. Skims
> ▶ 02. Column Selection
> ○ 03. Provenance

The previous tutorial created a skim by saving the complete event stream after a selection.

In practice, skims often contain only a subset of the available columns. This reduces storage requirements and creates a compact analysis-specific dataset.

FAST-HEP separates **which events are saved** from **which columns are saved**.

## 1. Inspect the output layout

This tutorial introduces a reusable output layout:

```yaml
outputs:
  dimuon_candidates:
    tree: events
    keep:
      - NJet
      - Jet_Px
      - Jet_Py
      - Jet_Pz
      - Jet_E
      - Jet_btag
      - Jet_ID

      - NMuon
      - Muon_Px
      - Muon_Py
      - Muon_Pz
      - Muon_E
      - Muon_Charge
      - Muon_Iso

      - Muon_Pt
      - IsolatedMuon
      - NIsolatedMuon
      - HasMuonAbove25
      - triggerIsoMu24
```

The output layout defines which quantities should be written to the skim.

Some of these quantities are used directly in the selection, while others are taken from the original source.


## 2. Inspect the writer

The writer references the output layout by name:

```yaml
write:
  - kind: root_tree
    path: dimuon_candidates.root
    use: dimuon_candidates
```

The `use` keyword tells the writer to load the configuration from the corresponding entry in `outputs`.

This keeps output schemas reusable and avoids duplicating long column lists throughout the workflow.

```{note}
Output layouts are currently used to control which columns are written.

In future releases they may also be used for dependency resolution and source optimisation, allowing FAST-HEP to automatically determine which branches must be loaded to produce a particular output.
```

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/04-save-data/02-column-selection/workflow.yaml \
  --outdir build/tutorials/04-save-data/02-column-selection
```

## 4. Inspect the outputs

Look at:

* `build/tutorials/04-save-data/02-column-selection/artifacts/files/`
* `build/tutorials/04-save-data/02-column-selection/artifacts/cutflows/`
* `build/tutorials/04-save-data/02-column-selection/reports/schema/`
* `build/tutorials/04-save-data/02-column-selection/run_summary.yaml`

The selection is identical to the previous tutorial, but the saved schema is different.

Compare the schema of the output file with the schema snapshot from `01-skims`.

Notice that the skim now contains only the columns requested by the output layout.

## Expected outputs

The schema snapshot after the selection shows all quantities available in the event stream:

```{literalinclude} /_static/_generated/tutorials/04-save-data/02-column-selection/snippets/schema.stream.summary.json
:language: json
```

The schema snapshot of the written output shows only the columns retained by the output layout:

```{literalinclude} /_static/_generated/tutorials/04-save-data/02-column-selection/snippets/schema.output.summary.json
:language: json
```

The writer manifest records the produced files and datasets:

```{literalinclude} /_static/_generated/tutorials/04-save-data/02-column-selection/snippets/files.manifest.json
:language: json
```
