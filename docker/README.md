# Docker-based Flask web application

## Introduction

Docker can be used to containerize applications so that they can run in any kind of environment that supports a container runtime.

## Usage

To build the image:

```sh
docker build -f docker/Dockerfile -t events-app .
```

To run the container:

```sh
docker run --name events-app --rm -d -p 5000:5000 events-app
```

Access the application at http://localhost:5000.