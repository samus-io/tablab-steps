# Uso de sentencias preparadas con JDBC en Jakarta EE 10.0

* Las sentencias preparadas son una característica esencial de `Java Database Connectivity (JDBC)` y desempeñan un papel crucial en Jakarta EE para crear aplicaciones empresariales seguras y fiables.
* JDBC actúa como puente entre las aplicaciones Java y los servidores de bases de datos, permitiendo la ejecución de sentencias SQL, y las sentencias preparadas contribuyen a esta funcionalidad ofreciendo un método seguro y eficaz para gestionar las consultas SQL.

## Cómo funcionan las sentencias preparadas con SQLite

* Considerando un escenario que requiera la ejecución de una consulta SQL para recuperar productos filtrados por `category` y `rating`, se pueden seguir los siguientes pasos para conseguirlo con sentencias preparadas:
  1. El objeto `Connection` dentro de una sentencia `try-with-resources` puede ser empleado para establecer una conexión. Este enfoque gestiona el ciclo de vida de la conexión de forma automática, reduciendo el riesgo de fuga de recursos, especialmente cuando se producen excepciones:

      ```java
      try (Connection conn = DriverManager.getConnection(URL)) {
        // SQL query
      } catch (SQLException e) {
          throw new RuntimeException(e);
      }
      ```

  1. Seguidamente, es necesario definir la consulta SQL con marcadores de posición (`?`) para los parámetros que se introducirán posteriormente, como `category` y `rating` en este caso:

      ```java
      String query = "SELECT id, name, price, category, stock, rating FROM products WHERE category = ? AND rating >= ?";
      ```

  1. Tras definir la consulta SQL, debe crearse un objeto `PreparedStatement` que contenga la consulta y los parámetros deben pasarse utilizando los métodos `setString` y `setDouble` de `PreparedStatement`:

      ```java
      PreparedStatement ps = conn.prepareStatement(query);
    
      ps.setString(1, category);
      ps.setDouble(2, rating);
      ```

      > :older_man: Los métodos para asignar valores de parámetros, tales como `setString`, `setDouble`, etc., deben usar tipos que sean compatibles con el tipo SQL especificado para el parámetro de entrada. Por ejemplo, si el parámetro está definido como un tipo SQL `INTEGER`, entonces se debe emplear el método `setInt`.

  1. Una vez introducidos los parámetros, se puede ejecutar la consulta SQL:

      ```java
      ResultSet rs = ps.executeQuery();
      ```

## Código de cumplimiento usando sentencias preparadas

* El fragmento de código completo que se muestra a continuación ilustra el uso de sentencias preparadas para recuperar productos basándose en `category` y `rating`:

  <details>
    <summary>Dependencies</summary>

    ```java
    import java.sql.Connection;
    import java.sql.PreparedStatement;
    import java.sql.ResultSet;
    import java.sql.SQLException;
    ```

  </details>
  
  ```java  
  public void findProductsByCategoryAndRating(String category, double rating) {
    try (Connection conn = DriverManager.getConnection(URL)) {
        String query = "SELECT id, name, price, category, stock, rating FROM products WHERE category=? AND rating >= ?";

        PreparedStatement ps = conn.prepareStatement(query);
        ps.setString(1, category);
        ps.setDouble(2, rating);

        ResultSet rs = ps.executeQuery();

        // Process the query

        ps.close();
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
  }
  ```

## Ejercicio para practicar :writing_hand:

* El siguiente formulario de inicio de sesión es susceptible a inyecciones SQL debido a que agrega directamente la entrada del usuario a la consulta SQL.
* El objetivo aquí es editar el código fuente abriendo el editor de código a través del botón `Open Code Editor` y habilitando el uso de sentencias preparadas vía JDBC para eliminar la vulnerabilidad.
  * Más concretamente, el código a modificar se encuentra en el método `loginWithCredentials` dentro de la clase `Auth`, localizada en `src/main/java/io/ontablab/Auth.java`.
* Después de implementar una solución correcta, prueba rellenando el formulario e introduciendo una carga útil en el campo de contraseña que podría haber explotado previamente la vulnerabilidad, como `" OR 1=1;-- `, comprobando que ya no funciona. Por último, pulsa el botón `Verify Completion` para confirmar que el ejercicio se ha completado.
* ¿Serás capaz de prevenir la vulnerabilidad de inyección SQL implementando el uso de sentencias preparadas? :slightly_smiling_face::muscle:
  @@ExerciseBox@@
