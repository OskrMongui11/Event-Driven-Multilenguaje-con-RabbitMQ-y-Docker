import com.rabbitmq.client.*;

public class Consumer {
    private final static String EXCHANGE_NAME = "demo_exchange";
    private final static String QUEUE_NAME = "demo_queue";

    public static void main(String[] args) throws Exception {
        String host = System.getenv("RABBIT_HOST");
        String user = System.getenv("RABBIT_USER");
        String pass = System.getenv("RABBIT_PASS");

        if (host == null) host = "rabbitmq";
        if (user == null) user = "user";
        if (pass == null) pass = "password";

        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost(host);
        factory.setUsername(user);
        factory.setPassword(pass);

        Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();

        // Declarar el exchange fanout (igual que en el producer)
        channel.exchangeDeclare(EXCHANGE_NAME, BuiltinExchangeType.FANOUT, true);

        // Declarar la cola (si no existe)
        channel.queueDeclare(QUEUE_NAME, false, false, false, null);

        // Vincular la cola con el exchange
        channel.queueBind(QUEUE_NAME, EXCHANGE_NAME, "");

        System.out.println(" [*] Esperando mensajes en '" + QUEUE_NAME + "'...");

        // Callback para recibir mensajes
        DeliverCallback deliverCallback = (consumerTag, delivery) -> {
            String message = new String(delivery.getBody(), "UTF-8");
            System.out.println(" [x] Recibido: '" + message + "'");
        };

        // Empezar a consumir
        channel.basicConsume(QUEUE_NAME, true, deliverCallback, consumerTag -> {});

        // Mantener vivo el proceso
        synchronized (Consumer.class) {
            Consumer.class.wait();
        }
    }
}
