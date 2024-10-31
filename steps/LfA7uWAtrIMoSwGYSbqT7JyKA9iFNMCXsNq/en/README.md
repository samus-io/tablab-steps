# General best practices against SQL injections

* To prevent SQL injection failures, it is crucial to avoid writing dynamic queries using string concatenation and ensure that user-supplied input containing malicious SQL cannot manipulate the query's intended logic.

## Mitigation measures

* Due to the wide variation in the pattern of SQL injection attacks, the following strategies are often unable to protect databases on their own. In order to cover all bases, they must be applied in combination with a WAF.

### Prepared statements

* In a Database Management System (DBMS), a `prepared statement`, `parameterized statement`, or `parameterized query` is a feature that allows the separation of SQL code from user-provided data.
  > While the term `parameterized query` is often used interchangeably with `prepared statement`, it generally refers to the practice of using parameters in SQL queries to make them more flexible and secure.
* A common prepared statement workflow usually involves three steps:
  1. **Prepare**: the application creates the statement template and sends it to the DBMS. Certain values, called _parameters_ or _placeholders_, are left unspecified:

      ```sql
      INSERT INTO products (name, price) VALUES (?, ?);
      ```

  1. **Compile**: the DBMS engine parses, compiles, and optimizes the SQL statement, and then saves the result in a prepared statement object without executing it. This process is performed only once.
  1. **Execute**: using user-provided data, the application supplies (or binds) values for the parameters of the statement template, and the DBMS executes the statement.
* The key advantage of using prepared statements is that parameters are treated as separate entities and not as part of the SQL code. This means that an attacker is not able to change the intent of a query, even if the SQL commands are inserted by an attacker.
  * In the above example, if an attacker attempts to enter as user `id` the value of `197' or '1'='1`, the use of parameterized queries ensures that the input is treated as data rather than executable code. Consequently, the query searches for an `id` that precisely matches the entire string `197' or '1'='1`, making it resistant to SQL injection attacks.
  * This parameterized approach helps protect the system from unauthorized manipulation of the database by treating user inputs as values, not as elements of the SQL query itself.

#### Object-Relational Mapping (ORM)

* Developers can use ORM frameworks to create database queries in a safer and developer-friendly way. ORM libraries avoid the need to write SQL code, since the ORM library generates prepared SQL statements directly from object-oriented code.
* While utilizing ORMs helps to mitigate SQL injection risks by abstracting SQL commands, it's not a foolproof solution. ORMs still construct SQL commands, so developers must implement robust validation to ensure system safety against SQL injections.

### Stored procedures

* With `stored procedures` it's possible to achieve the same approach that `prepared statements` offer.
  * The difference between prepared statements and stored procedures lies in where the SQL code is defined and stored. With stored procedures, the SQL code is defined and stored directly in the database, and the application calls upon it when needed. On the other hand, prepared statements involve defining and preparing SQL queries in the application code before execution.
  * The choice between them often depends on factors such as the architecture of the application and the preferences of the development team.
* However, stored procedures may present a higher risk compared to prepared statements, especially when they require permissions of a different nature in the DBMS to perform the task. This poses a danger in case of compromise, as the attacker would have more privileges and possibilities to perform more advanced actions.

### Allow-list input validation

* `Allow-list input validation` is the practice of only accepting as input a set of explicitly permitted values while all other unspecified values are implicitly disallowed.
* This is especially useful when dynamic SQL queries must be defined and where the values required to be dynamic cannot be set as parameters, such as table names or the sort order indicator (`ASC` or `DESC`). In this case, input validation or a full query redesign is the best bet to mitigate injection attacks.
* The code below shows how to carry out table name validation:

  ```php
  switch ($tableName) {
    case "fooTable": return true;
    case "barTable": return true;
    default: return new BadMessageException("Unexpected value provided as table name");
  }
  ```

* To handle a basic task like sorting, user input can be converted directly into a boolean. Then, use this boolean to choose a secure value to add to the query:

  ```sql
  "SELECT * FROM products ORDER BY price " + ($sortOrder ? "ASC" : "DESC");
  ```

### Escaping all user-supplied input

* This process consists of trying to escape all characters that have a special meaning in SQL from the user-supplied input and before this data is added into the database query.
* This mechanism can vary depending on the specific database and, of course, the programming language used and the libraries available for this purpose.
* Whenever possible and especially for new applications or those with a low tolerance for risk, instead of setting the primary defense against SQL injection attacks on character escaping, it is advised to construct or rewrite the code using security measures such as parameterized queries, stored procedures, or an ORM that automatically handles query construction.

### Principle of Least Privilege (PoLP)

* To minimize the potential damage of a successful SQL injection attack, it is important to keep the privileges assigned to each database account in the environment as low as possible. Therefore, do not assign `DBA` or `admin` access rights to accounts used by the application.
* It's also recommended to use multiple database users for different web applications.

### Web Application Firewall (WAF)

* A `Web Application Firewall (WAF)` is a security solution designed to protect web applications from various threats and attacks. It acts as an intermediary proxy that protects the web application server from a potentially malicious client by monitoring, filtering and controlling incoming and outgoing web traffic based on a set of policies.
* Although it cannot eliminate or resolve the existence of a vulnerability in a web application, it adds an additional layer of security essential to hinder the successful exploitation of a vulnerability by a malicious actor.
* It provides efficient protection not only for SQL injections but from a number of malicious security attacks such as Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), Session hijacking, Cookie poisoning, Parameter tampering, Denial of Service (DoS) attacks, etc.

## Quiz to consolidate :rocket:

* Complete the questionnaire by choosing the correct answer for each question.
  @@ExerciseBox@@
