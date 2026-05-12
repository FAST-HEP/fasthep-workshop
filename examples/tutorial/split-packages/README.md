# Split Packages Tutorial

This tiny workflow exercises the split package architecture without requiring external data.

It uses:

- `fasthep-flow` for compile/run orchestration
- `fasthep-carpenter` for the ROOT source, define transform, and histogram transform
- `fasthep-curator` for schema snapshots and runtime diagnostics
- `fasthep-render` for the final plot sink

Generate local toy data and run:

```bash
python scripts/ci/make_tutorial_data.py
fasthep run examples/tutorial/split-packages/author.yaml --outdir build/tutorial/split-packages
```

Outputs are written under `build/tutorial/split-packages`.
