# analysis-name

Template for a private or public FAST-HEP analysis repository.

Custom analysis modules belong under `src/analysis_name`. Registry entries expose spec/impl pairs in the same pattern as FAST-HEP packages:

- transforms in `impl/` and `spec/`
- hooks in `hooks/`
- sinks in `sinks/`
- profile resources in `profiles/`

`src/analysis_name/registry.yaml` is the package-owned registry layer for custom analysis components. Private analysis repositories are expected and encouraged when data or physics details are not public.

Start from:

```bash
fasthep run author.yaml --outdir build/analysis-name
```
