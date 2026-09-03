#!/bin/bash

docker compose down

docker compose up -d

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