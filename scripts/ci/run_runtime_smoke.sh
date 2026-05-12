#!/usr/bin/env bash
set -euo pipefail

fasthep run examples/tutorial/runtime-smoke/author.yaml --outdir build/tutorial/runtime-smoke

test -f build/tutorial/runtime-smoke/normalized.yaml
test -f build/tutorial/runtime-smoke/plan.yaml
test -f build/tutorial/runtime-smoke/run_summary.yaml
test -d build/tutorial/runtime-smoke/artifacts
