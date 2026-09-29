#!/bin/bash

PRIVATE_REPOSITORY="events-app"
PRIVATE_REGISTRY_SERVER="192.168.1.133"
PRIVATE_REGISTRY_PORT="3000"

if [[ "$#" != "1" ]]; then
    echo "Usage: $0 <tag>"
    exit 1
fi

IMAGE_TAG="$1"

imageName="${PRIVATE_REGISTRY_SERVER}:${PRIVATE_REGISTRY_PORT}/${PRIVATE_REPOSITORY}:${IMAGE_TAG}"

#trivy image --exit-code 1 --severity HIGH,CRITICAL ${imageName}

trivy image --severity HIGH,CRITICAL ${imageName}
