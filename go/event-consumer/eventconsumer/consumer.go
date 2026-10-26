package eventconsumer

import (
	"log"
	"os"

	amqp "github.com/rabbitmq/amqp091-go"
	"gopkg.in/yaml.v3"
)

type EventConsumer struct {
	Prefs Preferences
}

func (n *EventConsumer) SetPrefs(prefs Preferences) {
	n.Prefs.NotificationDelay = prefs.NotificationDelay
	n.Prefs.Sysadminemail = prefs.Sysadminemail
}

func (n *EventConsumer) Load(prefsFile string) error {
	prefs := Preferences{
		Sysadminemail:     "",
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
	log.Printf("Sending notification: (%v) to %v", msg, n.Prefs.Sysadminemail)
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
