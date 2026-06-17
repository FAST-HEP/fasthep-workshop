# Datasets

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
      files:
        - data/CMS/Zmumu/data.root
    - name: dy
      eventtype: mc
      group: signal
      files:
        - data/CMS/Zmumu/dy.root
```

Dataset names become the labels that later transforms, summaries, and renderers
can use for grouping. `eventtype` separates data from simulated samples.

## 3. Run the workflow

```bash
pixi run fasthep run tutorials/01-read-data/datasets/author.yaml --outdir build/tutorials/01-read-data/datasets
```

## 4. Inspect the outputs

Compare the schema report and `compile/dataset_entries.json` with the previous
tutorial. The workflow still only reads data and records schema information.
