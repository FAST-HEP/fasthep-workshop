# Data and MC paths

This tutorial shows how one workflow can describe shared data/MC processing
while keeping MC-only stages out of data execution.

The common path derives `Muon_Pt` from `Muon_Px` and `Muon_Py`, then fills and
renders a `Muon_Pt` histogram for both datasets.

The MC-only path derives `MCLepton_Pt` from `MCLepton_Px` and `MCLepton_Py`,
then fills and renders an MC-only histogram:

```yaml
applies_to:
  eventtype: mc
```

`applies_to` describes which datasets a node belongs to. It is separate from
`when`, which describes lifecycle timing such as partition, dataset, or final
execution.

Run the workflow from the repository root:

```bash
pixi run fasthep run tutorials/06-organise-workflows/01-data-and-mc/workflow.yaml \
  --outdir build/tutorials/06-organise-workflows/01-data-and-mc
```

You should get a graph like this:

```{mermaid}
flowchart TD
  read_events["read.events<br/>source<br/>workshop.toy_source"]:::source
  stage_MuonColumns["stage.MuonColumns<br/>transform<br/>hep.define"]:::transform
  stage_MuonPt["stage.MuonPt<br/>transform<br/>hep.hist"]:::sink
  render_MuonPt_0["render.MuonPt.0<br/>sink<br/>hep.render.hist1d"]:::sink
  stage_MCLeptonColumns["stage.MCLeptonColumns<br/>transform<br/>hep.define"]:::transform
  stage_MCLeptonPt["stage.MCLeptonPt<br/>transform<br/>hep.hist"]:::sink
  render_MCLeptonPt_0["render.MCLeptonPt.0<br/>sink<br/>hep.render.hist1d"]:::sink
  read_events -->|stream -> stream| stage_MuonColumns
  stage_MuonColumns -->|stream -> stream| stage_MuonPt
  stage_MuonColumns -->|stream -> stream| stage_MCLeptonColumns
  stage_MuonPt -->|hist -> target| render_MuonPt_0
  stage_MCLeptonColumns -->|stream -> stream| stage_MCLeptonPt
  stage_MCLeptonPt -->|hist -> target| render_MCLeptonPt_0
```

Expected behavior:

- the data dataset runs only the shared `Muon_Pt` path
- the ttbar dataset runs both the shared `Muon_Pt` path and the MC-only
  `MCLepton_Pt` path
- `MCLepton_Px` and `MCLepton_Py` are required only for ttbar
- the MC-only render uses `when: dataset`, so it runs for the ttbar dataset
  context and is skipped for data
