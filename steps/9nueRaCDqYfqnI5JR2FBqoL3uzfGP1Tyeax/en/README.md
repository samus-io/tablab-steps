# Information disclosure via error messages

* Information disclosure via error messages occurs when applications expose sensitive information to users through error messages.
* This typically occurs as a result of improper handling of errors and exceptions in the code, which can inadvertently expose the stack trace, framework details, system information, user data, or other sensitive content.
* Such disclosures can provide attackers with insights to understand the system's architecture and identify potential weaknesses to exploit.

## How this type of information disclosure arise?

* When applications send detailed user error messages, such as `User does not exist` or `Username found, but incorrect password`, these can help an attacker determine valid user accounts or other system details.
* When unexpected events occur and the application displays error messages with stack traces, database dumps, or code snippets can inadvertently reveal underlying software architecture, database schemas, or configuration details.
  * Error messages containing SQL errors, unhandled exceptions, or file paths can leak internal details. Examples of messages that should not be sent to the user include:

    ```sql
    SQL syntax error near 'user_input' in query SELECT * FROM users WHERE username = 'user_input'.
    ```

    ```java
    NullReferenceException: Object reference not set to an instance of an object at Project.Service.Authentication.CheckUser(String username, String password).
    ```

    ```java
    File not found at "C:\Program Files\MyApp\config.xml".
    ```

* Furthermore, insufficient input validation may result in errors when users enter unexpected values or data types, potentially producing error messages that expose system internals or logic. Examples of such messages that should not be shown to users include:

  ```plaintext
  The input 'abc123' is invalid for field 'age', expected type integer.
  ```

  ```plaintext
  XML parser error: element 'login' is not recognized.
  ```

## Recommended security approaches

* Instead of displaying the default error to users, **adopt a generic error message strategy**, such as 'Internal Server Error' or 'Oops, an error occurred, please try again'.
* **Develop a custom error handling mechanism** that intercepts and logs all uncaught errors and exceptions, safeguarding sensitive information from end user exposure.
* **Ensure comprehensive input validation is in place** to avoid errors that could potentially disclose internal system details via exception messages.
