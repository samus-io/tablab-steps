# Sentencias preparadas en .NET 8.0 con SQLite

* Las sentencias preparadas proporcionan un método eficiente y seguro para gestionar consultas SQL contra una base de datos, desempeñando un papel crucial en el desarrollo de aplicaciones empresariales robustas y seguras en `.NET`.

## Cómo funcionan las sentencias preparadas con SQLite

* Considerando un escenario que requiera la ejecución de una consulta SQL para recuperar productos filtrados por `category` y `rating`, se pueden seguir los siguientes pasos para conseguirlo con sentencias preparadas:
  1. El objeto `SqliteConnection` dentro de una sentencia `using` puede ser empleado para establecer una conexión. Este enfoque gestiona el ciclo de vida de la conexión de forma automática, reduciendo el riesgo de fuga de recursos, especialmente cuando se producen excepciones:

    ```csharp
    using (SqliteConnection connection = new SqliteConnection("Data Source=/path/to/database")) {
        connection.Open();
        // SQL query
    }
    ```

  1. Seguidamente, es necesario definir la consulta SQL con marcadores de posición (`@`) para los parámetros que se introducirán posteriormente, como `category` y `rating` en este caso:

    ```csharp
    string query = "SELECT id, name, price, category, stock, rating FROM products WHERE category = @Category AND rating >= @Rating";
    ```

  1. Tras definir la consulta SQL, debe crearse un objeto `SqliteCommand` que contenga la consulta y los parámetros deben pasarse mediante el método `AddWithValue`:

    ```csharp
    using (SqliteCommand command = new SqliteCommand(query, connection)) {
        command.Parameters.AddWithValue("@Category", category);
        command.Parameters.AddWithValue("@Rating", rating);

        // Query execution
    }
    ```

  1. Una vez introducidos los parámetros, se puede ejecutar la consulta SQL:

    ```csharp
    SqliteDataReader reader = command.ExecuteReader();

    // Read the SQL query result
    ```

  1. En determinadas situaciones, basta con determinar si el resultado contiene alguna fila o ninguna. Esto puede hacerse utilizando el método `ExecuteScalar`:

    ```csharp
    var result = command.ExecuteScalar();
    if (result == null) {
      // No rows returned
    }
    ```

## Código de cumplimiento usando sentencias preparadas

* El fragmento de código completo que se muestra a continuación ilustra el uso de sentencias preparadas para recuperar productos basándose en `category` y `rating`:

  ```csharp
  public void FindProductsByCategoryAndRating(string category, double rating) {
    try 
    {
      using (SqliteConnection connection = new SqliteConnection("Data Source=/path/to/database")) {
          connection.Open();

          string query = "SELECT id, name, price, category, stock, rating FROM products WHERE category = @Category AND rating >= @Rating";

          using (SqliteCommand command = new SqliteCommand(query, connection)){
              command.Parameters.AddWithValue("@Category", category);
              command.Parameters.AddWithValue("@Rating", rating);

              SqliteDataReader reader = command.ExecuteReader();

              // Read the SQL query result
          }
      }
    }
    catch (Exception ex) {
      Console.WriteLine("Database error: " + ex.Message);
    }
  }
  ```

## Ejercicio para practicar :writing_hand:

* El siguiente formulario de inicio de sesión es susceptible a inyecciones SQL debido a que agrega directamente la entrada del usuario a la consulta SQL.
* El objetivo aquí es editar el código fuente abriendo el editor de código a través del botón `Open Code Editor` y habilitando el uso de sentencias preparadas para eliminar la vulnerabilidad.
  * Más concretamente, el código a modificar se encuentra en el método `ValidateUserCredentials` dentro de la clase `Database`, localizada en `WebApp/Services/DatabaseManager.cs`.
* Después de implementar una solución correcta, prueba rellenando el formulario e introduciendo una carga útil en el campo de contraseña que podría haber explotado previamente la vulnerabilidad, como `' OR 1=1;-- `, comprobando que ya no funciona. Por último, pulsa el botón `Verify Completion` para confirmar que el ejercicio se ha completado.
* ¿Serás capaz de prevenir la vulnerabilidad de inyección SQL implementando el uso de sentencias preparadas? :slightly_smiling_face::muscle:
  @@ExerciseBox@@
