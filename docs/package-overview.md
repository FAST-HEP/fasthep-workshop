# Package Overview

- `fasthep-flow` owns the workflow model, compiler, runtime, backend interface, and registry/profile mechanics. Its Python import namespace is `hepflow`.
- `fasthep-carpenter` owns HEP transforms, ROOT sources/writers, and expression helpers.
- `fasthep-curator` owns schema inspection, diagnostics, provenance helpers, and runtime hooks.
- `fasthep-render` owns plot/report rendering sinks and render style helpers.
- `fasthep-cli` owns the `fasthep` command.
- `fasthep-workshop` owns tutorials, examples, public validation workflows, and analysis templates.

For detailed migration boundaries, see `../PACKAGE_MAP.md`.
