#!/bin/bash

DEPLOYMENT_SERVER="192.168.1.30"
DEPLOYMENT_USER="admin"

# Get the latest remote tracking information
git fetch

# Check if our local repository is behind upstream
#UPSTREAM_CHANGES=$(git rev-list --count HEAD..origin/main)
UPSTREAM_CHANGES=1

if [[ "$UPSTREAM_CHANGES" != "1" ]]; then
    exit 0
fi

git pull

COMMIT_HASH=$(git rev-parse --short HEAD)

echo "Building image..."
(cd ../; docker build -f docker/Dockerfile -t events-app .)
docker tag events-app tarof429/events-app:${COMMIT_HASH}
docker push tarof429/events-app:${COMMIT_HASH}

scp ../docker-compose/docker-compose3.yaml ${DEPLOYMENT_USER}@${DEPLOYMENT_SERVER}:docker-compose.yaml
scp deployment2.sh ${DEPLOYMENT_USER}@${DEPLOYMENT_SERVER}:deployment.sh
ssh ${DEPLOYMENT_USER}@${DEPLOYMENT_SERVER} chmod +x deployment.sh
ssh ${DEPLOYMENT_USER}@${DEPLOYMENT_SERVER} COMMIT_HASH=${COMMIT_HASH} ./deployment.sh
