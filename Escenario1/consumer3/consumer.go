// consumer3/consumer.go
package main

import (
	"fmt"
	"log"
	"os"

	amqp "github.com/rabbitmq/amqp091-go"
)

func getenv(k, d string) string {
	if v := os.Getenv(k); v != "" { return v }
	return d
}

func main() {
	host := getenv("RABBIT_HOST", "rabbitmq")
	user := getenv("RABBIT_USER", "guest")
	pass := getenv("RABBIT_PASS", "guest")
	url := fmt.Sprintf("amqp://%s:%s@%s:5672/", user, pass, host)

	conn, err := amqp.Dial(url)
	if err != nil { log.Fatalf("dial: %v", err) }
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil { log.Fatalf("chan: %v", err) }
	defer ch.Close()

	ex := "demo_exchange"
	if err := ch.ExchangeDeclare(ex, "fanout", true, false, false, false, nil); err != nil {
		log.Fatalf("exchange declare: %v", err)
	}

	q, err := ch.QueueDeclare("", false, true, true, false, nil) // name="", exclusive -> cola anónima
	if err != nil { log.Fatalf("queue declare: %v", err) }

	if err := ch.QueueBind(q.Name, "", ex, false, nil); err != nil {
		log.Fatalf("queue bind: %v", err)
	}

	msgs, err := ch.Consume(q.Name, "", true, true, false, false, nil)
	if err != nil { log.Fatalf("consume: %v", err) }

	fmt.Println("Go Consumer esperando mensajes...")
	for m := range msgs {
		fmt.Println("[Go] Mensaje recibido:", string(m.Body))
	}
}
