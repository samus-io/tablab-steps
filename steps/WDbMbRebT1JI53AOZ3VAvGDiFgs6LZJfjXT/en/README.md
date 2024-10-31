# Enforcing file upload limits using Bucket4j in Java Jakarta

* Restricting file size, the total uploads a user can perform, the frequency of uploads within a specific period by a user, and also the download request rates are important security considerations for applications offering file upload and download features.
* Below there are a few examples of how to implement these limits in a Java Jakarta application.

## Limiting file size

* The following code snippet retrieves the size of the uploaded file in bytes, and if the file exceeds 1 MB, it returns an HTTP 400 (Bad Request) error:

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

* The [Bucket4j][1] library implements rate limiting based on the token-bucket algorithm, where each client is given a "bucket" of tokens representing the number of allowed requests within a certain time window.
* When a request is made, a token is consumed from the bucket, and once the tokens are depleted, further requests are blocked until the bucket is refilled after the defined time interval.
* The `isClientAllowed` function applies this rate limiting by assigning each client a bucket. The bucket allows up to a certain number of requests (e.g., 100) during a specified time window (e.g., 900 seconds).
* If a client’s bucket has available tokens, one is consumed and the request is allowed; otherwise, the request is blocked until the bucket refills after the window expires:

  ```java
  import java.io.IOException;
  import java.time.Duration;
  import java.util.concurrent.ConcurrentHashMap;
  import io.github.bucket4j.Bucket;
  ```

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

* To implement rate limiting for an upload or download endpoint based on IP, the `isClientAllowed` function is called as follows:

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

* Similarly, to rate limit an endpoint by session, the `isClientAllowed` function can be called using the session ID as the client identifier:

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

* In most scenarios, the web application is not directly exposed to the end client, as it is often located behind a load balancer or a security mechanism like a Web Application Firewall (WAF).
* This could lead to the source IP address of the HTTP packets received by the application being the intermediary's IP, rather than the end client's. In such cases, headers like `X-Forwarded-For` may need to be used to provide the application with the client's real IP address:
  
  ```java
  System.out.println(request.getHeader("X-Forwarded-For"));
  ```

* In order to adjust for this, when running the web application behind a reverse proxy, the `getClientIp` function can be used to get the real client IP:

  ```java
  private String getClientIP(HttpServletRequest request) {
      String xfHeader = request.getHeader("X-Forwarded-For");
      if (xfHeader == null) {
          return request.getRemoteAddr(); // Return the client IP if the header is not present
      }
      return xfHeader.split(",")[0]; // Get the first IP in the list if the header exists
  }
  ```

## Exercise to practice :writing_hand:

* The given application offers a basic file upload with Java Jakarta without any security validation conducted on the server-side. The goal here is to open the code editor using the `Open Code Editor` button and edit the source code to introduce two security measures:
  * A file size limit of 1 KB. If a file uploaded exceeds this size, an HTTP response with a `400 Bad Request` status code should be returned.
  * Each IP address should be limited to 10 file uploads within a 30-second window. Exceeding this limit should result in an HTTP response with status code `429 Too Many Requests`, and the IP should remain blocked for 30 seconds.
    * Be aware that the application is placed under multiple reverse proxy layers, as it runs within a Cloud Run container on GCP.
* In order to complete the exercise, the web application located in `src/main/java/io/ontablab/FileUploadServlet.java` is where code modifications should be added to support these features.
  @@ExerciseBox@@

[1]: https://github.com/bucket4j/bucket4j
