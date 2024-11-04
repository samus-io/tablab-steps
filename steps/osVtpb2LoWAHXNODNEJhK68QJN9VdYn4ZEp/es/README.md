# Fundamentos de la Same-Origin Policy

* La `Same-Origin Policy (SOP)` es un concepto importante para la seguridad de las páginas web. No se trata de un estándar de internet, sino una política de seguridad de los navegadores web. Esta política previene la interacción entre páginas de diferentes orígenes.
* Un origen está definido por la combinación de protocolo, host y puerto:

  ```powershell
  https://domain.tbl
  http://example.tbl:8080
  ```

* El primer ejemplo tiene como protocolo el `https`, el host `domain.tbl` y el puerto `443`.
* El segundo ejemplo tiene como protocolo es `http`, el host `example.tbl` y el puerto `8080`.
  
## Como funciona SOP

* La política `SOP` se puede resumir con la siguiente frase: *"Se puede acceder a las propiedades de otro documento solo si se tiene el mismo origen"*. Básicamente evita que el código JavaScript de un origen pueda acceder al contenido generado por otro origen.
* No todo el contenido es considerado un *"documento"*, hay algunas excepciones. Los archivos CSS, JavaScript e imágenes están excluidas de la política `SOP`. Permitiendo a un origen hacer peticiones e interactuar con la respuesta de estas. Si esto no fuera así, no se podrían visualizar imágenes o incluir código JavaScript de otros orígenes.
* Un ejemplo donde se aplica la política `SOP` podría ser el siguiente:
  ![SOP Example][1]
  * El usuario hace una petición a `https://domain.tbl` y al cargar el código JavaScript, este realiza una petición hacia `https://example.tbl/account`.
  * La petición se ha realizado correctamente pero el código JavaScript al intentar leer la respuesta, la `SOP` bloqueará esa acción.
  * De esta forma, se evita que el origen `https://domain.tbl` tenga acceso a información del origen `https://example.tbl`. Si esto no fuera así, al obtener la respuesta se podría recopilar datos sensibles del usuario.

## Cuando se aplica la política de SOP

* El navegador aplica la política `SOP` en los casos que considere que hay una potencial interacción entre dos orígenes distintos. Estas interacciones se pueden resumir en los siguientes puntos:
  * Código JavaScript: Una página no puede acceder al contenido de un `iframe` a menos que sea del mismo origen.
  * Cookies: Una cookie no puede ser compartida con orígenes diferentes.
    * Las cookies funcionan de distinta forma, se considera origen únicamente el host, de manera que solo el dominio y el subdominio forman el origen.
  * Peticiones AJAX (`XmlHTTPRequest`): Las peticiones JavaScript que interactúen con otro origen se llevaran a cabo exitosamente, pero no se podrá acceder a la respuesta de un origen diferente.
* La política `SOP` no elimina completamente la interacción entre dos orígenes diferentes. Hay algunos casos los cuales se permite esta interacción, como pueden ser los siguientes:
  * Como se ha mencionado anteriormente, se pueden hacer peticiones entre diferentes orígenes, de forma que sí que hay interacción entre ellos, pero sin que se pueda acceder a la respuesta. Esto también se aplica a los formularios, de manera que se puede crear un formulario y enviarlo a otro origen.
  * Otro caso es cuando utilizamos un `iframe`, donde este permite cargar el contenido de un origen distinto mediante un `frame` (siempre y cuando otras políticas de seguridad nos lo permitan). Cabe destacar que aunque sea possible crear un `frame` de otro origen, la regla sigue siendo la misma, no se puede acceder a la respuesta o contenido del `frame` pero si es posible interactuar con él.
  * También los archivos CSS, JavaScript e imágenes están excluidas de la política `SOP`.

[1]: /static/images/how-sop-works-example.png
