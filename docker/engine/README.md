# Docker-based Flask web application

## Introduction

Docker can be used to containerize applications so that they can run in any kind of environment that supports a container runtime.

## Usage

To build the image:

```sh
docker build -f docker/engine/Dockerfile -t events-app .
```

or build the image and tag it to push to the local docker registry:

```sh
docker build -f docker/engine/Dockerfile -t localhost:3000/events-app:latest .
```

To push the image to a local docker registry:

```sh
docker push localhost:3000/events-app:latest 
```

To run the container, run:

```sh
docker run --name events-app --rm -d -p 5000:5000 \
-e FLASK_APP=events_app \
-e MESSAGE_BROKER_TYPE=none events-app
```

Rabbitmq integration is best done using docker compose. 

Access the application at http://localhost:5000.

To push the image to docker registry (for example):

```sh
docker tag  events-app:latest tarof429/events-app:latest
docker push tarof429/events-app:latest
```

## [Running tests](#running_tests)

Unit tests (pytests) can be run inside of a container. This strategy provides an environment neutral way of running unit tests. Tests can be run by overriding the entrypoint and providing arguments to the cotainer.

To run the tests, run the following.

```sh
$ docker run  --entrypoint python --name events-app --rm \
-e FLASK_APP=events_app -e MESSAGE_BROKER=none events-app \
-m pytest --ignore="tests/integration"
============================= test session starts ==============================
platform linux -- Python 3.15.2, pytest-9.2.0, pluggy-1.6.0
rootdir: /app
plugins: metadata-3.1.1, html-4.2.0
collected 12 items

tests/test_auth.py .                                                     [  8%]
tests/test_event_db.py ..                                                [ 25%]
tests/test_prefs.py ....                                                 [ 58%]
tests/test_web_ui.py .....                                               [100%]

============================== 12 passed in 1.43s ==============================
```

See the readme for docker compose.