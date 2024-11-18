# Prepared statements using JDBC in Spring Boot 3.5

* Prepared statements are a key feature in `Java Database Connectivity (JDBC)`, particularly vital within the context of Spring Boot for developing robust and secure enterprise applications.
* In Spring Boot, JDBC acts as the bridge between Java applications and database servers, allowing for the execution of SQL statements.
* Prepared statements enhance this functionality by offering an efficient and secure way to handle SQL queries.

## Example of prepared statements

* Consider a scenario where we need to execute an SQL query to retrieve products filtered by category and rating. To accomplish this using prepared statements, we can proceed with the following steps.
* First, to initiate a connection, use the `Connection` object within a `try-with-resources` statement. This approach automatically handles closing the connection, thus preventing resource leaks, especially when exceptions occur.

  ```java
  try (Connection conn = DriverManager.getConnection(URL)) {
    // SQL query
  } catch (SQLException e) {
      throw new RuntimeException(e);
  }
  ```

* Then, define your SQL query with placeholders (`?`) for parameters you intend to pass later, in this case, we will pass the category and rating:

  ```java
  String query = "SELECT id, name, price, category, stock, rating FROM products WHERE category = ? AND rating >= ?";
  ```

* After defining the SQL query, create a `PreparedStatement` object that will contain the SQL query and pass the parameters using `setString` and `setDouble` methods of `PreparedStatement`:

  ```java
  PreparedStatement ps = conn.prepareStatement(query);
  ps.setString(1, category);
  ps.setDouble(2, rating);
  ```

  > :older_man: The setter methods (such as `setShort`, `setString`, etc.) for assigning parameter values must use types that are compatible with the SQL type specified for the input parameter. For example, if the parameter is defined as an SQL type `INTEGER`, then the `setInt` method should be employed.

* With the parameters set, execute the SQL query:

  ```java
  ResultSet rs = ps.executeQuery();
  ```

## Complete code snippet

* Here is the complete example demonstrating how to use prepared statements to fetch products based on category and rating:

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

## Exercise to practice :writing_hand:

* The following login form is susceptible to SQL injection due to directly appending user input to the SQL query.
* The objective here is to edit the source code opening the code editor through the `Open Code Editor` button, and enabling the use of prepared statements via JDBC to eliminate the vulnerability.
* More precisely, the code to be modified resides in the static method `loginWithCredentials` within the `Auth` class, located in `src/main/java/io/ontablab/Auth.java`.
* Will you be able to prevent the SQL injection flaw by implementing prepared statements? :slightly_smiling_face::muscle:
* Once you believe you've implemented a correct solution, test it by introducing a payload that previously exploited the vulnerability, such as `" OR 1=1;-- `, and verify that no longer works.
  @@ExerciseBox@@
