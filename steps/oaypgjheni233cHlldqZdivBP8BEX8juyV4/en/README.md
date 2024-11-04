# File extension validation

* Extension validation ensures that uploaded files match the expected and approved file types by checking their extensions.

![File extension validation][1]

## Recommended security practices

* **Decode from URL-encoded format file names** prior to validation to prevent bypass techniques like null byte characters (e.g., `image.php%00.png`).
* **Apply robust filtering** to avoid common pitfalls, such as regex patterns that can be bypassed.
* In cases where the web application only accepts a single file type (e.g., `.pdf`), **hardcode the allowed extension** when storing the file. If more file types are required, **define an allow-list** that restricts file extensions to only those necessary for business needs (e.g., `.jpg`, `.jpeg`, `.png`).
* **Disallow files with multiple extensions or missing extensions** to mitigate the risk of exploitation.

  > :warning: Be aware that frontend validation can be bypassed, making it insufficient; it should only be considered a tool for improving user experience.

@@TagStart@@java

## Non-compliant code in Java

* The given code snippet uses Java Jakarta for file uploads, but its extension validation is susceptible to a double extension bypass. It only checks for `.jpg`, `.jpeg`, `.png` in the file name, which is inadequate:

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
  import java.util.regex.Pattern;
  ```

  ```java
  @WebServlet("/upload")
  @MultipartConfig
  public class FileUploadServlet extends HttpServlet {

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

          // Get the filename
          String filename = filePart.getSubmittedFileName();

          Pattern pattern = Pattern.compile("\\.(jpg|jpeg|png)");
          if (!pattern.matcher(filename).matches()) {
              JsonObject model = Json.createObjectBuilder().add("message", "Unexpected file extension").build();
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

## Non-compliant code in Node.js using `multer`

* The given code snippet uses `multer` for file uploads, but its extension validation is susceptible to a double extension bypass. It only checks for `.jpg`, `.jpeg`, `.png` in the file name, which is inadequate:

  ```javascript
  const express = require("express");
  const multer = require("multer");

  const upload = multer({
    ...
  });

  const app = express();

  app.post("/upload", upload.single("file"), (req, res) => {
    if (!req.file) {
      res.status(400).json({ message: "No file uploaded" });
      return;
    }

    const { originalname } = req.file;

    if (!originalname.match(/\.(jpg|jpeg|png)/)) {
      res.status(400).json({ message: "Unexpected file extension" });
      return;
    }

    res.send("File uploaded successfully");
  });
  ```

@@TagEnd@@

@@TagStart@@java

## Compliant code in Java

* The code snippet below secures the file upload feature by decoding the file name before validation, applying an allow-list of allowed extensions, and preventing files with multiple or missing extensions:

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
  import java.net.URLDecoder;
  import java.nio.charset.StandardCharsets;
  import java.util.Set;
  ```

  ```java
  @WebServlet("/upload")
  @MultipartConfig
  public class FileUploadServlet extends HttpServlet {

      private static final Set<String> ALLOWED_EXTENSIONS = Set.of(".jpg", ".jpeg", ".png");

      private Boolean isAllowedFileExtension(String filename) {
          String decodedFilename = URLDecoder.decode(filename, StandardCharsets.UTF_8);
          String lowerCaseFilename = decodedFilename.toLowerCase();
          Integer lastDotIndex = lowerCaseFilename.lastIndexOf(".");
          if (lastDotIndex == -1) // No extension found
              return false;
          if (lowerCaseFilename.split("\\.").length -1 > 1) // Multiple extension found
              return false;
          String extension = lowerCaseFilename.substring(lastDotIndex);
          return ALLOWED_EXTENSIONS.contains(extension);
      }

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

          // Get the filename
          String filename = filePart.getSubmittedFileName();

          if (!isAllowedFileExtension(filename)) {
              JsonObject model = Json.createObjectBuilder().add("message", "Unexpected file extension").build();
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

## Compliant code in Node.js using `multer`

* The code snippet below secures the file upload feature by decoding the file name before validation, applying an allow-list of allowed extensions, and preventing files with multiple or missing extensions:

  ```javascript
  const ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png"];

  const isAllowedFileExtension = (filename) => {
    const decodedFilename = decodeURIComponent(filename);
    const lowerCaseFilename = decodedFilename.toLowerCase();
    const lastDotIndex = lowerCaseFilename.lastIndexOf(".");

    if (lastDotIndex === -1) return false; // No extension found
    if (lowerCaseFilename.split(".").length - 1 > 1) return false; // Multiple extension found

    const extension = lowerCaseFilename.slice(lastDotIndex);

    return ALLOWED_EXTENSIONS.includes(extension);
  };
  ```

  ```javascript
  const upload = multer({
    ...
    fileFilter: (req, file, cb) => {
      if (isAllowedFileExtension(file.originalname)) {
        cb(null, true);
        return;
      }

      const error = new multer.MulterError("LIMIT_UNEXPECTED_FILE", file.fieldname);
      error.message = "Unexpected file extension";
      cb(error);
    }
  });
  const uploadSingleFile = upload.single("file");
  ```

  ```javascript
  app.post("/upload", (req, res) => {
    uploadSingleFile(req, res, (err) => {
      if (err instanceof multer.MulterError) {
        res.status(400).send({ message: err.message });
        return;
      } else if (err) {
        res.status(500).json({ message: "An unknown error occurred while processing the file" });
        return;
      }

      if (!req.file) {
        res.status(400).json({ message: "No file uploaded" });
        return;
      }
      
      res.send("File uploaded successfully");
    });
  });
  ```

@@TagEnd@@

## File extension validation on the client-side

* The file extension can be checked on the frontend using the HTML accept attribute, which helps prevent users from sending unexpected files, though it is not reliable for security purposes:

  ```html
  <input type="file" id="fileInput" accept=".jpg, .jpeg, .png" />
  ```

[1]: /static/images/file-extension-validation.png
