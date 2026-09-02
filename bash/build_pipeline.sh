#!/bin/bash

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
(cd ..; docker build -f docker/Dockerfile -t events-app .)

(cd ../docker-compose; docker compose down)

(cd ../docker-compose; docker compose up -d)

for i in {1..5}; do
    sleep 3
    curl http://localhost:5000 > /dev/null
    STATUS=$?

    if [[ "$STATUS" = "0" ]];  then
        break
    fi
done

if [[ "$STATUS" = "0" ]]; then
    echo "Application is running"
else
    echo "Application is down"
fi

exit $STATUS