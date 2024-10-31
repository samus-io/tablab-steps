# Cómo implementar cabeceras en Apache 2.54.X

* Para definir cabeceras en Apache es bastante sencillo, primero hay que habilitar el módulo `mod_headers`. Para ello hay que ejecutar el siguiente comando en el servidor y luego reiniciar el Apache:

  ```bash
  sudo a2enmod headers
  sudo service apache2 restart
  ```

* Para especificar las cabeceras que se quieren implementar hay que modificar el archivo de configuración de Apache y añadir el siguiente contenido:

  ```
  Header always set Content-Security-Policy "default-src 'none'"
  ```

* En este ejemplo se especifica que el servidor envié la cabecera de respuesta `Content-Security-Policy` con el valor `default: none`.
* Después de realizar estos cambios es importante reiniciar el Apache o recargar la configuración:

  ```
  sudo service apache2 reload
  ```
