# Project fields

> Part 3 of 3 in **Transform Data**
>
> ✓ 01. Derived Columns  
> ✓ 02. Object Selections  
> ▶ 03. Project Fields

This tutorial reads one public CMS Open Data NanoAOD file directly over XRootD
and aliases a long technical branch name to an analysis-facing field name.

Real datasets often have long technical branch names. Projection lets an
analysis keep only useful fields and rename them to analysis-level names before
later skimming or summarising.

## 1. Inspect the dataset file

The dataset is defined separately in `datasets.yaml`:

```yaml
datasets:
  DoubleMuon:
    files:
      - root://eospublic.cern.ch//eos/opendata/cms/...
```

No local ROOT file is downloaded. XRootD support is required in the runtime
environment.

## 2. Inspect the projection

`author.yaml` reads a small branch list and aliases a long HLT branch:

```yaml
analysis:
  stages:
    - id: ProjectAnalysisFields
      op: hep.project_fields
      params:
        aliases:
          analysis_trigger: HLT_Photon26_R9Id85_OR_CaloId24b40e_Iso50T80L_Photon16_AND_HE10_R9Id65_Eta2_Mass60
```

The original branch remains available, and the new `analysis_trigger` alias is
added to the event stream.

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/02-transform-data/03-project-fields/author.yaml --outdir build/tutorials/02-transform-data/03-project-fields
```

## 4. Inspect the outputs

Look at:

- `build/tutorials/02-transform-data/03-project-fields/reports/schema/`
- `build/tutorials/02-transform-data/03-project-fields/run_summary.yaml`

The schema snapshots show the original remote branches and the added
`analysis_trigger` alias. Note that by default only used branches are loaded.

---

## Next steps

Previous: {doc}`02. Object Selections </tutorials/02-transform-data/02-object-selections>`
