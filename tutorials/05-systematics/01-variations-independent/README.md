# Independent systematic variations

This tutorial compiles one independent plan and graph for each systematic
variation, including nominal. It uses generated toy events, so no data download
is required.

From the fasthep-workshop repository root, after `pixi install`, run:

```bash
pixi run fasthep run tutorials/05-systematics/01-variations-independent/workflow.yaml \
  --outdir build/tutorials/05-systematics/01-variations-independent
```

Compilation expands all five plans: `nominal`, `trigger_eff_up`,
`trigger_eff_down`, `muon_pt_scale_up` and `dataset_alt`. The `run` command then
executes nominal only. To execute another saved plan, use:

```bash
pixi run fasthep run-plan \
  build/tutorials/05-systematics/01-variations-independent/compile/trigger_eff_up/plan.yaml
```

Variation expansion multiplexes the same workflow into independent copies while
substituting selected values:

- `dataset_alt` replaces the `toy` dataset with `toy_alt`.
- `muon_pt_scale_up` substitutes the muon momentum field with its scaled value.
- `trigger_eff_up` and `trigger_eff_down` apply the corresponding trigger
  efficiency weight.

For this tutorial, the graphs have identical topology: the same nodes and
connections describe the analysis in every variation. Graph parameters,
metadata and inputs may differ to record the substitutions, so serialized
graphs need not be byte-identical. Compare their values as well as their diagrams.

All paths below are relative to the output directory selected with `--outdir`:

```text
compile/
  normalized.yaml
  systematics.yaml
  <variation>/
    normalized.yaml
    plan.yaml
    graph_render.json
graph/
  <variation>/
    graph.mmd
    graph.dot
    graph.json
    graph.d2
    graph.svg
reports/
  <variation>/
    run_summary.yaml
```

Each `compile/<variation>/` contains the expanded workflow and saved plan;
`compile/systematics.yaml` lists all generated plans. Each `graph/<variation>/`
contains its source graph artifacts and, when the optional D2 renderer succeeds,
`graph.svg`. Source graphs are saved before SVG rendering, and
`compile/<variation>/graph.json` records the rendering result when the
hook completes.

Execution reports are scoped to `reports/<variation>/`; `run_summary.yaml` is
written when that variation is executed. Histogram and plot products likewise
use `artifacts/<variation>/`. Compiling all variations does not execute them all.

Next: [02. Inline variation matrix](https://github.com/FAST-HEP/fasthep-workshop/blob/main/tutorials/05-systematics/02-variation-matrix-inline/README.md) puts
nominal and affected variation branches into one plan and graph.
