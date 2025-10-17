Taller: Arquitectura Event-Driven Multilenguaje con RabbitMQ y Docker

Autores:
- Oscar Mauricio Mongui Piñeros 
- Marcos Orjuela
- Gabriel Pedraza

Universidad Industrial de Santander (UIS)
Fecha: 16 de Octubre de 2025

1. OBJETIVOS
- Comprender y aplicar el estilo arquitectural event-driven en un entorno distribuido.
- Implementar un sistema de mensajería basado en RabbitMQ utilizando el protocolo AMQP.
- Desplegar productores y consumidores en diferentes lenguajes dentro de contenedores Docker.
- Probar y comparar el funcionamiento del sistema bajo escenarios centralizados y distribuidos.

2. DISEÑO DEL SISTEMA
Descripción general
El sistema desarrollado sigue una arquitectura orientada a eventos (Event-Driven), donde varios productores publican mensajes hacia un broker RabbitMQ, el cual los enruta hacia diferentes consumidores que los procesan de manera asíncrona.

Cada servicio se ejecuta dentro de un contenedor Docker independiente, lo que garantiza aislamiento, portabilidad y facilidad de despliegue entre diferentes nodos.

Lenguajes y componentes utilizados
- Python: Productores y consumidores básicos (carpetas `producer/`, `producer2/`, `consumer/`) usando `pika`.
- JavaScript (Node.js): Productor y consumidor (`producer3/`, `consumer2/`) usando `amqplib`.
- Go (Golang): Servicios (`producer4/`, `consumer3/`) usando `streadway/amqp`.
- Java: Consumidor (`consumer4/`) usando `amqp-client`.
- RabbitMQ: Imagen `rabbitmq:3-management` como broker central.

3. ESCENARIOS DE DISTRIBUCIÓN
Se implementaron tres escenarios para evaluar comportamiento y distribución.

Escenario 1 — Centralizado
- Descripción: Todos los contenedores (RabbitMQ, productores y consumidores) se ejecutan en un único nodo físico.
- Técnica: Un único `docker-compose.yml` en `Escenario1/` con todos los servicios. RabbitMQ expone puertos 5672 (AMQP) y 15672 (management).
- Resultado: Comunicación funcional entre todos los servicios de distintos lenguajes en el mismo entorno local. Útil para pruebas y validación.

Escenario 2 — Distribuido en 2 nodos
- Configuración: Nodo 1 con productores y consumidores; Nodo 2 con RabbitMQ.
- Técnica: Dos `docker-compose` (uno por nodo). Los servicios en Nodo 1 usan la variable `RABBITMQ_HOST` apuntando a la IP del Broker en Nodo 2.
- Resultado: Operación correcta con comunicaciones LAN y monitores del broker mostrando colas activas.

Escenario 3 — Distribuido en 3 nodos
- Configuración: Nodo 1 (Python/Node.js), Nodo 2 (Go/Java), Nodo 3 (RabbitMQ).
- Técnica: Tres `docker-compose` y una red Docker externa (ejemplo: `docker network create rabbitmq_net --driver bridge`).
- Resultado: Servicios en diferentes nodos conectados al broker central, validando ejecución paralela y distribución física.

4. EVIDENCIAS DE EJECUCIÓN
- Ejecución simultánea de productores y consumidores en terminales PowerShell.
- Logs de recepción de mensajes en consumidores (Python, Node.js, Go, Java).
- RabbitMQ Management mostrando colas activas, mensajes pendientes y confirmaciones ACK.
- Recomendación: Incluya capturas de pantalla en esta sección (no incluidas aquí por privacidad).

5. COMPARACIÓN ENTRE ESCENARIOS
- Escenario 1: Centralizado — Complejidad baja, comunicación local, escalabilidad limitada.
- Escenario 2: Distribuido (2 nodos) — Complejidad media, comunicación LAN, mejor tolerancia.
- Escenario 3: Distribuido (3 nodos) — Complejidad alta, comunicación LAN, alta escalabilidad y tolerancia.

Análisis: El despliegue centralizado sirve para validación rápida. Separar el broker mejora la estabilidad. Distribuir en tres nodos aumenta tolerancia y permite pruebas más realistas.

6. CONCLUSIONES
- Se implementó un sistema Event-Driven multilenguaje usando RabbitMQ y Docker.
- Contenedores facilitaron aislamiento y despliegue de servicios heterogéneos.
- RabbitMQ demostró ser adecuado para integración asíncrona.
- Escenarios distribuidos mostraron retos en redes y configuración de IPs.


