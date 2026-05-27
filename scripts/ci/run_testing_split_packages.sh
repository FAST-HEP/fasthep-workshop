#!/usr/bin/env bash
set -euo pipefail

python scripts/ci/make_testing_data.py
fasthep compile examples/testing/split-packages/author.yaml --outdir build/testing/split-packages

test -f build/testing/split-packages/compile/normalized.yaml
test -f build/testing/split-packages/compile/plan.yaml
