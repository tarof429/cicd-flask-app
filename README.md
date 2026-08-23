# Event Manager

## Introduction

This is a containerized Flask web application for creating and managing events.

<img src="images/events.png" />

## Architecture

A CI/CD Pipeline is used to create a container image containing the Flask web application. We use docker-compose to orchestrate the web container and the PostgreSQL container.
```mermaid
flowchart LR
    CI[CI/CD Pipeline] --> Image[Container Image]
    Image --> Compose[Docker Compose]
    Compose --> Flask[Flask Application]
    Compose --> DB[(PostgreSQL)]
```

## Technology Stack

- Python
- Flask
- SQLAlchemy
- PostgreSQL
- Docker
- Docker Compose
- Pytest
- Alembic/Flask-Migrate
- KVM
- Kickstart