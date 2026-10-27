package eventconsumer

import (
	"log"
	"os"
	"strconv"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
	"gopkg.in/yaml.v3"
)

type EventConsumer struct {
	Prefs Preferences
}

func (n EventConsumer) FailOnError(err error, msg string) {
	if err != nil {
		log.Panicf("%s: %s", msg, err)
	}
}

func (n *EventConsumer) SetPrefs(prefs Preferences) {
	n.Prefs.NotificationDelay = prefs.NotificationDelay
	n.Prefs.FromEmail = prefs.FromEmail
	n.Prefs.ToEmail = prefs.ToEmail
}

func (n *EventConsumer) Load(prefsFile string) error {
	prefs := Preferences{
		FromEmail:         "",
		ToEmail:           "",
		NotificationDelay: "0",
	}

	f, err := os.ReadFile(prefsFile)
	if err != nil {
		log.Println("No preferences file found")
		return err
	} else {
		if err := yaml.Unmarshal(f, &prefs); err != nil {
			log.Println("Unmarshal failed")
			return err
		} else {
			log.Println("Successfully unmarshalled preferences")
			n.Prefs = prefs
			return nil
		}
	}
}

func (n EventConsumer) SendNotification(msg string) {
	i, err := strconv.Atoi(n.Prefs.NotificationDelay)

	if err != nil {
		log.Printf("Unable to parse %v\n", i)
	}
	log.Printf("Sleeping for %v seconds", i)
	time.Sleep(time.Second * time.Duration(i))
	log.Printf("Sending notification with subject: (%v) from: %v to: %v\n",
		msg, n.Prefs.FromEmail, n.Prefs.ToEmail)
}

func (n EventConsumer) ReceiveFromQueue(ch *amqp.Channel, queueName string) (<-chan amqp.Delivery, error) {

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
