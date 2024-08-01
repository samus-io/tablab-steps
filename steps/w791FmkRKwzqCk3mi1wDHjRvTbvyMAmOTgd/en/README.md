# Finding improper error handling

## Methods to find improper error handling

* **Passing invalid parameter type**: send to the server a parameter with another data type. If the server is waiting for an integer, send a string or boolean. For example, if the server expects an age parameter as an integer, send `twenty` or `true` instead.

* **Application logic break**: try to break the application logic, for example:

  * Send XML when the server expects JSON or vice versa:
  * Send an empty JSON or XML payload to see how the application handles it.
  * Send a malformed JSON or XML to check error handling.

* **HTTP protocol break**: try sending a request that breaks the HTTP protocol. One example would be to send invalid headers format, or invalid HTTP version.  
* **Boundary value analysis**: provide input at the boundary of acceptable values to see if the application handles edge cases correctly. For example, if the application expects an age between 1 and 100, send 0 and 101.
* **Fuzz testing**: use automated tools to send random and malformed data to the application to discover unhandled exceptions. For example, submit multiple random strings to username field and check if it shares the details on existance of that username.
* **Monitoring application behavior**: observe the application's response to unexpected user behavior and inputs to identify areas lacking proper error handling. For example, tracking how the application responds to invalid form submissions.
* **Using invalid credentials**: attempt to authenticate with incorrect credentials to see if error messages expose sensitive information. For example, entering incorrect username and password to check the error message.
* **Resource exhaustion**: try to overwhelm the application by consuming excessive resources (e.g., sending large files, multiple requests) to check how it handles resource limits. For example, uploading a very large file to test resource handling.
* **Injection attacks**: test for various types of injection attacks (e.g., SQL injection, command injection) to see if the application handles and logs errors correctly. For example, sending SQL injection payloads to input fields.
* **Mismatched content types**: send mismatched content types in HTTP headers to see if the application processes and handles the errors gracefully. For example, sending a JSON payload with an `application/xml` content type.
* **Null values**: send null values where the application expects valid data to check if null pointer exceptions or similar errors are properly managed.
* **Invalid URLs**: access invalid or non-existent endpoints to see how the application handles 404 error and other HTTP status codes.
* **Code review**: this can be a time consuming task, but searching the code for error handling logic is another valuable approach.
