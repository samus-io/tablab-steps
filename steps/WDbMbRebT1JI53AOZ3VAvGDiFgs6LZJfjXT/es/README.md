# Aplicación de límites en la carga de archivos con Bucket4j en Java Jakarta

* Restringir el tamaño de los archivos, el total de subidas que puede realizar un usuario y las tasas de solicitudes de carga y descarga son consideraciones de seguridad importantes para las aplicaciones que ofrecen funcionalidades de carga y descarga de archivos.
* Seguidamente se muestran algunos ejemplos de cómo implementar estos límites en una aplicación Java Jakarta utilizando la librería [Bucket4j][1].

## Limitar el tamaño de los archivos

* El siguiente fragmento de código determina el tamaño del archivo cargado en bytes y si el archivo supera 1 MB, devuelve una respuesta HTTP `400 Bad Request`:

  ```java
  // Allow file size up to 1 MB
  Part filePart = request.getPart("file");
  Long fileSize = filePart.getSize();

  if (fileSize > 1000000) {
      response.setStatus(400);
      return;
  }
  ```

## Limitar las tasas de carga y descarga con Bucket4j

* La librería [Bucket4j][1] adopta el algoritmo *token-bucket* para limitar la tasa de transferencia, asignando a cada cliente un *bucket* de *tokens* que representan el número permitido de peticiones en una ventana de tiempo determinada.
* Cada vez que se envía una solicitud se consume un *token* del *bucket* y, cuando no existen *tokens* disponibles, se bloquean las sucesivas solicitudes hasta que se recargan los *tokens* tras el intervalo de tiempo definido.
* En el siguiente código, el método `isClientAllowed` impone la limitación de tasa asignando a cada cliente un *bucket* que permite un número determinado de peticiones (e.g., 100 peticiones) dentro de una ventana de tiempo definida (e.g., 15 minutos). Si hay *tokens* disponibles en el *bucket* de un cliente, se utiliza uno para permitir la petición; si no, la petición se deniega hasta que se repone el *bucket* cuando se restablece la ventana de tiempo:

  <details>
    <summary>Dependencias</summary>

    ```java
    import java.io.IOException;
    import java.time.Duration;
    import java.util.concurrent.ConcurrentHashMap;
    import io.github.bucket4j.Bucket;
    ```

  </details>

  ```java
  private static final Duration RATE_LIMIT_TIME_WINDOW = Duration.ofSeconds(900); // 15 minutes window
  private static final Integer MAX_REQUESTS_PER_CLIENT = 100; // Allow 100 requests per IP per 15 minutes
  private static final ConcurrentHashMap<String, Bucket> clientRateLimit = new ConcurrentHashMap<>();

  // Creates a new bucket for a client with a predefined capacity and refill rate
  private Bucket createNewBucket(String clientIdentifier) {
      return Bucket.builder().addLimit(limit -> limit.capacity(MAX_REQUESTS_PER_CLIENT)
              .refillGreedy(MAX_REQUESTS_PER_CLIENT, RATE_LIMIT_TIME_WINDOW)).build();
  }

  // Checks if a client, identified by 'clientIdentifier', is allowed to proceed based on their rate limit
  private Boolean isClientAllowed(String clientIdentifier) {
      // Retrieves the client's bucket or creates a new one if it doesn't exist
      Bucket bucket = clientRateLimit.computeIfAbsent(clientIdentifier, this::createNewBucket);
      return bucket.tryConsume(1);
  }
  ```

* Para aplicar una limitación de tasa basada en la dirección IP para un *endpoint* de carga o descarga se puede invocar el método `isClientAllowed` como se demuestra a continuación:

  ```java
  public void uploadFile(HttpServletRequest request, HttpServletResponse response) {
      String clientIP = request.getRemoteAddr();

      if (!isClientAllowed(clientIP)) {
          response.setStatus(429);
          return;
      }

      // File upload logic
  }
  ```

* Del mismo modo, para aplicar una limitación de tasa por sesión para un *endpoint*, se puede llamar al método `isClientAllowed` utilizando el ID de sesión como identificador de cliente:

  ```java
  public void uploadFile(HttpServletRequest request, HttpServletResponse response) {
      String clientSessionId = request.getSession().getId();

      if (!isClientAllowed(clientSessionId)) {
          response.setStatus(429);
          return;
      }

      // File upload logic
  }
  ```

  > :older_man: Siempre que las funciones de carga o descarga de archivos estén disponibles cuando el usuario está autenticado, es muy recomendable aplicar este tipo de restricción a la sesión iniciada por el usuario en lugar de otros valores superficiales como la dirección IP de origen.

### Consideraciones al restringir por dirección IP

* En la mayoría de los casos, la aplicación web no está expuesta directamente al usuario final, sino que suele estar ubicada detrás de un balanceador de carga o de un mecanismo de seguridad como un cortafuegos de aplicaciones web (WAF).
* Esto podría provocar que la dirección IP de origen de los paquetes HTTP recibidos por la aplicación fuera la IP del intermediario, en lugar de la del cliente final. En estos casos, puede ser necesario utilizar cabeceras como `X-Forwarded-For` para proporcionar a la aplicación la dirección IP real del cliente:
  
  ```java
  System.out.println(request.getHeader("X-Forwarded-For"));
  ```

* Para ajustarse a esto, cuando se ejecuta la aplicación web detrás de un proxy inverso, se puede emplear un método como `getClientIP` para recuperar la IP real del cliente:

  ```java
  private String getClientIP(HttpServletRequest request) {
      String xffHeader = request.getHeader("X-Forwarded-For");

      if (xffHeader == null) {
          return request.getRemoteAddr(); // Return the client IP if the header is not present
      }
      
      return xffHeader.split(",")[0]; // Get the first IP in the list if the header exists
  }
  ```

  > :warning: La cabecera `X-Forwarded-For` puede ser controlada por el usuario, lo que significa que puede incluir cualquier valor, como direcciones IP falsificadas o datos no válidos. En algún punto de la infraestructura, es necesario sanearla y descartar entradas irrelevantes.

## Ejercicio para practicar :writing_hand:

* La aplicación dada ofrece una carga básica de archivos sin ninguna validación de seguridad realizada en el lado del servidor. El objetivo aquí es abrir el editor de código usando el botón `Open Code Editor` y editar el código fuente para incorporar dos medidas de seguridad:
  * Un límite de tamaño de archivo de 1 KB. Si un archivo cargado supera este tamaño, se debe devolver una respuesta HTTP con un código de estado `400 Bad Request`.
  * Cada dirección IP debe estar limitada a 10 subidas de archivos en una ventana de 30 segundos. Si se sobrepasa este límite, se debe recibir una respuesta HTTP con el código de estado `429 Too Many Requests` y la IP debe permanecer bloqueada durante 30 segundos.
    * Hay que tener en cuenta que la aplicación se coloca bajo múltiples capas de proxy inverso, ya que se ejecuta dentro de un contenedor Cloud Run en GCP.
* Con el fin de completar el ejercicio, en la clase ubicada en `src/main/java/io/ontablab/FileUploadServlet.java` es donde se deben añadir las modificaciones de código para soportar estas características.
  @@ExerciseBox@@

[1]: https://github.com/bucket4j/bucket4j
