# Fundamentos de la cabecera Strict-Transport-Security

* La cabecera de respuesta `Strict-Transport-Security (HSTS)` es un mecanismo de seguridad que informa al navegador que solo acceda a la aplicación web usando HTTPS, y que cualquier intento futuro de acceder por HTTP sea redirigido automáticamente a HTTPS. Este mecanismo es útil para prevenir ataques de `Man-in-the-Middle`.

> :older_man: Un ataque `Man-in-the-Middle` es una técnica de ciberseguridad en que un adversario se interpone en la comunicación entre un usuario y el servidor, con el fin de interceptar, modificar o suplantar los mensajes entre las dos partes.

## Directivas

* La cabecera `Strict-Transport-Security (HSTS)` solamente tiene dos directivas:
  * `max-age=<expire-time>`: determina el tiempo en segundos que el navegador debe recordar que solo acceda por HTTPS al sitio.
  * `includeSubDomains`: si se especifica esta directiva, la cabecera aplica a todos los subdominios.
* En este ejemplo la cabecera informará al navegador que solo acceda por HTTPS a su dominio y todos sus subdominios por un periodo de un año:

  ```
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  ```
