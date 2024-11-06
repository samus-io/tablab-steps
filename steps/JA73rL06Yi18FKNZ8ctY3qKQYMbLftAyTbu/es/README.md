# Almacenamiento de archivos y permisos del sistema de ficheros al cargar archivos

* Siempre que sea posible, se deben almacenar los archivos cargados en un servidor o servicio independiente dedicado exclusivamente al almacenamiento de archivos. Este enfoque proporciona una completa segregación de funciones entre la aplicación que gestiona las interacciones de los usuarios y las solicitudes de carga respecto al servidor que gestiona el almacenamiento de archivos, reduciendo así el impacto de posibles vulnerabilidades.
  * Si no es posible disponer de un sistema de almacenamiento independiente y es necesario guardar los archivos en el mismo servidor, se debe garantizar que se almacenan fuera del directorio *webroot*. De este modo se evita el acceso directo a los archivos a través del servidor web, minimizando el riesgo de explotación.
* Garantizar los permisos adecuados para los archivos, especialmente cuando se almacenan en el servidor, también es esencial para reducir los riesgos de seguridad.
* Se recomienda mantener los archivos cargados en memoria o en almacenamiento temporal durante el procesamiento y transferirlos al almacenamiento permanente únicamente después de pasar las comprobaciones de seguridad, ya que así se evita que los archivos maliciosos sean accesibles antes de ser eliminados por el proceso de validación.
* Si los usuarios necesitan acceder a los archivos cargados, ya estén almacenados en el mismo servidor, en otro servidor o en un servicio de almacenamiento, es aconsejable evitar conceder acceso directo. Un enfoque seguro consiste en implementar un gestor en el lado del servidor que asigne archivos a identificadores únicos, garantizando un acceso controlado y mitigando el riesgo de exposición no autorizada a archivos sensibles.

## Restringir los permisos del sistema de ficheros

* Los permisos del sistema de ficheros deben restringirse para controlar las acciones del usuario sobre los archivos subidos, normalmente permitiendo solo el acceso de lectura y escritura para archivos como imágenes o documentos e impidiendo los permisos de ejecución.
  * Si se requieren permisos de ejecución, se recomienda validar el contenido del archivo antes de almacenarlo como mejor práctica para detectar y bloquear macros, scripts ocultos o cualquier forma de malware.
  * Adicionalmente, si un archivo no requiere acceso de lectura, debe almacenarse únicamente con permisos de escritura, lo que limita el riesgo de acceso no autorizado.

## Uso de un controlador al permitir acceso público

* Cuando los archivos almacenados en un servidor requieren acceso público, se aconseja evitar el acceso directo a los archivos cargados a través directamente de URL. En su lugar, se recomienda implementar un controlador en el lado del servidor para suministrar los archivos de forma segura mediante un sistema de mapeo interno que haga referencia a los archivos por medio de identificadores únicos en lugar de por sus nombres reales.
  * A modo de ejemplo, el sistema debe asignar un ID único a cada nombre de archivo correspondiente (e.g., `12345` &rarr; `document.pdf`).
* Permitir el acceso directo de URLs a archivos (e.g., `https://domain.tbl/uploads/document.pdf`) puede exponer la aplicación a importantes riesgos de seguridad, particularmente en presencia de vulnerabilidades existentes relacionadas con ataques de *path traversal*, acceso no autorizado a archivos y potencial fuga de información sensible a través de URLs predecibles.
* Un gestor en el lado del servidor permite aplicar fácilmente permisos y controles de acceso antes de servir un archivo, garantizando que solamente los usuarios autorizados puedan acceder a ficheros específicos.

### Cómo funciona

* Una vez cargado y almacenado un archivo, este recibe un identificador único, y la conexión entre este identificador y el nombre del archivo se almacena en una base de datos o sistema equivalente.
* Cuando un usuario solicita un archivo (por ejemplo, solicitando `https://example.tbl/uploads/12345`), el gestor procesa la solicitud, busca el ID único `12345` en el sistema de mapeo, recupera el archivo asociado y se lo entrega al usuario.

@@TagStart@@java

## Código de incumplimiento en Java almacenando archivos en el mismo servidor Linux

* El siguiente fragmento de código en Java Jakarta almacena los archivos directamente en el directorio `uploads` dentro de la *webroot* y los hace accesibles al público a través de URLs (e.g., `https://domain.tbl/uploads/document.pdf`) sin ningún tipo de mapeo interno o saneamiento:

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

## Código de incumplimiento en Node.js usando `multer` y almacenando archivos en el mismo servidor Linux

* El siguiente fragmento de código utiliza `multer` para manejar la subida de archivos, sin embargo, almacena los archivos directamente en el directorio `uploads` dentro de la raíz web, y los hace accesibles públicamente a través de URLs (e.g., `https://domain.tbl/uploads/document.pdf`) sin ningún tipo de mapeo interno o saneamiento:

  ```javascript
  const express = require("express");
  const multer = require("multer");
  const path = require("path");
  const fs = require("fs");

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

## Código de cumplimiento en Java almacenando archivos en el mismo servidor Linux

* Manteniendo los archivos en memoria, almacenándolos fuera de *webroot* con los permisos adecuados e incorporando un sistema de mapeo para el acceso público, el siguiente código se adhiere a las mejores prácticas para el almacenamiento de archivos y permisos del sistema de ficheros:

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
  ...
  }
  ```

  * En este caso, el código está diseñado para tener en cuenta únicamente las cargas de archivos PDF en la aplicación.

* El código siguiente corresponde a la funcionalidad de descarga de archivos:

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
  ...
  }
  ```

* Sin embargo, antes de ejecutar este código, debe crearse primero la tabla `files`:

  ```sql
  CREATE TABLE IF NOT EXISTS files (
    id TEXT PRIMARY KEY,
    original_name TEXT,
    stored_name TEXT,
    path TEXT
  )
  ```

* Asimismo, también se debe crear el directorio para almacenar las cargas fuera de la raíz web:

  ```bash
  sudo mkdir -p /srv/uploads
  ```

* La propiedad del directorio `uploads` debe establecerse para el usuario sin privilegios que ejecuta el servidor (e.g., `www-data`), permitiendo únicamente a este usuario gestionar los archivos:

  ```bash
  sudo chown -R www-data:www-data /srv/uploads
  ```

* Por último, los permisos deben ajustarse para permitir únicamente el acceso de lectura y escritura al usuario `www-data`:

  ```bash
  sudo chmod -R 600 /srv/uploads
  ```

@@TagEnd@@

@@TagStart@@node.js

## Código de cumplimiento en Node.js usando `multer` y almacenando archivos en el mismo servidor Linux

* Manteniendo los archivos en memoria con `multer`, almacenándolos fuera del *webroot* con los permisos adecuados e incorporando un sistema de mapeo para el acceso público, el siguiente código se adhiere a las mejores prácticas para el almacenamiento de archivos y permisos del sistema de ficheros:

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

  * En este caso, el código está diseñado para tener en cuenta únicamente cargas de archivos PDF en la aplicación.

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

* Sin embargo, antes de ejecutar este código, debe crearse un usuario dedicado y sin privilegios para la aplicación:

  ```bash
  sudo useradd -m -s /bin/bash nodeapp
  ```

* Asimismo, también se debe crear el directorio para almacenar las cargas fuera de la raíz web:

  ```bash
  sudo mkdir -p /srv/uploads
  ```

* La propiedad del directorio `uploads` debe establecerse en `nodeapp`, permitiendo solamente a este usuario gestionar los archivos:

  ```bash
  sudo chown -R nodeapp:nodeapp /srv/uploads
  ```

* Los permisos deben ajustarse para permitir únicamente el acceso de lectura y escritura al usuario `nodeapp`:

  ```bash
  sudo chmod -R 600 /srv/uploads
  ```

* Por último, la aplicación Node.js puede ejecutarse bajo el usuario `nodeapp`:

  ```bash
  sudo -u nodeapp node /path/to/the/nodejs/app.js
  ```

@@TagEnd@@
