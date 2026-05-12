# Runtime Smoke Tutorial

This tiny workflow runs end to end without external files. It uses a small toy source helper so CI can validate the split package path quickly.

It still exercises:

- flow compile/run
- carpenter `hep.define` and `hep.hist`
- curator schema snapshots and runtime hooks
- render histogram sinks

Run:

```bash
fasthep run examples/tutorial/runtime-smoke/author.yaml --outdir build/tutorial/runtime-smoke
```
