# Community Calendar App

## Introduction

This is the Flask version of the community event calendar application.

<img src="images/events.png" />

## Initial Setup

This application uses a virtual environment using `pip`. Below is an example of how to create the virtual environment with a directory called venv.

```sh
python -m venv venv
```

To activate it, run:

```sh
. ./venv/bin/activate
```

To deactivate it, run

```sh
deactivate
```

## Creating the database

This Flask application uses migrations to initialize the database. Tables are created based on classes defined in `models.py`. Because both `models.py` and `app.py` need a reference to the same SQLAlchemy object, this object is instantiated within `models.py` (see the section on Factories and extensions at https://flask.palletsprojects.com/en/stable/patterns/appfactories/), 

To initialize the database:

```sh
flask db init
```

To create a migration:

```sh
flask db migrate -m "Initial"
```

Create the events table:

```sh
flask db upgrade
```

## Usage

To run the application:

```sh
flask run
```

To run tests:

```sh
python -m pytest
```

## Running in Docker

To build the image:

```sh
docker build -f docker/Dockerfile -t events-app .
```

To run the container:

```sh
docker run --name events-app --rm -d -p 5000:5000 events-app
```

## Docker Compose

The docker-compose file will use Postgres as the backing database.

```sh
docker compose -f docker/docker-compose.yaml up -d
```

There are two services in the docker-compose file. The first service is the Postgres database. The second sevice runs the Flask application. Since the database needs to have the correct schema, this can take a while before it is available for use. To handle this suituation, the docker-compose file defines both a dependency asnd a healthcheck; this pattern is discussed at https://docs.docker.com/compose/how-tos/startup-order/. Furthermore, the Flask application service defines the POSTGRES_URL so that it can connect to the external database.

