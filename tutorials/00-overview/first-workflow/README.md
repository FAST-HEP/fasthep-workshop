# First Workflow

> Part 1 of 1 in **Overview**
>
> ▶ 01. First Workflow

This tutorial shows a complete FAST-HEP workflow from start to finish.

You are **not expected to understand every detail yet**.

The goal is to see the entire analysis pipeline once before we explore each piece in dedicated tutorials.

By the end of this page, you will have run a workflow that:

```text
toy data
→ derived quantity
→ histogram
→ plot
```

and produced a publication-style analysis output with only a small amount of YAML.

## What this tutorial demonstrates

This workflow includes:

* a dataset definition
* a data source
* a derived variable
* a histogram
* a rendered plot

The following tutorials explain each concept individually.

- {doc}`ROOT Files </tutorials/01-read-data/01-root-files>`
- {doc}`Datasets </tutorials/01-read-data/02-datasets>`
- {doc}`Remote Data </tutorials/01-read-data/03-remote-data>`
- {doc}`Derived Columns </tutorials/02-transform-data/01-derived-columns>`
- {doc}`Object Selections </tutorials/02-transform-data/02-object-selections>`
- {doc}`Histograms </tutorials/03-summarise-data/01-histograms>`
- {doc}`Render Histograms </tutorials/03-summarise-data/02-render-histograms>`

The tutorials listed above cover the building blocks needed to understand this workflow. 

As you progress through the workshop you will encounter many additional topics, including remote data access, skimming, systematics, distributed execution, GPU acceleration, and complete public analysis records.

## Tutorial files

```text
tutorials/00-overview/first-workflow/
├── author.yaml
├── README.md
└── expected/
```

The workflow itself is defined in:

```text
author.yaml
```

## Workflow overview

This workflow:

1. generates toy events
2. computes a derived variable
3. fills a histogram
4. renders a plot

```{mermaid}
flowchart TD
  read_events["read.events<br/>source<br/>workshop.toy_source"]
  stage_BasicVars["stage.BasicVars<br/>transform<br/>hep.define"]
  stage_MuonPt["stage.MuonPt<br/>transform<br/>hep.hist"]
  render_MuonPt_0["render.MuonPt.0<br/>sink<br/>hep.render.hist1d"]

  read_events -->|stream -> stream| stage_BasicVars
  stage_BasicVars -->|stream -> stream| stage_MuonPt
  stage_MuonPt -->|hist -> target| render_MuonPt_0
```

FAST-HEP compiles workflows into dependency-aware execution graphs.

You do not need to understand every node in this graph yet.

For now, the important idea is that data flows through a series of operations:

```text
source
→ transform
→ summarise
→ render
```

The remainder of the workshop explores each of these steps separately.

## The workflow file

FAST-HEP workflows are declarative.

Rather than writing explicit event loops, you describe:

- what data should be processed
- which quantities should be computed
- which outputs should be produced

FAST-HEP then builds an execution plan automatically.

This workshop focuses on learning by doing. Throughout the tutorials you will build workflows incrementally and discover the language through practical examples.

For a more complete description of the workflow language and FAST-HEP architecture, see:

- [FAST-HEP documentation](https://fast-hep.github.io)
- [fasthep-flow documentation](https://fasthep-flow.readthedocs.io)
- [fasthep-carpenter documentation](https://fasthep-carpenter.readthedocs.io)
- [fasthep-curator documentation](https://fasthep-curator.readthedocs.io)

The complete workflow is shown at the end of this tutorial.

## Run the tutorial

From the repository root:

```bash
pixi run fasthep run tutorials/00-overview/first-workflow/author.yaml \
  --outdir build/tutorials/00-overview/first-workflow
```

## Inspect the outputs

The workflow produces outputs under:

```text
build/tutorials/00-overview/first-workflow/
```

The most important directories are:

```text
build/tutorials/00-overview/first-workflow/
├── artifacts/
├── compile/
├── graph/
├── reports/
└── run_summary.yaml
```

* `artifacts/` contains user-facing outputs such as plots and histograms
* `compile/` contains compiler products and execution plans
* `graph/` contains workflow visualisations
* `reports/` contains diagnostics and metadata
* `run_summary.yaml` summarises the workflow execution

## Expected outputs

A curated set of expected outputs is provided in:

```text
tutorials/00-overview/first-workflow/expected/
```

These files highlight the most important results from the build directory.

### Plot

The workflow produces a histogram of the derived muon transverse momentum.

```{figure} /_static/_generated/tutorials/00-overview/first-workflow/plots/MuonPt.png
:alt: Muon transverse momentum histogram
:width: 420px
:target: /_static/_generated/tutorials/00-overview/first-workflow/plots/MuonPt.png

Expected `MuonPt.png` plot produced by this tutorial.
```

### Histogram metadata

The expected directory also contains a small histogram manifest (`expected/snippets/histograms.manifest.json`):

```{literalinclude} /_static/_generated/tutorials/00-overview/first-workflow/snippets/histograms.manifest.json
:language: json
```

This demonstrates how histogram products are recorded and tracked.

Your generated outputs should look similar, although exact values may vary slightly between environments and package versions.

## Full workflow

:::{dropdown} Show `author.yaml`
```{literalinclude} ../../../tutorials/00-overview/first-workflow/author.yaml
:language: yaml
```
:::

## What happens next?

This tutorial showed the complete workflow all at once.

The rest of the workshop introduces each concept separately:

1. reading data
2. transforming data
3. creating histograms
4. rendering outputs

one step at a time.

Continue with {doc}`tutorials/01-read-data/01-root-files </tutorials/01-read-data/01-root-files>`

which introduces the first real analysis input: ROOT files.
