# producer/producer.py
import pika
import time
import json
import os
import sys

# Variables de entorno con valores por defecto
RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_USER = os.getenv("RABBIT_USER", "user")
RABBIT_PASS = os.getenv("RABBIT_PASS", "password")
EXCHANGE = "demo_exchange"


def connect_with_retries(retries=10, delay=1):
    """Intentar conectar a RabbitMQ con reintentos."""
    credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    params = pika.ConnectionParameters(host=RABBIT_HOST, credentials=credentials)
    attempt = 0

    while True:
        try:
            conn = pika.BlockingConnection(params)
            return conn
        except Exception as e:
            attempt += 1
            if attempt >= retries:
                print(f"[!] No se pudo conectar después de {attempt} intentos: {e}", file=sys.stderr)
                raise
            wait = delay * attempt
            print(f"[!] Conexión fallida (intento {attempt}/{retries}), reintentando en {wait}s... ({e})")
            time.sleep(wait)


def main():
    """Envia mensajes continuamente al exchange."""
    connection = connect_with_retries()
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout', durable=True)

    count = 1
    try:
        while True:
            message = {
                "id": count,
                "msg": f"Mensaje Python-1 #{count}"
            }
            body = json.dumps(message)
            channel.basic_publish(exchange=EXCHANGE, routing_key='', body=body)
            print(f"[x] Enviado: {body}", flush=True)
            count += 1
            time.sleep(3)
    except KeyboardInterrupt:
        print("Producer detenido.")
    finally:
        try:
            connection.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
