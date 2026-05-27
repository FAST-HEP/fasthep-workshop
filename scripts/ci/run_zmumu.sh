#!/usr/bin/env bash
set -euo pipefail

outdir="${1:-build/Zmumu}"
fasthep compile examples/CMS/Zmumu/author.yaml --outdir "${outdir}"

test -f "${outdir}/compile/normalized.yaml"
test -f "${outdir}/compile/plan.yaml"
test -f "${outdir}/graph/graph.mmd"
test -f "${outdir}/graph/graph.dot"
