# Cómo implementar el atributo de las Cookies HttpOnly en IIS 10.0

* Para implementar el atributo `HttpOnly` únicamente hay que añadir la siguiente configuración en el archivo `web.config`:

  ```xml
  <configuration>
    <system.web>
      ...
      <httpCookies httpOnlyCookies="true"/>
      ...
    </system.web>
  </configuration>
  ```

* Con esta instrucción se añadirá el atributo `HttpOnly` a todas las Cookies enviadas por el backend.
