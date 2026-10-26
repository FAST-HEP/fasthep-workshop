# fasthep-workshop Agent Instructions

`fasthep-workshop` owns runnable FAST-HEP examples, tutorials, and training
documentation. It is a user-facing learning repository, not a development
workspace for unreleased package source trees.

## Ownership

This repository owns:

- runnable FAST-HEP examples and tutorials;
- training documentation explaining each tutorial;
- selected output snippets, figures, tables, and artifacts used by the training
  material;
- small training datasets and acquisition helpers where applicable;
- small workshop-specific example capabilities in `src/fasthep_workshop/`.

This repository does not own:

- the high-level project portal; that belongs in `fast-hep.github.io`;
- detailed package APIs or implementation documentation; those belong in the
  package repositories;
- cross-package source integration and editable development environments; those
  belong in `fasthep-dev`;
- realistic migration repositories such as `hinv`, which are analysis
  migrations rather than general tutorials.

## Important Locations

- `tutorials/` - incremental tutorial source workflows, READMEs, expected
  snippets, and retained training assets.
- `docs/` - Sphinx training documentation; many pages include tutorial README
  content.
- `examples/` - standalone examples and smoke-test workflows.
- `data/` and `tutorials/data/` - small local datasets and download manifests.
- `src/fasthep_workshop/registry.yaml` and
  `src/fasthep_workshop/profiles/registry.yaml` - workshop profile/registry
  entries.
- `src/fasthep_workshop/sources/`, `transforms/`, `sinks/`, and `hooks/` -
  small training implementations used by examples.
- `scripts/check_expected.sh` - compare one tutorial build with its expected
  outputs.
- `scripts/sync_expected.py` - sync curated outputs listed in
  `expected/manifest.yaml`.
- `scripts/ci/` - focused CI smoke helpers for selected examples.
- `tests/` and `tests/smoke/` - checks for tutorial structure, compileability,
  selected runtime behaviour, and expected-output tooling.
- `templates/analysis-repo/` - tutorial template material.

## Commands

Use the production Workshop environment from the repository root:

```bash
pixi install
pixi run format
pixi run lint
pixi run lint-fix
pixi run typecheck
pixi run test
pixi run test-smoke
pixi run build
pixi run check
pixi run ci
pixi run check-dist
pixi run -e docs docs
pixi run -e docs docs-clean
pixi run -e docs docs-serve
```

`test` runs `pytest -m 'not smoke'`; `test-smoke` runs smoke tests. `check`
runs `lint`, `typecheck`, and `test`. `ci` runs `check` and `build`. Build
before `check-dist` so `dist/*` exists. Documentation commands run in the
`docs` environment.

Run one tutorial in a standalone Workshop clone with released dependencies:

```bash
pixi run fasthep run tutorials/<tutorial>/workflow.yaml \
  --outdir build/tutorials/<tutorial>
```

When testing unreleased upstream package changes from the `fasthep-dev`
workspace, use the dev environment and the workspace-relative tutorial path:

```bash
pixi run -e dev fasthep run \
  workshop/tutorials/<tutorial>/workflow.yaml \
  --outdir build/tutorials/<tutorial>
```

Replace `<tutorial>` with paths such as
`02-transform-data/01-derived-columns` or
`03-summarise-data/04-cutflow-tables`. Add `--chunk-size`, `--partition`, or
other tutorial-specific options only when the tutorial documents them.

Download small CMS tutorial data when needed:

```bash
pixi run fasthep download tutorials/data/CMS/Zmumu/files.json --outdir data
```

Sync curated expected outputs only for the tutorial being updated:

```bash
pixi run python scripts/sync_expected.py tutorials/<tutorial> \
  --build build/tutorials/<tutorial>
```

## Tutorial Conventions

- Tutorials should be incremental, focused, reproducible, and readable from a
  clean clone after `pixi install`.
- Early tutorials should remain fast. Scaling tutorials may require substantial
  resources and should say so explicitly.
- Run only the tutorial being changed by default. Do not run the complete
  tutorial suite unless explicitly requested.
- If an upstream change may affect multiple tutorials, ask which additional
  tutorials should be run.
- Test unreleased upstream package changes through the `fasthep-dev` `dev`
  environment rather than modifying the production Workshop dependency set.
- Do not launch Dask, HTCondor, SLURM, GPU, or other infrastructure-dependent
  examples without confirming the required submit environment is available.
- Use small partitions and isolated output directories for development runs.
- Keep authored workflow YAML concise and avoid exposing compiler-generated
  detail.
- Use public package interfaces and avoid depending on implementation internals.
- Distinguish executable commands from illustrative or placeholder examples.

## Outputs and Assets

Routine workflow outputs belong under `build/` or a fresh temporary output
directory. Do not make unrelated generated output part of a change.

Curated training assets under `tutorials/**/expected/` are intentionally
retained documentation fixtures. Keep snippets, plots, and tables synchronized
with meaningful output changes, but do not regenerate unrelated tutorials.
`docs/conf.py` copies these expected assets into `docs/_static/_generated/`
during documentation builds; edit the tutorial expected assets, not generated
docs output.

## Testing Expectations

- Use `pixi run test` for routine non-smoke tests. These do not execute every
  tutorial end to end.
- Use focused tests when editing one area, for example
  `pixi run pytest tests/test_scale_execution_tutorials.py` or
  `pixi run pytest tests/smoke/test_sync_expected.py`.
- Smoke tests may run selected examples or tutorials and can require local data
  or a fully assembled FAST-HEP environment.
- Do not start full distributed or infrastructure-backed tutorials unless the
  user explicitly asks and the required environment is confirmed.

## Generated Files and Care Areas

- `src/fasthep_workshop/_version.py` is generated by Hatch/Hatch-VCS. Do not
  edit it by hand; keep `src/fasthep_workshop/_version.pyi` aligned with
  imports.
- Build outputs, docs builds, distribution artifacts, downloaded data, and
  temporary runtime diagnostics are generated products unless they are curated
  expected tutorial assets.

## Documentation and Changelog

User-facing changes — new features, behavior changes, bug fixes, breaking changes — must add an
entry to `CHANGELOG.md` under `## [Unreleased]`, in the matching [Keep a
Changelog](https://keepachangelog.com/en/1.1.0/) category (Added, Changed, Deprecated, Removed,
Fixed, Security). Changes that affect public APIs, CLI behaviour, or user-facing workflows should
also update the relevant page under `docs/`.
