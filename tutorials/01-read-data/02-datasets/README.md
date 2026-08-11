# Datasets

> Part 2 of 3 in **Read Data**
>
> ✓ 01. ROOT Files  
> ▶ 02. Datasets  
> ○ 03. Remote Data

This tutorial extends the ROOT-file reader example to two datasets.

## 1. Reuse the downloaded files

```bash
pixi run fasthep download --json tutorials/data/CMS/Zmumu/files.json --destination data
```

## 2. Inspect the dataset entries

```yaml
data:
  datasets:
    - name: data
      eventtype: data
      group: observed
      metadata:
        label: Collision data
      files:
        - data/CMS/Zmumu/data.root
    - name: dy
      eventtype: mc
      group: signal
      metadata:
        label: Drell-Yan simulation
      files:
        - data/CMS/Zmumu/dy.root
```

The example above defines two datasets: `data` and `dy`.

Datasets represent logical analysis inputs. Each dataset contains one or more files together with metadata describing how the workflow should treat them.

A dataset can specify:

- `eventtype` to distinguish between real data (`data`) and simulated events (`mc`)
- `group` to combine related datasets into a common category (for example multiple background samples contributing to the same process)
- `metadata` for additional user- or experiment-specific information

Dataset names and groups become labels that later transforms, histograms, cutflows, and renderers can use when processing or displaying results.

The `metadata` field is optional and can contain arbitrary key-value pairs.
FAST-HEP itself does not interpret these values, but individual modules may use them to customise behaviour, labels, styling, or experiment-specific processing.



## 3. Run the workflow

```bash
pixi run fasthep run tutorials/01-read-data/02-datasets/workflow.yaml --outdir build/tutorials/01-read-data/02-datasets
```

## 4. Inspect the outputs

Compare the schema report, `compile/dataset_entries.json`, and
`compile/dataset_metadata.json` with the previous tutorial. The workflow still
only reads data and records schema information.

## Expected outputs

The synced metadata snippet shows ROOT entry counts discovered during compile.
FAST-HEP can inspect ROOT files and record event counts automatically; you do
not need to maintain this information manually in your dataset YAML.

```{literalinclude} /_static/_generated/tutorials/01-read-data/02-datasets/snippets/dataset_metadata.json
:language: json
```
