package main

import (
	"log"
	"os"

	amqp "github.com/rabbitmq/amqp091-go"
	"gopkg.in/yaml.v3"
)

func failOnError(err error, msg string) {
	if err != nil {
		log.Panicf("%s: %s", msg, err)
	}
}

func sendNotification(msg string) {
	log.Printf("Sending notification: (%v)", msg)
}

type Preferences struct {
	sysadminemail     string `yaml:sysadminemail`
	notificationDelay string `yaml:notificationDelay`
}

func main() {
	var user = os.Getenv("AMPQ_USER")
	var password = os.Getenv("AMPQ_PASSWORD")
	var host = os.Getenv("AMPQ_HOST")
	var port = os.Getenv("AMPQ_PORT")
	var vhost = os.Getenv("AMPQ_VHOST")
	var prefsFile = os.Getenv("PREFERENCES_CONFIG")

	f, err := os.ReadFile(prefsFile)
	if err != nil {
		log.Fatal(err)
	}

	var prefs Preferences

	if err := yaml.Unmarshal(f, &prefs); err != nil {
		log.Fatal(err)
	}

	log.Printf("sysadminemail: %v¥n", prefs.sysadminemail)
	log.Printf("notificationdelay: %v¥n", prefs.notificationDelay)

	url := "amqp://" + user + ":" + password + "@" + host + ":" + port + "/" + vhost
	conn, err := amqp.Dial(url)

	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"event_confirmation", // name
		true,                 // durability
		false,                // delete when unused
		false,                // exclusive
		false,                // no-wait
		amqp.Table{
			amqp.QueueTypeArg: amqp.QueueTypeQuorum,
		},
	)
	failOnError(err, "Failed to declare a queue")

	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		true,   // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	failOnError(err, "Failed to register a consumer")

	var forever chan struct{}

	go func() {
		for d := range msgs {
			log.Printf("Received a message: (%s)", d.Body)
			sendNotification(string(d.Body))
		}
	}()

	log.Printf(" [*] Waiting for messages. To exit press CTRL+C")
	<-forever

}
