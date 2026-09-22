# CMS H->tautau (draft)

Draft skeleton for a CMS H->tautau (mu-tau) FAST-HEP workflow. It is not a
physics reproduction: `PairSelection`, `BackgroundEstimation`, `Discriminant`,
and `Templates` are `workshop.placeholder_stage` stand-ins for the real
analysis phases described in the source study
(`external/analysis_cms_higgs_tautau` in the `fasthep-dev` workspace). The
workflow runs end-to-end against `workshop.toy_source` toy events so its
structure stays runnable while those stages are ported incrementally.

Run it with the standalone Workshop environment:

```bash
fasthep run examples/CMS/higgs_tautau/workflow.yaml --outdir build/examples/CMS/higgs_tautau
```

Or from the `fasthep-dev` `dev` environment:

```bash
pixi run -e dev fasthep run workshop/examples/CMS/higgs_tautau/workflow.yaml --outdir build/examples/CMS/higgs_tautau
```
