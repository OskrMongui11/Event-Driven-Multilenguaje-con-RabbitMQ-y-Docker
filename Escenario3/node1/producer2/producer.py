# producer/producer.py
import pika
import time
import json
import os
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

def main():
    creds = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    params = pika.ConnectionParameters(host=RABBIT_HOST, credentials=creds)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='demo_exchange', exchange_type='fanout', durable=True)

    n = 1
    while True:
        msg = f"Mensaje Python2 #{n}"
        channel.basic_publish(exchange='demo_exchange', routing_key='', body=msg)
        print(f"[x] Enviado: {msg}", flush=True)
        n += 1
        time.sleep(3)

if __name__ == "__main__":
    main()
