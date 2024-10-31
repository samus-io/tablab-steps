# Cómo implementar cabeceras en IIS 10.0

* Para añadir una cabecera al IIS únicamente se deberá añadir el siguiente contenido en el archivo `web.config`:

  ```xml
  <configuration>
    <system.webServer>
    <httpProtocol>
     <customHeaders>
        <add name="Content-Security-Policy" value="default-src 'none'" />
      </customHeaders>
    </httpProtocol>
    </system.webServer>
  </configuration>
  ```

* En este ejemplo se ha añadido la cabecera `Content-Security-Policy` con el valor `default-src 'none'`.
* Tenga en cuenta que la etiqueta `configuration` ya estará añadida al archivo `web.config`, es importante no repetirla y solo añadir el contenido dentro de la etiqueta.
* Una vez aplicado las modificaciones al archivo `web.config` se tendrá que reiniciar el IIS para que tenga efecto.
