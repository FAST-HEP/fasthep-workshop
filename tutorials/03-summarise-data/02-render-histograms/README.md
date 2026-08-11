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

This separation allows the same histogram to be rendered in different ways without rerunning the analysis.
During the final stages of an analysis it is common to adjust labels, ranges, styling, or experiment branding many times while the underlying histogram remains unchanged.

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

The `style` selects a rendering configuration from `styles.yaml`.

The `when: final` option tells FAST-HEP to render only after all datasets have been processed and merged into the final histogram product.

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/03-summarise-data/02-render-histograms/workflow.yaml --outdir build/tutorials/03-summarise-data/02-render-histograms
```

## 4. Inspect the outputs

Look at:

- `build/tutorials/03-summarise-data/02-render-histograms/artifacts/histograms/`
- `build/tutorials/03-summarise-data/02-render-histograms/artifacts/plots/`
- `build/tutorials/03-summarise-data/02-render-histograms/render/specs/`
- `build/tutorials/03-summarise-data/02-render-histograms/run_summary.yaml`

The histogram artifact contains the machine-readable histogram data.

The plot in `artifacts/plots/` is a rendered view of that histogram.

The render specification in `render/specs/` records exactly how the plot was produced, including the style and source histogram.

This separation allows plots to be regenerated or adjusted without rerunning the full analysis.

## Expected outputs

The synced expected output includes the rendered dimuon-mass plot and the
histogram manifest that points to the source artifact.

```{figure} /_static/_generated/tutorials/03-summarise-data/02-render-histograms/plots/DiMuonMass.png
:alt: Dimuon mass plot
:width: 640px
:target: /_static/_generated/tutorials/03-summarise-data/02-render-histograms/plots/DiMuonMass.png

Expected dimuon-mass plot produced by this tutorial.
```
The rendered plot is produced from the histogram artifact generated in the previous tutorial.

The histogram manifest records the histogram products available for rendering:

```{literalinclude} /_static/_generated/tutorials/03-summarise-data/02-render-histograms/snippets/histograms.manifest.json
:language: json
```

The corresponding render specification is written under:
```
build/tutorials/03-summarise-data/02-render-histograms/render/specs/render_DiMuonMass_0.yaml
```

:::{dropdown} Show render specification
```{literalinclude} /_static/_generated/tutorials/03-summarise-data/02-render-histograms/snippets/render_DiMuonMass_0.yaml
:language: yaml
```
:::
