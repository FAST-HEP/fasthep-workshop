#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage:"
    echo "  $0 beginner/first-workflow"
    echo "  $0 tutorials/beginner/first-workflow"
    exit 1
fi

tutorial="$1"

if [[ "$tutorial" != tutorials/* ]]; then
    tutorial="tutorials/${tutorial}"
fi

author="${tutorial}/author.yaml"
build_dir="${tutorial}/build"
expected_dir="${tutorial}/expected"

if [[ ! -f "${author}" ]]; then
    echo "Missing author.yaml:"
    echo "  ${author}"
    exit 1
fi

if [[ ! -d "${expected_dir}" ]]; then
    echo "Missing expected directory:"
    echo "  ${expected_dir}"
    exit 1
fi

echo "Cleaning build directory..."
rm -rf "${build_dir}"
mkdir -p "${build_dir}"
touch "${build_dir}/.gitkeep"

echo "Running tutorial..."
pixi run fasthep run "${author}" --outdir "${build_dir}"
touch "${build_dir}/.gitkeep"

if ! find "${expected_dir}" -mindepth 1 -print -quit | grep -q .; then
    touch "${expected_dir}/.gitkeep"
fi

echo
echo "Comparing outputs..."

exclude_args=(
    --exclude ".gitkeep"
    --exclude "debug/"
    --exclude "**/__pycache__/"
)

# debug/ is intentionally excluded because backend/runtime diagnostics can contain
# non-deterministic logs and performance files that are not tutorial goldens.
diff_output="$(
    rsync -rcn --delete --itemize-changes \
        "${exclude_args[@]}" \
        "${build_dir}/" \
        "${expected_dir}/"
)"

if [[ -n "${diff_output}" ]]; then
    echo "${diff_output}"
    echo
    echo "Tutorial output check FAILED"
    exit 1
fi

echo "Tutorial output check PASSED"
