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

The workflow derives an isolated-muon mask, computes the dimuon invariant mass,
and fills a weighted histogram:

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

`EventWeight` makes the Monte Carlo samples comparable to data rather than
treating every simulated event equally.

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/03-summarise-data/01-histograms/author.yaml --outdir build/tutorials/03-summarise-data/01-histograms
```

## 4. Inspect the outputs

Look at:

- `build/tutorials/03-summarise-data/01-histograms/artifacts/histograms/`
- `build/tutorials/03-summarise-data/01-histograms/run_summary.yaml`

The histogram artifact is a machine-readable product that later render stages
can turn into plots.

---

## Next steps

Next: {doc}`02. Render Histograms </tutorials/03-summarise-data/02-render-histograms>`
