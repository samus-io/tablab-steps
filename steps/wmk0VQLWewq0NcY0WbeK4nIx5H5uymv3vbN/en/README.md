# Enforcing CORS in Apache

## Apache configuration files

* The configuration of Apache can be managed from different configuration files, depending on the operating system it can be the file `apache2.conf` or `httpd.conf`.
* In Linux systems, these files are typically found in `/etc/apache2` or `/etc/httpd`, while in Windows they may be under `C:\Program Files (x86)\Apache Group\Apache2`.
  * The default global configuration file is usually located at `/etc/apache2/apache2.conf` on most Linux distributions
* When using Virtual Hosts to run multiple web applications on a single server, changes to the global configuration files will affect all applications
  * If the configuration should only apply to one specific web application, it is better to modify the appropriate file inside the `sites-available` directory, which holds the configuration files for individual applications.
* It is also possible to configure Apache using `.htaccess` files in the same format as the other configuration files, but these will only take effect in the directory in which they are stored.

## Implementing CORS headers

* Setting headers in Apache is quite simple through the `mod_headers` module. To enable this module, run the following commands on the server and restart Apache:

  ```bash
  sudo a2enmod headers
  sudo service apache2 restart
  ```

* Once the module is enabled, headers can be configured by editing the appropriate Apache configuration file.
* In the following example, to add the `Access-Control-Allow-Origin` response header, include the following directive in the configuration file:

  ```apacheconf
  Header always set Access-Control-Allow-Origin "https://example.tbl"
  ```

* This configuration instructs the server to send the `Access-Control-Allow-Origin` header with the value `https://example.tbl`.
* After applying the changes, restart or reload Apache to apply the updated configuration

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

* The goal here is to to update the source code via the `Open Code Editor` button and apply the CORS mechanism, while fulfilling the outlined requirements:
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
