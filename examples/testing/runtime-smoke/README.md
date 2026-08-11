# Runtime Smoke Validation

This tiny workflow runs end to end without external files. It uses a small toy source helper so CI can validate the split package path quickly.

It still exercises:

- flow compile/run
- carpenter `hep.define` and `hep.hist`
- curator schema snapshots and runtime hooks
- render histogram sinks

Run:

```bash
fasthep run examples/testing/runtime-smoke/workflow.yaml --outdir build/testing/runtime-smoke
```
