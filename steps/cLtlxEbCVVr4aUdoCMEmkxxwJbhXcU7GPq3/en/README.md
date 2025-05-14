# Enforcing CORS in Java Jakarta

* In Java Jakarta, `Cross-Origin Resource Sharing (CORS)` can be enabled by adding specific headers to the HTTP response. This allows a web application running on one origin to access resources from a different origin.
* `CORS` headers can be added using the `setHeader` method of the `HttpServletResponse` object within a servlet:

  ```java
  protected void doGet(HttpServletRequest request, HttpServletResponse response) {
    response.setHeader("Access-Control-Allow-Origin", "https://domain.tbl");
  }
  ```

* In the example above, the server response includes the `Access-Control-Allow-Origin` header with the value `https://domain.tbl`. This configuration permits cross-origin requests originating from that specific domain.

## Enabling CORS using Filter

* To enable `CORS` support, a `Filter` can be implemented to intercept requests before they reach the endpoint and apply the required HTTP headers. This approach ensures that cross-origin requests are properly handled in accordance with the `CORS` specification.
* The following example defines a `Filter` that implements CORS handling for HTTP requests. This `CorsFilter` intercepts incoming requests and adds the appropriate CORS headers when the origin matches a predefined value:

  ```java
  public class CorsFilter implements Filter {

      private static final String ALLOWED_ORIGIN = "https://domain.tbl";
      private static final String ALLOWED_METHODS = "GET, POST, DELETE";
      private static final String ALLOWED_HEADERS = "Authorization, Content-Type";

      @Override
      public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
              throws IOException, ServletException {

          HttpServletRequest  httpRequest  = (HttpServletRequest) request;
          HttpServletResponse httpResponse = (HttpServletResponse) response;

          String origin = httpRequest.getHeader("Origin");
          String method = httpRequest.getMethod();

          if (ALLOWED_ORIGIN.equals(origin)) {
              httpResponse.setHeader("Access-Control-Allow-Origin", ALLOWED_ORIGIN);

              if ("OPTIONS".equalsIgnoreCase(method)) {
                  httpResponse.setHeader("Access-Control-Allow-Methods", ALLOWED_METHODS);
                  httpResponse.setHeader("Access-Control-Allow-Headers", ALLOWED_HEADERS);
                  httpResponse.setStatus(HttpServletResponse.SC_OK);
                  return; // Skip further processing for preflight
              }
          }

          chain.doFilter(request, response);
      }
  }
  ```

* The filter is configured to:
  * Allow cross-origin requests from a specific origin (`https://domain.tbl`).
  * Support the HTTP methods `GET`, `POST`, and `DELETE`.
  * Accept the request headers `Authorization` and `Content-Type`.
  * Handle CORS preflight requests (those using the `OPTIONS` method) by returning an immediate `200 OK` response with the necessary headers, preventing the request from reaching the application logic.

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

* The goal here is to to update the source code via the `Open Code Editor` button and apply the CORS mechanism **only to the `DELETE` method at `/api/products/:id`**, while fulfilling the outlined requirements and keeping other routes unaffected:
  * The only allowed origin must be `https://example.tbl`.
  * The only allowed HTTP method must be `DELETE`.
  * A custom header named `X-CSRF-Token` must be allowed.
  * The application must correctly handle preflight requests for the `DELETE /api/products/:id` endpoint by allowing HTTP `OPTIONS` requests to **only that exact same route**.
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
