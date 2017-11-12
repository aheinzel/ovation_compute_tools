#!/bin/bash

set -o pipefail

if [ $# -ne 1 ]
then
    echo "USAGE: ${1} activity_download_folder" >&2
    exit 255
fi

FOLDER="${1}"
FN_LOG="${FOLDER}/execution.log"
FN_CONTAINER=$(find "${FOLDER}/related" -name "*.simg" | head -1)

echo "Using container: $(basename "${FN_CONTAINER}")"
singularity run --bind "${FOLDER}:/data" "${FN_CONTAINER}" 2>&1 | head -10000
STATUS=$?
echo "Exit status: ${STATUS}"

exit ${STATUS}
