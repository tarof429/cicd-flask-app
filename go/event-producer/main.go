package main

import (
	"context"
	"log"
	"os"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
)

func failOnError(err error, msg string) {
	if err != nil {
		log.Panicf("%s: %s", msg, err)
	}
}

func sendToQueue(ch *amqp.Channel, queueName string, msg string) error {

	q, err := ch.QueueDeclare(
		queueName, // name
		true,      // durability
		false,     // delete when unused
		false,     // exclusive
		false,     // no-wait
		amqp.Table{
			amqp.QueueTypeArg: amqp.QueueTypeQuorum,
		},
	)
	failOnError(err, "Failed to declare a queue")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	body := msg
	err = ch.PublishWithContext(ctx,
		"",     // exchange
		q.Name, // routing key
		false,  // mandatory
		false,  // immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(body),
		})
	failOnError(err, "Failed to publish a message")
	log.Printf(" [x] Sent %s\n", body)

	return err
}

func main() {
	var user = os.Getenv("AMPQ_USER")
	var password = os.Getenv("AMPQ_PASSWORD")
	var host = os.Getenv("AMPQ_HOST")
	var port = os.Getenv("AMPQ_PORT")
	var vhost = os.Getenv("AMPQ_VHOST")

	url := "amqp://" + user + ":" + password + "@" + host + ":" + port + "/" + vhost

	conn, err := amqp.Dial(url)
	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	func() {
		// prefs := eventproducer.Preferences{
		// 	Sysadminemail:     "admin@foo.com",
		// 	NotificationDelay: "10",
		// }

		for {
			//err2 := sendToQueue(ch, "event_confirmation", fmt.Sprintf("%q", prefs))

			err2 := sendToQueue(ch, "event_confirmation", "Added new event: test")
			if err2 != nil {
				failOnError(err2, "Failed to send message")
			}
			time.Sleep(5 * time.Second)

		}
	}()
}
