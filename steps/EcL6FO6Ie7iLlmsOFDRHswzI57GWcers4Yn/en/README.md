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
      <p>Please try again later or reach out to our support team.</p>
    </body>
  </html>
  ```

### Custom error pages in Apache

* Apache provides multiple ways to configure custom error pages, allowing better control over how errors are displayed to users. Each HTTP status code can have its own dedicated error page, ensuring specific messages for different types of errors:

  ```apache
  ErrorDocument 404 /path/to/file/error404.html
  ErrorDocument 500 /path/to/file/error500.html
  ```

  * Note that the path must be relative, not absolute. It should be relative to Apache's root directory where the application is hosted (e.g., `/var/www/data/`).
* Additionally, one error page, like `error5XX.html`, may also be used for multiple error codes:

  ```apache
  ErrorDocument 500 /path/to/file/error5XX.html
  ErrorDocument 501 /path/to/file/error5XX.html
  ErrorDocument 502 /path/to/file/error5XX.html
  ErrorDocument 503 /path/to/file/error5XX.html
  ...
  ```

* Both approaches can be combined, allowing customized handling for specific errors while using a general page for others.
  * Typically, distinct error pages are used for various 4XX HTTP client errors, while one unified page is applied to all 5XX HTTP server errors.

## Exercise to practice :writing_hand:

* The following application does not apply any custom error page, causing the default web server error page to be shown and revealing the server version and operating system.
* The goal here is to adjust the Apache configuration through the code editor accessed using the `Open Code Editor` button, modifying the `apache.conf` file to display `404.html` for the `404 Not Found` HTTP error and `5XX.html` for all 5XX errors from 500 to 511, excluding 509, which does not exist.
  * The paths `/404.html` and `/5XX.html` are valid references for being used within the configuration file.
  * Additionally, these files must contain appropriate error page content written in HTML.
* The behavior can be tested through the simulated browser by visiting `/404` to induce a `404 Not Found` response, `/500` to cause a `500 Internal Server Error`, and subsequent codes accordingly.
* After making the changes, press the `Verify Completion` button to confirm the exercise has been completed.

  @@ExerciseBox@@
