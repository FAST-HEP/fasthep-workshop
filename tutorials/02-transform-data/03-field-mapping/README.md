# Field Mapping

> Part 3 of 3 in **Transform Data**
>
> ✓ 01. Derived Columns  
> ✓ 02. Object Selections  
> ▶ 03. Field Mapping

This tutorial reads the small local CMS Z &rarr; $\mu\mu$ ROOT files and maps a dataset-specific branch name to an analysis-facing field name.

Different datasets, skims, and analysis groups often use different names for the same physical quantity. FAST-HEP field mappings allow workflows to use stable analysis-facing names while mapping them onto dataset-specific branches.

This separation keeps analysis logic independent of a particular data format and makes workflows easier to share between datasets, collaborations, and processing stages.

In this example, the input branch `triggerIsoMu24` is mapped to the analysis-facing field name `analysis_trigger`. Later stages use that stable name without needing to know the original dataset branch.

```text
dataset branch
        ↓
field mapping
        ↓
analysis logic
```

```{note}
Field mapping becomes especially useful when switching between datasets.

In later tutorials, the same workflow can be run on different input formats by changing only the dataset definitions and field mappings, while leaving the analysis stages unchanged.
```

## 1. Inspect the dataset file

The dataset is defined separately in `datasets.yaml`:

```yaml
data:
  datasets:
    - name: data
      files:
        - data/CMS/Zmumu/data.root
```

These files are provided by the workshop data setup and are read locally.

## 2. Inspect the field mapping

Rather than using experiment-specific branch names throughout the workflow, FAST-HEP allows analyses to define their own field names.

This tutorial maps a dataset trigger branch to the analysis-facing field `analysis_trigger`:

```yaml
fields:
  analysis_trigger:
    stream: events
    branch: triggerIsoMu24
```

The workflow can then refer to `analysis_trigger` instead of the dataset-specific branch name.

For example, the selection stage becomes:

```yaml
selection:
  All:
    - "analysis_trigger == 1"
```
This keeps analysis logic independent of experiment-specific naming conventions and makes workflows easier to read and maintain.

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/02-transform-data/03-field-mapping/author.yaml --outdir build/tutorials/02-transform-data/03-field-mapping
```
## 4. Inspect the outputs

Look at:

- `build/tutorials/02-transform-data/03-field-mapping/compile/deps.yaml`
- `build/tutorials/02-transform-data/03-field-mapping/reports/schema/`
- `build/tutorials/02-transform-data/03-field-mapping/run_summary.yaml`

This workflow never references the original CMS branch name inside the analysis logic. Instead, the selection uses the analysis-facing field:

```text
analysis_trigger
```

FAST-HEP resolves this mapping automatically and determines which source branch must be loaded from the dataset.

The schema snapshots show the event stream before and after the selection stage, while the dependency report records how analysis fields are connected to the underlying dataset branches.

Notice that only the branches required by the workflow are loaded from the remote NanoAOD file.

## Expected outputs

The dependency report shows how the analysis-facing field is resolved back to the original dataset branch.

```{literalinclude} /_static/_generated/tutorials/02-transform-data/03-field-mapping/snippets/deps.yaml
:language: yaml
```

The cutflow summary demonstrates that later stages operate entirely on the analysis field name rather than the original CMS branch name.

```{literalinclude} /_static/_generated/tutorials/02-transform-data/03-field-mapping/snippets/TriggerSelection.summary.json
:language: json
```

Field mappings provide a stable interface between datasets and analysis logic. This becomes particularly useful when working with skims or collaborating with other groups that use different branch naming conventions.

In later tutorials, the same analysis workflow can be run on different datasets by changing only the dataset definitions and field mappings, while leaving the analysis stages unchanged.
