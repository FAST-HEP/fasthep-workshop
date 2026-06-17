# Reading ROOT files

This tutorial shows how to read ROOT files with FAST-HEP.

## 1. Download the example files

```bash
fasthep download --json workshop/tutorials/data/CMS/Zmumu/files.json --destination data
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
fasthep run workshop/tutorials/01-read-data/root-files/author.yaml --outdir build/tutorials/01-read-data/root-files
```

## 4. Inspect the outputs

Look at:

- `build/tutorials/01-read-data/root-files/compile/normalized.yaml`
- `build/tutorials/01-read-data/root-files/compile/plan.yaml`
- `build/tutorials/01-read-data/root-files/reports/schema/`
- `build/tutorials/01-read-data/root-files/run_summary.yaml`

## 5. What happened?

FAST-HEP resolved the dataset entry, read selected branches from the ROOT tree
with the `root_tree` source, and ran a schema observer on the resulting event
stream. No selections, histograms, skims, or distributed execution are used here.
