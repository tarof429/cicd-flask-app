package main

import (
	"event-producer/eventproducer"
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

	eventproducer := eventproducer.EventProducer{}

	url := "amqp://" + user + ":" + password + "@" + host + ":" + port + "/" + vhost

	conn, err := amqp.Dial(url)
	eventproducer.FailOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	eventproducer.FailOnError(err, "Failed to open a channel")
	defer ch.Close()

	func() {
		// prefs := eventproducer.Preferences{
		// 	Sysadminemail:     "admin@foo.com",
		// 	NotificationDelay: "10",
		// }

		for {
			//err2 := sendToQueue(ch, "event_confirmation", fmt.Sprintf("%q", prefs))

			err2 := eventproducer.SendToQueue(ch, "event_confirmation", "Added new event: test")
			if err2 != nil {
				eventproducer.FailOnError(err2, "Failed to send message")
			}
			time.Sleep(5 * time.Second)

		}
	}()
}
