# Event Notifier

## Introduction

The event notifier gets messages from the event queue.

## Usage

To build:

```sh
make
```

To run the vent notifier:

```sh
AMPQ_USER=user AMPQ_PASSWORD=password \
   AMPQ_HOST=localhost AMPQ_PORT=5672 \
   AMPQ_VHOST=rabbitmq ./event-notifier 
 ```

To build the docker container:

```sh
docker build -t event-notifier .
```

To run the docker container:

```sh
docker run \
   --name event-notifier \
   --rm \
   -e AMPQ_USER=user \
   -e AMPQ_PASSWORD=password \
   -e AMPQ_HOST=localhost \
   -e AMPQ_PORT=5672 \
   -e AMPQ_VHOST=rabbitmq \
   event-notifier 
```