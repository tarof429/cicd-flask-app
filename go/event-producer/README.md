# Event Producer

## Introduction

The event producer puts messages into the queue.

## Usage

To build:

```sh
make
```

To run the event producer:

```sh
AMPQ_USER=user AMPQ_PASSWORD=password \
   AMPQ_HOST=localhost AMPQ_PORT=5672 \
   AMPQ_VHOST=rabbitmq ./event-producer 
 ```