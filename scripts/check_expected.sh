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

echo "Running tutorial..."
pixi run fasthep run "${author}" --outdir "${build_dir}"

echo
echo "Comparing outputs..."

diff_found=0

while IFS= read -r expected_file; do
    rel="${expected_file#${expected_dir}/}"
    build_file="${build_dir}/${rel}"

    if [[ ! -f "${build_file}" ]]; then
        echo "Missing build output:"
        echo "  ${rel}"
        diff_found=1
        continue
    fi

    if ! cmp -s "${expected_file}" "${build_file}"; then
        echo "Different output:"
        echo "  ${rel}"
        diff_found=1
    else
        echo "OK:"
        echo "  ${rel}"
    fi

done < <(find "${expected_dir}" -type f ! -name ".gitkeep" | sort)

echo

if [[ "${diff_found}" -ne 0 ]]; then
    echo "Tutorial output check FAILED"
    exit 1
fi

echo "Tutorial output check PASSED"