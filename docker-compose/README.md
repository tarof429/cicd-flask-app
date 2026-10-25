# Docker-compose based Flask web application

## Introduction

Containers often have dependencies on other containers. For this purpose, docker-compose acts as a container orchestrator.

The docker-compose file in this directory specifies two services. Each service refers to a docker image. When run, docker containers are created and linked using docker networking so that the events-app can communicate with the PostgreSQL database.

## Usage

The basic syntax is:

```sh
docker compose -f docker/docker-compose.yaml up -d
```

Docker compose files 2-4 were created for deployment to servers using either the bash script or Jenkins pipeline.

The *docker-compose5.yaml* script was created after notification was introduced in the code. Because it specifies DATABASE_URI (which we were doing earlier), the app will use the db service. The volume has been fixed to point to the correct location.


The *docker-compose6.yaml* script integrates with the event-notifier.

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

The *docker-compose-test2.yaml* script and beyond relies on docker registry to be running. See [here](../docker-registry/README.md#private_registry). 

Next build the test image and push it to the docker registry. See [here](../docker/README.md#building_test_container).

To run *docker-compose-test-5.yaml*:

```sh
PRIVATE_REGISTRY_SERVER=localhost \
PRIVATE_REGISTRY_PORT=3000 \
PRIVATE_REPOSITORY=events-app-test \
PRIVATE_EVENT_APP_REPOSITORY=events-app-test \
IMAGE_TAG=latest \
docker compose -f docker-compose-test5.yaml up \
--abort-on-container-exit --exit-code-from app
```

Test results will be stored in a docker volume, which you can view by running:

```sh
docker run --rm -v test-reports:/source:ro python:latest \
  python -c 'import xml.dom.minidom, sys; print(xml.dom.minidom.parse("/source/result.xml").toprettyxml())'
```

If the tests pass, the result will look like this:

```sh
$ docker run --rm -v test-reports:/source:ro python:latest \
  python -c 'import xml.dom.minidom, sys; print(xml.dom.minidom.parse("/source/result.xml").toprettyxml())'
<?xml version="1.0" ?>ach
<testsuites name="pytest tests">
	<testsuite name="pytest" errors="0" failures="0" skipped="0" tests="6" time="0.182" timestamp="2026-10-20T04:43:11.332254+00:00" hostname="60315a82605c">
		<testcase classname="tests.integration.test_publish" name="test_publish_to_rabbitmq" time="0.029"/>
		<testcase classname="tests.test_event_db" name="test_event_persistence" time="0.014"/>
		<testcase classname="tests.test_event_db" name="test_long_event_name_persistence" time="0.012"/>
		<testcase classname="tests.test_web_ui" name="test_request_example" time="0.017"/>
		<testcase classname="tests.test_web_ui" name="test_list_events" time="0.016"/>
		<testcase classname="tests.test_web_ui" name="test_add_and_update_event" time="0.033"/>
	</testsuite>
</testsuites>
```
