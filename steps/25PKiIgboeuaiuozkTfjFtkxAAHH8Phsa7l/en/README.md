# Prepared statements in Ruby on Rails 8

* Prepared statements provide an efficient and secure method for managing SQL queries against a database, playing a crucial role in developing robust and secure enterprise applications written in Ruby on Rails.

## How prepared statements works

* Considering a scenario requiring the execution of an SQL query to retrieve products filtered by `category` and `rating`, the following basic steps can be used to achieve this with prepared statements:
  1. Start by creating the SQL query with parameter placeholders (`?`), as seen with `category` and `rating` in this case:
  
     ```rb
     query = "SELECT id, name, price, category, stock, rating FROM products WHERE category = ? AND rating >= ?"
     ```

  1. After defining the SQL query, prepare an ordered array of variables to pass to the parameters, ensuring the first parameter corresponds to the first array element:

     ```rb
     params = [category, rating]
     ```

  1. Once the parameters are set, the SQL query can be executed:

     ```rb
     result = ActiveRecord::Base.connection.exec_query(query, "SQL", params)
     ```

## Compliant code using prepared statements

* The complete code snippet below illustrates the use of prepared statements for retrieving products based on `category` and `rating`:

  ```rb
  def findProductsByCategoryAndRating(category, rating)
    query = "SELECT id, name, price, category, stock, rating FROM products WHERE category = ? AND rating >= ?"
    params = [category, rating]
    
    result = ActiveRecord::Base.connection.exec_query(query, "SQL", params)
    
    # Read the SQL query result
  end
  ```

## Exercise to practice :writing_hand:

* The following login form is susceptible to SQL injection due to directly appending user input to the SQL query.
* The objective here is to edit the source code opening the code editor through the `Open Code Editor` button, and enabling the use of prepared statements to eliminate the vulnerability.
  * More precisely, the code to be modified resides in the method `loginWithCredentials` within the `AuthService` class, located in `app/services/AuthService.rb`.
* After implementing a correct solution, test it by filling out the form and entering a payload in the password field that could have previously exploited the vulnerability, such as `' OR 1=1;-- `, and verify that no longer works. Finally, press the `Verify Completion` button to confirm that the exercise has been completed.
* Will you be able to prevent the SQL injection flaw by implementing prepared statements? :slightly_smiling_face::muscle:
  @@ExerciseBox@@
