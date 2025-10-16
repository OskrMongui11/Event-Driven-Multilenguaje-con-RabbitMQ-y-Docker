# consumer/consumer.py
import pika
import json
import os
import time
import sys

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_USER = os.getenv("RABBIT_USER", "user")
RABBIT_PASS = os.getenv("RABBIT_PASS", "password")
EXCHANGE = "demo_exchange"

def connect_with_retries(retries=10, delay=1):
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

def on_message(ch, method, properties, body):
    try:
        payload = json.loads(body.decode())
    except Exception:
        payload = body.decode()
    print(f"[v] Mensaje recibido: {payload}", flush=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = connect_with_retries()
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout', durable=True)

    q = channel.queue_declare(queue='', exclusive=True)
    queue_name = q.method.queue
    channel.queue_bind(exchange=EXCHANGE, queue=queue_name)

    print("Esperando mensajes. Ctrl+C para salir.")
    channel.basic_consume(queue=queue_name, on_message_callback=on_message)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Consumer detenido.")
    finally:
        try:
            connection.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
