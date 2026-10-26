package main

import (
	"event-producer/eventproducer"
	"fmt"
	"os"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
)

func main() {
	var user = os.Getenv("AMPQ_USER")
	var password = os.Getenv("AMPQ_PASSWORD")
	var host = os.Getenv("AMPQ_HOST")
	var port = os.Getenv("AMPQ_PORT")
	var vhost = os.Getenv("AMPQ_VHOST")

	producer := eventproducer.EventProducer{}

	url := "amqp://" + user + ":" + password + "@" + host + ":" + port + "/" + vhost

	conn, err := amqp.Dial(url)
	producer.FailOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	producer.FailOnError(err, "Failed to open a channel")
	defer ch.Close()

	for i := range 3 {
		err2 := producer.SendToQueue(ch, "event_confirmation", fmt.Sprintf("Added new event: test%v", i))
		if err2 != nil {
			producer.FailOnError(err2, "Failed to send message")
		}
	}

	time.Sleep(1 * time.Second)

	producer.Prefs = eventproducer.Preferences{
		NotificationDelay: "1",
		Sysadminemail:     "admin@foo.com",
	}

	delay := 0

	for i := range 3 {

		producer.Prefs = eventproducer.Preferences{
			Sysadminemail:     fmt.Sprintf("admin%v@foo.com", i),
			NotificationDelay: fmt.Sprintf("%v", delay),
		}

		err2 := producer.SendToQueue(ch, "confirmation_prefs", fmt.Sprintf("%q", producer.Prefs))

		if err2 != nil {
			producer.FailOnError(err2, "Failed to send message")
		}

		delay = delay + 1
	}

}
