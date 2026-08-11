# Reading ROOT files

> Part 1 of 3 in **Read Data**
>
> ▶ 01. ROOT Files  
> ○ 02. Datasets  
> ○ 03. Remote Data

This tutorial shows how to read ROOT files with FAST-HEP.

## 1. Download the example files

```bash
pixi run fasthep download --json tutorials/data/CMS/Zmumu/files.json --destination data
```

The manifest downloads small Z &rarr; $\mu\mu$ datasets from the CMS experiment into `data/CMS/Zmumu/`.

## 2. Inspect the workflow

The important pieces of `workflow.yaml` are:

```yaml
data:
  datasets:
    - name: data
      eventtype: data
      files:
        - data/CMS/Zmumu/data.root

sources:
  events:
    kind: root_tree
    tree: events
    branches:
      - NMuon
      - Muon_Px
      - Muon_Py
      - Muon_Pz
      - EventWeight
```

The workflow reads the `events` tree and records a schema snapshot.

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/01-read-data/01-root-files/workflow.yaml --outdir build/tutorials/01-read-data/01-root-files
```

## 4. Inspect the outputs

Look at:

- `build/tutorials/01-read-data/01-root-files/compile/normalized.yaml`
- `build/tutorials/01-read-data/01-root-files/compile/plan.yaml`
- `build/tutorials/01-read-data/01-root-files/reports/schema/`
- `build/tutorials/01-read-data/01-root-files/run_summary.yaml`

## 5. What happened?

FAST-HEP resolved the dataset entry, read selected branches from the ROOT tree
with the `root_tree` source, and ran a schema observer on the resulting event
stream.

## Expected outputs

This tutorial produces two outputs that are particularly useful when exploring a new dataset:

- the event schema, which describes the contents of the event stream
- the run summary, which records what FAST-HEP executed

### Event schema

```{literalinclude} /_static/_generated/tutorials/01-read-data/01-root-files/snippets/schema.json
:language: json
```
The schema describes the branches available in `data/CMS/Zmumu/data.root`, including their names and types.

Because this tutorial restricts the source to a small set of branches, only those branches appear in the schema report. In a real analysis, schema inspection is often used to explore unfamiliar datasets and identify the quantities needed for later stages.

### Run summary
The run summary records what FAST-HEP processed and which modules were involved in the workflow execution.

:::{dropdown} Show run_summary.yaml
```{literalinclude} /_static/_generated/tutorials/01-read-data/01-root-files/snippets/run_summary.yaml
:language: yaml
```
:::

At this stage the run summary is primarily useful as a diagnostic record. Later tutorials will show how FAST-HEP reports and summaries can be turned into more human-readable outputs.
