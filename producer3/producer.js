import amqplib from "amqplib";

const RABBIT_HOST = process.env.RABBIT_HOST || "rabbitmq";
const RABBIT_USER = process.env.RABBIT_USER || "user";
const RABBIT_PASS = process.env.RABBIT_PASS || "password";
const EXCHANGE = "demo_exchange";

async function main() {
  const conn = await amqplib.connect(`amqp://${RABBIT_USER}:${RABBIT_PASS}@${RABBIT_HOST}`);
  const ch = await conn.createChannel();
  await ch.assertExchange(EXCHANGE, "fanout", { durable: true });

  let count = 1;
  while (true) {
    const msg = `Mensaje NodeJS #${count}`;
    ch.publish(EXCHANGE, "", Buffer.from(msg));
    console.log(`[x] Enviado: ${msg}`);
    count++;
    await new Promise(r => setTimeout(r, 3000));
  }
}

main().catch(err => console.error("Error:", err));
