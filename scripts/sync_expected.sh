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

build_dir="${tutorial}/build"
expected_dir="${tutorial}/expected"

if [[ ! -d "${build_dir}" ]]; then
    echo "Missing build directory: ${build_dir}" >&2
    exit 1
fi

mkdir -p "${expected_dir}"

find "${expected_dir}" -mindepth 1 -delete

rsync -a \
    --exclude ".gitkeep" \
    --exclude "debug/" \
    --exclude "**/__pycache__/" \
    "${build_dir}/" \
    "${expected_dir}/"

touch "${build_dir}/.gitkeep"
touch "${expected_dir}/.gitkeep"

echo "Synced:"
echo "  ${build_dir}/"
echo "to:"
echo "  ${expected_dir}/"
