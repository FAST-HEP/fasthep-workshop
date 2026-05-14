# fasthep-workshop

`fasthep-workshop` is the home for FAST-HEP tutorials, examples, regression workflows, public validation workflows, and the first lightweight analysis-repository template.

This repository is primarily content and validation material, not an implementation package. Examples should use public data or include fetch/generation instructions.

## Install

Basic workflow tools:

```bash
pip install fasthep-flow fasthep-cli
```

HEP analysis workflows:

```bash
pip install fasthep-flow fasthep-carpenter fasthep-curator fasthep-render fasthep-cli
```

Later this should become:

```bash
pip install "fasthep[hep]"
```

## Run Examples

Compile the Zmumu tutorial:

```bash
fasthep compile examples/CMS/Zmumu/author.yaml --outdir build/Zmumu
```

Run the CI-friendly runtime smoke tutorial:

```bash
fasthep run examples/tutorial/runtime-smoke/author.yaml --outdir build/tutorial/runtime-smoke
```

Compile the generated-data ROOT split package tutorial:

```bash
python scripts/ci/make_tutorial_data.py
fasthep compile examples/tutorial/split-packages/author.yaml --outdir build/tutorial/split-packages
```

Outputs appear under the selected `build/...` directory. Runtime artifacts are written under `artifacts/`.

## CI Role

These examples are intended as public golden-path validation workflows. Public CI should run parse/compile smoke checks and small runtime examples. CERN GitLab can add private-data and heavier validation workflows without making private data required here.
