# Tipos de inyección SQL

* Existen algunos tipos de inyecciones SQL en función del método de explotación utilizado para llevar a cabo el ataque.

![Types of SQL Injection][1]

## Inyecciones SQL in-band

* Las inyecciones SQL in-band aprovechan el mismo canal utilizado para inyectar el código SQL, es decir, el resultado de la explotación se incluye directamente en la página de respuesta de la aplicación web vulnerable.
* Las técnicas más comunes en esta categoría son las inyecciones SQL basadas en UNION y las basadas en errores.

### Inyecciones SQL basadas en UNION

* Las inyecciones SQL basadas en UNION implican el uso del operador `UNION` que combina los resultados de múltiples sentencias `SELECT` para obtener datos de múltiples tablas como un único conjunto. Los datos obtenidos se añaden a la consulta original.
* En el siguiente ejemplo se inyecta la carga útil SQL `new' UNION SELECT username, email, password FROM users; -- -` en la consulta:

  ```sql
  SELECT name, description, brand FROM products WHERE status='new' UNION SELECT username, email, password FROM users; -- -' AND taxable = true;
  ```

* Para que una consulta `UNION` tenga éxito, deben cumplirse dos condiciones:
  * Las consultas `SELECT` individuales deben devolver el mismo número de columnas.
  * Los tipos de datos de cada columna deben ser compatibles entre las consultas individuales.

### Inyecciones SQL basadas en errores

* Las inyecciones SQL basadas en errores se producen cuando un adversario fuerza a la DMBS a emitir un mensaje de error y recuperar datos mediante los propios errores.
* En el siguiente ejemplo se inyecta la carga útil SQL `new' OR user_name()=1;-- -` en la consulta:

  ```sql
  SELECT name, description, brand FROM products WHERE status='new' OR user_name()=1; -- - AND taxable = true;
  ```

* Los errores pueden enviarse a través de la salida de la aplicación web (in-band) o por otros medios, como informes automatizados, archivos de registro o correos electrónicos de advertencia (out-of-band para los últimos tres casos).

## Inyecciones SQL Out-Of-Band (OOB)

* Al contrario que los vectores in-band, las técnicas Out-Of-Band (OOB) utilizan canales alternativos para extraer datos del servidor, incluyendo peticiones HTTP, resolución DNS, correo electrónico, sistema de archivos, conexiones a otras bases de datos, etc.

## Inyecciones SQL inference/blind

* Las inyecciones SQL inference/blind no reflejan los resultados de la inyección en la salida, sino que requieren que se deduzca si la expresión probada tuvo éxito incluso si no se devuelve ningún dato, simplemente observando una diferencia en la forma en que se comporta una aplicación. Así que, en este caso, el adversario debe encontrar un método de inferencia para explotar la vulnerabilidad.
* La explotación por inferencia se lleva a cabo principalmente mediante inyecciones SQL basadas en booleanos o bien en tiempo.

### Inyecciones SQL boolean-based

* Las inyecciones SQL boolean-based se fundamentan en el envío de una consulta SQL a la base de datos que devolverá `TRUE` o `FALSE`.
* A modo de ejemplo, la siguiente consulta determina si la longitud del valor del campo `password` tiene más de 5 caracteres:

  ```sql
  ' or (length((SELECT password FROM users WHERE id=1)) > 5 )
  ```

* Una vez procesada la consulta, el contenido dentro de la respuesta HTTP será diferente dependiendo de si el resultado es `TRUE` o `FALSE`, y esto hará que la aplicación actúe de forma diferente, lo que permitirá deducir valores almacenados en la base de datos.

### Inyecciones SQL basadas en tiempo

* Las inyecciones SQL basadas en tiempo se fundamentan en el envío de una consulta SQL a la base de datos que obligará a la base de datos a esperar un tiempo determinado antes de responder en caso de que se cumpla alguna condición predefinida.
* A modo de ejemplo, la siguiente consulta obliga al SGBD a esperar 10 segundos en caso de que la condición sea `TRUE`:

  ```sql
  select if((SELECT database()="ecommercedb"), sleep(10), null); -- -
  ```

* El tiempo de respuesta permitirá al adversario deducir si el resultado de la consulta es `TRUE` o `FALSE`, lo que permitirá averiguar valores almacenados en la base de datos.

## Inyecciones SQL de segundo orden

* La inyección SQL de segundo orden se produce cuando los datos suministrados por el usuario son almacenados por la aplicación y posteriormente incorporados a consultas SQL de forma insegura:
  1. Primero, el adversario envía una petición maliciosa.
  1. La aplicación almacena los datos y responde a la petición sin presentar por el momento ninguna vulnerabilidad.
  1. El adversario envía otra petición (una segunda petición).
  1. Para gestionar la segunda petición, la aplicación recupera la información almacenada anteriormente y la procesa. Esta vez, se ejecuta la consulta inyectada por el adversario.
* El exploit se envía en una petición y se activa cuando la aplicación gestiona una petición diferente.
* Los escáneres automatizados modernos son incapaces de realizar lo necesario para descubrir vulnerabilidades de segundo orden. Esto se debe a que hay varios escenarios posibles, y sin una comprensión del significado y el uso de los elementos de datos dentro de la aplicación, el trabajo involucrado en la detección de inyecciones SQL de segundo orden crece exponencialmente. El factor humano es necesario.

[1]: /static/images/learning/types-of-sql-injection.png
