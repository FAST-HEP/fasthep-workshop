# Getting Started

Install the split packages needed by the workflow you want to run.

For HEP examples:

```bash
pip install fasthep-flow fasthep-carpenter fasthep-curator fasthep-render fasthep-cli
```

Then run a workflow:

```bash
fasthep run examples/tutorial/runtime-smoke/author.yaml --outdir build/tutorial/runtime-smoke
```

Examples use package-owned profiles:

```yaml
use:
  profiles:
    - registry
    - fasthep_carpenter:registry
    - fasthep_curator:registry
    - fasthep_curator:default_context
    - fasthep_curator:runtime_diagnostics
    - fasthep_render:registry
```
