# Fundamentos de la cabecera X-Content-Type-Options

* La cabecera de respuesta `X-Content-Type-Options` obliga a los navegadores a utilizar el `Content-Type` enviado por el servidor web y evitar que este interprete un `Content-Type` diferente.

> :older_man: La cabecera de respuesta `Content-Type` indica que tipo de contenido está enviando la respuesta del servidor, como por ejemplo `text/html` para contenido HTML o `application/json` para JSON.

* Impedir que los navegadores de los usuarios interpreten un `Content-Type` distinto al deseado, puede prevenir, en algunas ocasiones, vulnerabilidades del lado del cliente.
* Esta cabecera solo cuenta con una directiva, así que la implementación de esta, quedaría de la siguiente forma:

  ```
  X-Content-Type-Options: nosniff
  ```
