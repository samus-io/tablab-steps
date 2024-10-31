# Cómo prevenir los errores de configuración de CORS

* Si no se configura bien el `CORS` puede tener un alto impacto en la seguridad de la aplicación web, dejando al descubierto información sensible de usuarios o incluso pueden aparecer otras vulnerabilidades.
* Por lo tanto, es importante establecer el `CORS` solo si es necesario para el funcionamiento de la aplicación web.
* Para evitar una mala configuración del `CORS` es importante seguir los siguientes puntos:
  * Especificar qué orígenes están permitidos. Es crucial que no se utilice una wildcard (`*`), ya que esto permitiría acceder a cualquier origen a la respuesta de la aplicación web.
  * Únicamente permitir orígenes de confianza:

    ```
    Access-Control-Allow-Origin: https://domain.tbl
    ```

  * Nunca usar la cabecera `Access-Control-Allow-Origin` con el valor `null`. Utilizar este valor es prácticamente idéntico a usar una wildcard.
  * Únicamente usar la cabecera `Access-Control-Allow-Credential: true` si es absolutamente necesaria.
  * Determinar qué métodos son los que el servidor tiene que aceptar con la cabecera `Access-Control-Allow-Methods`.
  * Cabe destacar que implementar la política de `CORS` correctamente no es un reemplazo de la protección por parte del servidor. Aunque se configure correctamente, el servidor tiene que implementar otras protecciones de seguridad como la autenticación y evitar que se filtren datos sensibles.
