#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage:"
    echo "  $0 beginner/first-workflow"
    exit 1
fi

TUTORIAL_ROOT="tutorials/$1"

mkdir -p \
    "${TUTORIAL_ROOT}/assets" \
    "${TUTORIAL_ROOT}/build" \
    "${TUTORIAL_ROOT}/expected"

touch "${TUTORIAL_ROOT}/README.md"
touch "${TUTORIAL_ROOT}/author.yaml"
touch "${TUTORIAL_ROOT}/build/.gitkeep"

echo "Created tutorial scaffold:"
echo "  ${TUTORIAL_ROOT}"
