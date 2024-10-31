# Fundamentos de Cross-Origin Resource Sharing (CORS)

* Si bien la `Same-Origin Policy (SOP)` es necesaria y un componente importante en la seguridad web, también es muy restrictiva cuando dos orígenes diferentes necesitan comunicarse entre ellos.
* `Cross-Origin Resource Sharing (CORS)` es un mecanismo que utiliza las cabeceras HTTP para evadir la `SOP` y permitir a dos orígenes diferentes interactuar entre ellos.
* El caso más usado de `CORS` es en una API alojada en otro origen al de la aplicación web, donde esta devuelve información necesaria para el correcto funcionamiento de la aplicación y se necesita acceder a las respuestas de la API por JavaScript. Entonces, aplicando estas cabeceras, es posible permitir que se acceda a la respuesta evadiendo la `SOP`.

## Cabeceras de Cross-Origin Resource Sharing (CORS)

### Cabeceras del lado del servidor

* Estas cabeceras de respuesta `HTTP` son utilizadas por el servidor que quiere permitir a otros orígenes acceder a su respuesta e interactuar con ellos.

|Cabecera|Descripción|Ejemplo|
|:--:|:--:|:--:|
|`Access-Control-Allow-Origin`|Es utilizada por la aplicación web para determinar qué orígenes pueden acceder a su respuesta e interactuar con él.|Access-Control-Allow-Origin: `https://domain.tbl`|
|`Access-Control-Allow-Credentials`|Indica si la petición puede incluir las credenciales (Cookies) del usuario que la realiza. Si no se especifica esta cabecera su valor por defecto será `false`.|Access-Control-Allow-Credentials: true|
|`Access-Control-Allow-Methods`|Determina qué métodos son aceptados por el servidor al realizar una petición desde otro origen.|Access-Control-Allow-Methods: POST, GET, OPTIONS, DELETE|
|`Access-Control-Allow-Headers`|Determina que cabeceras `HTTP` no estándar son aceptadas por la aplicación web al realizar una petición desde otro origen.|Access-Control-Allow-Headers: Front-End-Https|
|`Access-Control-Max-Age`|Especifica cuanto tiempo en segundos se puede guardar en la cache del navegador el valor de las cabeceras `Access-Control-Allow-Methods` y `Access-Control-Allow-Headers`.|Access-Control-Max-Age: 3600|
|`Access-Control-Expose-Headers`|Esta cabecera permite indicar que cabeceras de respuesta puede acceder otro origen. Por defecto, solo se puede acceder a las cabeceras `Cache-Control`, `Content-Language`, `Content-Length`, `Content-Type`, `Expires`, `Last-Modified` y `Pragma`. Así entonces las cabeceras que se especifiquen en `Access-Control-Expose-Headers` se podrá acceder mediante JavaScript en las peticiones que se realicen en otro origen.|Access-Control-Expose-Headers: Content-Encoding|

### Cabeceras del lado del cliente

* Las siguientes cabeceras `HTTP` se envían por parte del cliente (el usuario) para enviar información sobre la petición que se llevará a cabo. Normalmente se envían en las peticiones `Preflight`.

|Cabecera|Descripción|Ejemplo|
|:--:|:--:|:--:|
|`Origin`|Determina desde que origen se ha realizado la petición.|Origin: `https://domain.tbl`|
|`Access-Control-Request-Method`|Esta cabecera se envía con las peticiones con el método `OPTIONS` para especificar que método se utilizará en la petición.|Access-Control-Request-Method: POST|
|`Access-Control-Request-Header`|Esta cabecera se envía con las peticiones con el método `OPTIONS` para especificar que cabeceras `HTTP` no estándar se envían junto con la petición.|Access-Control-Request-Headers: Front-End-Https|
