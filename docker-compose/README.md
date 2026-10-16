# Docker-compose based Flask web application

## Introduction

Containers often have dependencies on other containers. For this purpose, docker-compose acts as a container orchestrator.

The docker-compose file in this directory specifies two services. Each service refers to a docker image. When run, docker containers are created and linked using docker networking so that the events-app can communicate with the PostgreSQL database.

## Usage

The basic syntax is:

```sh
docker compose -f docker/docker-compose.yaml up -d
```

Access the application at http://localhost:5000.

## Tests

To run the tests:

```sh
docker compose -f docker-compose-test.yaml up --abort-on-container-exit --exit-code-from app
```

If the tests fail, you should see:

```sh
app-1  | ============================= test session starts ==============================
app-1  | platform linux -- Python 3.10.21, pytest-9.1.1, pluggy-1.6.0
app-1  | rootdir: /app
app-1  | collected 3 items
app-1  | 
app-1  | tests/test_event_db.py .F.                                               [100%]
app-1  | 
app-1  | =================================== FAILURES ===================================
app-1  | __________________________________ test_false __________________________________
app-1  | 
app-1  |     def test_false():
app-1  | >       assert False
app-1  | E       assert False
app-1  | 
app-1  | tests/test_event_db.py:33: AssertionError
app-1  | =========================== short test summary info ============================
app-1  | FAILED tests/test_event_db.py::test_false - assert False
app-1  | ========================= 1 failed, 2 passed in 0.48s ==========================
app-1 exited with code 1
Aborting on container exit...
Container docker-compose-app-1 Stopping 
Container docker-compose-app-1 Stopped 
Container docker-compose-db-1 Stopping 
db-1   | 2026-09-04 16:58:43.159 UTC [1] LOG:  received fast shutdown request
db-1   | 2026-09-04 16:58:43.159 UTC [1] LOG:  aborting any active transactions
db-1   | 2026-09-04 16:58:43.161 UTC [1] LOG:  background worker "logical replication launcher" (PID 33) exited with exit code 1
db-1   | 2026-09-04 16:58:43.161 UTC [28] LOG:  shutting down
db-1   | 2026-09-04 16:58:43.170 UTC [1] LOG:  database system is shut down
Container docker-compose-db-1 Stopped 
db-1 exited with code 0
```

Docker compose files 2-4 were created for deployment to servers using either the bash script or Jenkins pipeline.

The *docker-compose5.yaml* script was created after notification was introduced in the code. Because it specifies DATABASE_URI (which we were doing earlier), the app will use the db service. The volume has been fixed to point to the correct location.

The *docker-compose-test2.yaml* script and beyond relies on docker registry. See [here](../docker-registry/README.md#private_registry). 

Next build the test image. See [here](../docker/README.md#building_test_container).

To run *docker-compose-test-4.yaml*:

```sh
PRIVATE_REGISTRY_SERVER=localhost \
PRIVATE_REGISTRY_PORT=3000 \
PRIVATE_REPOSITORY=events-app-test \
IMAGE_TAG=latest \
docker compose -f docker-compose-test4.yaml up \
--abort-on-container-exit --exit-code-from app
```

## Notes

There are two services in the docker-compose file. The first service is the Postgres database. The second sevice runs the Flask application. Since the database needs to have the correct schema, this can take a while before it is available for use. To handle this suituation, the docker-compose file defines both a dependency asnd a healthcheck; this pattern is discussed at https://docs.docker.com/compose/how-tos/startup-order/. Furthermore, the Flask application service defines the POSTGRES_URL so that it can connect to the external database.

