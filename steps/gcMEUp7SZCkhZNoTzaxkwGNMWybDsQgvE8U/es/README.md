# Cómo eliminar cabeceras de respuesta en Apache 2.54.X

* Para poder eliminar cabeceras en Apache, primero hay que habilitar el módulo `mod_headers`. Para ello hay que ejecutar el siguiente comando en el servidor y luego reiniciar el Apache:

  ```bash
  sudo a2enmod headers
  sudo service apache2 restart
  ```

* En ocasiones hay algunas cabeceras de respuestas que no se tienen que enviar, como podría ser la cabecera de respuesta `Server`.
* Para eliminar las cabeceras de respuesta hay que definir la siguiente instrucción en el archivo de configuración correspondiente:

  ```apacheconf
  Header always unset Server
  ```
