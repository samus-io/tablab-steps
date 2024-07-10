# Introduction to Prepared Statements

* Prepared statements are a critical feature in database management systems that enhance security and performance when executing SQL queries.
* They play a significant role in preventing SQL injection attacks, a common vulnerability in applications that process user input.

## What are Prepared Statements?

* A prepared statement is a precompiled SQL statement designed to be executed multiple times with different parameters.
* Prepared statements improve efficiency because the SQL statement is parsed, compiled, and optimized by the database once, and then executed multiple times with varying parameter values.
* The process involves two main steps:
  * **Preparation**: The SQL statement template is created and sent to the database server. This template contains placeholders for parameters.
  * **Execution**: Parameters are bound to the placeholders, and the statement is executed.

## Limitations of Prepared Statements

* Prepared statements are highly secure and efficient for handling `column` values.
* However, they cannot be used for `dynamic` selection of tables or columns.
* For scenarios requiring dynamic table or column selection in SQL queries, it is necessary to use an `allow-list (whitelist)` to ensure that only permitted values are included in the query.

## Prepared Statements vs. Parameterized Queries

* **Prepared Statements**
  * Precompile the SQL statement once, enabling repeated execution with different parameter values.
  * Enhance performance for repeated query execution due to single-time parsing and compilation.
  * Provide strong protection against SQL injection by clearly separating query structure from data.

* **Parameterized Queries**
  * Allow inclusion of parameters in SQL queries, but each execution requires parsing and compiling the SQL statement.
  * Offer similar security benefits against SQL injection as prepared statements, though with potentially less performance optimization for repeated queries.

## Prepared Statements vs. Stored Procedures

* **Prepared Statements**
  * Precompile a specific SQL statement with placeholders for parameters.
  * Managed at the application level,  facilitating dynamic query execution based on user input.

* **Stored Procedures**
  * Precompiled collections of SQL statements stored within the database.
  * Can include control structures such as loops and conditional statements, allowing more complex logic than a single prepared statement.
  * Managed at the database level, which can enhance security and centralize business logic.

## ORMs and Prepared Statements

* `Object-Relational Mappers (ORMs)` like Sequelize, TypeORM, and Hibernate use prepared statements internally to interact securely with the database.
* ORMs abstract database operations into high-level programming constructs, ensuring safe SQL query generation and execution without direct raw SQL execution by developers.
* This built-in security helps prevent SQL injection vulnerabilities by utilizing prepared statements or parameterized queries.

### Raw SQL Queries in ORMs

* While facilitating flexibility, direct execution of raw SQL queries via ORMs poses security risks if not handled properly.
* Incorporating user inputs into raw SQL queries without adequate sanitization or parameterization can expose vulnerabilities to SQL injection.

### Vulnerability to SQL Injection

* Despite the protective measures provided by ORMs, vulnerabilities persist if raw SQL queries are mishandled.
* Inadequate sanitization or parameterization of user inputs, when directly interpolated into raw SQL queries, heightens the susceptibility to SQL injection attacks.

## Best Practices

* **Prefer ORM Method**s: Opt for ORM methods over direct execution of raw SQL queries whenever feasible.
* **Sanitize User Inputs**: When resorting to raw SQL queries, meticulously sanitize user inputs to thwart potential SQL injection vulnerabilities.
* **Parameterize Queries**: Employ parameterized queries to treat user inputs as data rather than executable SQL code.
* **Avoid Dynamic Queries**: Limit the use of dynamic SQL queries, where user inputs dictate query structure or logic, to mitigate security risks.
