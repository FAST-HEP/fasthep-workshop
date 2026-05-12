#!/usr/bin/env bash
set -euo pipefail

outdir="${1:-build/L1Trigger}"
fasthep compile examples/CMS/L1Trigger/author.yaml --outdir "${outdir}"

test -f "${outdir}/normalized.yaml"
test -f "${outdir}/plan.yaml"
test -f "${outdir}/graph.mmd"
test -f "${outdir}/graph.dot"
