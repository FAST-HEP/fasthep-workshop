# Remote data

> Part 3 of 3 in **Read Data**
>
> ✓ 01. ROOT Files  
> ✓ 02. Datasets  
> ▶ 03. Remote Data

This tutorial reads one public CMS Open Data ROOT file directly over XRootD.

The file is a NanoAOD sample from the `DoubleMuon` dataset. It is related to
the Z &rarr; $\mu\mu$ examples in the workshop, but the path name remains
`Zmumu` where paths use that convention.

## 1. Inspect the dataset file

The dataset is defined separately in `datasets.yaml`:

```yaml
datasets:
  DoubleMuon:
    files:
      - root://eospublic.cern.ch//eos/opendata/cms/...
```

For one file this is not necessary, but real analyses usually have many
datasets and many files per dataset. Keeping datasets separate makes that list
easier to maintain.

## 2. Inspect the workflow

`author.yaml` includes the dataset file:

```yaml
include:
  - datasets.yaml
```

The workflow reads the `Events` tree and records a schema snapshot. It does not
make histograms, skim events, or use distributed execution.

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/01-read-data/03-remote-data/author.yaml --outdir build/tutorials/01-read-data/03-remote-data
```

XRootD support is required in the runtime environment. If the command fails
while opening the `root://` URL, check that the environment has the required
Uproot/XRootD support (`fsspec-xrootd`) and network access.

## 4. Inspect the outputs

Look at:

- `build/tutorials/01-read-data/03-remote-data/reports/schema/read_events/events__DoubleMuon__0.json`
- `build/tutorials/01-read-data/03-remote-data/run_summary.yaml`

## Expected outputs

Remote files can contain many branches, especially NanoAOD files. Schema
inspection helps you understand what is available before writing analysis
stages, and FAST-HEP can inspect the schema without reading the whole dataset.

```{literalinclude} /_static/_generated/tutorials/01-read-data/03-remote-data/snippets/schema.summary.json
:language: json
```

The snippet above is shortened to the first few entries. The full schema report
is written under:

```text
build/tutorials/01-read-data/03-remote-data/reports/schema/
```
