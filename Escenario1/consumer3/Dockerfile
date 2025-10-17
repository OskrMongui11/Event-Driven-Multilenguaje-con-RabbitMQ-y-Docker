# consumer3/Dockerfile -- basado en tu producer que funciona
FROM golang:1.22-alpine

WORKDIR /app
COPY go.mod ./
RUN go mod download

COPY . .

# asegura la dependencia del cliente RabbitMQ
RUN go get github.com/rabbitmq/amqp091-go@latest

# compila el binario llamado "consumer"
RUN go build -o consumer .

CMD ["./consumer"]
