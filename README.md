# Taller: Arquitectura Event-Driven Multilenguaje con RabbitMQ y Docker

Repositorio con ejemplos y despliegues Docker para un taller práctico sobre arquitectura orientada a eventos (Event-Driven) usando RabbitMQ como broker y servicios escritos en Python, Node.js, Go y Java.

Contenido principal

- `Escenario1/` — Despliegue centralizado (un solo nodo) con un `docker-compose.yml` que contiene RabbitMQ, productores y consumidores en varios lenguajes.
- `Escenario2/` — Despliegue distribuido en 2 nodos (configuración por nodos con `docker-compose-node1.yml` y `docker-compose-node2.yml`).
- `Escenario3/` — Despliegue distribuido en 3 nodos (arquitectura más separada con `docker-compose-node*.yml`).

Lenguajes y componentes incluidos

- Python: `producer/`, `producer2/`, `consumer/` (usa `pika`).
- Node.js: `producer3/`, `consumer2/` (usa `amqplib`).
- Go: `producer4/`, `consumer3/` (usa `streadway/amqp`).
- Java: `consumer4/` (usa `amqp-client`).
- RabbitMQ: se usa la imagen oficial `rabbitmq:3-management` para el broker y su interfaz de administración en el puerto 15672.

Resumen de escenarios

- Escenario 1 (Centralizado): Todos los servicios y RabbitMQ se ejecutan en un único `docker-compose.yml` (ver `Escenario1/docker-compose.yml`). Ideal para pruebas locales.
- Escenario 2 (Distribuido en 2 nodos): Separación del broker en un nodo y los productores/consumidores en otro. Cada nodo tiene su `docker-compose` propio (`Escenario2/node1/docker-compose-node1.yml`, `Escenario2/node2/docker-compose-node2.yml`).
- Escenario 3 (Distribuido en 3 nodos): Brokers y servicios separados a través de tres nodos. Se utiliza una red Docker externa (ej. `rabbitmq_net`) para conectar los nodos.

Cómo ejecutar (ejemplo para Escenario1 en localhost)

1. Abrir una terminal PowerShell en la raíz de `Escenario1`.
2. Construir y levantar los servicios:

```powershell
docker-compose up --build -d
```

3. Abrir la interfaz de RabbitMQ en http://localhost:15672 — usuario y contraseña por defecto configurados en el `docker-compose.yml` (ver variables en el archivo).
4. Ver logs de productores/consumidores con:

```powershell
docker-compose logs -f consumer
# o
docker-compose logs -f producer1
```

Notas de seguridad y privacidad

- No se incluyen datos sensibles en este repositorio. Las credenciales usadas en los `docker-compose` son para entorno de laboratorio y deben cambiarse para entornos reales.

Contribuciones

Si deseas contribuir, abre un issue o pull request con mejoras, correcciones o nueva integración de lenguajes.

Licencia

Este repositorio se comparte con fines educativos.
