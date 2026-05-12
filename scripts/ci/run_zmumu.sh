#!/usr/bin/env bash
set -euo pipefail

outdir="${1:-build/Zmumu}"
fasthep compile examples/CMS/Zmumu/author.yaml --outdir "${outdir}"

test -f "${outdir}/normalized.yaml"
test -f "${outdir}/plan.yaml"
test -f "${outdir}/graph.mmd"
test -f "${outdir}/graph.dot"
