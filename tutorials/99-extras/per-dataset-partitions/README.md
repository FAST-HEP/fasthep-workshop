# Per-Dataset Partitions

This extra is the playground for running one dataset at a time. It takes the
nine Zmumu ROOT inputs and gives each dataset its own `chunk_size`, chosen so
that every dataset has five partitions. That is artificial, since `qcd` has 142
events and `data` has 469384, but it gives each dataset the same partition
numbers, 1 to 5, to work with.

The analysis is the one from [Partitioned ROOT Skim](../partitioned-root-skim/):
derive dimuon quantities, select candidate events, fill a mass histogram and
write a ROOT skim. Only the partitioning differs.

> **Status.** This example needs the per-dataset mode of `fasthep run`
> (`execution.partitioning.per_dataset`, dataset `chunk_size`, `--dataset` and
> `--list-partitions`), which is being designed in the FAST-HEP task
> `2026-11-17-cli-run-dataset-option`. Until it lands the workflow does not
> compile, and the commands below are the intended usage. The structure test
> (`tests/test_per_dataset_partitions_tutorial.py`) already checks the chunk
> sizes.

## Inputs

`datasets.yaml` uses the same files and event counts as
`tutorials/03-summarise-data/01-histograms/datasets.yaml`, with
`chunk_size = ceil(nevents / 5)`:

| dataset | events | chunk size | partitions |
|---|---|---|---|
| data | 469384 | 93877 | 5 |
| dy | 77729 | 15546 | 5 |
| qcd | 142 | 29 | 5 |
| single_top | 5684 | 1137 | 5 |
| ttbar | 36941 | 7389 | 5 |
| wjets | 109737 | 21948 | 5 |
| ww | 4580 | 916 | 5 |
| wz | 3367 | 674 | 5 |
| zz | 2421 | 485 | 5 |

The last partition of each dataset is a little shorter than the others.
`workflow.yaml` sets `execution.partitioning.per_dataset: true`, which turns on
dataset-local partition numbers and one compile unit per dataset.

## Inspect

From the workshop repository root:

```bash
pixi run fasthep run tutorials/99-extras/per-dataset-partitions/workflow.yaml \
  --outdir build/tutorials/99-extras/per-dataset-partitions \
  --list-partitions
```

This lists the partitions for every dataset without running anything. Add
`--dataset qcd` to list one dataset.

## Run one dataset

```bash
pixi run fasthep run tutorials/99-extras/per-dataset-partitions/workflow.yaml \
  --outdir build/tutorials/99-extras/per-dataset-partitions \
  --dataset qcd
```

Run a single partition of that dataset with `--partition 3`. The number counts
inside `qcd`, so `--dataset qcd --partition 3` and `--dataset zz --partition 3`
are different slices of the data.

Running other datasets into the same `--outdir` is safe: each one writes its own
compile unit and run directory, and they share only the files that are
identical for every dataset.

## Outputs

The skim parts are named after the dataset and the partition number:

```text
build/tutorials/99-extras/per-dataset-partitions/artifacts/files/dimuon_per_dataset_skim/qcd/1.root
build/tutorials/99-extras/per-dataset-partitions/artifacts/files/dimuon_per_dataset_skim/qcd/2.root
...
```

Each dataset directory holds five files, one per partition.
