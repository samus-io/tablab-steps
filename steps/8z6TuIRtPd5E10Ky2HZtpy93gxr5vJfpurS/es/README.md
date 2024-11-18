# Desafíos de las aplicaciones en la carga y descarga de archivos

* Cuando se implementan funcionalidades de carga y descarga de archivos en una aplicación, es crucial imponer ciertos límites para garantizar la seguridad y el rendimiento.

![Upload and download limits when uploading files][1]

## Consideraciones de seguridad

* Generalmente, emplear un servicio de almacenamiento dedicado, posiblemente de terceros, es la mejor opción desde el punto de vista de la seguridad. En cualquier caso, independientemente del enfoque adoptado, deberían existir las siguientes medidas:
  * **Limitar el tamaño** de cualquier archivo cargado para evitar un uso excesivo del espacio de almacenamiento y para proteger al sistema de archivos excesivamente grandes que podrían afectar a su rendimiento o provocar errores.
  * **Limitar el total de cargas que un usuario puede realizar** para proteger la capacidad de almacenamiento y minimizar el riesgo de un ataque de `Denegación de Servicio (DoS)` restringiendo el número de ficheros que un usuario puede subir. Esta medida ayuda a evitar a prevenir que el systema se sature con un exceso de archivos, lo cual podría consumir los recursos de almacenamiento.
  * **Limitar el número de solicitudes de carga y descarga** imponiendo restricciones al número de solicitudes de carga y descarga que un usuario puede realizar en un breve periodo de tiempo. Esto ayuda a evitar que un solo usuario sature el sistema con un gran número de solicitudes en un corto periodo de tiempo y garantiza un procesamiento fluido del tráfico legítimo.

@@TagStart@@java

## Código de incumplimiento en Java Jakarta

* Se muestra seguidamente un ejemplo de implementación vulnerable en Java Jakarta en la que no se aplican las medidas de seguridad mencionadas:

  <details>
    <summary>Dependencias</summary>

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
    <summary>Código contextual</summary>

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

## Código de incumplimiento en Node.js usando `multer`

* Se muestra seguidamente un ejemplo de implementación vulnerable usando `multer` y `Express` en la que no se aplican las medidas de seguridad mencionadas:

  <details>
    <summary>Dependencias</summary>

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

  * En este código **no se impone ningún límite de tamaño de archivo**, lo que permite a los usuarios subir archivos excesivamente grandes, que pueden provocar caídas del servidor o un consumo significativo de almacenamiento.
  * **No se establecen límites al número total de archivos que un usuario puede cargar**, lo que permite cargas ilimitadas que pueden poner en peligro la capacidad de almacenamiento del servidor.
  * **No existe límite de la tasa de carga y descarga**, lo que permite a los usuarios enviar un gran volumen de solicitudes de carga y descarga al servidor, agotando potencialmente sus recursos, degradando el rendimiento general o incluso provocando una denegación de servicio (DoS).

[1]: /static/images/speed-limit.png
