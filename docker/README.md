# Docker-based Flask web application

## Introduction

Docker can be used to containerize applications so that they can run in any kind of environment that supports a container runtime.

## Usage

To build the image:

```sh
docker build -f docker/Dockerfile3 -t events-app .
```

or build the image and tag it to push to the local docker registry:

```sh
docker build -f docker/Dockerfile3 -t localhost:3000/events-app:latest .
```

To push the image to a local docker registry:

```sh
docker push localhost:3000/events-app:latest 
```

To run the container:

```sh
docker run --name events-app --rm -d -p 5000:5000 events-app
```

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
docker build -f docker/Dockerfile.test3 -t events-app-test .
```

If we run it with a failing tests, we'lll see:

```sh
$ docker run --name events-app-test --rm events-app-test
============================= test session starts ==============================
platform linux -- Python 3.10.21, pytest-9.1.1, pluggy-1.6.0
rootdir: /app
collected 3 items

tests/test_event_db.py .F.                                               [100%]

=================================== FAILURES ===================================
__________________________________ test_false __________________________________

    def test_false():
>       assert False
E       assert False

tests/test_event_db.py:33: AssertionError
=========================== short test summary info ============================
FAILED tests/test_event_db.py::test_false - assert False
========================= 1 failed, 2 passed in 0.50s ==
```

Or if we want to push to the local registry:

```sh
docker build -f docker/Dockerfile.test3 -t localhost:3000/events-app-test:latest .
```

To push the image:

```sh
docker push localhost:3000/events-app-test:latest
```