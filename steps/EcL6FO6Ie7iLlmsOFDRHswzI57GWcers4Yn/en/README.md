# Information disclosure via error pages in Apache 2.4

* Error pages, whether default or misconfigured, can unintentionally expose sensitive details that attackers might exploit. These leaks fall under information disclosure vulnerabilities.
* Common error pages like `404 Not Found` or `500 Internal Server Error` may reveal server details, including the type and version of software in use, such as Apache or Nginx.
* Some error messages expose internal directory structures or file names. For example, a missing resource message might state `File /var/www/html/app/secrets.txt not found`, unintentionally revealing server paths and possibly sensitive files.
* Attackers can use this information to identify vulnerabilities, target outdated software, or map the system architecture for further exploitation.

## Prevention techniques

* Custom error pages should be implemented to prevent default error messages from exposing sensitive system details, as default error pages often reveal sensitive information.
* These pages should be generic and user-friendly, ensuring they do not disclose specifics about the server, application framework, or software versions.
* The following HTML code represents a simple custom error page that can be used to handle errors in a web application:

  ```html
  <!DOCTYPE html>
  <html>
    <head>
      <title>Error</title>
    </head>
    <body>
      <h1>Sorry, an error has occurred.</h1>
      <p>Code error: %{STATUS}</p>
      <p>URL requested: %{REQUEST_URI}</p>
      <p>Please try again later.</p>
    </body>
  </html>
  ```

* In this example, `STATUS` corresponds to the HTTP status code returned by the server and `REQUEST_URI` the URL of the server. While these variables can be used to provide additional context, they are not strictly necessary.

* Apache provides multiple ways to configure custom error pages, allowing better control over how errors are displayed to users.
* Each HTTP status code can have its own dedicated error page, ensuring specific messages for different types of errors:

  ```apacheconf
  ErrorDocument 404 /path/to/file/error404.html
  ErrorDocument 403 /path/to/file/error403.html
  ErrorDocument 500 /path/to/file/error500.html
  ```

* Also, a single generic error page can also be used for a range of error codes, simplifying configuration:

  ```apacheconf
  ErrorDocument 400-599 /path/to/file/error.html
  ```

* Both approaches can be combined, allowing customized handling for specific errors while using a general page for others.
* For example, one error page can be assigned to all `4XX` HTTP client errors and another to `5XX` HTTP server errors.
