# Enforcing CORS in Nginx

* Nginx enforces CORS by adding precise HTTP headers that define which origins, methods, and headers are allowed in cross-origin requests.

## Adding CORS headers to Nginx web server

* Adding headers in Nginx is straightforward, as it doesn't need additional modules.
* As example, to include the `Access-Control-Allow-Origin` header, the following directive should be added inside the `server` block of the configuration file:

  ```nginx
  server {
    add_header Access-Control-Allow-Origin "https://example.tbl" always;
  }
  ```

  * This configuration instructs the server to send the `Access-Control-Allow-Origin` header with the value `https://example.tbl`.
* Once the changes are made, Nginx must be reloaded to apply the new configuration:

  ```bash
  sudo service nginx reload
  ```

## Exercise to practice :writing_hand:

* The application below provides a basic API for products, where a product can be retrieved via a `GET` request to `/api/products/:id` and removed with a `DELETE` request to the same endpoint.
  * This behavior can be tested in the terminal below by sending appropriate requests with the `curl` command line tool:

    ```bash
    curl -X GET $APP_URL/api/products/1; echo
    ```

    ```bash
    curl -X DELETE $APP_URL/api/products/1; echo
    ```

    * Notice that `$APP_URL` is an environment variable that points to the base path of the application.

* The goal here is to to update the source code via the `Open Code Editor` button and apply the CORS mechanism while fulfilling the outlined requirements:
  * The only allowed origin must be `https://example.tbl`.
  * The only allowed HTTP method must be `DELETE`.
  * A custom header named `X-CSRF-Token` must be allowed.
  * The application must correctly handle preflight requests for the `DELETE /api/products/:id` endpoint by allowing HTTP `OPTIONS` requests.
* After implementing the changes and redeploying the app, use `curl` to send requests and review the HTTP response headers for manual validation:

  ```bash
  curl -sS -X OPTIONS "$APP_URL" -i -H "Origin: https://example.tbl" -H "Access-Control-Request-Method: DELETE" | grep -i '^access-control-'
  ```

  * `-s` indicates silent mode (no progress meter) and `-S` shows errors if they happen (overrides silent suppression).
  * `-X OPTIONS` tells `curl` to use the `OPTIONS` HTTP method.
  * `-i` includes response headers in the output.
  * `-H "Origin: https://example.tbl"` simulates a cross-origin request.
  * `-H "Access-Control-Request-Method: DELETE"` mimics a preflight request to ask if DELETE is allowed.
  * `grep -i '^access-control-'` filters only headers that start with `access-control-` (case-insensitive).

  This is the expected result upon executing the command above:

    ```bash
    access-control-allow-origin: https://example.tbl
    access-control-allow-methods: DELETE
    access-control-allow-headers: X-CSRF-Token
    ```

* Once done, press the `Verify Completion` button to confirm the exercise has been successfully completed.

  @@ExerciseBox@@
