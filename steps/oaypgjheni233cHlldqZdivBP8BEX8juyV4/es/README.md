# Validación de extensiones de archivo

* La validación de extensiones garantiza que los archivos cargados coinciden con los tipos de archivo previstos mediante la comprobación de sus extensiones.

![File extension validation][1]

## Prácticas de seguridad recomendadas

* **Descodificar los nombres de archivo del formato URL codificado** antes de proceder a la validación para evitar técnicas de *bypass* como el uso del carácter de *byte* nulo (e.g., `image.php%00.png`).
* En los casos en que la aplicación web solamente acepte un único tipo de archivo (e.g., `.pdf`), **hardcodear la extensión permitida** en el momento de almacenar el archivo. Si se permiten múltiples tipos de archivo, entonces **definir una lista de extensiones permitidas** que restrinja las extensiones de archivo a solamente las requeridas para las necesidades de la organización (e.g., `.jpg`, `.jpeg` y `.png`).
* **Descartar archivos con múltiples extensiones o sin extensiones** para mitigar el riesgos de explotación.
* **Aplicar un filtrado robusto** en la validación para evitar errores comunes, como los patrones regex que se pueden eludir.

  > :warning: Hay que tener en cuenta que la validación en el lado del ciente puede eludirse, lo que la hace insuficiente; solamente se debe considerar como una herramienta para mejorar la experiencia del usuario.

@@TagStart@@java

## Código de incumplimiento en Java

* El siguiente fragmento de código en Java Jakarta aplica una validación de extensión que puede eludirse mediante el uso de una extensión doble. Únicamente comprueba si aparece `.jpg`, `.jpeg` o `.png` en el nombre del archivo, lo cual es insuficiente:

  <details>
    <summary>Dependencias</summary>

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

  </details>

  ```java
  @WebServlet("/upload")
  @MultipartConfig
  public class FileUploadServlet extends HttpServlet {

      @Override
      protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
          Part filePart;

          try {
              // Get the file part from the request
              filePart = request.getPart("file");
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

          response.getOutputStream().println("File uploaded successfully");
          response.setStatus(200);
      }
  }
  ```

@@TagEnd@@

@@TagStart@@node.js

## Código de incumplimiento en Node.js usando `multer`

* El siguiente fragmento de código utiliza `multer` para cargar archivos, pero la validación de extensión aplicada puede eludirse mediante el uso de una extensión doble. Únicamente comprueba si aparece `.jpg`, `.jpeg` o `.png` en el nombre del archivo, lo cual es insuficiente:

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

## Código de cumplimiento en Java

* El fragmento de código que se muestra seguidamente protege la función de carga de archivos descodificando el nombre del archivo antes de la validación, aplicando una lista de extensiones permitidas y evitando los archivos sin extensión o con extensiones múltiples:

  <details>
    <summary>Dependencias</summary>

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

  </details>

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
              filePart = request.getPart("file");
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

          response.getOutputStream().println("File uploaded successfully");
          response.setStatus(200);
      }
  }
  ```

@@TagEnd@@

@@TagStart@@node.js

## Código de cumplimiento en Node.js usando `multer`

* El fragmento de código que se muestra seguidamente protege la función de carga de archivos descodificando el nombre del archivo antes de la validación, aplicando una lista de extensiones permitidas y evitando los archivos sin extensión o con extensiones múltiples:

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

## Validación de extensiones de archivo en el lado del cliente

* La extensión del archivo puede comprobarse en el frontend mediante el atributo HTML `accept`, lo que contribuye a evitar que los usuarios envíen archivos inesperados, aunque no es fiable a efectos de seguridad:

  ```html
  <input type="file" id="fileInput" accept=".jpg, .jpeg, .png" />
  ```

[1]: /static/images/file-extension-validation.png
