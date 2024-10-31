# Identificar inyecciones SQL

* Para encontrar manualmente una inyección SQL, en primer lugar, es necesario identificar todos los puntos en los que la aplicación utiliza datos proporcionados por el usuario para construir una consulta.
* Cualquiera de los siguientes puede considerarse como entrada de datos:
  * Parámetros GET/POST.
  * Cookies.
  * Cabeceras HTTP: `User-Agent`,   `Cookie`,   `Accept`, etc.
* A continuación, el siguiente paso es intentar inyectar como datos de entrada caracteres especiales que se conoce que provocan que la consulta SQL sea sintácticamente inválida, como:
  * Terminadores de cadena: `'` o `"`.
  * Comandos SQL: `SELECT`,   `UNION`, entre otros.
  * Comentarios SQL: `#` o `-- `.
* En cada intento, se debe comprobar si la aplicación web empieza a comportarse de forma extraña.
* Se recomienda probar una inyección a la vez para entender más fácilmente qué vector de inyección tiene éxito.
* Alternativamente, es posible descubrir de una forma eficaz la mayoría de las vulnerabilidades de inyección SQL empleando una herramienta automatizada diseñada para este fin, como puede ser [sqlmap][1].

## Señales de la presencia de una inyección SQL

* La aplicación muestra **mensajes de error** detallados después de romper supuestamente la consulta SQL.
* La aplicación tarda **mucho tiempo en responder**, aún más después de introducir comandos SQL que causan retrasos deliberados (por ejemplo, utilizando las funciones `SLEEP` o `BENCHMARK` en MySQL).
* La aplicación **actúa de forma diferente** cuando se inyectan condiciones booleanas.

## Detección basada en boolean

* La idea detrás de este proceso es simple; crear payloads que transformen las consultas de la aplicación web en condiciones `TRUE`/`FALSE`. Primero, se puede probar una condición siempre verdadera:

  ```sql
  SELECT name, email FROM users WHERE id='197' or '1'='1';
  ```

  Seguidamente, con una condición siempre falsa para observar si la salida es la misma:

  ```sql
  SELECT name, email FROM users WHERE id='197' or '1'='2';
  ```

  Si la aplicación web es vulnerable, reaccionará de forma diferente y devolverá dos salidas distintas (por ejemplo, cambiará el texto de la página web si la condición es `TRUE` frente a si es `FALSE`).

* Si una aplicación web no muestra errores en su salida, entonces se puede considerar un escenario de inyección SQL Blind, donde todavía es posible identificar la inyección SQL utilizando una técnica de detección basada en booleanos como la presente.

## Ejercicio para practicar :writing_hand:

* Se sospecha que el siguiente formulario de login es vulnerable a inyección SQL. Intenta iniciar sesión utilizando cualquier tipo de credenciales de tu elección pero introduciendo caracteres especiales para intentar manipular la consulta SQL que se ejecuta en segundo plano.
* Para que quede claro, este es el pseudocódigo que se ejecuta en el servidor cuando un usuario intenta iniciar sesión:

  ```javascript
    function login(username, password) {
        query = `SELECT * FROM User WHERE username = "${username}" AND password = "${password}"`;
        user = database.execute(query);

        if (user) {
            return true;
        } else {
            return "We couldn't match your credentials to a valid account."
        }
    }
  ```

* Ten en cuenta que si se ingresan credenciales no válidas o una carga útil SQL que rompe la consulta incorrectamente, no se devolverá ningún usuario de la consulta y el formulario de inicio de sesión mostrará un mensaje de advertencia que menciona `We couldn't match your credentials to a valid account.`.
* ¿Serás capaz de encontrar una carga útil SQL que te permita iniciar sesión sin llegar a conocer ninguna credencial válida? :slightly_smiling_face::muscle:
  @@ExerciseBox@@

[1]: https://sqlmap.org/
