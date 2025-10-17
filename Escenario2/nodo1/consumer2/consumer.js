// consumer2/consumer.js
import amqp from "amqplib";

const RABBIT = process.env.RABBIT_HOST || "rabbitmq";
const USER = process.env.RABBIT_USER || "guest";
const PASS = process.env.RABBIT_PASS || "guest";
const EXCHANGE = "demo_exchange";

async function main() {
  const conn = await amqp.connect(`amqp://${USER}:${PASS}@${RABBIT}:5672/`);
  const ch = await conn.createChannel();
  await ch.assertExchange(EXCHANGE, "fanout", { durable: true });

  // cola anónima y exclusiva -> recibe copias
  const q = await ch.assertQueue("", { exclusive: true });
  await ch.bindQueue(q.queue, EXCHANGE, "");

  console.log("NodeJS Consumer esperando mensajes...");
  ch.consume(q.queue, (msg) => {
    if (!msg) return;
    console.log("[NodeJS] Mensaje recibido:", msg.content.toString());
  }, { noAck: true });
}

main().catch(console.error);
