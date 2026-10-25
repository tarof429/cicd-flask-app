package main

import (
	"event-notifier/eventnotifier"
	"log"
	"os"
	"strconv"

	amqp "github.com/rabbitmq/amqp091-go"
)

func failOnError(err error, msg string) {
	if err != nil {
		log.Panicf("%s: %s", msg, err)
	}
}

func receiveFromQueue(ch *amqp.Channel, queueName string) (<-chan amqp.Delivery, error) {

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

	if err != nil {
		return nil, err
	}

	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		true,   // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)

	return msgs, err
}

func main() {
	var user = os.Getenv("AMPQ_USER")
	var password = os.Getenv("AMPQ_PASSWORD")
	var host = os.Getenv("AMPQ_HOST")
	var port = os.Getenv("AMPQ_PORT")
	var vhost = os.Getenv("AMPQ_VHOST")
	var prefsFile = os.Getenv("PREFERENCES_CONFIG")

	eventnotifier := eventnotifier.Notifier{}
	unmarshalled, err := eventnotifier.Load(prefsFile)

	if err != nil {
		log.Printf("Failed to load preferences")
	}

	var notificationDelay int
	var sysadminemail string

	if unmarshalled {
		notificationDelay, err := strconv.Atoi(eventnotifier.Prefs.NotificationDelay)
		sysadminemail = eventnotifier.Prefs.Sysadminemail

		if err != nil {
			failOnError(err, "Invalid notificationDelay value")
		}

		log.Printf("Delaying notification by %v seconds\n", notificationDelay)
	}

	log.Printf("NotificationDelay: %v\n", notificationDelay)
	log.Printf("Sysadminemail: %v\n", sysadminemail)

	url := "amqp://" + user + ":" + password + "@" + host + ":" + port + "/" + vhost
	conn, err := amqp.Dial(url)

	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	event_confirmation_msgs, err := receiveFromQueue(ch, "event_confirmation")

	if err != nil {
		failOnError(err, "Failed to receive from queue")
	}

	// q, err := ch.QueueDeclare(
	// 	"event_confirmation", // name
	// 	true,                 // durability
	// 	false,                // delete when unused
	// 	false,                // exclusive
	// 	false,                // no-wait
	// 	amqp.Table{
	// 		amqp.QueueTypeArg: amqp.QueueTypeQuorum,
	// 	},
	// )
	// failOnError(err, "Failed to declare event_confirmation queue")

	// msgs, err := ch.Consume(
	// 	q.Name, // queue
	// 	"",     // consumer
	// 	true,   // auto-ack
	// 	false,  // exclusive
	// 	false,  // no-local
	// 	false,  // no-wait
	// 	nil,    // args
	// )

	// failOnError(err, "Failed to register a consumer")

	var forever chan struct{}

	go func() {
		for d := range event_confirmation_msgs {
			log.Printf("Received a message: (%s)", d.Body)
			eventnotifier.SendNotification(string(d.Body))
		}
	}()

	log.Printf(" [*] Waiting for messages. To exit press CTRL+C")
	<-forever
}
