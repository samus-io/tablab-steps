# X-Content-Type-Options header basics

* The `X-Content-Type-Options` response header forces browsers to use the `Content-Type` sent by the web server and prevent the browser from interpreting a different `Content-Type`.

> :older_man: The `Content-Type` response header indicates what type of content the server response is sending, such as `text/html` for HTML content or `application/json` for JSON.

* Preventing user browsers from interpreting a different `Content-Type` than intended can sometimes prevent client-side vulnerabilities.
* This header has only one directive, so the implementation of this would look like this:

  ```
  X-Content-Type-Options: nosniff
  ```
