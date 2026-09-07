# Inline variation matrix

Continue from [01. Independent variations](https://github.com/FAST-HEP/fasthep-workshop/blob/main/tutorials/05-systematics/01-variations-independent/README.md).
The first tutorial creates separate plans and structurally identical graphs with
substituted configuration. Here, one plan and graph contain nominal processing
and four affected branches expanded inline. Those branches are available for
parallel execution when the selected backend and strategy support it; this
example does not require parallel execution.

From the fasthep-workshop repository root, after `pixi install`, run:

```bash
pixi run fasthep run tutorials/05-systematics/02-variation-matrix-inline/workflow.yaml \
  --outdir build/tutorials/05-systematics/02-variation-matrix-inline
```

The example reuses `toy://dy`, seed 1729, and muon transverse momentum, with just
1,000 generated events and no download. Two illustrative momentum uncertainties,
`scale` (2%) and `alignment` (5%), replace the independent tutorial's broader set
of dataset, momentum and trigger variations. These constants demonstrate
propagation; they are not detector calibrations.

The single matrix combines two `source` values with two `direction` values:

| Branch name | Momentum relative to nominal |
| --- | --- |
| nominal | 1.00 |
| scale_up | 1.02 |
| scale_down | 0.98 |
| alignment_up | 1.05 |
| alignment_down | 0.95 |

`name: '{source}_{direction}'` names each combination. The same substitutions
populate `group`, `direction` and user `metadata`. The normalized workflow also
records `matrix_values` and `matrix_origin`, so the concrete branch and its
original matrix remain inspectable. `include_nominal: true` expresses the
intention to retain nominal; inline expansion preserves the original nodes.

`BasicVars` is the shared unaffected prefix after the source: it computes raw
muon momentum, the two fractional uncertainties, and the signs `up = 1` and
`down = -1`. `anchor: CalibrateMuon` starts cloning at the calibration stage.
The templated `patch` replaces that stage's variable definitions. For example,
`scale_down` evaluates `RawMuonPt * (1 + scale * down)` while nominal uses
`RawMuonPt`. Only the anchor receives the patch; its affected downstream
`MuonKinematics` stage is copied and consumes the varied momentum.

`stop_before: [Output]` keeps the final output stage and writer shared. Immediately
before that boundary, the compiler inserts exports and a collection node to join
the nominal stream with the four varied results. The one-entry export mapping

```yaml
'MuonPt_{source}_{direction}': MuonPt
```

maps a distinct destination field name on the left to the branch-local field on
the right. It exports only the downstream momentum needed for this comparison;
raw source columns and intermediate calibration fields need no export mapping.
The shared `Output` stage labels the nominal field `MuonPt_nominal` and writes
all five results together. No event filtering is performed, so the branches
retain matching event and muon ordering for collection.

Relative to the selected output directory, inspect:

```text
compile/normalized.yaml
compile/plan.yaml
graph/graph.mmd
graph/graph.dot
graph/graph.json
graph/graph.d2
graph/graph.svg
run_summary.yaml
artifacts/files/momenta/toy/0_0.root
```

SVG output requires the optional D2 renderer. Unlike tutorial 01, there are no
`compile/<variation>/` or `graph/<variation>/` directories: one `run` executes
nominal and all four inline branches. The ROOT `events` tree contains five
separate result fields: `MuonPt_nominal`, `MuonPt_scale_up`, `MuonPt_scale_down`,
`MuonPt_alignment_up` and `MuonPt_alignment_down`. The file path shown assumes
the default single partition; changing partitioning may produce more part files.

In the graph, the source and `BasicVars` appear once. `CalibrateMuon` and
`MuonKinematics` each have nominal plus four copies, followed by four exports,
one collection node, and the shared output stage and writer. Compare the five
fields for the same event: their momentum ratios should match the table above.
