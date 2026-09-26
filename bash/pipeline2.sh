#!/bin/bash

set -o pipefail

PRIVATE_REGISTRY_SERVER="${PRIVATE_REGISTRY_SERVER:-192.168.1.133}"
PRIVATE_REGISTRY_PORT="${PRIVATE_REGISTRY_PORT:-3000}"
PRIVATE_REPOSITORY="${PRIVATE_REPOSITORY:-events-app}"
PUBLIC_REPOSITORY="${PUBLIC_REPOSITORY:-tarof429/events-app}"
DEPLOYMENT_SERVER="${DEPLOYMENT_SERVER:-192.168.1.30}"
DEPLOYMENT_USER="${DEPLOYMENT_USER:-admin}"

### Checkout ###
git pull

COMMIT_HASH=$(git rev-parse --short HEAD)

echo "Commit hash: ${COMMIT_HASH}"

### Build ###
echo "Running tests..."
(cd ../;COMMIT_HASH=${COMMIT_HASH} docker build -f docker/Dockerfile.test2 \
    -t ${PRIVATE_REGISTRY_SERVER}:${PRIVATE_REGISTRY_PORT}/${PRIVATE_REPOSITORY}:${COMMIT_HASH} .)

(cd ../;COMMIT_HASH=${COMMIT_HASH} docker push \
    ${PRIVATE_REGISTRY_SERVER}:${PRIVATE_REGISTRY_PORT}/${PRIVATE_REPOSITORY}:${COMMIT_HASH})

### Test ###
(cd ../docker-compose;COMMIT_HASH=${COMMIT_HASH} PRIVATE_REGISTRY_SERVER=${PRIVATE_REGISTRY_SERVER} \
    PRIVATE_REGISTRY_PORT=${PRIVATE_REGISTRY_PORT} PRIVATE_REPOSITORY=${PRIVATE_REPOSITORY} \
    docker compose -f docker-compose-test3.yaml up --abort-on-container-exit --exit-code-from app)
TEST_STATUS=$?

mkdir -p test-reports

docker run -v test-reports:/source:ro alpine:latest 'cp /source/report.html test-reports/report.html'

if [[ $TEST_STATUS = "1" ]]; then
    echo "Tests failed"
    exit 1
fi
