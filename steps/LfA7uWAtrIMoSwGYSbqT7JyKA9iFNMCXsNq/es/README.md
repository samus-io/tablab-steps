# Mejores prácticas para prevenir inyecciones SQL

* Para prevenir fallos de inyección SQL, es crucial evitar escribir consultas dinámicas utilizando concatenación de cadenas y asegurarse también de que la entrada de datos suministrada por el usuario, aunque contenga código SQL malicioso, no pueda manipular la lógica prevista de la consulta.

## Medidas de mitigación

* Debido a la amplia variación en el patrón de los ataques de inyección SQL, las siguientes estrategias son a menudo incapaces de proteger las bases de datos por sí solas. Por este motivo, para cubrir todas las bases, deben aplicarse en combinación con un WAF.

### Prepared statements

* En un Sistema de Gestión de Bases de Datos (SGBD), un `prepared statement` (en Español, sentencia preparada), `parameterized statement` o `parameterized query` es una característica que permite separar el código SQL de los datos proporcionados por el usuario.
  > Aunque el término `parameterized query` se utiliza a menudo indistintamente con `prepared statement`, este en general se refiere a la práctica de utilizar parámetros en las consultas SQL para hacerlas más flexibles y seguras.
* Utilizando sentencias preparadas el flujo de trabajo más común normalmente consta de los siguientes pasos:
  1. **Preparación**: la aplicación crea la plantilla de la sentencia y lo envía al SGBD. Algunos valores, llamados parámetros o marcadores de posición, se dejan sin especificar:

      ```sql
      INSERT INTO products (name, price) VALUES (?, ?);
      ```

  1. **Compilación**: el motor del SGBD analiza, compila y optimiza la sentencia SQL y, a continuación, guarda el resultado sin ejecutar. Este proceso solo se realiza una vez.
  1. **Ejecución**: utilizando datos introducidos por el usuario, la aplicación proporciona (o vincula) valores para los parámetros de la plantilla de la sentencia y el DBMS la ejecuta.
* La ventaja clave de utilizar sentencias preparadas es que los parámetros se tratan como entidades separadas y no como parte del código SQL. Esto significa que un adversario no puede cambiar la intención de una consulta, incluso si se insertan comandos SQL válidos.
  * En el ejemplo anterior, si un adversario intenta introducir como `id` de usuario el valor `197' or '1'='1`, el uso de sentencias preparadas garantiza que la entrada se trate como datos y no como código ejecutable. En consecuencia, la consulta buscará un `id` que coincida exactamente con la cadena completa `197' or '1'='1`, lo que la hace resistente a los ataques de inyección SQL.
  * Este enfoque parametrizado ayuda a proteger el sistema de manipulaciones no autorizadas de la base de datos al tratar las entradas del usuario siempre como valores y no como elementos de la propia consulta SQL.

#### Object-Relational Mapping (ORM)

* Los desarrolladores pueden utilizar frameworks ORM para crear consultas a bases de datos de una forma más segura y sencilla. Las librerías ORM evitan la necesidad de escribir código SQL, ya que la misma librería genera sentencias SQL preparadas directamente a partir de código orientado a objetos.
* Aunque la utilización de frameworks ORM ayuda a mitigar los riesgos de inyección SQL mediante la abstracción de comandos SQL, no es una solución infalible. Los frameworks ORM siguen construyendo comandos SQL, por lo que los desarrolladores deben implementar una validación robusta de datos de entrada para garantizar la seguridad del sistema frente a las inyecciones SQL.

### Stored procedures

* Con los `stored procedures` (en Español, procedimientos almacenados) es posible lograr el mismo enfoque que ofrecen las sentencias preparadas.
  * La diferencia entre las sentencias preparadas y los procedimientos almacenados radica en dónde se define y almacena el código SQL. Con los procedimientos almacenados, el código SQL se define y almacena directamente en la base de datos y la aplicación lo invoca cuando es necesario. Por el contrario, para las sentencias preparadas la definición y preparación de consultas SQL se lleva a cabo en el propio código de la aplicación antes de su ejecución.
  * La elección entre estos suele depender de factores como la arquitectura de la aplicación y las preferencias del equipo de desarrollo.
* Sin embargo, los procedimientos almacenados pueden presentar un mayor riesgo en comparación con las sentencias preparadas, especialmente cuando requieren permisos de distinta naturaleza en el SGBD para realizar la tarea. Esto supone un peligro en caso de compromiso, ya que el atacante tendría más privilegios y posibilidades de realizar acciones más avanzadas.

### Allow-list input validation

* La práctica de `allow-list input validation` (en Español, validación de entrada mediante lista de permitidos) consiste en aceptar como entrada solo un conjunto de valores explícitamente admitidos, mientras que el resto de valores no especificados se rechazan implícitamente.
* Se trata de una técnica especialmente útil cuando deben definirse consultas SQL dinámicas y cuando los valores que deben ser dinámicos no pueden establecerse como parámetros, como pueden ser los nombres de tabla o el indicador de orden de clasificación (`ASC` o `DESC`). En este caso, la validación de la entrada o bien un rediseño completo de la consulta es la mejor apuesta para mitigar los ataques de inyección SQL.
* El código siguiente muestra cómo realizar la validación del nombre de la tabla:

  ```php
  switch ($tableName) {
    case "fooTable": return true;
    case "barTable": return true;
    default: return new BadMessageException("Unexpected value provided as table name");
  }
  ```

* Para gestionar una tarea básica como la ordenación, la entrada del usuario puede convertirse directamente en un booleano. A continuación, se puede utilizar este booleano para elegir un valor seguro que añadir a la consulta:

  ```sql
  "SELECT * FROM products ORDER BY price " + ($sortOrder ? "ASC" : "DESC");
  ```

### Escaping all user-supplied input

* El proceso de `escaping all user-supplied input` (en Español, escapar todas las entradas proporcionadas por el usuario) consiste en intentar escapar todos los caracteres de la entrada proporcionada por el usuario que tienen un significado especial en SQL y antes de que estos datos se añadan a la consulta de la base de datos.
* Este mecanismo puede variar en función de la base de datos y, por supuesto, del lenguaje de programación utilizado y de las librerías disponibles para ello.
* Siempre que sea posible, y especialmente para las nuevas aplicaciones o aquellas con una baja tolerancia al riesgo, en lugar de establecer la defensa principal contra los ataques de inyección SQL en el escape de caracteres, se aconseja construir o reescribir el código utilizando medidas de seguridad como sentencias preparadas, procedimientos almacenados o el uso de un ORM que gestione automáticamente la construcción de consultas.

### Principle of Least Privilege (PoLP)

* Para minimizar el daño potencial de un ataque de inyección SQL exitoso es importante mantener los privilegios asignados a cada cuenta de base de datos tan bajos como sea posible. Por lo tanto, es recomendable no asignar derechos de acceso `DBA` o `admin` a las cuentas utilizadas por la aplicación.
* También se recomienda utilizar varios usuarios de base de datos para diferentes aplicaciones web.

### Web Application Firewall (WAF)

* Un `Web Application Firewall (WAF)` es una solución de seguridad diseñada para proteger las aplicaciones web de diversas amenazas y ataques. Se trata de un elemento de red que actúa como un proxy intermediario para proteger al servidor donde se aloja la aplicación web de un cliente potencialmente malicioso mediante la supervisión, el filtrado y el control del tráfico web entrante y saliente en función de un conjunto de políticas.
* Aunque no puede eliminar o resolver la existencia de una vulnerabilidad en una aplicación web, añade una capa adicional de seguridad esencial para dificultar la explotación exitosa de una vulnerabilidad por parte de un actor malicioso.
* Proporciona una protección eficaz no solo contra las inyecciones SQL, sino también contra una serie de ataques de seguridad maliciosos, como Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), Session hijacking, Cookie poisoning, Parameter tampering, ataques de Denegación de Servicio (DoS), etc.

## Test para consolidar :rocket:

* Completa el cuestionario eligiendo la respuesta correcta para cada pregunta.
  @@ExerciseBox@@
