# Prepared statements using JDBC in Spring Boot 3.5

* Prepared statements are an essential feature of `Java Database Connectivity (JDBC)`, playing a crucial role within Spring Boot for building secure and reliable enterprise applications.
* JDBC acts as the bridge between Java applications and database servers, allowing for the execution of SQL statements, and prepared statements contribute to this functionality by delivering a secure and effective method for handling SQL queries.

## How prepared statements work with SQLite

* Considering a scenario requiring the execution of an SQL query to retrieve products filtered by `category` and `rating`, the following steps can be used to achieve this with prepared statements:
  1. The `Connection` object within a `try-with-resources` statement can be employed to establish a connection. This approach manages the connection lifecycle automatically, reducing the risk of resource leaks, particularly during exceptions:

      ```java
      try (Connection conn = DriverManager.getConnection(URL)) {
        // SQL query
      } catch (SQLException e) {
          throw new RuntimeException(e);
      }
      ```

  1. Next, the SQL query should include placeholders (`?`) for parameters to be added later,  such as `category` and `rating` in this case:

      ```java
      String query = "SELECT id, name, price, category, stock, rating FROM products WHERE category = ? AND rating >= ?";
      ```

  1. After defining the SQL query, a `PreparedStatement` object should be created to hold the query, and the parameters should be passed using `setString` and `setDouble` methods of `PreparedStatement`:

      ```java
      PreparedStatement ps = conn.prepareStatement(query);

      ps.setString(1, category);
      ps.setDouble(2, rating);
      ```

      > :older_man: The setter methods (such as `setString`, `setDouble`, etc.) for assigning parameter values must use types that are compatible with the SQL type specified for the input parameter. For example, if the parameter is defined as an SQL type `INTEGER`, then the `setInt` method should be employed.

  1. Once the parameters are set, the SQL query can be executed:

      ```java
      ResultSet rs = ps.executeQuery();
      ```

## Compliant code using prepared statements

* The complete code snippet below illustrates the use of prepared statements for retrieving products based on `category` and `rating`:

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

## Exercise to practice :writing_hand:

* The following login form is susceptible to SQL injection due to directly appending user input to the SQL query.
* The objective here is to edit the source code opening the code editor through the `Open Code Editor` button, and enabling the use of prepared statements via JDBC to eliminate the vulnerability.
  * More precisely, the code to be modified resides in the static method `loginWithCredentials` within the `Auth` class, located in `src/main/java/io/ontablab/Auth.java`.
* After implementing a correct solution, test it by filling out the form and entering a payload in the password field that could have previously exploited the vulnerability, such as `" OR 1=1;-- `, and verify that no longer works. Finally, press the `Verify Completion` button to confirm that the exercise has been completed.
* Will you be able to prevent the SQL injection flaw by implementing prepared statements? :slightly_smiling_face::muscle:
  @@ExerciseBox@@
