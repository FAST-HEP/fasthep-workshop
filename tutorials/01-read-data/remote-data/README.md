# Remote data

This tutorial reads one public CMS Open Data ROOT file directly over XRootD.
No local ROOT file is downloaded.

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
pixi run fasthep run tutorials/01-read-data/remote-data/author.yaml --outdir build/tutorials/01-read-data/remote-data
```

XRootD support is required in the runtime environment. If the command fails
while opening the `root://` URL, check that the environment has the required
Uproot/XRootD support and network access.

## 4. Inspect the outputs

Look at:

- `build/tutorials/01-read-data/remote-data/compile/normalized.yaml`
- `build/tutorials/01-read-data/remote-data/compile/plan.yaml`
- `build/tutorials/01-read-data/remote-data/reports/schema/`
- `build/tutorials/01-read-data/remote-data/run_summary.yaml`
