#!/usr/bin/env bash
set -euo pipefail

fasthep run examples/testing/runtime-smoke/workflow.yaml --outdir build/testing/runtime-smoke

test -f build/testing/runtime-smoke/compile/normalized.yaml
test -f build/testing/runtime-smoke/compile/plan.yaml
test -f build/testing/runtime-smoke/run_summary.yaml
test -d build/testing/runtime-smoke/artifacts
