# Prepared statements using SQLite in .NET 8.0

* Prepared statements are a key feature in `SQLite`, particularly vital within the context of `.NET` for developing robust and secure enterprise applications.
* Prepared statements enhance this functionality by offering an efficient and secure way to handle SQL queries.

## Example of prepared statements

* Consider a scenario where we need to execute an SQL query to retrieve products filtered by category and rating. To accomplish this using prepared statements, we can proceed with the following steps.
* First, to initiate a connection, use the `SqliteConnection` object within a `using` statement. This approach automatically handles closing the connection, thus preventing resource leaks, especially when exceptions occur.
  
  ```csharp
  using (SqliteConnection connection = new SqliteConnection("Data Source=/path/to/database")) {
      connection.Open();
      // SQL query
  }
  ```

* Then, define your SQL query with parameters using placefolders (`@`) for parameters you intend to pass later, in this case, we will pass the category and rating:

  ```csharp
  string query = "SELECT id, name, price, category, stock, rating FROM products WHERE category = @Category AND rating >= @Rating";
  ```

* After defining the SQL query, create a `SqliteCommand` object that will contain the SQL query and pass the parameters using `AddWithValue` method:

  ```csharp
  using (SqliteCommand command = new SqliteCommand(query, connection)){
      command.Parameters.AddWithValue("@Category", category);
      command.Parameters.AddWithValue("@Rating", rating);

      // Query execution
  }
  ```

* With the parameters set, execute the SQL query:

  ```csharp
  SqliteDataReader reader = command.ExecuteReader();

  // Read the SQL query result
  ```

* In some cases, it is only necessary to know whether the result has returned any rows or no rows at all. To achieve this it is possible to execute the `ExecuteScalar` method:
  
  ```csharp
  var result = command.ExecuteScalar();
  if (result == null) {
    // No rows returned
  }
  ```

## Complete code snippet

* Here is the complete example demonstrating how to use prepared statements to fetch products based on category and rating:

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
* More precisely, the code to be modified resides in the static method `ValidateUserCredentials` within the `Database` class, located in `WebApp/Services/DatabaseManager.cs`.
* Will you be able to prevent the SQL injection flaw by implementing prepared statements? :slightly_smiling_face::muscle:
* Once you believe you've implemented a correct solution, test it by introducing a payload that previously exploited the vulnerability, such as `" OR 1=1;-- `, and verify that no longer works.
  @@ExerciseBox@@
