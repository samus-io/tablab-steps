# Prepared Statements in .NET 8.0 with SQLite

* Prepared statements provide an efficient and secure method for managing SQL queries against a database, playing a crucial role in developing robust and secure enterprise applications in `.NET`.

## How prepared statements work with SQLite

* Considering a scenario requiring the execution of an SQL query to retrieve products filtered by `category` and `rating`, the following steps can be used to achieve this with prepared statements:
  1. The `SqliteConnection` object within a `using` statement can be employed to establish a connection. This approach manages the connection lifecycle automatically, reducing the risk of resource leaks, particularly during exceptions:

      ```csharp
      using (SqliteConnection connection = new SqliteConnection("Data Source=/path/to/database")) {
          connection.Open();
          // SQL query
      }
      ```

  1. Next, the SQL query should include placeholders (`@`) for parameters to be added later,  such as `category` and `rating` in this case:

      ```csharp
      string query = "SELECT id, name, price, category, stock, rating FROM products WHERE category = @Category AND rating >= @Rating";
      ```

  1. After defining the SQL query, a `SqliteCommand` object should be created to hold the query, and the parameters should be passed using the `AddWithValue` method:

      ```csharp
      using (SqliteCommand command = new SqliteCommand(query, connection)) {
          command.Parameters.AddWithValue("@Category", category);
          command.Parameters.AddWithValue("@Rating", rating);

          // Query execution
      }
      ```

  1. Once the parameters are set, the SQL query can be executed:

      ```csharp
      SqliteDataReader reader = command.ExecuteReader();

      // Read the SQL query result
      ```

  1. In certain situations, determining whether the result contains any rows or none is sufficient. This can be done using the `ExecuteScalar` method:

      ```csharp
      var result = command.ExecuteScalar();
      if (result == null) {
        // No rows returned
      }
      ```

## Compliant code using prepared statements

* The complete code snippet below illustrates the use of prepared statements for retrieving products based on `category` and `rating`:

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

## Exercise to practice :writing_hand:

* The following login form is susceptible to SQL injection due to directly appending user input to the SQL query.
* The objective here is to edit the source code opening the code editor through the `Open Code Editor` button, and enabling the use of prepared statements to eliminate the vulnerability.
  * More precisely, the code to be modified resides in the method `ValidateUserCredentials` within the `Database` class, located in `WebApp/Services/DatabaseManager.cs`.
* After implementing a correct solution, test it by filling out the form and entering a payload in the password field that could have previously exploited the vulnerability, such as `' OR 1=1;-- `, and verify that no longer works. Finally, press the `Verify Completion` button to confirm that the exercise has been completed.
* Will you be able to prevent the SQL injection flaw by implementing prepared statements? :slightly_smiling_face::muscle:
  @@ExerciseBox@@
