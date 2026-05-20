# First workflow

This tutorial introduces the smallest useful FAST-HEP workflow:

```text
toy source → derived variable → histogram → plot
```

The workflow uses the workshop toy source to generate event data, derives a new muon transverse momentum variable, fills a histogram, and renders the result as a PNG plot.

## What this tutorial demonstrates

You will see how to:

- load FAST-HEP profiles
- define datasets
- configure a source
- define a derived variable
- fill a histogram
- render a plot (PNG)

## Files

```text
tutorials/beginner/first-workflow/
├── author.yaml
├── README.md
├── expected/
├── assets/
└── build/
```

The main workflow file is:

```text
author.yaml
```

## Workflow overview

This workflow:

1. generates toy events
2. derives a new variable
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

FAST-HEP workflows are compiled into dependency-aware execution graphs.

In this tutorial:

- the source generates toy events
- a transform derives `Muon_Pt`
- another transform fills a histogram
- a rendering sink produces a PNG plot

The graph above is generated from the workflow definition and shows how data and artifacts flow between operations.

## The workflow file

The workflow is defined in:

```text
author.yaml
```

FAST-HEP workflows are declarative:

- you describe what should happen
- FAST-HEP determines how to execute it

The workflow is organised into sections.

---

## Profiles

The workflow begins by loading profiles:

```yaml
use:
  profiles:
    - registry
    - fasthep_carpenter:registry
    - fasthep_render:registry
    - fasthep_workshop:registry
```

Profiles register operations, sources, sinks, hooks, and rendering behavior.

In this workflow:

| Profile | Purpose |
|---|---|
| `registry` | core FAST-HEP workflow runtime |
| `fasthep_carpenter:registry` | transforms and histogramming |
| `fasthep_render:registry` | rendering and plotting |
| `fasthep_workshop:registry` | tutorial toy source |

```{note}
The first profile, `registry`, is the built-in FAST-HEP workflow registry.

In future user-facing presets such as `workshop` or `hep-default` may hide these details in `author.yaml`, while the fully resolved profiles remain visible in generated plans.
```

See also:

- FAST-HEP concepts: profiles and registries
- `fasthep-flow` documentation

---

## Datasets

The workflow defines a dataset:

```yaml
data:
  datasets:
    - name: toy
      eventtype: mc
      files:
        - toy://dy
```

Datasets describe logical analysis inputs.

In this tutorial:

```text
toy://dy
```

is a virtual dataset URI interpreted by the workshop toy source.

```{note}
`toy://dy` is not a physical file.

The workshop toy source interprets this URI internally to generate deterministic synthetic events for tutorials.
```

This allows tutorials to run without downloading external datasets.

---

## Sources

The workflow then defines a source:

```yaml
sources:
  events:
    kind: workshop.toy_source
```

Sources introduce data streams into workflows.

In this case:

```text
workshop.toy_source
```

generates synthetic event data containing:

- muons
- jets
- event weights
- trigger decisions
- missing transverse energy

The source produces an event stream called:

```text
events
```

which downstream operations consume.

---

## Transforms

The workflow derives a new variable:

```yaml
- id: BasicVars
  op: hep.define
  params:
    variables:
      - name: Muon_Pt
        expr: "sqrt(Muon_Px ** 2 + Muon_Py ** 2)"
```

This transform computes:

```text
Muon_Pt
```

from:

```text
Muon_Px
Muon_Py
```

```{note}
FAST-HEP describes what should be computed rather than explicitly writing event loops.

The workflow engine determines execution order and dependencies automatically.
```

See also:

- FAST-HEP concepts: workflow language
- `fasthep-flow` documentation

---

## Histogramming

The next stage fills a histogram:

```yaml
- id: MuonPt
  op: hep.hist
  params:
    axes:
      - name: Muon_Pt
        source: Muon_Pt
        type: regular
        bins:
          low: 0
          high: 120
          nbins: 60
```

This operation:

- reads the derived `Muon_Pt`
- fills histogram bins
- produces a histogram artifact

The histogram configuration specifies:

- histogram axes
- binning
- ranges
- weighting behavior

In this tutorial the histogram is unweighted.

---

## Rendering

The histogram is then rendered as a PNG plot:

```yaml
render:
  style: muon_pt
```
which references this style:
```yaml
styles:
  muon_pt:
    op: hep.render.hist1d
    figure:
      size: [8, 6]
      dpi: 150
    axes:
      x:
        name: Muon_Pt
        label: "Muon $p_T$ [GeV]"
        limits: [0, 120]
      y:
        name: events
        label: "Events"
        scale: linear
```

Rendering is separated from histogram creation.

This allows:

- plots to be regenerated independently
- rendering styles to be reused
- visual appearance to evolve separately from analysis logic

The render sink uses:

```text
hep.render.hist1d
```

to generate the final output image.

---

## Run the tutorial

From the `fasthep-workshop` repository root:

```bash
pixi run fasthep run tutorials/beginner/first-workflow/author.yaml \
  --outdir tutorials/beginner/first-workflow/build
```

The output plot should be written to the build directory.

## Expected output

After running, inspect:

```text
tutorials/beginner/first-workflow/build/
```

The main expected output is:

```text
├── artifacts
│   └── MuonPt.png
├── graph.dot
├── graph.mmd
├── normalized.yaml
├── plan.yaml
└── run_summary.yaml

```

You can compare your generated output against:

```text
tutorials/beginner/first-workflow/expected/
```

## Full workflow

```yaml
version: 1.0

use:
  profiles:
    - registry
    - fasthep_carpenter:registry
    - fasthep_render:registry
    - fasthep_workshop:registry

data:
  datasets:
    - name: toy
      eventtype: mc
      files:
        - toy://dy

sources:
  events:
    kind: workshop.toy_source
    stream_type: event_stream

styles:
  muon_pt:
    op: hep.render.hist1d
    figure:
      size: [8, 6]
      dpi: 150
    axes:
      x:
        name: Muon_Pt
        label: "Muon $p_T$ [GeV]"
        limits: [0, 120]
      y:
        name: events
        label: "Events"

analysis:
  stages:
    - id: BasicVars
      op: hep.define
      params:
        variables:
          - name: Muon_Pt
            expr: "sqrt(Muon_Px ** 2 + Muon_Py ** 2)"

    - id: MuonPt
      op: hep.hist
      params:
        axes:
          - name: Muon_Pt
            source: Muon_Pt
            type: regular
            bins:
              low: 0
              high: 120
              nbins: 60
      render:
        style: muon_pt
        when: final
        out: MuonPt.png
```

## What to try next

Try changing:

- the number of events
- the histogram range
- the number of bins
- the render style
- the random seed

Then rerun the workflow and compare the output.

## Next tutorial

The next tutorial adds a selection step and shows how cuts affect the resulting histogram.