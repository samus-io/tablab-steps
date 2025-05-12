# Enforcing CORS using Express in Node.js

* In Express applications, `Cross-Origin Resource Sharing (CORS)` can be enforced using the official `cors` middleware, which simplifies the process of setting required CORS headers.

## Importing and configuring `cors` middleware

* The `cors` middleware must be installed using a package manager such as `npm` or `yarn`. Once installed, it should be imported at the top of the Express application file:

  ```javascript
  const cors = require("cors");
  ```

* Further adjustments to CORS behavior can be made by defining a configuration object. This object specifies the origin, methods, and headers allowed for cross-origin requests:

  ```javascript
  const corsOptions = {
    origin: "https://domain.tbl",
    methods: ["GET", "POST", "DELETE"],
    allowedHeaders: ["Authorization", "Content-Type"],
    credentials: true
  };
  ```

## Enabling CORS in Express

* To apply CORS settings globally across all routes, the middleware should be used with `app.use()`:

  ```javascript
  app.use(cors(corsOptions));
  ```

* When no configuration is needed, CORS can be enabled using default settings by calling the middleware without arguments:

  ```javascript
  const cors = require("cors");
  app.use(cors());
  ```

* For fine-grained control, it can also be selectively applied to individual routes rather than globally:

  ```javascript
  app.get("/products/:id", cors(), (req, res, next) => {
    res.json({ message : "This is CORS-enabled for a single route"})
  });
  ```

### Enabling CORS preflight requests

* In order to handle preflight requests globally, the middleware can be used to respond to all `OPTIONS` requests:

  ```javascript
  // Global preflight handler
  app.options("*", cors(corsOptions)); // Respond to all OPTIONS requests with CORS headers, even if no route exists
  ```

* Alternatively, preflight requests can also be restricted to specific routes that require them:

  ```javascript
  // Preflight handler for a specific endpoint
  app.options("/products/:id", cors(corsOptions)); // Enable CORS for preflight OPTIONS requests on /products/:id only
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
  * The application must correctly handle preflight requests for the `DELETE /api/products/:id` endpoint by allowing HTTP `OPTIONS`.
* After implementing the changes and redeploying the app, use `curl` to send requests and review the HTTP response headers for manual validation:

  ```bash
  curl -sS -X OPTIONS "$APP_URL/api/products/1" -i -H "Origin: https://example.tbl" -H "Access-Control-Request-Method: DELETE" | grep -i '^access-control-'
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
