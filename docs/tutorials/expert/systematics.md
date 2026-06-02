# Systematic variations

This tutorial introduces the FAST-HEP systematics model. It is intentionally
narrow: it shows how to describe workflow variations, how those variations are
expanded into plans, and how to inspect what changed.

Statistical uncertainties come from finite samples. Systematic uncertainties
come from imperfect knowledge of measurements, calibrations, efficiencies,
simulation models, or other analysis inputs.

FAST-HEP models systematic uncertainties as workflow variations:

```text
nominal workflow
  ↓
systematic expansion
  ↓
variation-specific plans
```

The first implementation favours transparency over optimisation. Each
variation is expanded into its own workflow copy and plan, so you can inspect
exactly what FAST-HEP will run.

This tutorial assumes you already understand `author.yaml`, workflow stages,
compilation, and plans.

## 1. Defining variations

Systematics are declared in the top-level `systematics` block.

```yaml
systematics:
  include_nominal: true

  variations:
    - name: trigger_eff_up
      group: trigger_eff
      direction: up
      weight:
        multiply:
          - TriggerEffWeight_up

    - name: trigger_eff_down
      group: trigger_eff
      direction: down
      weight:
        multiply:
          - TriggerEffWeight_down
```

The key fields are:

- `name`: the unique variation name. This is also used in output paths.
- `group`: a grouping label, usually the systematic source.
- `direction`: a direction such as `up` or `down`.
- `weight`: rules for changing event weights in the variation.

When this workflow is compiled, FAST-HEP writes one plan per generated
variation:

```text
build/
└── compile/
    ├── nominal/
    │   └── plan.yaml
    ├── trigger_eff_up/
    │   └── plan.yaml
    └── trigger_eff_down/
        └── plan.yaml
```

If `include_nominal: true`, FAST-HEP also writes the nominal plan. If it is
false, only the requested variations are written.

## 2. Weight variations

The first supported weight rule is multiplicative:

```yaml
weight:
  multiply:
    - TriggerEffWeight_up
```

FAST-HEP applies this rule to analysis stages that already have a
`params.weight_expr`. It does not add a weight to unweighted stages.

Authored stage:

```yaml
analysis:
  stages:
    - id: WeightedHist
      op: hep.hist
      params:
        axes:
          - name: mass
            type: regular
            source: DiMuonMass
            bins: {nbins: 60, low: 60, high: 120}
        weight_expr: EventWeight
```

In the nominal plan, the expression stays as authored:

```yaml
weight_expr: EventWeight
```

In the `trigger_eff_up` plan, the expression is rewritten:

```yaml
weight_expr: "(EventWeight) * (TriggerEffWeight_up)"
```

With multiple multipliers, FAST-HEP appends each one:

```yaml
weight_expr: "(EventWeight) * (TriggerEffWeight_up) * (ScaleFactor_up)"
```

This rewrite happens before graph lowering and plan generation. Runtime backends
receive an ordinary plan with the variation-specific expression already in it.

## 3. Object variations

Object-level variations can be represented with field replacements.

```yaml
systematics:
  include_nominal: true

  variations:
    - name: jes_up
      group: jes
      direction: up
      replace:
        Jet_Pt: Jet_Pt_JESUp
        Jet_Eta: Jet_Eta_JESUp
```

FAST-HEP rewrites simple expression-bearing stage parameters. For example:

```yaml
selection:
  - Jet_Pt > 30
  - abs(Jet_Eta) < 2.4
```

becomes:

```yaml
selection:
  - Jet_Pt_JESUp > 30
  - abs(Jet_Eta_JESUp) < 2.4
```

Exact source parameters are also rewritten:

```yaml
axes:
  - name: jet_pt
    source: Jet_Pt
```

becomes:

```yaml
axes:
  - name: jet_pt
    source: Jet_Pt_JESUp
```

The replacement is token-aware. Replacing `Jet_Pt` does not modify a longer
name such as `Jet_PtRaw` unless that name is explicitly listed in `replace`.

Current support is deliberately conservative. FAST-HEP rewrites:

- `params.variables[].expr`
- `params.weight_expr`
- `params.selection` strings
- `params.axes[].source` when it is an exact match
- `params.source` when it is an exact match

It does not rewrite arbitrary strings such as labels, output paths, stage IDs,
or operation names. Advanced object propagation is future work.

## 4. Dataset variations

Some systematics are represented by alternative samples. In FAST-HEP, a
variation can replace one dataset with another:

```yaml
data:
  datasets:
    - name: ttbar
      eventtype: mc
      files:
        - data/ttbar.root

    - name: ttbar_hdamp_up
      eventtype: mc
      files:
        - data/ttbar_hdamp_up.root

systematics:
  include_nominal: true

  variations:
    - name: ttbar_hdamp_up
      group: hdamp
      direction: up
      applies_to:
        datasets: [ttbar]
      datasets:
        replace:
          ttbar: ttbar_hdamp_up
```

The variation keeps the logical dataset name `ttbar`, but uses the replacement
sample content. This keeps downstream grouping and plotting stable.

The expanded variation workflow contains a dataset like:

```yaml
data:
  datasets:
    - name: ttbar
      eventtype: mc
      files:
        - data/ttbar_hdamp_up.root
      meta:
        systematic_replacement:
          nominal_dataset: ttbar
          replacement_dataset: ttbar_hdamp_up
```

Replacement-only datasets are removed from the active variation workflow after
substitution, so the variation does not process both `ttbar` and
`ttbar_hdamp_up`.

## 5. Running variations

Compile the workflow as usual:

```bash
fasthep compile author.yaml --outdir build
```

If systematics are present, this writes per-variation plans under
`build/compile/`.

Run a specific plan with `fasthep run-plan`:

```bash
fasthep run-plan build/compile/nominal/plan.yaml
fasthep run-plan build/compile/trigger_eff_up/plan.yaml
```

When no explicit `--outdir` is provided, variation plans use the workflow build
root and namespace outputs by variation:

```text
build/
├── artifacts/
│   ├── nominal/
│   │   ├── histograms/
│   │   └── plots/
│   └── trigger_eff_up/
│       ├── histograms/
│       └── plots/
├── reports/
│   ├── nominal/
│   └── trigger_eff_up/
├── debug/
│   ├── nominal/
│   └── trigger_eff_up/
└── run_summary.yaml
```

For now, `fasthep run author.yaml --outdir build` compiles all variation plans
and runs the nominal plan only when a nominal variation was generated. To run
other variations, call `fasthep run-plan` on the specific plan.

## 6. Inspecting plans

Each variation plan contains variation metadata in the plan context. For
example, `build/compile/trigger_eff_up/plan.yaml` contains:

```yaml
context:
  variation:
    name: trigger_eff_up
    group: trigger_eff
    direction: up
    is_nominal: false
    weight:
      multiply:
        - TriggerEffWeight_up
```

Plans also record rewrite metadata when FAST-HEP changed the expanded workflow:

```yaml
context:
  variation:
    rewrites:
      weight_expr:
        - stage: WeightedHist
          original: EventWeight
          rewritten: "(EventWeight) * (TriggerEffWeight_up)"
          multipliers:
            - TriggerEffWeight_up
```

For dataset replacements, the plan context records the logical dataset with the
replacement payload:

```yaml
context:
  datasets:
    ttbar:
      files:
        - data/ttbar_hdamp_up.root
      meta:
        systematic_replacement:
          nominal_dataset: ttbar
          replacement_dataset: ttbar_hdamp_up
```

Inspecting plans is the recommended first debugging step. It lets you check
which workflow copy was generated, which expressions were rewritten, and which
datasets are active before any runtime backend starts processing events.

## 7. Current limitations

Currently implemented:

- variation expansion
- per-variation plan generation
- variation-specific runtime output directories
- weight multiplication
- simple field replacement
- simple dataset replacement

Not yet implemented:

- caching
- partial graph reuse
- systematic profile expansion
- advanced object propagation
- nuisance modelling
- statistical inference

The current implementation is intended to be inspectable and predictable. It is
not yet optimised for large production campaigns.

## 8. Looking ahead

Future releases may optimise systematic workflows by reusing identical
intermediate products:

```text
nominal workflow
systematic workflow
```

where the two workflows share any steps that do not depend on the systematic
variation. For now, FAST-HEP keeps the model explicit: each variation has its
own expanded workflow and plan.
