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

Each event contributes to a two-dimensional bin defined by:

- the number of muons (`NMuon`)
- the number of isolated muons (`NIsoMuon`)

FAST-HEP fills the histogram exactly as it would a 1D histogram, except that each event is placed into a bin on both axes simultaneously.

EventWeight is still used when filling the histogram.

## 2. Inspect the renders

The render block creates three views of the same histogram:

- a 2D heatmap
- a projection onto the `nMuons` axis
- a projection onto the `nIsoMuons` axis

The heatmap is defined directly (in `styles.yaml`):
```yaml
n_muons_heatmap:
  op: hep.render.heatmap2d
```
The projections share most of their data/MC styling. Instead of repeating the same plot configuration twice, `styles.yaml` defines a reusable base style:
```yaml
base_counts_data_mc:
  op: hep.render.data_mc
  data_mc:
    data: data
    signals: [dy]
    backgrounds: [qcd, single_top, ttbar, wjets, ww, wz, zz]
    stack: true
    ratio: true
```
Each projection then reuses that base style and only changes the axis-specific parts:
```yaml
n_muons_proj_x:
  op: hep.render.project
  project:
    axis: nMuons
    keep_dataset: true
    then:
      use: base_counts_data_mc
      with:
        axes:
          x: {name: nMuons, label: "Number of $\\mu$", limits: [0, 5]}
```

The `project.axis` setting chooses which axis remains after projection. The other histogram axis is integrated over.

`keep_dataset: true` preserves the dataset axis, so the projected 1D histogram can still be rendered as a data/MC comparison.

This means a single 2D histogram product can produce several different plots without rerunning the analysis.

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/03-summarise-data/03-two-dimensional-histograms/workflow.yaml --outdir build/tutorials/03-summarise-data/03-two-dimensional-histograms
```

## 4. Inspect the outputs

Look at:

- `build/tutorials/03-summarise-data/03-two-dimensional-histograms/artifacts/histograms/`
- `build/tutorials/03-summarise-data/03-two-dimensional-histograms/artifacts/plots/`
- `build/tutorials/03-summarise-data/03-two-dimensional-histograms/render/`
- `build/tutorials/03-summarise-data/03-two-dimensional-histograms/run_summary.yaml`

Notice that only one histogram artifact is produced.

The heatmap and both projections are generated from the same histogram product during rendering.

## Expected outputs

The synced expected outputs include one heatmap image, both rendered projections,
and the histogram manifest.

```{figure} /_static/_generated/tutorials/03-summarise-data/03-two-dimensional-histograms/plots/NumberMuons_heatmap_data.png
:alt: Number of muons heatmap for data
:width: 420px
:target: /_static/_generated/tutorials/03-summarise-data/03-two-dimensional-histograms/plots/NumberMuons_heatmap_data.png

Expected 2D heatmap preview for the data sample.
```

```{figure} /_static/_generated/tutorials/03-summarise-data/03-two-dimensional-histograms/plots/NumberMuons_proj_nMuons.png
:alt: Number of muons projection
:width: 420px
:target: /_static/_generated/tutorials/03-summarise-data/03-two-dimensional-histograms/plots/NumberMuons_proj_nMuons.png

Expected projection onto the `nMuons` axis.
```

```{figure} /_static/_generated/tutorials/03-summarise-data/03-two-dimensional-histograms/plots/NumberMuons_proj_nIsoMuons.png
:alt: Number of isolated muons projection
:width: 420px
:target: /_static/_generated/tutorials/03-summarise-data/03-two-dimensional-histograms/plots/NumberMuons_proj_nIsoMuons.png

Expected projection onto the `nIsoMuons` axis.
```

The heatmap shows the full two-dimensional distribution.

The projection plots collapse the histogram onto a single axis by integrating over the other dimension. This allows the same histogram product to be explored from multiple perspectives without rerunning the analysis.

The histogram manifest records the underlying histogram artifact from which all three plots were produced.

```{literalinclude} /_static/_generated/tutorials/03-summarise-data/03-two-dimensional-histograms/snippets/histograms.manifest.json
:language: json
```
