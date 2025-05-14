# Enforcing CORS in Apache

* `Cross-Origin Resource Sharing (CORS)` enforcement in Apache involves explicitly configuring allowed origins, methods, and headers using the `mod_headers` module to control cross-origin access to specific endpoints.

## Apache configuration files overview

* Apache configuration may be handled through various files, such as `apache2.conf` or `httpd.conf`, depending on the operating system.
  * In Linux systems, these files are usually located in `/etc/apache2` or `/etc/httpd`, and in Windows in `C:\Program Files (x86)\Apache Group\Apache2`.
  * The file `/etc/apache2/apache2.conf` usually serves as the default global configuration on many Linux systems.
* When virtual hosts are used to run multiple applications on a single web server, changes to global configuration files will impact all of them. Therefore, to target a specific web application, it's preferable to modify the relevant file in the `sites-available` directory, which contains individual application configurations.
* Apache can also be configured using `.htaccess` files, which follow the same format as other config files but apply only to the directories in which they are located.

## Adding CORS headers to Apache web server

* Headers can be set easily in Apache using the `mod_headers` module. To activate it, execute the commands below on the server and restart Apache.

  ```bash
  sudo a2enmod headers
  sudo service apache2 restart
  ```

  * Once the module is enabled, headers can be configured by editing the appropriate Apache configuration file.
* As example, to include the `Access-Control-Allow-Origin` response header, the following directive should be placed in the correct configuration file:

  ```apacheconf
  Header always set Access-Control-Allow-Origin "https://example.tbl"
  ```

  * This configuration instructs the server to send the `Access-Control-Allow-Origin` header with the value `https://example.tbl`.
* Once the changes are made, Apache must be restarted to apply the new configuration:

  ```bash
  sudo service apache2 reload
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

* **Note that the module `mod_headers` has been already activated and no action is required.**
* Once done, press the `Verify Completion` button to confirm the exercise has been successfully completed.

  @@ExerciseBox@@
