#!/bin/bash
set -euo pipefail # enable strict mode
IFS=$'\n\t'

# Derive the application name from the current directory
APP=${PWD##*/}

DOCKER_UPLOAD_TOKEN="${1-}"
if [ -z $DOCKER_UPLOAD_TOKEN ]; then
    set +e
    DOCKER_UPLOAD_TOKEN=`git config skyliner.artifact-token`
    set -e
fi

if [ -z $DOCKER_UPLOAD_TOKEN ]; then
    echo ""
    echo "Usage: "
    echo "./upload.sh <docker upload token>"
    exit -1
fi

# Build the Docker image
docker build -t $APP .

# Save the image to a TAR file
docker save -o image.tar $APP

# Find the full git commit hash for the current commit
COMMIT=$(git rev-parse HEAD)
BUILD=$(git rev-parse --short HEAD)

# Ask Skyliner for the upload URL, authenticating with the upload token
URL=$(curl -s -u ":$DOCKER_UPLOAD_TOKEN" -X POST https://www.skyliner.io/images/docker/$COMMIT)

# Upload the Docker image to Skyliner
echo "Uploading $APP Docker image (build $BUILD) to Skyliner:"
curl --progress-bar --upload-file image.tar $URL > /dev/null
