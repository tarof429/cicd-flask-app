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