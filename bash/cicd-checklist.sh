#!/bin/bash

# Checklist for runing CI/CD pipeline

PRIVATE_REGISTRY_SERVER="${PRIVATE_REGISTRY_SERVER:-167.71.119.175}"
DEPLOYMENT_SERVER="${DEPLOYMENT_SERVER:-167.172.114.181}"
PRIVATE_REGISTRY_PORT="${PRIVATE_REGISTRY_PORT:-3000}"

# Check user name
if [[ "$USER" != "admin" ]]; then
    echo "User is not admin":
    exit 1
fi

# Check that we're in a git repo
git pull

if [[ $? -ne 0 ]]; then
    echo "Not in a git repo"
    exit 1
fi

# Checking SSH to web server
ssh admin@${DEPLOYMENT_SERVER} echo

if [[ $? -ne 0 ]]; then
    echo "Not in a git repo"
    exit 1
fi

# Check our local docker registry
docker pull hello-world
docker tag hello-world ${PRIVATE_REGISTRY_SERVER}:${PRIVATE_REGISTRY_PORT}/hello-world
docker push ${PRIVATE_REGISTRY_SERVER}:${PRIVATE_REGISTRY_PORT}/hello-world

if [[ $? -ne 0 ]]; then
    echo "Docker push failed"
    exit 1
fi

echo "Done!"