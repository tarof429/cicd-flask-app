# Event Consumer

## Introduction

The event consumer gets messages from the queue.

## Usage

To build:

```sh
make
```

To run the event consumer:

```sh
AMPQ_USER=user AMPQ_PASSWORD=password \
   AMPQ_HOST=localhost AMPQ_PORT=5672 \
   AMPQ_VHOST=rabbitmq PREFERENCES_CONFIG=preferences.yaml ./event-consumer 
 ```

If the Flask application is run using docker compose, then the event notifier should be run as another service so that they can communicate with each other over the docker network.

When run as a service, it can be useful to see the log messages from the container:

```sh
$ docker logs  -f admin-eventconsumer-1 
2026/10/22 05:43:59  [*] Waiting for messages. To exit press CTRL+C
2026/10/22 05:46:10 Received a message: (Added new event: Celebrate events!!)
2026/10/22 05:46:10 Sending notification: (Added new event: Celebrate events!!)
```