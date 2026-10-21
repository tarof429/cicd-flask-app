# Community Calendar App

## Introduction

This is the Flask web application for creating and managing events. The tech stack includes:

- Flask
- Models
- Factories
- Templates
- Forms
- Configurations
- Migrations
- Tests

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

To run the application (whith no message broker):

```sh
MESSAGE_BROKER_TYPE=none flask run
```

Use the following command if you need to runthe application and access the application from another host:

```sh
MESSAGE_BROKER_TYPE=none flask run --host=0.0.0.0
```

To access the application, point your browser to:

```sh
http://localhost:5000
```

To run the application with an external rabbitmq (for example, rabbitmq running in a container):

```sh
MESSAGE_BROKER_TYPE=rabbitmq RABBITMQ_USER=user RABBITMQ_PASS=password RABBITMQ_HOST=localhost RABBITMQ_VHOST=rabbitmq flask run --host=0.0.0.0
 ```

If the application is configured to send messages to rabbitmq, then after adding an event, the following will show up in the log:

```sh
[2026-10-21 21:01:27,103] INFO in app: Publishing message for event: Go walking
```

To run non-integration tests:

```sh
python -m pytest --ignore **/integration
```

To run all the tests (rabbitmq must be running):

```sh
MESSAGE_BROKER_TYPE=rabbitmq RABBITMQ_USER=user RABBITMQ_PASS=password RABBITMQ_HOST=localhost RABBITMQ_VHOST=rabbitmq python -m pytest
```



