# Dask To HTCondor

This tutorial runs the same deterministic workload as
`tutorials/07-scale-execution/01-local-dask`, but asks Dask to obtain workers
from HTCondor.

It requires a configured HTCondor submit node. The submit host must be able to
create Dask HTCondor jobs, and the worker jobs must be able to import the same
FAST-HEP Python environment. This tutorial does not cover file forwarding,
X.509 proxy handling, custom worker resources, or Slurm.

HTCondor jobs provide reusable Dask workers. They are not necessarily mapped
one-to-one to Flow partitions: a smaller number of workers can process a larger
number of partition tasks over the lifetime of the Dask cluster.

## 1. Check HTCondor Availability

Check the submit daemon and the pool before running FAST-HEP:

```bash
condor_q -totals
condor_status -total
```

If either command fails, the failing layer is HTCondor availability, not
FAST-HEP or Dask. Resolve the submit-node or pool configuration first.

## 2. Submit One Worker

Run one Flow partition with one requested HTCondor-backed Dask worker:

```bash
pixi run fasthep run tutorials/07-scale-execution/02-dask-condor/workflow.yaml \
  --outdir build/tutorials/07-scale-execution/02-dask-condor-one-worker \
  --chunk-size 3000 \
  --workers 1 \
  --partition 1
```

This starts a Dask scheduler for the run, submits one HTCondor worker job, runs
one partition, then closes the client and cluster.

If this fails before a worker job appears in `condor_q`, inspect the Python and
Dask layer. Missing `dask-jobqueue` is reported explicitly by the backend. If a
job appears but the worker never joins, inspect the worker logs under:

```text
build/tutorials/07-scale-execution/02-dask-condor-one-worker/debug/dask/htcondor/
```

## 3. Run A Small Partition

Confirm that the small run completed one partition:

```bash
pixi run python - <<'PY'
import yaml
from pathlib import Path

summary = yaml.safe_load(
    Path("build/tutorials/07-scale-execution/02-dask-condor-one-worker/run_summary.yaml")
    .read_text()
)
print("backend:", summary["backend"])
print("partitions:", summary["npartitions"])
PY
```

## 4. Scale To Ten Worker Jobs

The tutorial workflow requests ten workers:

```yaml
execution:
  backend: dask
  strategy: htcondor
  config:
    workers: 10
```

You can also pass `--workers 10` on the command line. During the run, use
`condor_q` to confirm that worker jobs were requested:

```bash
condor_q "$USER" -wide
```

## 5. Run The Complete Workload

```bash
pixi run fasthep run tutorials/07-scale-execution/02-dask-condor/workflow.yaml \
  --outdir build/tutorials/07-scale-execution/02-dask-condor \
  --chunk-size 3000 \
  --workers 10
```

The full workload has 24 Flow partitions. Ten HTCondor worker jobs can therefore
process multiple partition tasks each. Worker reuse is visible in Dask task
scheduling and in the worker logs. The Flow run summary records partition
completion; HTCondor and Dask logs record worker startup, failures, and stderr.

## 6. Compare With Local Dask

After completing tutorial 01 and this tutorial, compare the reduced histogram
artifacts:

```bash
pixi run python - <<'PY'
import filecmp
from pathlib import Path

local_dask = Path("build/tutorials/07-scale-execution/01-local-dask")
condor = Path("build/tutorials/07-scale-execution/02-dask-condor")

for condor_path in sorted((condor / "artifacts/histograms").glob("*.json")):
    local_path = local_dask / condor_path.relative_to(condor)
    print(condor_path.name, filecmp.cmp(condor_path, local_path, shallow=False))
PY
```

The comparison should print `True` for each histogram artifact.

## Failures And Logs

Useful places to look:

- `build/tutorials/07-scale-execution/02-dask-condor/run_summary.yaml`
- `build/tutorials/07-scale-execution/02-dask-condor/debug/dask/htcondor/`
- `condor_q "$USER" -wide`
- `condor_history "$USER" -limit 10`

If the scheduler starts but workers do not join, the failing layer is usually
worker environment startup, worker importability, or pool policy. If workers join
and a partition task fails, the failing layer is the FAST-HEP partition task; use
the run summary and worker stderr together.

## Cleanup

The backend closes the Dask client and cluster after success or failure. Confirm
that no tutorial worker jobs remain:

```bash
condor_q "$USER" -wide
```

If tutorial jobs remain after an interrupted shell session, remove only the
specific tutorial cluster IDs after checking their owner and command:

```bash
condor_q "$USER" -wide
condor_rm <ClusterId>
```
