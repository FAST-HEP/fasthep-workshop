# FAST-HEP Workshop

`fasthep-workshop` contains tutorials, examples, and complete analysis workflows for the FAST-HEP ecosystem.

The workshop is designed to help users learn the FAST-HEP workflow language step-by-step, from reading ROOT files to running distributed analyses on HTCondor or Slurm.

## Getting Started

Clone the repository:

```bash
git clone https://github.com/FAST-HEP/fasthep-workshop.git
cd fasthep-workshop
```

### Install Pixi (Recommended)

FAST-HEP tutorials use Pixi to provide reproducible environments.

Follow the Pixi installation instructions:

https://pixi.sh/latest/

Then create the environment:

```bash
pixi install
```

Run commands inside the environment:

```bash
pixi run fasthep --help
```

### Alternative: pip

If you prefer not to use Pixi, install the required FAST-HEP packages manually:

```bash
pip install \
  fasthep-flow \
  fasthep-carpenter \
  fasthep-curator \
  fasthep-render \
  fasthep-toolbench \
  fasthep-cli \
  fasthep-workshop
```

Please note that all instructions include `pixi run` - if you do not use pixi, please exclude this prefix to the commands.

## Repository Layout

```text
tutorials/
    Step-by-step learning material

examples/
    Standalone examples and demonstrations

data/
    Example datasets and download manifests

docs/
    Additional documentation
```

### Tutorials

The tutorials are organised as a learning path.

```text
00-overview/
    Introduction to FAST-HEP

01-read-data/
    Reading ROOT files and datasets

02-transform-data/
    Derived quantities and selections

03-summarise-data/
    Histograms and cutflows

04-save-data/
    Skims and outputs

05-systematics/
    Variations and uncertainties

06-organise-workflows/
    Profiles, registries, and modular workflows

07-scale-execution/
    Distributed execution and resource pools

08-accelerators/
    GPU execution

09-extend-fasthep/
    Custom operations and extensions

10-complete/
    End-to-end analysis examples
```

Start here:

```text
tutorials/00-overview/first-workflow/
```

## Running a Tutorial

Most tutorials contain a dedicated README with instructions.

For example:

```bash
pixi run fasthep compile tutorials/00-overview/first-workflow/workflow.yaml
```

or:

```bash
pixi run fasthep run tutorials/00-overview/first-workflow/workflow.yaml
```

See the tutorial README for expected outputs and explanations.

## Expected Tutorial Outputs

Expected tutorial outputs are documentation fixtures, not full build snapshots.
They are synced with per-tutorial `expected/manifest.yaml` files:

```bash
pixi run python scripts/sync_expected.py tutorials/03-summarise-data/04-cutflow-tables --build build/tutorials/03-summarise-data/04-cutflow-tables
```

Manifests copy only curated outputs such as plots, small tables, and compact
JSON snippets into `expected/`.

## Example Data

Several tutorials use small CMS datasets based on the classic Z → μμ analysis.

Download the tutorial files:

```bash
pixi run fasthep download tutorials/data/CMS/Zmumu/files.json --outdir data
```

The downloaded files are intentionally small so that tutorials can run on a laptop.

## Output Structure

FAST-HEP workflows write outputs into a build directory.

Typical contents include:

```text
build/
├── artifacts/
├── compile/
├── debug/
├── graph/
├── render/
└── reports/
```

* `compile/` – compiler outputs such as normalized workflows and execution plans
* `graph/` – workflow visualisations
* `render/` – rendering metadata
* `reports/` – structured reports and summaries
* `artifacts/` – user-facing outputs
* `debug/` – backend and runtime diagnostics

## Next Steps

After completing the introductory tutorials, explore:

* distributed execution with HTCondor or Slurm,
* heterogeneous CPU/GPU worker pools,
* skimming workflows,
* complete analysis examples.


> 📝 The long-term goal is to build fully reproducible public analysis records using FAST-HEP.
