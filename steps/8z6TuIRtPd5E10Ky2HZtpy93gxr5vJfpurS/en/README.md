# Upload and download application challenges when uploading files

* When implementing file upload and download features in an application, it is crucial to impose certain limits to ensure security and performance.

## Security considerations to be taken into account

* **Limit the file size** of each uploaded file to prevent excessive use of storage space and to protect the server from dealing with files that are too large, potentially affecting its performance or causing crashes.
* **Limit the total uploads a user can perform** to protect storage capacity and minimize the risk of a `Denial of Service (DoS)` attack by restricting the number of files a user is allowed to upload. This measure helps to prevent the server from being flooded with excessive files, which could exhaust storage resources.
* **Limit the number of uploads in a given time period** by setting a rate limit on file uploads, preventing a single user from flooding the server with numerous requests within a short timeframe. This helps manage server load and ensures fair usage.
* **Limit the number of downloads/request rates** by setting restrictions on the number of download requests a user can make in a specific time period, similar to upload controls, to prevent abuse and ensure smooth processing of legitimate traffic.

@@TagStart@@java

## Non-compliant code in Java

* Here's an example of a vulnerable implementation where the above security measures are not properly applied using Java Jakarta:

  ```java
  import jakarta.json.Json;
  import jakarta.json.JsonObject;
  import jakarta.servlet.ServletConfig;
  import jakarta.servlet.ServletException;
  import jakarta.servlet.annotation.MultipartConfig;
  import jakarta.servlet.annotation.WebServlet;
  import jakarta.servlet.http.HttpServlet;
  import jakarta.servlet.http.HttpServletRequest;
  import jakarta.servlet.http.HttpServletResponse;
  import jakarta.servlet.http.Part;
  
  import java.io.File;
  import java.io.FileOutputStream;
  import java.io.IOException;
  import java.io.InputStream;
  ```

  ```java
  @WebServlet("/upload")
  @MultipartConfig
  public class FileUploadServlet extends HttpServlet {
  
      private static final int BUFFER_SIZE = 8192; // Buffer size for reading file chunks
      private String uploadFolderPath;
  
      @Override
      public void init(ServletConfig config) throws ServletException {
          super.init(config);
          // Define the path for the upload directory relative to the web application's root
          uploadFolderPath = getServletContext().getRealPath("/") + "uploads";
  
          // Create the directory if it does not exist
          File uploadDir = new File(uploadFolderPath);
          if (!uploadDir.exists()) {
              uploadDir.mkdirs();
          }
      }
  
      @Override
      protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
          Part filePart;
          try {
              filePart = request.getPart("formFile");
              String filename = filePart.getSubmittedFileName();
  
              // No file size limit
              // No upload rate limit
  
              // Save the file to the uploads directory
              saveFile(filename, filePart.getInputStream());
  
              // Send a success message back to the client
              sendSuccessResponse(response, "File uploaded successfully");
          } catch (ServletException | IOException e) {
              // Handle cases where the file part could not be retrieved
              sendErrorResponse(response, "No file uploaded", HttpServletResponse.SC_BAD_REQUEST);
          } catch (Exception e) {
              // Catch unexpected errors and respond with a general internal server error
              sendErrorResponse(response, "Internal server error", HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
          }
      }
  
      private void saveFile(String filename, InputStream fileContent) throws IOException {
          File file = new File(uploadFolderPath, filename);
  
          // Use try-with-resources to automatically close the FileOutputStream
          try (FileOutputStream fos = new FileOutputStream(file)) {
              byte[] buffer = new byte[BUFFER_SIZE];
              int bytesRead;
  
              // Read the file content in chunks to efficiently handle larger files
              while ((bytesRead = fileContent.read(buffer)) != -1) {
                  fos.write(buffer, 0, bytesRead);
              }
          }
      }
  
      private void sendSuccessResponse(HttpServletResponse response, String message) throws IOException {
          // Prepare a plain text response to indicate successful file upload
          response.setContentType("text/plain");
          response.setCharacterEncoding("UTF-8");
          response.setStatus(HttpServletResponse.SC_OK);
          try (var out = response.getOutputStream()) {
              out.println(message);
          }
      }
  
      private void sendErrorResponse(HttpServletResponse response, String message, int statusCode) throws IOException {
          // Create a JSON object to send back a structured error response
          JsonObject errorResponse = Json.createObjectBuilder()
                  .add("message", message)
                  .build();
  
          response.setContentType("application/json");
          response.setCharacterEncoding("UTF-8");
          response.setStatus(statusCode);
  
          // Write the JSON error message to the response output
          try (var out = response.getOutputStream()) {
              out.println(errorResponse.toString());
          }
      }
  }
  ```

@@TagEnd@@
@@TagStart@@node.js

## Non-compliant code in Node.js using `multer`

* Here's an example of a vulnerable implementation where the above security measures are not properly applied using `multer` and `Express.js`:

  ```javascript
  const express = require("express");
  const multer = require("multer");
  const path = require("path");
  const fs = require("fs");

  const app = express();

  // Define the path to the folder where uploaded files will be stored
  const uploadFolderPath = path.join(__dirname, "uploads");

  // Check if the 'uploads' folder exists; if not, create it
  if (!fs.existsSync(uploadFolderPath)) {
    fs.mkdirSync(uploadFolderPath, { recursive: true });
  }

  const storage = multer.diskStorage({
    destination: (req, file, cb) => {
      cb(null, uploadFolderPath);
    },
    filename: (req, file, cb) => {
      cb(null, file.originalname); // Use the original filename provided by the user
    }
  });

  const upload = multer({
    storage: storage
  });

  app.post("/upload", upload.single("file"), (req, res) => {
    res.send("File uploaded successfully");
  });

  app.get("/download/:fileName", (req, res) => {
    const { fileName } = req.params;
    const options = {
      root: uploadFolderPath,
      dotfiles: "deny"
    };

    res.sendFile(fileName, options, (err) => {
      if (err) {
        res.status(404).send("File not found");
      }
    });
  });
  ```

@@TagEnd@@

### Issues with this implementation

* **No file size limit** is currently enforced, allowing users to upload excessively large files, which can result in server crashes or significant storage consumption.
* **No upload rate limit** exists, enabling users to send a high volume of upload requests to the server, potentially exhausting its resources and causing a Denial of Service (DoS).
* **No download rate limit** means that users can continuously make download requests, potentially overwhelming the server and degrade performance for all users.
* **No proper error handling for uploads** is in place, so if an error occurs during the upload process it is not managed correctly, potentially leading to user experience issues and potential security vulnerabilities.