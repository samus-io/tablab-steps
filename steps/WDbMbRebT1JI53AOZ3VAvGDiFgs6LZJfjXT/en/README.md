# Enforcing file upload limits using Bucket4j in Java Jakarta

* Restricting file size, the total uploads a user can perform, and the upload and download request rates are important security considerations for applications offering file upload and download features.
* Below there are a few examples of how to implement these limits in a Java Jakarta application using the [Bucket4j][1] library.

## Limiting file size

* The following code snippet retrieves the size of the uploaded file in bytes, and if the file exceeds 1 MB, it returns an HTTP `400 Bad Request` response:

  ```java
  // Allow file size up to 1 MB
  Part filePart = request.getPart("file");
  Long fileSize = filePart.getSize();

  if (fileSize > 1000000) {
      response.setStatus(400);
      return;
  }
  ```

## Limiting uploads and download request rates using Bucket4j

* The [Bucket4j][1] library adopts the token-bucket algorithm for rate limiting, assigning each client a bucket of tokens which represent the allowable number of requests in a certain time window.
* Each time a request is submitted, it consumes a token from the bucket, and once there are no tokens left, further requests are blocked until the tokens are refilled after the defined time interval.
* In the following code, the `isClientAllowed` method enforces rate limiting by assigning each client a bucket that permits a set number of requests (e.g., 100 requests) within a defined time window (e.g., 15 minutes). If tokens are available in a client's bucket, one is used to allow the request; if not, the request is denied until the bucket is replenished when the time window resets:

  <details>
    <summary>Dependencies</summary>

    ```java
    import java.io.IOException;
    import java.time.Duration;
    import java.util.concurrent.ConcurrentHashMap;
    import io.github.bucket4j.Bucket;
    ```

  </details>

  ```java
  private static final Duration RATE_LIMIT_TIME_WINDOW = Duration.ofSeconds(900); // 15 minutes window
  private static final Integer MAX_REQUESTS_PER_CLIENT = 100; // Allow 100 requests per IP per 15 minutes
  private static final ConcurrentHashMap<String, Bucket> clientRateLimit = new ConcurrentHashMap<>();

  // Creates a new bucket for a client with a predefined capacity and refill rate
  private Bucket createNewBucket(String clientIdentifier) {
      return Bucket.builder().addLimit(limit -> limit.capacity(MAX_REQUESTS_PER_CLIENT)
              .refillGreedy(MAX_REQUESTS_PER_CLIENT, RATE_LIMIT_TIME_WINDOW)).build();
  }

  // Checks if a client, identified by 'clientIdentifier', is allowed to proceed based on their rate limit
  private Boolean isClientAllowed(String clientIdentifier) {
      // Retrieves the client's bucket or creates a new one if it doesn't exist
      Bucket bucket = clientRateLimit.computeIfAbsent(clientIdentifier, this::createNewBucket);
      return bucket.tryConsume(1);
  }
  ```

* To apply rate limiting based on IP address for an upload or download endpoint, the `isClientAllowed` method can be invoked as demonstrated below:

  ```java
  public void uploadFile(HttpServletRequest request, HttpServletResponse response) {
      String clientIP = request.getRemoteAddr();

      if (!isClientAllowed(clientIP)) {
          response.setStatus(429);
          return;
      }

      // File upload logic
  }
  ```

* Similarly, to apply rate limiting by session for an endpoint, the `isClientAllowed` method can be called using the session ID as the client identifier:

  ```java
  public void uploadFile(HttpServletRequest request, HttpServletResponse response) {
      String clientSessionId = request.getSession().getId();

      if (!isClientAllowed(clientSessionId)) {
          response.setStatus(429);
          return;
      }

      // File upload logic
  }
  ```

  > :older_man: As long as file upload or download features are only available when the user is authenticated, it is highly recommended to apply this type of restriction to the user's logged-in session rather than other superficial values such as the source IP address.

### Considerations when restricting per IP address

* In most scenarios, the web application is not directly exposed to the end client, as it is often located behind a load balancer or a security mechanism like a web application firewall (WAF).
* This could lead to the source IP address of the HTTP packets received by the application being the intermediary's IP, rather than the end client's. In such cases, headers like `X-Forwarded-For` may need to be used to provide the application with the client's real IP address:
  
  ```java
  System.out.println(request.getHeader("X-Forwarded-For"));
  ```

* In order to adjust for this, when running the web application behind a reverse proxy, a method like `getClientIP` may be employed to retrieve the real client IP:

  ```java
  private String getClientIP(HttpServletRequest request) {
      String xffHeader = request.getHeader("X-Forwarded-For");

      if (xffHeader == null) {
          return request.getRemoteAddr(); // Return the client IP if the header is not present
      }
      
      return xffHeader.split(",")[0]; // Get the first IP in the list if the header exists
  }
  ```

  > :warning: The `X-Forwarded-For` header is user-controlled, meaning it can include any values, such as spoofed IP addresses or invalid data. At some point in the infrastructure, it is necessary to sanitize it and discard irrelevant entries.

## Exercise to practice :writing_hand:

* The given application offers a basic file upload without any security validation conducted on the server-side. The goal here is to open the code editor using the `Open Code Editor` button and edit the source code to introduce two security measures:
  * A file size limit of 1 KB. If a file uploaded exceeds this size, an HTTP response with a `400 Bad Request` status code should be returned.
  * Each IP address should be limited to 10 file uploads within a 30-second window. Exceeding this limit should result in an HTTP response with status code `429 Too Many Requests`, and the IP should remain blocked for 30 seconds.
    * Note that the application is placed under multiple reverse proxy layers, as it runs within a Cloud Run container on GCP.
* In order to complete the exercise, the class located in `src/main/java/io/ontablab/FileUploadServlet.java` is where code modifications should be added to support these features.
* After making the changes, press the `Verify Completion` button to confirm that the exercise has been completed.

  @@ExerciseBox@@

[1]: https://github.com/bucket4j/bucket4j
