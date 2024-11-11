# Enforcing file upload limits using Express in Node.js

* Restricting file size, the total uploads a user can perform, and the upload and download request rates are important security considerations for applications offering file upload and download features.
* Below there are a few examples of how to implement these limits in a Node.js application using the `express` framework, `multer` middleware for handling file uploads and `express-rate-limit` package for basic upload/download rate limiting.

## Limiting file size

* The `multer` middleware accepts an options object, where the `limits` property allows to define the a `fileSize` configuration:

  ```javascript
  const upload = multer({
    storage: storage,
    limits: {
      fileSize: 1 * 1024 * 1024 // 1 MB file size limit
    }
  });
  ```

* This enables the handling of related errors either globally in the Express application or at each specific endpoint, as illustrated in the following example:

  ```javascript
  const uploadSingleFile = upload.single("file");

  app.post("/upload", (req, res) => {
    uploadSingleFile(req, res, (err) => {
      if (err instanceof multer.MulterError) {
        if (err.code === "LIMIT_FILE_SIZE") {
          res.status(400).json({ message: "File size cannot exceed 1 MB" });
          return;
        }

        // Handle other Multer errors here if needed
      }

      if (err) {
        res.status(500).json({ message: "An unknown error occurred while processing the file" });
        return;
      }

      res.send("File uploaded successfully");
    });
  });
  ```

## Limiting uploads and download request rates

* Rate limit for uploads to a maximum of 100 requests per 15 minutes per IP:

  ```javascript
  const { rateLimit } = require("express-rate-limit");
  ```

  ```javascript
  const uploadRateLimit = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes window
    max: 100, // Limit each IP to 100 requests per windowMs
    message: "Too many upload requests from this IP, please try again later"
  });

  app.post("/upload", uploadRateLimit, (req, res) => {
    // File upload logic here
  });
  ```

* Rate limit for downloads to a maximum of 100 requests per 15 minutes per IP:

  ```javascript
  const downloadRateLimit = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes window
    max: 100, // Limit each IP to 100 requests per windowMs
    message: "Too many download requests from this IP, please try again later"
  });

  app.get("/download/:filename", downloadRateLimit, (req, res) => {
    // File download logic here
  });
  ```

  > :older_man: As long as file upload or download features are only available when the user is authenticated, it is highly recommended to apply this type of restriction to the user's logged-in session rather than other superficial values such as the source IP address.

### Considerations when restricting per IP address

* In most scenarios, the web application is not directly exposed to the end client, as it is often located behind a load balancer or a security mechanism like a web application firewall (WAF).
* This could lead to the source IP address of the HTTP packets received by the application being the intermediary's IP, rather than the end client's. In such cases, headers like `X-Forwarded-For` may need to be used to provide the application with the client's real IP address:

  ```javascript
  console.log(req.headers["x-forwarded-for"]);
  ```

* In order to adjust for this, when running an Express app behind a reverse proxy, the `trust proxy` application setting may be used to expose information provided by the reverse proxy in the Express endpoints (i.e., as `req.ip`):

  ```javascript
  app.set("trust proxy", 1); // Trust the first hop away from the application and extract the next IP as client's IP address
  ```

  ```javascript
  app.set("trust proxy", "loopback, 172.16.0.10"); // Trust 'loopback' and '172.16.0.10' proxies for getting client's IP address
  ```

## Exercise to practice :writing_hand:

* The given application offers a basic file upload with Express without any security validation conducted on the server-side. The goal here is to open the code editor using the `Open Code Editor` button and edit the source code to introduce two security measures:
  * A file size limit of 1 KB. If a file uploaded exceeds this size, an HTTP response with a `400 Bad Request` status code should be returned.
  * Each IP address should be limited to 10 file uploads within a 30-second window. Exceeding this limit should result in an HTTP response with status code `429 Too Many Requests`, and the IP should remain blocked for 30 seconds.
    * Note that the application is placed under multiple reverse proxy layers, as it runs within a Cloud Run container on GCP.
* In order to complete the exercise, the Express application located in `app.js` is where code modifications should be added to support these features.
  @@ExerciseBox@@
