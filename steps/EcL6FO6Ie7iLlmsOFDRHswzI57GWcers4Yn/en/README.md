# Information disclosure via error pages in Apache 2.4

* Error pages, whether default or misconfigured, can unintentionally expose sensitive details that attackers could leverage. These leaks fall under information disclosure vulnerabilities.
  * Common error pages like `404 Not Found` or `500 Internal Server Error` may reveal server details, including the type and version of software in use, such as Apache, Nginx or any other web server.
  * Some error messages can expose internal directory structures or file names. For example, a missing resource message might state `File /var/www/html/app/secrets.txt not found`, unintentionally revealing server paths and possibly sensitive files.
* Attackers can use this information to identify vulnerabilities, target outdated software, or map the system architecture for further exploitation.

## Recommended security approaches

* Custom error pages should be implemented to prevent default error messages from exposing sensitive system details, as default error pages often reveal sensitive information.
* These pages should be generic and user-friendly, ensuring they do not disclose specifics about the server, application framework, or software versions.
* The following HTML code represents a simple custom error page that can be used to handle errors in a web application:

  ```html
  <!DOCTYPE html>
  <html>
    <head>
      <title>Oops, something went wrong</title>
    </head>
    <body>
      <h1>Sorry, an error has occurred.</h1>
      <p>URL requested: %{REQUEST_URI}</p>
      <p>HTTP error code: %{STATUS}</p>
      <p>Please try again later or reach out to our support team.</p>
    </body>
  </html>
  ```

  * In this example, `REQUEST_URI` is the URL requested, and `STATUS` represents the HTTP status code returned by the server. These variables can offer extra context but are not strictly required.

### Custom error pages in Apache

* Apache provides multiple ways to configure custom error pages, allowing better control over how errors are displayed to users. Each HTTP status code can have its own dedicated error page, ensuring specific messages for different types of errors:

  ```apache
  ErrorDocument 404 /path/to/file/error404.html
  ErrorDocument 403 /path/to/file/error403.html
  ErrorDocument 500 /path/to/file/error500.html
  ```

* Additionally, a single generic error page may also be used for multiple error codes, streamlining the configuration process:

  ```apache
  ErrorDocument 400-599 /path/to/file/error.html
  ```

* Both approaches can be combined, allowing customized handling for specific errors while using a general page for others.
  * For instance, a multiple error pages can be used for 4XX HTTP client errors, while a single one can handle all 5XX HTTP server errors.
