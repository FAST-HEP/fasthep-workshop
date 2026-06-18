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

The important pieces of `author.yaml` are:

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
```

The workflow reads the `events` tree and records a schema snapshot.

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/01-read-data/01-root-files/author.yaml --outdir build/tutorials/01-read-data/01-root-files
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
stream. No selections, histograms, skims, or distributed execution are used here.
