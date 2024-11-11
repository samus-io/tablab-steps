# File storage location and filesystem permissions when uploading files

* Whenever possible, store uploaded files on a separate server or service dedicated exclusively to file storage. This approach provides complete segregation of duties between the application  handling user interactions and upload requests from the server managing file storage, thereby reducing the impact of potential vulnerabilities.
  * If a separate storage server is not feasible and files need to be saved on the same server, ensure they are stored outside the webroot directory. This prevents direct access to the files through the web server, minimizing the risk of exploitation.
* Ensuring proper file permissions, especially when storing files on the server, is also essential for reducing security risks.
* Keeping uploaded files in memory or temporary storage during processing and only transferring them to permanent storage after passing validation checks is recommended, as it prevents malicious files from becoming accessible before being removed by validation.
* If users require access to uploaded files, whether stored on the same server, a different server, or a storage service, it is advisable to avoid granting direct access. A secure approach is to implement a server-side handler that maps files to unique IDs, ensuring controlled access and mitigating the risk of unauthorized exposure to sensitive files.

## Restrict filesystem permissions

* File storage permissions should be restricted to control user actions on uploaded files, typically permitting only read and write access for files like images or documents, while preventing execute permissions.
  * If execution permissions are required, validating the file content before storage is recommended as a best practice to detect and block macros, hidden scripts, or any form of malware.
  * Additionally, if a file does not require read access, it should be stored with write permissions only, limiting the risk of unauthorized access.

## Using a handler when allowing public access

* When stored files on a server require public access, it is advised to avoid direct access to uploaded files via URLs. Instead, implement a server-side handler to securely serve the files using an internal mapping system that references them by unique IDs rather than their actual file names.
  * As an example, the system should map a unique ID to each corresponding file name (e.g., `12345` &rarr; `document.pdf`).
* Permitting direct URL access to files (e.g., `https://domain.tbl/uploads/document.pdf`) can expose the application to major security risks, particularly in the presence of existing vulnerabilities related to path traversal attacks, unauthorized file access, and potential sensitive information leakage via predictable URLs.
* A server-side handler allows easy enforcement of permissions and access controls before serving a file, ensuring that only authorized users can access specific files.

### How it works

* Once a file is uploaded and stored, the file receives a unique ID, and the connection between this ID and the file name is saved in a database or equivalent system.
* When a file is requested by a user (e.g., getting `https://example.tbl/uploads/12345`), the handler processes the request, searches the unique ID `12345` in the mapping system, retrieves the associated file, and serves it to the user.

@@TagStart@@java

## Non-compliant code in Java Jakarta storing files on the same Linux server

* The following code snippet in Java Jakarta stores files directly in the `uploads` directory within the webroot, and makes them publicly accessible via URLs (e.g., `https://domain.tbl/uploads/document.pdf`) without any internal mapping or sanitization:

  <details>
    <summary>Dependencies</summary>

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

  </details>
  
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
              filePart = request.getPart("file");
              String filename = filePart.getSubmittedFileName();
  
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
  ```

  <details>
    <summary>Contextual code</summary>

    ```java  
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

  </details>

@@TagEnd@@

@@TagStart@@node.js

## Non-compliant code in Node.js using `multer` and storing files on the same Linux server

* The following code snippet uses `multer` for handling file uploads, however, it stores files directly in the `uploads` directory within the webroot, and makes them publicly accessible via URLs (e.g., `https://domain.tbl/uploads/document.pdf`) without any internal mapping or sanitization:

  <details>
    <summary>Dependencies</summary>

    ```javascript
    const express = require("express");
    const multer = require("multer");
    const path = require("path");
    const fs = require("fs");
    ```

  </details>

  ```javascript
  const app = express();

  // Define the path to the folder where uploaded files will be stored
  const uploadFolderPath = path.join(__dirname, "uploads");

  // Check if the 'uploads' folder exists; if not, create it
  if (!fs.existsSync(uploadFolderPath)) fs.mkdirSync(uploadFolderPath, { recursive: true });

  // Serve the 'uploads' folder as a static directory
  app.use("/uploads", express.static(uploadFolderPath));

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
    if (!req.file) {
      res.status(400).json({ message: "No file uploaded" });
      return;
    }

    res.send("File uploaded successfully");
  });
  ```

@@TagEnd@@

@@TagStart@@java

## Compliant code in Java storing files on the same Linux server

* By keeping files in memory, storing them outside the webroot with proper permissions, and incorporating a mapping system for public access, the following code adheres to best practices for file storage locations and filesystem permissions:

  <details>
    <summary>Dependencies</summary>

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
    import java.security.SecureRandom;
    import java.sql.Connection;
    import java.sql.PreparedStatement;
    import java.sql.SQLException;
    import java.util.UUID;
    ```

  </details>

  ```java
  @WebServlet("/upload")
  @MultipartConfig
  public class FileUploadServlet extends HttpServlet {
  
      private static final int BUFFER_SIZE = 8192; // Buffer size for reading file chunks
      private static final String UPLOAD_FOLDER_PATH = "/srv/uploads";
      private static final String ALPHANUMERIC_CHARACTERS = "abcdefghijklmnopqrstuvwxyz0123456789";
  
      @Override
      public void init(ServletConfig config) throws ServletException {
          super.init(config);

          // Create the directory if it does not exist
          File uploadDir = new File(UPLOAD_FOLDER_PATH);
          if (!uploadDir.exists()) {
              uploadDir.mkdirs();
          }
      }
  
      @Override
      protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
          Part filePart;

          try {
              filePart = request.getPart("file");
              String filename = filePart.getSubmittedFileName();
  
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
  
      private void saveFile(String originalName, InputStream fileContent) throws IOException {
          String id = generateUniqueId();
          String storedName = UUID.randomUUID() + ".pdf";
          File file = new File(UPLOAD_FOLDER_PATH, storedName);
          String path = file.getAbsolutePath();
  
          saveFileInDatabase(id, originalName, storedName, path);
  
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
  
      private void saveFileInDatabase(String id, String originalName, String storedName, String path) {
          try (Connection conn = DatabaseManager.getConnection()) {
              String query = "INSERT INTO files (id, original_name, stored_name, path) VALUES (?, ?, ?, ?)";
  
              PreparedStatement ps = conn.prepareStatement(query);
              ps.setString(1, id);
              ps.setString(2, originalName);
              ps.setString(3, storedName);
              ps.setString(4, path);
  
              ps.executeUpdate();
              ps.close();
          } catch (SQLException e) {
              throw new RuntimeException(e);
          }
      }
  ```

  <details>
    <summary>Contextual code</summary>

    ```java
        private String generateUniqueId() {
            SecureRandom secureRandom = new SecureRandom();
            StringBuilder stringBuilder = new StringBuilder(8);
    
            // Generate random characters from the ALPHANUMERIC_CHARACTERS
            for (int i = 0; i < 8; i++) {
                int index = secureRandom.nextInt(ALPHANUMERIC_CHARACTERS.length());
                stringBuilder.append(ALPHANUMERIC_CHARACTERS.charAt(index));
            }

            return stringBuilder.toString();
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

  </details>

  * In this case, the code is designed to consider only PDF file uploads to the application.

* The following code corresponds to the file download functionality:

  <details>
    <summary>Dependencies</summary>

    ```java
    import jakarta.json.Json;
    import jakarta.json.JsonArray;
    import jakarta.json.JsonArrayBuilder;
    import jakarta.json.JsonObject;
    import jakarta.servlet.ServletConfig;
    import jakarta.servlet.ServletException;
    import jakarta.servlet.annotation.WebServlet;
    import jakarta.servlet.http.HttpServlet;
    import jakarta.servlet.http.HttpServletRequest;
    import jakarta.servlet.http.HttpServletResponse;
    
    import java.io.File;
    import java.io.FileInputStream;
    import java.io.IOException;
    import java.io.OutputStream;
    import java.sql.Connection;
    import java.sql.PreparedStatement;
    import java.sql.ResultSet;
    import java.sql.SQLException;
    import java.util.Arrays;
    import java.util.Optional;
    ```

  </details>

  ```java
  @WebServlet("/download/*")
  public class FileDownloadServlet extends HttpServlet {
  
      private static final int BUFFER_SIZE = 8192; // Buffer size for file reading
      private static final String UPLOAD_FOLDER_PATH = "/srv/uploads";
  
      @Override
      public void init(ServletConfig config) throws ServletException {
        ...
      }
  
      @Override
      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
          String pathInfo = request.getPathInfo();
          String id = pathInfo.substring(1); // Extract the filename from the URL, removing the leading slash
          String path = getPathFromId(id);

          if (path == null) {
              sendErrorResponse(response, "File not found", HttpServletResponse.SC_NOT_FOUND);
              return;
          }
  
          File requestedFile = new File(path);
  
          // Check if the requested file exists; if not, send a 404 error response
          if (!requestedFile.exists()) {
              sendErrorResponse(response, "File not found", HttpServletResponse.SC_NOT_FOUND);
              return;
          }
  
          // Send the requested file back to the client
          sendFileResponse(response, requestedFile);
      }
  
      private String getPathFromId(String id) {
          try (Connection conn = DatabaseManager.getConnection()) {
              String query = "SELECT path FROM files WHERE id = ?";
  
              PreparedStatement ps = conn.prepareStatement(query);
              ps.setString(1, id);
  
              ResultSet rs = ps.executeQuery();
  
              if (rs.next())
                  return rs.getString(1);
              ps.close();
          } catch (SQLException e) {
              throw new RuntimeException(e);
          }

          return null;
      }
  ```

  <details>
    <summary>Contextual code</summary>

    ```java
        private void sendFileResponse(HttpServletResponse response, File file) throws IOException {
            // Determine the MIME type of the file to set the appropriate content type
            String mimeType = Optional.ofNullable(getServletContext().getMimeType(file.getAbsolutePath()))
                    .orElse("application/octet-stream");

            response.setContentType(mimeType);
            response.setContentLengthLong(file.length());
    
            // Use try-with-resources to ensure FileInputStream and OutputStream are closed properly
            try (FileInputStream inStream = new FileInputStream(file);
                OutputStream outStream = response.getOutputStream()) {
                byte[] buffer = new byte[BUFFER_SIZE];
                int bytesRead;
                
                // Read and write the file in chunks to handle large files efficiently
                while ((bytesRead = inStream.read(buffer)) != -1) {
                    outStream.write(buffer, 0, bytesRead);
                }
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

  </details>

* However, before running this code, the table `files` must be created first:

  ```sql
  CREATE TABLE IF NOT EXISTS files (
    id TEXT PRIMARY KEY,
    original_name TEXT,
    stored_name TEXT,
    path TEXT
  )
  ```

* Also, the directory for storing uploads outside the webroot must be created:

  ```bash
  sudo mkdir -p /srv/uploads
  ```

* The ownership of the `uploads` directory should be set to the non-privileged user that runs the server (e.g., `www-data`), allowing only this user to manage the files:

  ```bash
  sudo chown -R www-data:www-data /srv/uploads
  ```

* Finally, permissions should be adjusted to allow only read and write access for the `www-data` user:

  ```bash
  sudo chmod -R 600 /srv/uploads
  ```

@@TagEnd@@

@@TagStart@@node.js

## Compliant code in Node.js using `multer` and storing files on the same Linux server

* By keeping files in memory until validated by the `multer` package, storing them outside the webroot with proper permissions, and incorporating a mapping system for public access, the following code adheres to best practices for file storage locations and filesystem permissions:

  ```javascript
  const crypto = require("crypto");
  const sqlite3 = require("sqlite3");
  const uuid = require("uuid");
  ```

  ```javascript
  // Set up the SQLite database
  const db = new sqlite3.Database("./db.fileStorage.sqlite");

  db.run(`
    CREATE TABLE IF NOT EXISTS files (
      id TEXT PRIMARY KEY,
      original_name TEXT,
      stored_name TEXT,
      path TEXT
    )
  `);
  ```

  ```javascript
  // Define the path to the folder where uploaded files will be stored
  const uploadFolderPath = "/srv/uploads";

  const generateUniqueId = () => {
    return crypto.randomBytes(8).toString("hex");
  };

  const storage = multer.diskStorage({
    destination: (req, file, cb) => {
      cb(null, uploadFolderPath);
    },
    filename: (req, file, cb) => {
      file.id = generateUniqueId();
      const storedName = `${uuid.v4()}.pdf`;
      const filePath = path.join(uploadFolderPath, storedName);

      db.run(
        `INSERT INTO files (id, original_name, stored_name, path) VALUES (?, ?, ?, ?)`,
        [file.id, file.originalname, storedName, filePath],
        (err) => {
          if (err) {
            cb(err);
            return;
          }
          cb(null, storedName);
        }
      );
    }
  });
  ```

  * In this case, the code is designed to consider only PDF file uploads to the application.

  ```javascript
  const upload = multer({ storage: storage });
  const uploadSingleFile = upload.single("file");

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

      res.json({ message: "File uploaded successfully", fileId: req.file.id });
    });
  });

  app.get("/download/:id", (req, res) => {
    const { id } = req.params;

    db.get(`SELECT path FROM files WHERE id = ?`, [id], (err, row) => {
      if (err) {
        res.status(500).json({ message: "Error retrieving file" });
        return;
      }

      if (!row) {
        res.status(404).json({ message: "File not found" });
        return;
      }

      res.sendFile(row.path, (err) => {
        if (err) {
          res.status(500).json({ message: "Error downloading file" });
        }
      });
    });
  });
  ```

* However, before running this code, a dedicated, non-privileged user should be created for the application:

  ```bash
  sudo useradd -m -s /bin/bash nodeapp
  ```

* Also, the directory for storing uploads outside the webroot must be created:

  ```bash
  sudo mkdir -p /srv/uploads
  ```

* The ownership of the `uploads` directory should be set to `nodeapp`, allowing only this user to manage the files:

  ```bash
  sudo chown -R nodeapp:nodeapp /srv/uploads
  ```

* Permissions should be adjusted to allow only read and write access for the `nodeapp` user:

  ```bash
  sudo chmod -R 600 /srv/uploads
  ```

* Finally, the Node.js application can be run under the `nodeapp` user:

  ```bash
  sudo -u nodeapp node /path/to/the/nodejs/app.js
  ```

@@TagEnd@@
