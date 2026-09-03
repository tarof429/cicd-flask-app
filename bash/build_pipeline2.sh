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

echo "Building image..."
(cd ../; docker build -f docker/Dockerfile -t events-app .)
docker tag events-app tarof429/events-app:latest
docker push tarof429/events-app:latest

scp ../docker-compose/docker-compose2.yaml ${DEPLOYMENT_USER}@${DEPLOYMENT_SERVER}:docker-compose.yaml
scp deployment.sh ${DEPLOYMENT_USER}@${DEPLOYMENT_SERVER}:
ssh ${DEPLOYMENT_USER}@${DEPLOYMENT_SERVER} chmod +x deployment.sh
ssh ${DEPLOYMENT_USER}@${DEPLOYMENT_SERVER} ./deployment.sh
