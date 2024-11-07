# Saneamiento de nombres de archivo

* El saneamiento de nombres de archivo es un proceso esencial destinado a garantizar que los nombres de archivo sean seguros y compatibles con el sistema en el que se van a utilizar.
* Consiste en validar y potencialmente modificar los nombres originales de los archivos recibidos para prevenir amenazas de seguridad o fallos operativos que puedan comprometer la integridad del sistema.

## Lista de control de las medidas de seguridad

* Siempre que sea posible, se deben utilizar nombres de archivo únicos y aleatorios al almacenar los ficheros (e.g., adoptando UUID). Si las restricciones de lógica de la organización impiden este enfoque, entonces se recomienda:

  * [ ] Establecer un límite de longitud del nombre de archivo.
  * [ ] Limitar los caracteres permitidos (e.g., únicamente considerar `A-Z`, `a-z`, `0-9`, `-`, y `.` como caracteres válidos).
  * [ ] Tratar los nombres de archivo sin distinguir mayúsculas de minúsculas.
  * [ ] Restringir los nombres reservados en Windows y Linux.
  * [ ] Evitar los archivos ocultos y los puntos y espacios finales (e.g., `.htaccess`).

## Generar de nombres de archivo únicos y aleatorios

* La creación de nombres de archivo únicos y aleatorios al almacenar los archivos cargados evita las colisiones de nombres de archivo, mitiga los ataques path traversal, oculta los nombres de archivo originales que podrían exponer detalles sensibles, mejora la seguridad contra la ejecución de archivos maliciosos reduciendo el riesgo de que un atacante pueda localizar y ejecutar dichos archivos, y evita los ataques de enumeración de archivos.
* Una forma fiable de crear nombres de archivo impredecibles y no sobrescribibles es utilizar `Universally Unique Identifier (UUID)` o `Globally Unique Identifier (GUID)`.
* Este enfoque es especialmente útil en situaciones en las que no es necesario conservar los nombres de archivo originales proporcionados por los usuarios.

## Límites de longitud de los nombres de archivo

* Los distintos sistemas de archivos imponen límites variables a la longitud de los nombres de archivo, lo que puede afectar a la compatibilidad y la seguridad. Por ejemplo, el sistema de archivos `MS-DOS FAT` establece el formato de nombre de archivo `8.3`, que solo admite 8 caracteres para el nombre y 3 para la extensión, con el fin de mantener la compatibilidad con el software heredado.
* Los sistemas de archivos modernos como `NTFS` pueden soportar nombres de archivo más largos, aunque Windows ha impuesto tradicionalmente un límite `MAX_PATH` de 260 caracteres. Superar este límite puede provocar errores de truncamiento o de acceso a archivos, aunque las nuevas versiones de Windows permiten eliminar este límite mediante los ajustes de configuración adecuados.
* Tener en cuenta los límites de longitud de los nombres de archivo es esencial para evitar problemas como errores de acceso a los archivos, truncamientos o riesgos de seguridad debidos a una mala interpretación del sistema de archivos.

## Aplicar validación de entrada a los nombres del archivo

* Cuando se permiten nombres de archivo definidos por el usuario, es crucial validar exhaustivamente las entradas para prevenir vulnerabilidades como *path traversal* o ataques de inyección, así como para evitar errores operativos.
* *Path traversal* se refiere al proceso de manipulación de rutas de archivos para acceder a ubicaciones no deseadas fuera del directorio designado. Los usuarios maliciosos incluyen secuencias como `../` en los nombres de archivo para atravesar directorios y almacenar archivos en ubicaciones no deseadas. Por ejemplo, un nombre de archivo como `../../../../var/www/html/index.php` colocaría el archivo en *web root*, reemplazando potencialmente el contenido del archivo principal de una aplicación web PHP.
* Los nombres de archivo también pueden utilizarse para explotar vulnerabilidades relacionadas con la forma en que la aplicación procesa y gestiona el mismo. Por ejemplo, un nombre de archivo como `sleep(20)-- -.jpg` podría desencadenar una inyección SQL, `<svg onload=alert("XSS")>` podría conducir a XSS, y `; sleep 20;` podría dar lugar a una inyección de comandos.
* Permitir únicamente un conjunto seguro de caracteres, como caracteres alfanuméricos, guiones y puntos, es la práctica de seguridad más eficaz para evitar *path traversal* y ataques de inyección en los nombres de archivo.

## Distinción entre mayúsculas y minúsculas

* Para evitar conflictos como la sobreescritura involuntaria de archivos o problemas de acceso, es importante que los nombres de archivo no distingan entre mayúsculas y minúsculas. Utilizar convenciones de nomenclatura coherentes y validar sin diferenciar entre mayúsculas y minúsculas puede ayudar a mitigar los riesgos.
* Omitir este comportamiento puede llevar a la sobreescritura de archivos o a accesos no autorizados, especialmente en entornos que dependen del tratamiento de archivos son sensibles a mayúsculas y minúsculas.
* Por defecto, los sistemas de ficheros de Windows no distinguen entre mayúsculas y minúsculas, lo que significa que `Image.png`, `IMAGE.PNG` e `image.png` se consideran idénticos.

## Limitaciones de caracteres específicos del sistema para nombrar archivos

* Los distintos sistemas de ficheros aplican restricciones específicas a determinados caracteres en nombres de archivo para preservar la integridad del sistema y evitar errores de parseo de rutas de archivo.
* Intentar guardar un archivo utilizando nombres reservados o caracteres restringidos puede provocar errores inesperados e interrupciones del servicio.

### Caracteres restringidos y nombres reservados en Windows

* En Windows, los caracteres especiales `<`, `>`, `:`, `"`, `/`, `\`, `|`, `?`, `*`, `\x00` no están permitidos en los nombres de archivo.
* Adicionalmente, ciertos nombres como `AUX`, `COM1`, `COM2`, `COM3`, `COM4`, `COM5`, `COM6`, `COM7`, `COM8`, `COM9`, `CON`, `LPT1`, `LPT2`, `LPT3`, `LPT4`, `LPT5`, `LPT6`, `LPT7`, `LPT8`, `LPT9`, `NUL` y `PRN` están reservados por el sistema para dispositivos o recursos del mismo y no pueden utilizarse como nombres de fichero o directorio.
* Por otra parte, los [caracteres de control ASCII][1] comprendidos entre 0 y 31 tampoco están permitidos en los nombres de archivo.

### Caracteres restringidos y nombres reservados en Linux

* En Linux, los caracteres restringidos en los nombres de archivo son `/`, utilizado como separador de directorios, y el carácter nulo `\x00`, también conocido como terminador nulo, que se utiliza en muchos sistemas, incluido Linux, como terminador de cadenas.
* Los nombres reservados en sistemas tipo UNIX son `.` y `..`.

## Evitar archivos ocultos y que terminen con un punto o un espacio

* Empezar un nombre de archivo con un punto (e.g., `.htaccess`) está ampliamente aceptado y se utiliza habitualmente para crear archivos ocultos, especialmente en sistemas tipo UNIX, donde el punto indica que el archivo debe quedar oculto de los listados de directorios estándar, e incluso ser omitido en los análisis de seguridad automatizados. Los atacantes pueden aprovechar estos archivos para eludir controles de seguridad, ocultar scripts maliciosos o modificar configuraciones del servidor.
* Los archivos que terminan con un punto o un espacio pueden aprovecharse de las incoherencias en la forma en que los distintos sistemas operativos y sistemas de ficheros gestionan los nombres de archivo, lo que provoca errores de acceso a los mismos, problemas de compatibilidad en el Explorador de Windows o problemas con otras aplicaciones, incluso cuando el sistema de ficheros subyacente los admite.

@@TagStart@@java

## Código de incumplimiento en Java

* El siguiente fragmento de código muestra una implementación insegura de carga de archivos en una aplicación Java Jakarta, en la que se utiliza el nombre de archivo recibido por parte del usuario sin ningún tipo de validación, lo que conlleva riesgos como la sobreescritura y la enumeración de archivos, entre otros:

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
      private String uploadFolderPath;

      @Override
      public void init(ServletConfig config) throws ServletException {
          super.init(config);

          // Define the path to the folder where uploaded files will be stored
          uploadFolderPath = getServletContext().getRealPath("/") + "uploads";

          // Check if the 'uploads' folder exists; if not, create it
          File uploadDir = new File(uploadFolderPath);
          if (!uploadDir.exists()) {
              uploadDir.mkdirs();
          }
      }

      @Override
      protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
          Part filePart;

          try {
              // Get the file part from the request
              filePart = request.getPart("file");
          } catch (ServletException | IOException e) {
              JsonObject model = Json.createObjectBuilder().add("message", "No file uploaded").build();
              response.getOutputStream().println(model.toString());
              response.setStatus(400);
              return;
          }

          try {
              // Use the original filename provided by the user
              String filename = filePart.getSubmittedFileName(); 

              // Save the file using the filename and content stream from the file part
              saveFile(filename, filePart.getInputStream());
          } catch (IOException e) {
              response.setStatus(500);
              return;
          }

          response.getOutputStream().println("File uploaded successfully");
          response.setStatus(200);
      }
  
      private void saveFile(String filename, InputStream fileContent) throws IOException {
          File file = new File(uploadFolderPath, filename);

          // Try-with-resources to ensure the FileOutputStream is automatically closed after use
          try (FileOutputStream fos = new FileOutputStream(file)) {
              byte[] buffer = new byte[8192];
              int bytesRead;

              // Reads the file content in chunks and writes it to the destination file
              while ((bytesRead = fileContent.read(buffer)) != -1) {
                  fos.write(buffer, 0, bytesRead);
              }
          }
      }
  }
  ```

@@TagEnd@@

@@TagStart@@node.js

## Código de incumplimiento en Node.js usando `multer`

* El siguiente fragmento de código muestra una implementación insegura de carga de archivos en una aplicación `Express.js` utilizando `multer`, en la que se utiliza el nombre de archivo recibido por parte del usuario sin ningún tipo de validación, lo que conlleva riesgos como la sobreescritura y la enumeración de archivos, entre otros:

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

## Código de cumplimiento en Java generando un nombre de archivo aleatorio

* El siguiente fragmento de código ilustra cómo gestionar la carga de archivos en Java Jakarta y almacenar los archivos en una carpeta específica con nombres generados aleatoriamente mediante UUID, garantizando que los nombres de los archivos sean únicos e impredecibles:

  ```java
  import java.util.UUID;

  ...

  @Override
  protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {

    ...

    try {
        // Generate a random file name via UUID
        String filename = UUID.randomUUID() + ".pdf";

        // Save the file using the filename and content stream from the file part
        saveFile(filename, filePart.getInputStream());
    } catch (IOException e) {
        response.setStatus(500);
        return;
    }

    response.getOutputStream().println("File uploaded successfully");
    response.setStatus(200);
  }
  ```

  * En este caso, el código está diseñado para tener en cuenta únicamente cargas de archivos PDF en la aplicación.

@@TagEnd@@

@@TagStart@@node.js

## Código de cumplimiento en Node.js usando `multer` y generando un nombre de archivo aleatorio

* El siguiente fragmento de código ilustra cómo gestionar la carga de archivos utilizando el *middleware* `multer` y almacenando los archivos en una carpeta específica con nombres generados aleatoriamente mediante UUID, garantizando que los nombres de los archivos sean únicos e impredecibles:

  ```javascript
  const uuid = require("uuid");

  ...

  const storage = multer.diskStorage({
    destination: (req, file, cb) => {
      cb(null, uploadFolderPath);
    },
    filename: (req, file, cb) => {
      cb(null, `${uuid.v4()}.pdf`); 
    }
  });

  ...
  ```

  * En este caso, el código está diseñado para tener en cuenta únicamente cargas de archivos PDF en la aplicación.

@@TagEnd@@

@@TagStart@@java

## Código de cumplimiento en Java manteniendo el nombre de archivo original

* El siguiente fragmento de código muestra cómo gestionar la carga de archivos en Java Jakarta almacenando los archivos en una carpeta específica y conservando el nombre de archivo original enviado por el usuario.
* El código aplica un límite personalizado a la longitud de los nombres de archivo, restringe los caracteres y los nombres reservados, no distingue entre mayúsculas y minúsculas, evita los archivos ocultos o los que terminan con un punto o un espacio, y garantiza que no se produzcan colisiones entre los nombres de archivo:

<details>
  <summary>Dependencies</summary>

  ```java
  import java.net.URLDecoder;
  import java.nio.charset.StandardCharsets;
  import java.security.SecureRandom;
  import java.util.regex.Pattern;
  ```

</details>

  ```java
  private static final Integer MAX_FILENAME_LENGTH = 100;
  private static final String ALPHANUMERIC_CHARACTERS = "abcdefghijklmnopqrstuvwxyz0123456789";

  private String generateRandomString(Integer length) {
      SecureRandom secureRandom = new SecureRandom();
      StringBuilder stringBuilder = new StringBuilder(length);

      for (int i = 0; i < length; i++) {
          int index = secureRandom.nextInt(ALPHANUMERIC_CHARACTERS.length());
          stringBuilder.append(ALPHANUMERIC_CHARACTERS.charAt(index));
      }

      return stringBuilder.toString();
  }

  private Boolean isFilenameAllowed(String filename) {
      // Restrict to alphanumeric, hyphens, spaces and dots
      Pattern pattern = Pattern.compile("^[a-zA-Z0-9.\\- ]*$");
      return pattern.matcher(filename).matches();
  }

  private Boolean isWindowsReservedName(String filename) {
      Pattern pattern = Pattern.compile("^(con|prn|aux|nul|com[0-9]|lpt[0-9])(\\..*)?$", Pattern.CASE_INSENSITIVE);
      return pattern.matcher(filename).matches();
  }

  private String generateSafeFilename(String originalFilename) throws SecurityException {
      String decodedFilename = URLDecoder.decode(originalFilename, StandardCharsets.UTF_8);

      if (decodedFilename.length() > MAX_FILENAME_LENGTH)
          throw new SecurityException("File name too long");
      
      if (!isFilenameAllowed(decodedFilename))
          throw new SecurityException("File name can only contain alphanumeric characters, hyphens, dots and spaces");
  
      // Avoid hidden files and trailing periods and spaces
      String trimmedFilename = decodedFilename.replaceAll("^[.\\s]+|[.\\s]+$", "");

      // Handle case-insensitive
      String lowerCaseFilename = trimmedFilename.toLowerCase();

      // Replace spaces with hyphens
      String canonicalizedFilename = lowerCaseFilename.replaceAll("\\s+", "-");

      // Restrict reserved names in Windows
      if (isWindowsReservedName(canonicalizedFilename)) {
          throw new SecurityException("File name cannot be a Windows reserved name");
      }

      // Ensure no file name collisions
      String randomString = generateRandomString(6);
      return randomString + "_" + canonicalizedFilename;
  }
  ```

  ```java
  @Override
  protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {

    ...

    try {
        String filename = filePart.getSubmittedFileName();
        String safeFilename = generateSafeFilename(filename);

        saveFile(safeFilename, filePart.getInputStream());
    } catch (IOException e) {
        response.setStatus(500);
        return;
    }
    catch (SecurityException e) {
        response.setStatus(400);
        return;
    }

    response.getOutputStream().println("File uploaded successfully");
    response.setStatus(200);
  }
  ```

@@TagEnd@@

@@TagStart@@node.js

## Código de cumplimiento en Node.js usando `multer` y manteniendo el nombre de archivo original

* El siguiente fragmento de código demuestra cómo gestionar la subida de archivos utilizando el *middleware* `multer` y almacenando los archivos en una carpeta específica mientras se conserva el nombre de archivo original enviado por el usuario.
* El código aplica un límite personalizado a la longitud de los nombres de archivo, restringe caracteres y nombres reservados utilizando el paquete `sanitize-filename`, trata los nombres de archivo sin distinguir mayúsculas de minúsculas, evita los archivos ocultos o los que terminan con un punto o un espacio y garantiza que no se produzcan colisiones entre nombres de archivo:

  ```javascript
  const sanitizeFilename = require("sanitize-filename");
  ```

  ```javascript
  const MAX_FILENAME_LENGTH = 100;

  const generateRandomString = (length = 6) => {
    return Math.random().toString(36).substring(2, 2 + length);
  };

  const storage = multer.diskStorage({
    destination: (req, file, cb) => {
      cb(null, uploadFolderPath);
    },
    filename: (req, file, cb) => {
      const decodedFilename = decodeURIComponent(file.originalname);
      const error = new multer.MulterError("LIMIT_UNEXPECTED_FILE", file.fieldname);

      if (decodedFilename.length > MAX_FILENAME_LENGTH) {
        error.message = "File name too long";
        cb(error);
        return;
      }

      const trimmedFilename = decodedFilename.replace(/^[.\s]+|[.\s]+$/g, ""); // Remove enclosing periods and spaces
      const lowerCaseFilename = trimmedFilename.toLowerCase();
      const canonicalizedFilename = lowerCaseFilename.replace(/\s+/g, "-"); // Replace spaces with hyphens
      const sanitizedFilename = sanitizeFilename(canonicalizedFilename);

      if (!sanitizedFilename) {
        error.message = "Invalid file name";
        cb(error);
        return;
      }

      // Ensure no file name collisions
      const randomString = generateRandomString();
      const filename = `${randomString}_${sanitizedFilename}`;

      cb(null, filename);
    }
  });
  ```

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

      res.send("File uploaded successfully");
    });
  });
  ```

  > :warning: Dado que algunas de las medidas de seguridad implementadas pueden eliminar caracteres no deseados, es aconsejable aplicar primero el saneamiento del nombre del archivo y luego verificar la extensión del mismo.

@@TagEnd@@

[1]: https://www.ascii-code.com/