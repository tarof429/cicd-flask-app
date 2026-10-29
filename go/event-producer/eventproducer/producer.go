package eventproducer

import (
	"context"
	"log"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
)

type EventProducer struct {
	Prefs Preferences
}

func (n *EventProducer) FailOnError(err error, msg string) {
	if err != nil {
		log.Panicf("%s: %s", msg, err)
	}
}

func (n *EventProducer) SendToQueue(ch *amqp.Channel, queueName string, msg string) error {

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
		log.Printf("Failed to declare a queue: %v", err.Error())
		//n.FailOnError(err, "Failed to declare a queue")
		return err
	}

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

	if err != nil {
		//n.FailOnError(err, "Failed to publish a message")
		log.Printf("Failed to publish a message: %v\n", err.Error())
		return err

	}
	log.Printf(" [x] Sent %s\n", body)

	return nil
}
