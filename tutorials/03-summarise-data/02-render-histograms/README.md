# Render histograms

> Part 2 of 4 in **Summarise Data**
>
> ✓ 01. Histograms  
> ▶ 02. Render Histograms  
> ○ 03. Two-Dimensional Histograms  
> ○ 04. Cutflow Tables

This tutorial renders the weighted dimuon-mass histogram as a data/MC
comparison.

## 1. Inspect the style file

`styles.yaml` keeps visual presentation separate from analysis logic. The
workflow decides what to compute; the style file describes labels, colours,
stacking, ratio panels, and axis labels.

For example, `dimuon_mass` inherits the shared data/MC style and only changes
the axis labels for this plot.

## 2. Inspect the render block

The histogram stage requests rendering after the final merged histogram is
available:

```yaml
render:
  style: dimuon_mass
  when: final
```

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/03-summarise-data/02-render-histograms/author.yaml --outdir build/tutorials/03-summarise-data/02-render-histograms
```

## 4. Inspect the outputs

Look at:

- `build/tutorials/03-summarise-data/02-render-histograms/artifacts/histograms/`
- `build/tutorials/03-summarise-data/02-render-histograms/artifacts/plots/`
- `build/tutorials/03-summarise-data/02-render-histograms/render/`
- `build/tutorials/03-summarise-data/02-render-histograms/run_summary.yaml`

The plot output is the rendered view of the histogram product.
