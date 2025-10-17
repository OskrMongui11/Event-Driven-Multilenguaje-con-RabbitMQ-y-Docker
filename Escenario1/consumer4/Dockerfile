FROM openjdk:17-jdk-slim

WORKDIR /app

# Copiar el código y dependencias
COPY Consumer.java .
COPY amqp-client-5.16.0.jar .
COPY slf4j-api-2.0.7.jar .
COPY slf4j-simple-2.0.7.jar .

# Compilar el programa Java incluyendo todas las dependencias en el classpath
RUN javac -cp ".:amqp-client-5.16.0.jar:slf4j-api-2.0.7.jar:slf4j-simple-2.0.7.jar" Consumer.java

# Ejecutar el consumidor
CMD ["java", "-cp", ".:amqp-client-5.16.0.jar:slf4j-api-2.0.7.jar:slf4j-simple-2.0.7.jar", "Consumer"]
