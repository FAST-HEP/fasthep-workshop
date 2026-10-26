# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). This project uses
calendar versioning (`YYYY.MM.N`) rather than semantic versioning.

Add new entries under `## [Unreleased]`, in the category they belong to. At release time, rename
`## [Unreleased]` to `## [<version>] - <YYYY-MM-DD>` and start a fresh `## [Unreleased]` above it.

## [Unreleased]

### Added

- Scale-execution tutorials: the Dask-on-HTCondor tutorial updated with environment packing, a new
  draft `07-scale-execution` section, and a `fasthep-distributed` tutorial dependency to support
  them.
- `variation-matrix-inline` systematics tutorial, with documentation of independent variation
  graphs.
- Mermaid diagram support in the documentation build (extension and styles).

### Changed

- Documentation type-checking now targets Python 3.12.

### Deprecated

### Removed

### Fixed

- Documentation headings now consistently start at H1.
- Missing documentation files and cross-references added.

### Security

## [2026.08.2] - 2026-08-25

### Added

- `99-extras/partitioned-root-skim` tutorial demonstrating artifacts at partition boundaries.
