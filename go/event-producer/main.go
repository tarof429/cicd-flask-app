package main

import (
	"event-producer/eventproducer"
	"fmt"
	"log"
	"os"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
	yaml "gopkg.in/yaml.v3"
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

	// Send an event confirmation
	err = producer.SendToQueue(ch, "event_confirmation", "Added new event: Celebrate Birthday!")
	if err != nil {
		producer.FailOnError(err, "Failed to send message")
	}

	time.Sleep(5 * time.Second)

	// Change preferences and send it to the queue
	producer.Prefs = eventproducer.Preferences{
		Sysadminemail:     "hero@foo.com",
		NotificationDelay: fmt.Sprintf("%v", 3),
	}

	body, err := yaml.Marshal(producer.Prefs)

	if err != nil {
		log.Printf("Unable to encoce preferences")
	}

	err = producer.SendToQueue(ch, "confirmation_prefs", string(body))

	if err != nil {
		producer.FailOnError(err, "Failed to send message")
	}

	time.Sleep(5 * time.Second)

	// Send more event confirmations. The consumer should behave a little bit differently due
	// to the modified preferences.
	err = producer.SendToQueue(ch, "event_confirmation", "Added new event: Celebrate Holiday!")
	if err != nil {
		producer.FailOnError(err, "Failed to send message")
	}

}
