# Workflow Overview

FAST-HEP workflows start from an `author.yaml`, then compile to normalized author and execution-plan files.

Typical CLI flow:

```bash
fasthep normalise author.yaml --outdir build/example
fasthep make-plan build/example/normalized.yaml --outdir build/example
fasthep run-plan build/example/plan.yaml
```

The shorter form is:

```bash
fasthep run author.yaml --outdir build/example
```

Implementation packages contribute functionality through registry profiles. The workshop examples show how flow, carpenter, curator, and render profiles combine in an author file.
