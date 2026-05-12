#!/usr/bin/env bash
set -euo pipefail

python scripts/ci/make_tutorial_data.py
fasthep compile examples/tutorial/split-packages/author.yaml --outdir build/tutorial/split-packages

test -f build/tutorial/split-packages/normalized.yaml
test -f build/tutorial/split-packages/plan.yaml
