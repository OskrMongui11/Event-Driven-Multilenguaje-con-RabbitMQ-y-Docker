package main

import (
	"fmt"
	"log"
	"os"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
)

func main() {
	host := getenv("RABBIT_HOST", "rabbitmq")
	user := getenv("RABBIT_USER", "user")
	pass := getenv("RABBIT_PASS", "password")
	url := fmt.Sprintf("amqp://%s:%s@%s:5672/", user, pass, host)

	conn, err := amqp.Dial(url)
	if err != nil {
		log.Fatalf("No se pudo conectar: %v", err)
	}
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		log.Fatalf("Error al crear canal: %v", err)
	}
	defer ch.Close()

	exchange := "demo_exchange"
	ch.ExchangeDeclare(exchange, "fanout", true, false, false, false, nil)

	i := 1
	for {
		msg := fmt.Sprintf("Mensaje Go #%d", i)
		err = ch.Publish(exchange, "", false, false, amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(msg),
		})
		if err != nil {
			log.Printf("Error al enviar: %v", err)
		} else {
			log.Printf("[x] Enviado: %s", msg)
		}
		i++
		time.Sleep(3 * time.Second)
	}
}

func getenv(key, fallback string) string {
	val := os.Getenv(key)
	if val == "" {
		return fallback
	}
	return val
}
