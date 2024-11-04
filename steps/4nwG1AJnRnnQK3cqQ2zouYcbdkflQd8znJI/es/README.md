# ¿Qué es una inyección SQL (SQLi)?

* Una inyección SQL (SQLi) es un fallo de seguridad web que permite a actores maliciosos interrumpir y manipular las consultas que una aplicación realiza a su base de datos.
* La vulnerabilidad ocurre cuando un atacante puede insertar código SQL en una consulta pendiente de ser ejecutada a través de datos de entrada proporcionados por el cliente y consiguiendo que el código arbitrario introducido sea considerado como parte de la propia consulta.

## Cómo funciona

* Las técnicas de inyección SQL son posibles debido a la forma en que ciertas aplicaciones web construyen las sentencias SQL, es decir, aquellas en las que el código SQL previamente escrito por los programadores se mezcla directamente con los datos suministrados por el usuario, como en el siguiente ejemplo:

  ```sql
  SELECT name, email FROM users WHERE id=$id
  ```

  En la declaración anterior, la variable `$id` contiene el identificador de usuario que se ha proporcionado como parámetro de entrada, mientras que el resto de la consulta constituye la parte estática definida por el programador, haciendo así que la sentencia SQL sea dinámica en función de los datos proporcionados en la aplicación web.
* Debido a la forma en que se ha construido la sentencia SQL anterior, el usuario podría enviar como parámetro de entrada un valor especialmente diseñado para hacer que la sentencia SQL original ejecute acciones arbitrarias a elección de este. Por ejemplo, sería posible proporcionar `117 or 1=1`, cambiando así la lógica de la declaración SQL y modificando la cláusula `WHERE`, es decir, añadiendo una condición siempre verdadera como es `or 1=1`:
  ![Basic SQL Injection flow][1]
* Como se puede concluir, una inyección SQL exitosa requiere que el adversario produzca una consulta SQL sintéticamente correcta.
  * Cuando una aplicación devuelve un mensaje de error generado por una consulta incorrecta, entonces es más fácil reconstruir la lógica de consulta original y, por tanto, comprender cómo realizar la inserción correctamente.
  * Si la aplicación oculta los detalles de un error, el adversario se ve obligado a aplicar ingeniería inversa a la lógica de consulta original para generar una sentencia válida.

## Qué se podría conseguir con SQLi

* Recuperar información sensible de la base de datos, como contraseñas, datos de tarjetas de crédito o información personal del usuario.
* Modificar datos de la base de datos (insertar, actualizar o eliminar registros).
* Acceder al contenido de archivos específicos dentro del sistema de archivos del Sistema de Gestión de Bases de Datos (SGBD).
* Ejecutar operaciones privilegiadas en la base de datos como simplemente apagar el DBMS.
* Realizar ataques de denegación de servicio (DoS).
* Superar un mecanismo de seguridad, como puede ser un proceso de inicio de sesión, alterando el supuesto valor esperado por la aplicación en una determinada consulta para un conjunto específico de datos.
* En ciertos escenarios, un atacante puede aprovechar una inyección SQL para enviar comandos al sistema operativo, permitiendo que el servidor subyacente u otra infraestructura de backend se vea comprometida.
  * Este hecho representa una situación particularmente peligrosa, ya que abre la puerta al atacante para establecer una puerta trasera persistente en los sistemas de una organización, lo que puede conducir a un compromiso de largo plazo que puede permanecer sin ser detectado durante un período considerable.
* Como efecto colateral, causar daños de reputación y multas reglamentarias si se extraen datos y se publican o se venden.

## Threat modeling

* Las inyecciones SQL se han convertido en un problema frecuente en los sitios web de carácter *database-driven* por el hecho que esta vulnerabilidad es relativamente fácil de identificar y explotar, lo cual la convierte en un objetivo habitual y, en este sentido, es probable que cualquier sitio web o aplicación de software que gestione una base de datos se enfrente a intentos de ataques de esta naturaleza.
* Este fallo de seguridad se encuentra con frecuencia en aplicaciones PHP y ASP principalmente porque se suelen utilizar interfaces funcionales antiguas. En cambio, las aplicaciones Java y ASP.NET suelen ser menos susceptibles a inyecciones SQL explotables debido a las características inherentes de sus interfaces programáticas.

[1]: /static/images/basic-sql-injection-exploitation-flow.png
