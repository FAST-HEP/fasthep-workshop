# Partitioned ROOT Skim

This advanced example turns the nine-dataset dimuon histogram tutorial into a
partitioned analysis skim.

The workflow reads the same Zmumu ROOT inputs, derives dimuon quantities,
selects candidate dimuon events, fills a reduced histogram product, and writes
one ROOT skim part for each dataset partition.

```text
read events
    -> derive and select dimuon events
        -> fill histograms and cutflow
        -> write ROOT skim parts
```

## Inputs

`datasets.yaml` uses the same nine ROOT files as
`tutorials/03-summarise-data/01-histograms/datasets.yaml`:

- `data`
- `dy`
- `qcd`
- `single_top`
- `ttbar`
- `wjets`
- `ww`
- `wz`
- `zz`

The original event counts range from 142 events in `qcd` to 469384 events in
`data`. This extra tutorial deliberately caps each dataset declaration to the
first 120 events so the partition behavior is visible without creating
thousands of small ROOT files. The ROOT input files are not duplicated.

## Inspect

From the workshop repository root:

```bash
pixi run fasthep compile tutorials/99-extras/partitioned-root-skim/workflow.yaml \
  --outdir build/tutorials/99-extras/partitioned-root-skim \
  --chunk-size 40
```

The `--chunk-size 40` option is the configured event count per partition. With
120 declared events in each of the nine datasets, the plan contains about 27
partitions: three partitions per dataset. The small value is for demonstration,
not a production recommendation.

Inspect the compiled plan:

```bash
pixi run python - <<'PY'
import yaml
from pathlib import Path

plan = yaml.safe_load(
    Path("build/tutorials/99-extras/partitioned-root-skim/compile/plan.yaml")
    .read_text()
)
print("datasets:", sorted(plan["context"]["datasets"]))
print("partitions:", len(plan["partitions"]))
print("writer nodes:", [n["id"] for n in plan["nodes"] if n["role"] == "sink"])
PY
```

## Run

```bash
pixi run fasthep run tutorials/99-extras/partitioned-root-skim/workflow.yaml \
  --outdir build/tutorials/99-extras/partitioned-root-skim \
  --chunk-size 40
```

Repeated runs should use a fresh output directory, or remove only the previous
`build/tutorials/99-extras/partitioned-root-skim` directory before rerunning.

## Histogram Outputs

Look at:

- `build/tutorials/99-extras/partitioned-root-skim/artifacts/histograms/`
- `build/tutorials/99-extras/partitioned-root-skim/artifacts/cutflows/`

The histogram and cutflow products are reduced products. During partitioned
execution, partition-local histogram and cutflow values are combined into one
logical result per product and dataset/group according to the workflow
semantics.

## ROOT Skim Outputs

The ROOT writer is attached to `SelectDimuonEvents`, so it consumes the selected
event stream. It is a sibling consumer of the selected stream, not downstream of
the histogram or cutflow product.

The skim keeps a compact branch set:

- `EventWeight`
- `triggerIsoMu24`
- `NMuon`
- `Muon_Pt`
- `Muon_Charge`
- `NIsolatedMuon`
- `HasMuonAbove25`
- `DiMuon_Mass`

List the part files:

```bash
find build/tutorials/99-extras/partitioned-root-skim/artifacts/files/dimuon_partition_skim \
  -name '*.root' | sort
```

Each ROOT file corresponds to one successful partition writer invocation. The
part filenames include the dataset and partition key, so files from different
datasets and partitions do not collide.

The current runtime keeps lightweight writer results for these partition files
until finalization. Histogram and cutflow values are incrementally combined, but
ROOT artifact results are collected as one small reference-like result per
physical part. Event payloads are released after the partition is accepted.

## Validate The Skim

Use `uproot` from the workshop environment to inspect the files:

```bash
pixi run python - <<'PY'
from pathlib import Path
import uproot

root = Path("build/tutorials/99-extras/partitioned-root-skim")
parts = sorted((root / "artifacts/files/dimuon_partition_skim").glob("*/*.root"))
total = 0
for part in parts:
    with uproot.open(part) as handle:
        tree = handle["events"]
        total += tree.num_entries
        print(part.relative_to(root), tree.num_entries, tree.keys())
print("parts:", len(parts))
print("skim entries:", total)
PY
```

Compare the total skim entries with the selected-event count in the cutflow
artifact:

```bash
pixi run python - <<'PY'
import json
from pathlib import Path

path = Path(
    "build/tutorials/99-extras/partitioned-root-skim/"
    "artifacts/cutflows/SelectDimuonEvents.json"
)
payload = json.loads(path.read_text())
for dataset in payload["datasets"]:
    stats = payload["nodes"][-1]["stats"][dataset]
    print(dataset, "selected events:", stats["n_unweighted_out"])
PY
```

The comparison is per dataset. The sum of entries across a dataset's ROOT parts
matches that dataset's final selected-event count.
