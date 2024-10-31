# Types of SQL injection

* There are some types of SQL injections based on the exploitation method used to carry out the attack.

![Types of SQL Injection][1]

## In-band SQL injections

* `In-band SQL injections` leverage the same channel used to inject the SQL code, i.e. the result of the exploitation is included directly in the response page from the vulnerable web application.
* The most common techniques for this category are `UNION-based` and `Error-based` SQL injections.

### UNION-based SQL injections

* `UNION-based SQL injections` involve the use of the `UNION` operator that combines the results of multiple `SELECT` statements to fetch data from multiple tables as a single result set. The fetched data is appended to the original query.
* Consider the SQL injection payload `new' UNION SELECT username, email, password FROM users; -- -` for the following example:

  ```sql
  SELECT name, description, brand FROM products WHERE status='new' UNION SELECT username, email, password FROM users; -- -' AND taxable = true;
  ```

* A successful `UNION` query requires two conditions to be satisfied:
  * The individual `SELECT` queries must return the same number of columns.
  * The data types in each column must be compatible between the individual queries.

### Error-based SQL injections

* `Error-based SQL injections` occur when an attacker forces the DMBS to output an error message and retrieve data from the errors themselves.
* Consider the SQL injection payload `new' OR user_name()=1;-- -` for the following example:

  ```sql
  SELECT name, description, brand FROM products WHERE status='new' OR user_name()=1; -- - AND taxable = true;
  ```

* Errors could be sent either via the web application output (in-band) or by other means, such as automated reports, log files or warning emails (out-of-band for these last three cases).

## Out-Of-Band (OOB) SQL injections

* Contrary to In-band vectors, `Out-Of-Band (OOB) SQL injections` use alternative channels to extract data from the server, including HTTP requests, DNS resolution, email, file system, other DB connections, etc.

## Inference/Blind SQL injections

* `Blind SQL injections` do not reflect the results of the injection on the output, instead they require you to deduce whether the tested expression succeeded even if no data is returned, simply by observing a difference in the way an application behaves. So, in this case, the attacker must find an inference method to exploit the vulnerability.
* Inference exploitation is carried out mostly by using `Boolean-based` or `Time-based` SQL injections.

### Boolean-based SQL injections

* `Boolean-based SQL injections` rely on sending an SQL query to the database that will return `TRUE` or `FALSE`.
* As an example, the following query determines whether the value length of the `password` field is longer than 5 characters:

  ```sql
  ' or (length((SELECT password FROM users WHERE id=1)) > 5 )
  ```

* Once the query is processed, the content within the HTTP response will be different depending on whether the result is `TRUE` or `FALSE`, and this will cause the application to act differently, which will allow the attacker to infer values stored in the database.

### Time-based SQL injections

* `Time-based SQL injections` rely on sending an SQL query to the database that will force the database to wait a specified amount of time before responding in case some predefined condition matches.
* As an example, the following query forces the DBMS to wait 10 seconds in case the condition is `TRUE`:

  ```sql
  select if((SELECT database()="ecommercedb"), sleep(10), null); -- -
  ```

* The response time will let the attacker to deduce if the query result is `TRUE` or `FALSE`, which will also allow to infer values stored in the database.

## Second-order SQL injections

* `Second-order SQL injections` arise when user-supplied data is stored by the application and later incorporated into SQL queries in an unsafe way:
  1. First, the attacker submits a malicious request.
  1. The application stores that input and responds to the request without presenting any vulnerability.
  1. The attacker submits another request (a second request).
  1. To handle the second request, the application retrieves the previously stored input and processes it. This time, the attacker's injected query is executed.
* The exploit is submitted in one request and triggered when the application handles a different request.
* Modern automated scanners are still unable to perform what is necessary to discover second-order vulnerabilities. This is because there are several possible scenarios, and without an understanding of the meaning and use of data elements within the application, the work involved in detecting second-order SQL injections grows exponentially. The human factor is necessary.

[1]: /static/images/learning/types-of-sql-injection.png
