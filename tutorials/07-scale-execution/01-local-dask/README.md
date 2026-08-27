# Local Dask

This tutorial runs a partitioned toy analysis on four local Dask workers. The
input is generated deterministically, so the same workflow can be compared with
the ordinary local backend without downloading data.

## Workload

The workflow declares three toy datasets with 24000 generated events each. Run
it with a chunk size of 3000 events:

```bash
pixi run fasthep compile tutorials/07-scale-execution/01-local-dask/workflow.yaml \
  --outdir build/tutorials/07-scale-execution/01-local-dask \
  --chunk-size 3000
```

The plan has 24 Flow partitions: eight partitions for each dataset.

```bash
pixi run python - <<'PY'
import yaml
from collections import Counter
from pathlib import Path

plan = yaml.safe_load(
    Path("build/tutorials/07-scale-execution/01-local-dask/compile/plan.yaml")
    .read_text()
)
print("partitions:", len(plan["partitions"]))
print("by dataset:", dict(Counter(p["dataset"] for p in plan["partitions"])))
print("execution:", plan["execution"])
PY
```

## Run On Four Workers

```bash
pixi run fasthep run tutorials/07-scale-execution/01-local-dask/workflow.yaml \
  --outdir build/tutorials/07-scale-execution/01-local-dask \
  --chunk-size 3000
```

The four-worker limit is configured in `workflow.yaml`:

```yaml
execution:
  backend: dask
  strategy: local
  config:
    workers: 4
    threads_per_worker: 1
```

Each Flow partition becomes one Dask task. With 24 partitions and four workers,
Dask schedules more tasks than workers, so each worker is reused for multiple
partitions. The worker is the reusable execution slot; the Flow partition is the
unit of analysis work.

Partition-local histogram products are reduced after partition execution. The
final histogram artifacts are the reduced products, not one histogram file per
partition.

## Compare With Local Backend

Run the same workflow with the ordinary local backend:

```bash
pixi run fasthep run tutorials/07-scale-execution/01-local-dask/workflow.yaml \
  --outdir build/tutorials/07-scale-execution/01-local-dask-local \
  --chunk-size 3000 \
  --backend local
```

Compare the reduced histogram artifacts:

```bash
pixi run python - <<'PY'
import filecmp
from pathlib import Path

dask_root = Path("build/tutorials/07-scale-execution/01-local-dask")
local_root = Path("build/tutorials/07-scale-execution/01-local-dask-local")

for dask_path in sorted((dask_root / "artifacts/histograms").glob("*.json")):
    local_path = local_root / dask_path.relative_to(dask_root)
    print(dask_path.name, filecmp.cmp(dask_path, local_path, shallow=False))
PY
```

The comparison should print `True` for each histogram artifact.

## Inspect Execution

The run summary records Dask as the backend and reports the number of Flow
partitions submitted as Dask tasks:

```bash
pixi run python - <<'PY'
import yaml
from pathlib import Path

summary = yaml.safe_load(
    Path("build/tutorials/07-scale-execution/01-local-dask/run_summary.yaml")
    .read_text()
)
print(summary["backend"])
print("partitions processed:", summary["npartitions"])
PY
```
