# Docker-based Flask web application

## Introduction

Docker can be used to containerize applications so that they can run in any kind of environment that supports a container runtime.

## Usage

To build the image:

```sh
docker build -f docker/Dockerfile4 -t events-app .
```

or build the image and tag it to push to the local docker registry:

```sh
docker build -f docker/Dockerfile4 -t localhost:3000/events-app:latest .
```

To push the image to a local docker registry:

```sh
docker push localhost:3000/events-app:latest 
```

To run the container without rabbitmq:

```sh
docker run --name events-app --rm -d -p 5000:5000 -e FLASK_APP=events_app -e MESSAGE_BROKER_TYPE=none events-app
```

The only way to integrate the app with rabbitmq is to use docker compose.

Access the application at http://localhost:5000.

To push it to docker registry (for example):

```sh
docker tag  events-app:latest tarof429/events-app:latest
docker push tarof429/events-app:latest
```

## [Building test container](#building_test_container)

Unit tests (pytests) can be run inside of a container. This strategy provides an environment neutral way of running unit tests.

Before building this container, build the main container.

Next, build the test image; this Dockerfile points to `entrypoint_test.sh` which runs the tests. For example:

```sh
docker build -f docker/Dockerfile.test4 -t events-app-test .
```

If we run the tests, we'lll see:

```sh
$ docker run --name events-app-test --rm events-app-test --ignore="tests/integration"
============================= test session starts ==============================
platform linux -- Python 3.11.18, pytest-9.1.1, pluggy-1.6.0
rootdir: /app
plugins: metadata-3.1.1, html-4.2.0
collected 9 items

tests/test_event_db.py ..                                                [ 22%]
tests/test_prefs.py ....                                                 [ 66%]
tests/test_web_ui.py ...                                                 [100%]

----------------- generated xml file: /app/reports/result.xml ------------------
============================== 9 passed in 0.24s ===============================
```

If we want to push image to the local registry:

```sh
docker build -f docker/Dockerfile.test4 -t localhost:3000/events-app-test:latest .
```

To push the image:

```sh
docker push localhost:3000/events-app-test:latest
```