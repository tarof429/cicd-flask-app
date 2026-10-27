package main

import (
	eventconsumer "event-consumer/eventconsumer"
	"log"
	"os"
	"strconv"

	amqp "github.com/rabbitmq/amqp091-go"
	"gopkg.in/yaml.v3"
)

func main() {
	var user = os.Getenv("AMPQ_USER")
	var password = os.Getenv("AMPQ_PASSWORD")
	var host = os.Getenv("AMPQ_HOST")
	var port = os.Getenv("AMPQ_PORT")
	var vhost = os.Getenv("AMPQ_VHOST")
	var prefsFile = os.Getenv("PREFERENCES_CONFIG")

	consumer := eventconsumer.EventConsumer{}
	err := consumer.Load(prefsFile)

	if err != nil {
		log.Printf("Failed to load preferences")
	}
	notificationDelay, err := strconv.Atoi(consumer.Prefs.NotificationDelay)
	from := consumer.Prefs.FromEmail
	to := consumer.Prefs.ToEmail

	if err != nil {
		consumer.FailOnError(err, "Invalid notificationDelay value")
	}

	log.Printf("NotificationDelay: %v\n", notificationDelay)
	log.Printf("From: %v\n", from)
	log.Printf("To: %v\n", to)

	url := "amqp://" + user + ":" + password + "@" + host + ":" + port + "/" + vhost
	conn, err := amqp.Dial(url)

	consumer.FailOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	consumer.FailOnError(err, "Failed to open a channel")
	defer ch.Close()

	event_confirmation_chan, err := consumer.ReceiveFromQueue(ch, "event_confirmation")

	if err != nil {
		consumer.FailOnError(err, "Failed to receive from queue")
	}

	confirmation_prefs_chan, err := consumer.ReceiveFromQueue(ch, "confirmation_prefs")

	if err != nil {
		consumer.FailOnError(err, "Failed to receive from queue")
	}

	go func() {
		for d := range event_confirmation_chan {
			log.Printf("Received a confirmation message: (%s)", d.Body)
			consumer.SendNotification(string(d.Body))
		}
	}()

	go func() {
		for d := range confirmation_prefs_chan {
			log.Printf("Received prefs message: (%s)", d.Body)

			// Modify preferences
			err := yaml.Unmarshal(d.Body, &consumer.Prefs)

			if err != nil {
				log.Printf("Unable to parse message: %v\n", err.Error())
			}
		}
	}()

	log.Printf(" [*] Waiting for messages. To exit press CTRL+C")
	for {
	}
}
