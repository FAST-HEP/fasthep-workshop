# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). This project uses
calendar versioning (`YYYY.MM.N`) rather than semantic versioning.

Release sections are generated from the commit messages (`git-cliff`, rules in
[FAST-HEP/.github](https://github.com/FAST-HEP/.github/blob/main/docs/commit-convention.md)) when a
release is prepared. Do not edit them by hand, and do not add entries under `## [Unreleased]`: it
stays empty.

## [Unreleased]

## [2026.11.1] - 2026-11-02

### Changed

- `examples/CMS/Zmumu` selects its hook profiles explicitly (`registry`, each package's `registry`, and
  curator's `default_context` and `runtime_diagnostics`) instead of the `hep_debug` profile.
- FAST-HEP dependencies are pinned to the 2026.11.1 release set: exactly (`==`) in `pixi.toml`, the released
  environment, and as floors (`>=`) in `pyproject.toml`, so an editable development checkout keeps resolving
  after a dependency's next commit. `fasthep-curator` stays at 2026.10.1 (no changes since).
- The pixi environments cap Python below 3.15: `xrootd` has no wheel for it and failed to build from source.

### Fixed

- `examples/LZ/mssi` no longer lists `SS_skim_U238-late_AnodeGridWires.root`, which is not in its download
  manifest (`remote_data.json`).

## [2026.10.1] - 2026-10-26

### Added

- Scale-execution tutorials: the Dask-on-HTCondor tutorial updated with environment packing, a new
  draft `07-scale-execution` section, and a `fasthep-distributed` tutorial dependency to support
  them.
- `variation-matrix-inline` systematics tutorial, with documentation of independent variation
  graphs.
- Mermaid diagram support in the documentation build (extension and styles).

### Changed

- Documentation type-checking now targets Python 3.12.

### Fixed

- Documentation headings now consistently start at H1.
- Missing documentation files and cross-references added.

## [2026.08.2] - 2026-08-25

### Added

- `99-extras/partitioned-root-skim` tutorial demonstrating artifacts at partition boundaries.
