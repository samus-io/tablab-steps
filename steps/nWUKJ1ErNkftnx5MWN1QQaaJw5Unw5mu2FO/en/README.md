# Prepared statements in Laravel 11.3

* Prepared statements provide an efficient and secure method for managing SQL queries against a database, playing a crucial role in developing robust and secure enterprise applications in `PHP`.

## How prepared statements work

* Considering a scenario requiring the execution of an SQL query to retrieve products filtered by `category` and `rating`, the following steps can be used to achieve this with prepared statements:
  1. The SQL query should include placeholders (`?`) for parameters to be added later,  such as `category` and `rating` in this case:

      ```php
      $query = "SELECT id, name, price, category, stock, rating FROM products WHERE category = ? AND rating >= ?";
      ```

  1. After defining the SQL query, the `DB` facade should be used to execute the query, and the parameters should be passed:

      ```php
      $result = DB::select($query, [$category, $rating]);
      ```

> :older_man: In a Laravel application, a facade is a structural design pattern that provides a simple, static interface to access an underlying class or service within the Laravel application. Facades act as a "wrapper" around complex logic, making it easier to call methods of various classes in Laravel's service container.

## Compliant code using prepared statements

* The complete code snippet below illustrates the use of prepared statements for retrieving products based on `category` and `rating`:

  <details>
    <summary>Dependencies</summary>

    ```php
    use Illuminate\Support\Facades\DB;
    ```
  
  </details>

  ```php
  public function findProductsByCategoryAndRating($category, $rating)
  {
    $query = "SELECT id, name, price, category, stock, rating FROM products WHERE category = ? AND rating >= ?";

    $result = DB::select($query, [$category, $rating]);

    // Read the SQL query result
  }
  ```

## Exercise to practice :writing_hand:

* The following login form is susceptible to SQL injection due to directly appending user input to the SQL query.
* The objective here is to edit the source code opening the code editor through the `Open Code Editor` button, and enabling the use of prepared statements to eliminate the vulnerability.
  * More precisely, the code to be modified resides in the method `loginWithCredentials` within the `AuthService` class, located in `app/Services/AuthService.php`.
* After implementing a correct solution, test it by filling out the form and entering a payload in the password field that could have previously exploited the vulnerability, such as `' OR 1=1;-- `, and verify that no longer works. Finally, press the `Verify Completion` button to confirm that the exercise has been completed.
* Will you be able to prevent the SQL injection flaw by implementing prepared statements? :slightly_smiling_face::muscle:
  @@ExerciseBox@@