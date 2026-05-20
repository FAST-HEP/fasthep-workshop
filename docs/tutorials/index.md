## Beginner tutorials

### 1. First workflow: source → define → plot

Goal: understand `author.yaml`.

Covers:

* toy source
* `hep.define`
* derived variable: `Muon_Pt = sqrt(Muon_Px**2 + Muon_Py**2)`
* histogram
* simple render

Output:

* one plot

### 2. Add a selection

Goal: show analysis cuts.

Covers:

* `hep.define`
* boolean masks
* `hep.selection.cutflow`
* histogram after selection
* cutflow output

Output:

* selected plot
* cutflow artifact

### 3. Weighted histograms and datasets

Goal: introduce MC-style weighting.

Covers:

* multiple datasets
* flat dataset-dependent weights
* `weight_expr`
* dataset axis
* data/MC style render

Output:

* stacked Data/MC plot
* ratio panel if available

### 4. Multiple outputs from one workflow

Goal: show that one workflow can produce several artifacts.

Covers:

* several histograms
* shared styles
* render specs
* output naming
* final render timing

Output:

* `Muon_Pt`
* `Muon_Eta`
* `Muon_Iso`

### 5. Two-dimensional histograms and projections

Goal: introduce richer artifacts.

Covers:

* 2D histogram
* heatmap render
* projection render
* per-dataset rendering

Output:

* heatmap
* x projection
* y projection

## Intermediate tutorials

### 6. Inspect before running

Goal: debugging-heavy workflow development.

Covers:

* `fasthep normalise`
* `fasthep make-plan`
* `fasthep compile`
* reading `normalised.yaml`
* reading `plan.yaml`
* dependency inference

Output:

* normalised workflow
* plan
* explanation of what changed

### 7. Schema snapshots and diagnostics

Goal: introduce curator.

Covers:

* observers
* `hep.schema_snapshot`
* runtime diagnostics profile
* error context
* schema artifacts

Output:

* schema snapshot
* runtime summary/error report

### 8. Writing outputs with sinks

Goal: distinguish artifacts from persisted analysis products.

Covers:

* sink configuration
* ROOT/parquet/JSON output, depending on current support
* output paths
* final vs partition/dataset timing

Output:

* persisted file
* summary artifact

### 9. Profiles and custom registries

Goal: show extension composition.

Covers:

* `fasthep_workshop:registry`
* package-provided profile
* how operation names resolve
* why profiles matter
* local `.fasthep/profiles/...` scaffolding

Output:

* same workflow, now explained through registry/profile loading

### 10. Analysis repository layout

Goal: show “real analysis repo” structure.

Covers:

* `src/fasthep_workshop/`
* `profiles/registry.yaml`
* `transforms/`
* `sources/`
* tests
* package install/editable install

Output:

* users understand how to copy the pattern

## Advanced tutorials

### 11. Parallel workflows and multiple regions

Goal: demonstrate analysis branching.

Covers:

* signal/control regions
* multiple stages or parallel outputs
* shared upstream definitions
* multiple histograms from shared dataflow

Output:

* signal-region plot
* control-region plot
* comparison artifact if available

### 12. Backend selection

Goal: run the same workflow with different execution backends.

Covers:

* local backend
* Dask local backend
* backend config
* partitioning
* runtime summaries

Planned notes:

* `dask:htcondor`
* `dask:dirac`
* Snakemake

### 13. Strategies

Goal: tune execution without changing analysis logic.

Covers:

* backend-specific settings
* partition sizing
* scheduling hints
* optimisation hooks

Status:

* work in progress
* mark as roadmap/preview until stable

### 14. Render from specs

Goal: separate producing artifacts from rendering them.

Covers:

* render spec files
* re-rendering existing histograms
* style iteration
* plot-only workflows

Output:

* update plot style without rerunning analysis

### 15. Validation and comparison

Goal: compare outputs across runs.

Covers:

* histogram comparisons
* reference outputs
* validation reports
* regression-style checks

Status:

* current render/comparison support now
* future `fasthep-validate` later

## Expert tutorials

### 16. Write a custom source

Goal: explain source extension.

Covers:

* toy source implementation
* source spec
* registry entry
* stream type
* deterministic generated data

Output:

* user can implement `my_analysis.sources.*`

### 17. Write a custom transform

Goal: custom physics logic.

Covers:

* transform function
* spec
* dependency parser if needed
* registry entry
* tests

Output:

* new operation available as `my_analysis.my_transform`

### 18. Write a custom sink

Goal: custom output/artifact writing.

Covers:

* sink spec
* implementation
* timing: partition/dataset/final
* file output

Output:

* custom persisted artifact

### 19. Write hooks / diagnostics

Goal: runtime lifecycle extension.

Covers:

* lifecycle timing
* diagnostics hooks
* summaries
* error reporting

Output:

* custom runtime summary

### 20. Profiling and performance

Goal: optimize real analyses.

Covers:

* runtime summaries
* Dask reports
* partition sizing
* memory-aware execution
* slow-read diagnostics

### 21. Systematics

Goal: future advanced physics workflow pattern.

Covers:

* systematic variations
* weight variations
* repeated renders
* comparison outputs
