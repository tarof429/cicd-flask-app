# Introduction

The *event-consumer* receives messages from on or more queues.

The *event-producer* is a test server that genrates messages and puts them into the queues.

## Usage

To build both projects, run:

```sh
make
```

The docker compose file is an easy way to run the event-consumer and event-producer. Below is output that shows messages sent and received.

```sh
eventproducer-1  | 2026/10/28 18:03:49  [x] Sent Added new event: Celebrate Birthday!
eventconsumer-1  | 2026/10/28 18:03:49 Received a confirmation message: (Added new event: Celebrate Birthday!)
eventconsumer-1  | 2026/10/28 18:03:49 Sleeping for 1 seconds
eventconsumer-1  | 2026/10/28 18:03:50 Sending notification with subject: (Added new event: Celebrate Birthday!) from: admin@foo.com to: guest@foo.com
eventproducer-1  | 2026/10/28 18:03:54  [x] Sent from: hero@foo.com
eventproducer-1  | to: guest@foo.com
eventproducer-1  | notificationDelay: "3"
eventproducer-1  | 
eventconsumer-1  | 2026/10/28 18:03:54 Received prefs message: (from: hero@foo.com
eventconsumer-1  | to: guest@foo.com
eventconsumer-1  | notificationDelay: "3"
eventconsumer-1  | )
eventproducer-1  | 2026/10/28 18:03:59  [x] Sent Added new event: Celebrate Holiday!
rabbitmq-1       | 2026-10-28 18:03:59.364108+00:00 [info] <0.1099.0> closing AMQP connection (172.22.0.5:42132 -> 172.22.0.3:5672, vhost: 'rabbitmq', user: 'user', duration: '10s')
eventconsumer-1  | 2026/10/28 18:03:59 Received a confirmation message: (Added new event: Celebrate Holiday!)
eventconsumer-1  | 2026/10/28 18:03:59 Sleeping for 3 seconds
eventproducer-1 exited with code 0
eventconsumer-1  | 2026/10/28 18:04:02 Sending notification with subject: (Added new event: Celebrate Holiday!) from: hero@foo.com to: guest@foo.com
```