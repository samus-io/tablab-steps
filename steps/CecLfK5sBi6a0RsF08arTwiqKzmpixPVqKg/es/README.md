# Cómo implementar cabeceras en Nginx 1.25.X

* Para implementar cabeceras en Nginx hay que modificar el archivo de configuración correspondiente al servidor. Luego para poder adjuntar una cabecera de respuesta en Nginx es necesario añadir el siguiente contenido dentro de la sección `http` o `server`:

  ```nginx
  http {
    ...
    add_header Content-Security-Policy "default-src 'none';";
    ...
    server {
        listen 80;
        server_name example.tbl;
        ...
    }
  }
  ```

* En este ejemplo se añade la cabecera `Content-Security-Policy` con el valor `default-src 'none'` a las cabeceras de respuesta de la aplicación web.
* Después de realizar los cambios correspondientes al archivo de configuración es necesario reiniciar el servidor para que tengan efecto.
