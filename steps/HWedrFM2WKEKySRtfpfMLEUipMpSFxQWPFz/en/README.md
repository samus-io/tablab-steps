# Finding SQL injections

* To manually find an SQL injection, first, identify all the points where the application uses user-supplied input to build a query.
* Any of the following may be considered as input:
  * GET/POST parameters.
  * Cookies.
  * HTTP headers: `User-Agent`, `Cookie`, `Accept`, etc.
* Then, try to inject into the input special characters that are known to cause the SQL query to be syntactically invalid, such as:
  * String terminators: `'` or `"`.
  * SQL commands: `SELECT`, `UNION`, and others.
  * SQL comments: `#` or `-- `.
* For each attempt, check if the web application starts to behave oddly.
* It's recommended to test one injection at a time to be able to understand what injection vector is successful.
* Alternatively, you can efficiently discover the majority of SQL injection vulnerabilities by employing an automated tool designed for this purpose, such as [sqlmap][1].

## Signs of a SQL injection found

* The application displays detailed **error messages** after supposedly breaking the SQL query.
* The application takes unusually **long time to respond**, even more after entering SQL commands that cause deliberate delays (for instance, using the `SLEEP` or `BENCHMARK` functions in MySQL).
* The application **acts differently** when injecting boolean conditions.

### Boolean-based detection

* The idea behind this process is simple; try to craft payloads which transform the web application queries into `TRUE`/`FALSE` conditions (e.g. use an SQL payload like `' or 1=1`).
* First, try an always `TRUE` condition:

  ```sql
  SELECT name, email FROM users WHERE id='197' or '1'='1';
  ```

  Later, try an always `FALSE` condition and check if the ouput is the same:

  ```sql
  SELECT name, email FROM users WHERE id='197' or '1'='2';
  ```

  If the web application is vulnerable, it will react differently and return two different outputs (e.g. it changes the text on the web page if the condition is `TRUE` vs if it's `FALSE`).
* If a web application does not display errors on its output consider a Blind SQL injection scenario, where it's still possible to test for SQL injection by using a Boolean-based detection technique.

## Exercise to practice :writing_hand:

* We suspect that the following login form is vulnerable to SQL injection. You can verify it while trying to log in using any random credential of our choice but entering special characters to check if it's possible to manipulate the SQL query that is executed behind the scenes.
* To be clear, this is the pseudocode that is executed on the server when a user tries to log in:

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

* Note that if invalid credentials or an SQL payload that breaks the query incorrectly are entered, no user will be returned from the query and the login form will display a warning message stating `We couldn't match your credentials to a valid account.`.
* Will you be able to find a SQL payload that allows you to log in without knowing any valid credentials? :slightly_smiling_face::muscle:
  @@ExerciseBox@@

[1]: https://sqlmap.org/
