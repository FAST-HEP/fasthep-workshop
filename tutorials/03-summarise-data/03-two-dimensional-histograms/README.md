# Two-dimensional histograms

> Part 3 of 4 in **Summarise Data**
>
> ✓ 01. Histograms  
> ✓ 02. Render Histograms  
> ▶ 03. Two-Dimensional Histograms  
> ○ 04. Cutflow Tables

This tutorial fills and renders a 2D histogram of the number of muons versus the
number of isolated muons.

Only the histogram dimensionality is new here. The dataset list, derived
quantities, weights, and styles follow the same pattern as the previous
tutorials.

## 1. Inspect the histogram

The histogram has one dataset axis and two physics axes:

```yaml
axes:
  - {name: nMuons, source: NMuon, type: regular, bins: {low: 0, high: 5, nbins: 6}}
  - {name: nIsoMuons, source: NIsoMuon, type: regular, bins: {low: 0, high: 5, nbins: 6}}
```

`EventWeight` is still used when filling the histogram.

## 2. Inspect the renders

The render block creates:

- a 2D heatmap
- an `nMuons` projection
- an `nIsoMuons` projection

The projection styles reuse the same data/MC styling as the 1D dimuon-mass
plot.

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/03-summarise-data/03-two-dimensional-histograms/author.yaml --outdir build/tutorials/03-summarise-data/03-two-dimensional-histograms
```

## 4. Inspect the outputs

Look at:

- `build/tutorials/03-summarise-data/03-two-dimensional-histograms/artifacts/histograms/`
- `build/tutorials/03-summarise-data/03-two-dimensional-histograms/artifacts/plots/`
- `build/tutorials/03-summarise-data/03-two-dimensional-histograms/render/`
- `build/tutorials/03-summarise-data/03-two-dimensional-histograms/run_summary.yaml`
