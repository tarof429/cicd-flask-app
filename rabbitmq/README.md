# RabbitMQ

RabbitMQ is a message broker. We use it to store notification such as creating new events.

To see events in RabbitMQ, point your browser to server host with the default port 15672.

Below is a screenshot of RabbitMQ with a message.

<img src="images/rabbit_mq_message.png"/>

For development, it can be handy to run rabbitmq in a docker container while running the Flask app outside of a container.


```sh
docker run -d --name rabbitmq --rm -p 15672:15672 -p 5672:5672  -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password -e RABBITMQ_DEFAULT_VHOST=rabbitmq rabbitmq:4.3.6-management-alpine
```