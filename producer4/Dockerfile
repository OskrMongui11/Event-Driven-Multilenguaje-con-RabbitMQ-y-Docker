FROM golang:1.21-alpine

WORKDIR /app
COPY go.mod ./
RUN go mod download


COPY . .

RUN go get github.com/rabbitmq/amqp091-go@latest

RUN go build -o producer .

CMD ["./producer"]
