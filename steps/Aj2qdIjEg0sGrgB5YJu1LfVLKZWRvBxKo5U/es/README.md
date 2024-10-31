# Uso de sentencias preparadas con JDBC en Jakarta EE 10.0

* Las sentencias preparadas son una característica clave en `Java Database Connectivity (JDBC)`, especialmente vital en el contexto de Jakarta EE 10.0 para el desarrollo de aplicaciones empresariales robustas y seguras.
* En Jakarta EE, JDBC actúa como un puente entre las aplicaciones Java y los servidores de bases de datos, permitiendo la ejecución de sentencias SQL.
* Las sentencias preparadas mejoran esta funcionalidad al ofrecer una forma eficiente y segura de manejar consultas SQL.

## Ejemplo de sentencias preparadas

* Se considera un escenario donde es necesario ejecutar una consulta SQL para recuperar productos según su categoría y calificación. Para lograr esto mediante sentencias preparadas, se procede con los siguientes pasos.
* Primero, para iniciar una conexión, se utiliza el objeto `Connection` dentro de una declaración `try-with-resources`. Este enfoque maneja automáticamente el cierre de la conexión, previniendo fugas de recursos, especialmente cuando ocurren excepciones.

  ```java
  try (Connection conn = DriverManager.getConnection(URL)) {
    // SQL query
  } catch (SQLException e) {
      throw new RuntimeException(e);
  }
  ```

* Luego, se define la consulta SQL con marcadores de posición (`?`) para los parámetros que se pretenden pasar más adelante, en este caso, se pasarán la categoría y la calificación:

  ```java
  String query = "SELECT id, name, price, category, stock, rating FROM products WHERE category = ? AND rating >= ?";
  ```

* Después de definir la consulta SQL, se crea el objeto `PreparedStatement` que contendrá la consulta SQL y se pasan los parámetros utilizando los métodos `setString` y `setDouble` del `PreparedStatement`:

  ```java
  PreparedStatement ps = conn.prepareStatement(query);
  ps.setString(1, category);
  ps.setDouble(2, rating);
  ```

  > :older_man: Los métodos para asignar valores de parámetros, tales como `setShort`, `setString`, etc., deben usar tipos que sean compatibles con el tipo SQL especificado para el parámetro de entrada. Por ejemplo, si el parámetro está definido como un tipo SQL `INTEGER`, entonces se debe emplear el método `setInt`.

* Una vez establecidos los parámetros, se ejecuta la consulta SQL:

  ```java
  ResultSet rs = ps.executeQuery();
  ```

## Fragmento de código completo

* Aquí se presenta el ejemplo completo que demuestra cómo utilizar sentencias preparadas para obtener productos basados en la categoría y la calificación:

  ```java
  import java.sql.Connection;
  import java.sql.PreparedStatement;
  import java.sql.ResultSet;
  import java.sql.SQLException;
  
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

* El siguiente formulario de inicio de sesión es susceptible a inyecciones SQL debido a que se agrega directamente la entrada del usuario a la consulta SQL.
* El objetivo aquí es editar el código fuente abriendo el editor de código mediante el botón `Open Code Editor` e implementar una estrategia de sentencias preparadas vía JDBC para eliminar la vulnerabilidad.
* Más precisamente, el código a modificar se encuentra en el método estático `loginWithCredentials` de la clase `Auth`, ubicada en `src/main/java/io/ontablab/Auth.java`.
* ¿Serás capaz de prevenir la vulnerabilidad de inyección SQL implementando el uso de sentencias preparadas? :slightly_smiling_face::muscle:
* Una vez creas que has implementado una solución correcta, prueba introduciendo una carga útil que previamente explotaba la vulnerabilidad, como puede ser `" OR 1=1;-- `, y verifica que ya no funciona.
  @@ExerciseBox@@
