# Docker-compose based Flask web application

## Introduction

Containers often have dependencies on other containers and for this purpose docker-compose acts as a container orchestrator.

## Usage

```sh
docker compose -f docker/docker-compose.yaml up -d
```

Access the application at http://localhost:5000.

## Notes

There are two services in the docker-compose file. The first service is the Postgres database. The second sevice runs the Flask application. Since the database needs to have the correct schema, this can take a while before it is available for use. To handle this suituation, the docker-compose file defines both a dependency asnd a healthcheck; this pattern is discussed at https://docs.docker.com/compose/how-tos/startup-order/. Furthermore, the Flask application service defines the POSTGRES_URL so that it can connect to the external database.

