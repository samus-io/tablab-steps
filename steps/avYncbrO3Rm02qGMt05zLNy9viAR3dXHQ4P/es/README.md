# Aplicación de control de acceso a funciones de cambio de contraseña en Node.js

* Una vulnerabilidad IDOR surge cuando un usuario malicioso puede utilizar una referencia directa para acceder o alterar un objeto no autorizado. Un ejemplo común involucra aplicaciones web que permiten ver o modificar datos sensibles a través de simples peticiones. En estos casos, la falta de verificación de permisos del solicitante puede permitir a usuarios no autorizados acceder o manipular datos de la cuenta de otros usuarios.

## Ejercicio para practicar :writing_hand:

* La siguiente aplicación carece de controles de acceso adecuados, ya que no existen protecciones en el lado del servidor para mitigar una vulnerabilidad IDOR que permite a un usuario autenticado cambiar las contraseñas de otros usuarios, lo que podría dar lugar a la toma de control de cuentas.
* En esta aplicación en particular, un usuario malicioso podría utilizar `curl` en la terminal para autenticarse en la aplicación con unas credenciales válidas (i.e., nombre de usuario `johndoe` y contraseña `VcW;seD8qYEn`) enviando una petición al endpoint `/login` y considerando `$APP_URL` una variable de entorno que representa la ruta base de la aplicación:

  ```bash
  curl -s -i -X POST \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode 'username=johndoe' \
    --data-urlencode 'password=VcW;seD8qYEn' \
    $APP_URL/login
  ```

  Tras obtener una respuesta, se puede recuperar una cookie llamada `sessionId`. Si la respuesta indica éxito con un código de estado HTTP `200 OK`, esta cookie puede utilizarse para interactuar con *endpoints* limitados a usuarios autenticados.

  Los usuarios maliciosos pueden enviar una petición PATCH al *endpoint* `/change-password`, proporcionando el nuevo valor de contraseña para el nombre de usuario especificado e incluyendo la cookie `sessionId` obtenida anteriormente:

    ```bash
    curl -s -i -X PATCH \
      -H 'Content-Type: application/json' \
      -d '{ "username": "johndoe", "newPassword": "123456" }' \
      -b 'sessionId=<session_cookie_value>' \
      $APP_URL/change-password
    ```

  Debido a una vulnerabilidad IDOR, proporcionar una referencia directa a otro nombre de usuario existente en la base de datos, como `jackson01`, `jennifer`, `alice99`, o `dianak`, provocaría el cambio de su contraseña y permitiría el inicio de sesión con las nuevas credenciales. Te animamos a que lo pruebes por ti mismo.
* El propósito de este ejercicio es modificar el código fuente mediante el botón `Open Code Editor` para implementar un control de acceso en el lado del servidor que garantice que los usuarios únicamente puedan cambiar su propia contraseña, devolviendo una respuesta con código de estado `401 Unauthorized` en caso de intentos no autorizados.
  * Más concretamente, el *endpoint* PATCH `/change-password` de la aplicación Express en `app.js` debería incorporar modificaciones de código para soportar esta funcionalidad.
* Tras realizar los cambios, se debe pulsar el botón `Verify Completion` para confirmar que se ha completado el ejercicio.

  @@ExerciseBox@@
