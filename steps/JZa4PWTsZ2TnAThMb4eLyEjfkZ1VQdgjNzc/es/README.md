# Cómo implementar el atributo de las Cookies HttpOnly en Apache 2.54.X

* Para implementar el atributo `HttpOnly` hay que modificar el archivo de configuración de Apache y añadir la siguiente linea:

  ```apacheconf
  Header edit Set-Cookie ^(.*)$ $1;HttpOnly;
  ```

* Con esta configuración, Apache modificará todas las cabeceras de respuesta `Set-Cookie` donde el valor coincida con la expresión regular `^(.*)$` (en este caso, cualquier valor) y modificará el valor de la cabecera por `$1;HttpOnly;` donde `$1` es el valor original de la cabecera `Set-Cookie`.
