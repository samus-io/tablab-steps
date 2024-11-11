# Validación insegura de tipos de archivo

* Los mecanismos habituales para determinar el tipo de un archivo utilizan la cabecera `Content-Type`, la cual indica el tipo de archivo dentro de una petición HTTP, y el número mágico situado al principio del contenido del archivo. Ambos métodos son vulnerables a la manipulación por parte de usuarios maliciosos, lo que los hace completamente inseguros para la validación del tipo de archivo desde el punto de vista de la seguridad.

  > :older_man: Estos métodos siguen siendo útiles para detectar rápidamente el tipo de archivo y mejorar la experiencia del usuario, aunque no fiables a efectos de seguridad.

## Validación de tipos de archivo mediante la cabecera `Content-Type`

* La cabecera `Content-Type` se utiliza para indicar el [tipo MIME][1] original (e.g., `image/png`, `text/plain`, `application/pdf`) del recurso antes de cualquier codificación de contenido aplicada previamente a la transmisión.
* MIME, abreviatura de `Multipurpose Internet Mail Extensions (MIME)`, es un estándar desarrollado a principios de los 90 para permitir que los correos electrónicos incluyeran contenido multimedia y otros archivos binarios, el cual también se emplea en la web para definir la naturaleza de los datos en el cuerpo del mensaje, la codificación aplicada y cómo deben procesarse o mostrarse:

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

  * Las cabeceras HTTP que se utilizan habitualmente junto con MIME para gestionar el contenido en las transacciones HTTP son:
    * `Content-Type`: para especificar el tipo y subtipo de medio del contenido.
    * `Content-Disposition`: para indicar si el contenido puede mostrarse `inline` (valor por defecto), lo que significa como parte de una página web, o tratarse como un `attachment` para ser descargado en el almacenamiento local. En un cuerpo `multipart/form-data`, la cabecera HTTP `Content-Disposition` se encarga de proporcionar información sobre cada subparte.
* La validación del tipo de archivo basada en el tipo MIME de la cabecera `Content-Type` no es fiable a nivel de seguridad, ya que puede ser fácilmente suplantada, a pesar de que ciertas librerías o paquetes pueden depender de este valor para determinar que el archivo coincide con el tipo esperado.
* Sin embargo, puede seguir siendo útil para mejorar la experiencia del usuario ofreciendo una comprobación preliminar de los tipos de archivo incorrectos.

@@TagStart@@java

### Código de incumplimiento en Java Jakarta

* Esta implementación en Java Jakarta gestiona las cargas de archivos identificando el tipo de archivo a través de la cabecera HTTP `Content-Type` recibida y seguidamente realiza una comprobación de seguridad en consecuencia que puede ser fácilmente eludida suplantando la cabecera `Content-Type` en la solicitud:

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
    import java.util.Set;
    ```

  </details>

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
              filePart = request.getPart("file");
          }
          catch (ServletException | IOException e) {
              JsonObject model = Json.createObjectBuilder().add("message", "No file uploaded").build();
              response.getOutputStream().println(model.toString());
              response.setStatus(400);
              return;
          }

          // Get MIME type via the Content Type and compare it with allowed MIME types
          String mimetype = filePart.getContentType();

          if (!ALLOWED_TYPES.contains(mimetype)) {
              JsonObject model = Json.createObjectBuilder().add("message", "Unexpected file type").build();
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

### Código de incumplimiento en Node.js usando `multer`

* Esta implementación utiliza el paquete `multer` para gestionar las cargas de archivos, el cual identifica el tipo de archivo a través de la cabecera HTTP `Content-Type` recibida, y seguidamente realiza una comprobación de seguridad en consecuencia que puede ser fácilmente eludida suplantando la cabecera `Content-Type` en la solicitud:

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

### Validación de tipos de archivo en el lado del cliente

* El tipo de archivo a través de MIME también puede verificarse en *front-end* con unas pocas líneas de JavaScript, lo que ayuda a evitar que los usuarios envíen archivos no deseados, aunque no es válido desde el punto de vista de la seguridad:

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

## Validación de tipos de archivo mediante el número mágico

* El número mágico es una secuencia única de *bytes* situada al principio del contenido de un archivo que se utiliza para identificar el tipo de archivo, según una [lista de firmas de archivos][1]. Estos *bytes* sirven como firma para el archivo, permitiendo al sistema operativo o a las aplicaciones determinar su tipo, incluso sin basarse en la extensión del mismo:
  * Los archivos `jpeg (jpg)` empiezan por `FF D8 FF` (correspondiente a `ÿØÿÛ`).
  * Los archivos `png` empiezan por `89 50 4E 47 0D 0A 1A 0A` (correspondiente a `‰PNG␍␊␚␊`).
  * Los archivos `pdf` empiezan por `25 50 44 46 2D` (correspondiente a `%PDF-`).
  * Los archivos `zip` empiezan por `50 4B 03 04` (correspondiente a `PK␃␄`).
* Los atacantes pueden añadir fácilmente un número mágico válido a los archivos maliciosos, haciéndolos parecer legítimos. Por ejemplo, añadir la firma `%PDF-2.0` al principio de un archivo *webshell* puede engañar al sistema haciéndole creer que se trata de un archivo PDF.
  > :older_man: `webshell` es el nombre común dado a un *script* utilizado por los atacantes que, cuando se carga en un servidor web, les permite ejecutar comandos del sistema y tomar el control del servidor como si tuvieran acceso directo a la línia de comandos, pero todo de forma remota a través de la web.
* Aunque no resulta útil para la seguridad, el número mágico puede ser conveniente para comprobar el tipo de archivo enviado por el usuario y evitar que se carguen archivos erróneos en una aplicación web. Sin embargo, el principal problema es que determinadas librerías o paquetes se pueden basar únicamente en este número para identificar el tipo de archivo.

@@TagStart@@java

### Código de incumplimiento en Java Jakarta usando `Apache Tika`

* El siguiente fragmento de código utiliza la librería `Apache Tika`, la cual identifica el tipo de archivo a través del número mágico, y seguidamente realiza una comprobación de seguridad en consecuencia que puede ser fácilmente eludida a través de la manipulación del número mágico del archivo:

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
    import org.apache.tika.Tika;

    import java.io.IOException;
    import java.util.Set;
    ```

  </details>

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
              filePart = request.getPart("file");
          }
          catch (ServletException | IOException e) {
              JsonObject model = Json.createObjectBuilder().add("message", "No file uploaded").build();
              response.getOutputStream().println(model.toString());
              response.setStatus(400);
              return;
          }

          // Get MIME type via the magic number and compare it with allowed MIME types
          Tika tika = new Tika();
          String mimetype = tika.detect(filePart.getInputStream());

          if (!ALLOWED_TYPES.contains(mimetype)) {
              JsonObject model = Json.createObjectBuilder().add("message", "Unexpected file type").build();
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

### Código de incumplimiento en Node.js usando `file-type`

* El siguiente fragmento de código utiliza el paquete `file-type`, el cual identifica el tipo de archivo a través del número mágico, y seguidamente realiza una comprobación de seguridad en consecuencia que puede ser fácilmente eludida a través de la manipulación del número mágico del archivo:

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
