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

The *docker-compose7.yaml* script enables more customization of credentials. It was created in conjunction with *Jenkinsfile-18*.

The *docker-compose-local.yaml* script provides local deployment. You can run it like:

```sh
 docker compose --env-file ./cicd-credentials.sh  -f docker-compose-local.yaml up -d
```

Where cicd-credentals.sh may look something like this:

```sh
RUNTIME_MODE=dev
DB_USER=admin
DB_PASS=verysecret
DB_HOST=db
DB_NAME=mydb
```

## Testing

The *docker-compose-test.yaml* script is the earliest script used for testing. The application itself only integrated with a database.

The *docker-compose-test2.yaml* script and beyond relies on docker registry to be running. See [here](../docker-registry/README.md#private_registry). 

Early attempts to run the tests required a test image to be built and a separate docker compose file to mount a volume for the test results.

To run the tests with docker compose, override the entrypoint with *python*, specify the *app* service, and pass *-m pytest* as arguments to that service. This will override the normal behavior which is to run the application.

```sh
PRIVATE_REGISTRY_SERVER=localhost \
PRIVATE_REGISTRY_PORT=3000 \
PRIVATE_EVENT_APP_REPOSITORY=events-app \
IMAGE_TAG=latest \
docker compose run --rm --entrypoint python app  -m pytest
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
<?xml version="1.0" ?>
<testsuites name="pytest tests">
	<testsuite name="pytest" errors="0" failures="0" skipped="0" tests="13" time="1.748" timestamp="2026-11-24T19:43:11.428519+00:00" hostname="2ad8d357138f">
		<testcase classname="tests.integration.test_publish" name="test_publish_to_rabbitmq" time="0.126"/>
		<testcase classname="tests.test_auth" name="test_pasword_length" time="0.165"/>
		<testcase classname="tests.test_event_db" name="test_event_persistence" time="0.100"/>
		<testcase classname="tests.test_event_db" name="test_long_event_name_persistence" time="0.098"/>
		<testcase classname="tests.test_prefs" name="test_write_then_load_prefs" time="0.097"/>
		<testcase classname="tests.test_prefs" name="test_write_then_load_prefs2" time="0.096"/>
		<testcase classname="tests.test_prefs" name="test_load_prefs" time="0.096"/>
		<testcase classname="tests.test_prefs" name="test_load_write_load_write_load_prefs" time="0.096"/>
		<testcase classname="tests.test_web_ui" name="test_request_example" time="0.105"/>
		<testcase classname="tests.test_web_ui" name="test_list_events" time="0.107"/>
		<testcase classname="tests.test_web_ui" name="test_add_and_update_event" time="0.118"/>
		<testcase classname="tests.test_web_ui" name="test_login_as_admin" time="0.187"/>
		<testcase classname="tests.test_web_ui" name="test_test_admin_change_name" time="0.278"/>
	</testsuite>
</testsuites>
```
