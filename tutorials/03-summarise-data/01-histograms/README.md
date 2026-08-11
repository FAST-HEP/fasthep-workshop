# Histograms

> Part 1 of 4 in **Summarise Data**
>
> ▶ 01. Histograms  
> ○ 02. Render Histograms  
> ○ 03. Two-Dimensional Histograms  
> ○ 04. Cutflow Tables

This tutorial creates the first weighted histogram product for the full Z &rarr;
$\mu\mu$ dataset collection.

It focuses on histogram definitions, binning, event weights, and histogram
artifacts. Rendering comes in the next tutorial.

## 1. Inspect the inputs

The full dataset list lives in `datasets.yaml`.

`styles.yaml` is present from this section onward. Here it is intentionally
empty because this tutorial only creates histogram products. Later tutorials use
it to keep visual presentation separate from analysis logic.

## 2. Inspect the histogram stage

The workflow derives an isolated-muon mask, computes the dimuon invariant mass, and fills a weighted histogram.

```yaml
- id: DiMuonMass
  op: hep.hist
  params:
    dataset_axis: true
    storage: weighted
    axes:
      - name: dimu_mass
        source: DiMuon_Mass
        type: regular
        bins: {low: 60, high: 120, nbins: 60}
    weight_expr: EventWeight
```

The histogram has one physics axis, `dimu_mass`, which is filled from the derived field `DiMuon_Mass`.

The option `dataset_axis: true` tells FAST-HEP to keep the datasets separate inside the histogram.
This means data, signal, and background samples can be accumulated together while still remaining distinguishable later during rendering.

The option `storage: weighted` enables weighted histogram storage. The histogram is filled using:
```
weight_expr: EventWeight
```

`EventWeight` is especially important for simulated samples.
It makes Monte Carlo samples comparable to data by applying the appropriate event weights, typically including cross-section normalisation and other correction factors.

```{note}
For clarity, this tutorial explicitly specifies options such as
`dataset_axis`, `storage`, and histogram axis types.

In most workflows, FAST-HEP can infer sensible defaults automatically.
These options are shown here so you can see how histogram products are configured before moving on to rendering and more advanced summaries.
```

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/03-summarise-data/01-histograms/workflow.yaml --outdir build/tutorials/03-summarise-data/01-histograms
```

## 4. Inspect the outputs

Look at:

- `build/tutorials/03-summarise-data/01-histograms/artifacts/histograms/`
- `build/tutorials/03-summarise-data/01-histograms/run_summary.yaml`

The histogram artifact is a machine-readable product. At this stage it is not yet a plot; it is a persisted histogram that later render stages can turn into visual outputs.

This separation is useful because the same histogram can be rendered in different ways without rerunning the analysis.

## Expected outputs

The synced histogram manifest records the histogram artifact produced by the run.

```{literalinclude} /_static/_generated/tutorials/03-summarise-data/01-histograms/snippets/histograms.manifest.json
:language: json
```
The manifest shows which histogram products were written under `artifacts/histograms/`.
In the next tutorial, this product is used as the input for rendering.
