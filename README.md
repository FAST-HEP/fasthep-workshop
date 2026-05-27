# fasthep-workshop

`fasthep-workshop` is the home for FAST-HEP tutorials, examples, regression workflows, public validation workflows, and the first lightweight analysis-repository template.

It is also a lightweight installable analysis-example package. Its import namespace is `fasthep_workshop`, and package-owned registry/profile resources demonstrate how an analysis repository can contribute custom components without relying on fragile `scripts.*` imports.

## Install

Basic workflow tools:

```bash
pip install fasthep-flow fasthep-cli
```

HEP analysis workflows:

```bash
pip install fasthep-flow fasthep-carpenter fasthep-curator fasthep-render fasthep-cli fasthep-workshop
```

Later this should become:

```bash
pip install "fasthep[hep]"
```

## Run Examples

Tutorial examples are intended for users and docs. Testing examples are internal
validation workflows for CI, smoke tests, and package integration checks.

Compile the Zmumu tutorial:

```bash
fasthep compile examples/CMS/Zmumu/author.yaml --outdir build/Zmumu
```

Run the CI-friendly runtime smoke workflow:

```bash
fasthep run examples/testing/runtime-smoke/author.yaml --outdir build/testing/runtime-smoke
```

Compile the generated-data ROOT split package validation workflow:

```bash
python scripts/ci/make_testing_data.py
fasthep compile examples/testing/split-packages/author.yaml --outdir build/testing/split-packages
```

Outputs appear under the selected `build/...` directory. Compiler products are written under `compile/`, graph files under `graph/`, and runtime artifacts under `artifacts/`.

## CI Role

These examples are intended as public golden-path validation workflows. Public CI should run parse/compile smoke checks and small runtime examples. CERN GitLab can add private-data and heavier validation workflows without making private data required here.
