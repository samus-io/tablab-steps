# Insecure file type validation

* Common mechanisms for determining the type of a file include the `Content-Type` header, which indicates the media type of a file within a HTTP request, and the magic number located at the beginning of a file content. Both of these methods are vulnerable to manipulation by malicious users, making them completely unsafe for file type validation from a security standpoint.

  > :older_man: These methods remain valuable for quick file type detection to boost user experience, but they are not reliable for security purposes.

## File type validation through the `Content-Type` header

* The `Content-Type` header is used to indicate the original [MIME type][1] (e.g., `image/png`, `text/plain`, `application/pdf`) of the resource prior to any content encoding applied before transmission.
* MIME, short for `Multipurpose Internet Mail Extensions (MIME)`, is a standard developed in the early 1990s to enable emails to include multimedia content and other binary files, and it is also employed on the web to define the nature of the data in the message body, the encoding applied, and how it should be processed or displayed:

  ```text
  HTTP/1.1 200 OK
  Content-Type: multipart/form-data; boundary="ExampleBoundary"

  --ExampleBoundary
  Content-Disposition: form-data; name="text"

  Here is the text you were looking for.

  --ExampleBoundary
  Content-Disposition: form-data; name="file"; filename="example.jpg"
  Content-Type: image/jpeg

  [binary JPEG data]

  --ExampleBoundary--
  ```

  * The HTTP headers that are commonly used in conjunction with MIME to manage content in HTTP transactions are:
    * `Content-Type`: to specify the media type and subtype of the content.
    * `Content-Disposition`: to indicate if the content should be displayed inline, as part of a web page, or treated as an attachment to be downloaded to local storage. In a `multipart/form-data` body, the HTTP `Content-Disposition` header is responsible for providing information about each subpart.
* File type validation based on the MIME type in the `Content-Type` header is unreliable for security purposes since it can be easily spoofed, even though certain libraries or packages may depend on this value to confirm that file matches the expected type.
* However, it can still be useful to enhance the user experience by offering a preliminary check for incorrect file types.

@@TagStart@@java

### Non-compliant code in Java

* This implementation uses Java Jakarta to handle file uploads, which identifies the file type via the received `Content-Type` HTTP header, and then performs a security check accordingly that can be easily bypassed by spoofing the `Content-Type` header in the request:

  ```java
  import jakarta.json.Json;
  import jakarta.json.JsonObject;
  import jakarta.servlet.ServletException;
  import jakarta.servlet.annotation.MultipartConfig;
  import jakarta.servlet.annotation.WebServlet;
  import jakarta.servlet.http.HttpServlet;
  import jakarta.servlet.http.HttpServletRequest;
  import jakarta.servlet.http.HttpServletResponse;
  import jakarta.servlet.http.Part;

  import java.io.IOException;
  import java.util.Set;
  ```

  ```java
  @WebServlet("/upload")
  @MultipartConfig
  public class FileUploadServlet extends HttpServlet {

      private static final Set<String> ALLOWED_TYPES = Set.of("image/jpeg", "image/png");

      @Override
      protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
          Part filePart;
          try {
              // Get the file part from the request
              filePart = request.getPart("formFile");
          }
          catch (ServletException | IOException e) {
              JsonObject model = Json.createObjectBuilder().add("message", "No file uploaded").build();
              response.getOutputStream().println(model.toString());
              response.setStatus(400);
              return;
          }

          // Get MIME type and compare it with allowed MIME types
          String mimetype = filePart.getContentType();
          if (!ALLOWED_TYPES.contains(mimetype)) {
              JsonObject model = Json.createObjectBuilder().add("message", "Unexpected file type").build();
              response.getOutputStream().println(model.toString());
              response.setStatus(400);
              return;
          }

          // Respond to the client
          response.getOutputStream().println("File uploaded successfully");
          response.setStatus(200);
      }
  }
  ```

@@TagEnd@@

@@TagStart@@node.js

### Non-compliant code in Node.js using `multer`

* This implementation uses `multer` to handle file uploads, which identifies the file type via the received `Content-Type` HTTP header, and then performs a security check accordingly that can be easily bypassed by spoofing the `Content-Type` header in the request:

  ```javascript
  import express from "express";
  import multer from "multer";

  const ALLOWED_TYPES = ["image/jpeg", "image/png"];

  const upload = multer({
    ...
  });

  const app = express();

  app.post("/upload", upload.single("file"), (req, res) => {
    if (!req.file) {
      res.status(400).json({ message: "No file uploaded" });
      return;
    }

    const { mimetype } = req.file;

    if (!ALLOWED_TYPES.includes(mimetype)) {
      res.status(400).json({ message: "Unexpected file type" });
      return;
    }

    res.send("File uploaded successfully");
  });
  ```

@@TagEnd@@

### File type validation on the client-side

* The file type via the MIME type can also be verified on the frontend with a few lines of JavaScript, which helps prevent users from sending unexpected files, though it is not suitable for security purposes:

  ```javascript
  const fileInput = document.getElementById("fileInput");

  fileInput.addEventListener("change", function () {
    const file = fileInput.files[0];

    if (!file) return;

    const validTypes = ["image/jpeg", "image/png"];
    if (!validTypes.includes(file.type)) {
      // Handle unexpected file notification
    }
  });
  ```

## File type validation through magic number

* The magic number is a unique sequence of bytes located at the beginning of a file's content that is used to identify the file type, according to a [list of file signatures][1]. These bytes serve as a signature for the file, allowing the operating system or applications to determine its type, even without relying on the file extension:
  * `jpeg (jpg)` files start with `FF D8 FF` (corresponding to `ÿØÿÛ`).
  * `png` files start with `89 50 4E 47 0D 0A 1A 0A` (corresponding to `‰PNG␍␊␚␊`).
  * `pdf` files start with `25 50 44 46 2D` (corresponding to `%PDF-`).
  * `zip` files start with `50 4B 03 04` (corresponding to `PK␃␄`).
* Malicious users can easily prepend a valid magic number to malicious files, making them seem legitimate. For instance, adding the `%PDF-2.0` signature at the start of a webshell file can trick the system into thinking it's a PDF file.
* Although not beneficial for security, they can be useful for checking the type of file sent by the user and preventing wrong files from being loaded into a web application. However, the main issue is that libraries or packages may solely rely on these numbers for file type identification.

@@TagStart@@java

### Non-compliant code in Java using `Apache Tika`

* The code snippet below uses the `Apache Tika` library, which identifies the file type via magic number, and then proceeds with a security check accordingly that can be easily circumvented through the manipulation of the file's magic number:

  ```java
  import jakarta.json.Json;
  import jakarta.json.JsonObject;
  import jakarta.servlet.ServletException;
  import jakarta.servlet.annotation.MultipartConfig;
  import jakarta.servlet.annotation.WebServlet;
  import jakarta.servlet.http.HttpServlet;
  import jakarta.servlet.http.HttpServletRequest;
  import jakarta.servlet.http.HttpServletResponse;
  import jakarta.servlet.http.Part;
  import org.apache.tika.Tika;

  import java.io.IOException;
  import java.util.Set;
  ```

  ```java
  @WebServlet("/upload")
  @MultipartConfig
  public class FileUploadServlet extends HttpServlet {

      private static final Set<String> ALLOWED_TYPES = Set.of("image/jpeg", "image/png");
  
      @Override
      protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
          Part filePart;
          try {
              // Get the file part from the request
              filePart = request.getPart("formFile");
          }
          catch (ServletException | IOException e) {
              JsonObject model = Json.createObjectBuilder().add("message", "No file uploaded").build();
              response.getOutputStream().println(model.toString());
              response.setStatus(400);
              return;
          }
          Tika tika = new Tika();

          // Get MIME type via magic number and compare it with allowed MIME types
          String mimetype = tika.detect(filePart.getInputStream());
          System.out.println(mimetype);
          if (!ALLOWED_TYPES.contains(mimetype)) {
              JsonObject model = Json.createObjectBuilder().add("message", "Unexpected file type").build();
              response.getOutputStream().println(model.toString());
              response.setStatus(400);
              return;
          }

          // Respond to the client
          response.getOutputStream().println("File uploaded successfully");
          response.setStatus(200);
      }
  }
  ```

@@TagEnd@@

@@TagStart@@node.js

### Non-compliant code in Node.js using `file-type`

* The code snippet below uses the `file-type` package, which identifies the file type via magic number, and then proceeds with a security check accordingly that can be easily circumvented through the manipulation of the file's magic number:

  ```javascript
  import express from "express";
  import multer from "multer";
  import { fileTypeFromBuffer } from "file-type";

  const ALLOWED_TYPES = ["image/jpeg", "image/png"];

  const upload = multer({
    ...
  });

  const app = express();

  app.post("/upload", upload.single("file"), async (req, res) => {
    if (!req.file) {
      res.status(400).json({ message: "No file uploaded" });
      return;
    }

    const { buffer } = req.file;

    // Get the MIME type from buffer
    const fileType = await fileTypeFromBuffer(buffer);

    if (!ALLOWED_TYPES.includes(fileType.mime)) {
      res.status(400).json({ message: "Unexpected file type" });
      return;
    }

    res.send("File uploaded successfully");
  });
  ```

@@TagEnd@@

[1]: https://developer.mozilla.org/en-US/docs/Web/HTTP/MIME_types/Common_types
