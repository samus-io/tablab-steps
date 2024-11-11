# Aplicación de control de acceso a funciones de carga de archivos en Java Jakarta

* Al aplicar control de acceso a las funcionalidades de carga de archivos, es esencial tener en cuenta tanto el acceso a la propia función de carga de archivos de la aplicación como el acceso a los archivos cargados.
* Generalmente, la función de carga de archivos de la aplicación se encuentra abierta al público o restringida a ciertos usuarios, mientras que el acceso a los archivos se encuentra abierto al público, restringido a ciertos usuarios o totalmente prohibido.
* Autenticación, autorización y control de acceso son los términos que intervienen en este proceso:
  * La autenticación es el proceso de verificación de la identidad de un usuario o sistema.
  * La autorización es el proceso de especificar qué acciones o recursos están permitidos a un usuario o sistema.
  * El control de acceso se refiere a los mecanismos que imponen tanto la autenticación como la autorización, determinando quién puede acceder a qué recursos y en qué circunstancias.
* La aplicación de estos conceptos ayuda a evitar la carga no autorizada de archivos, las filtraciones de datos y el acceso a información confidencial.

## Código de incumplimiento en Java Jakarta

* El siguiente fragmento de código carece de mecanismos de control de acceso, lo que expone a la aplicación web a ser susceptible de vulnerabilidades de *broken access control* y a una potencial filtración de información:

  <details>
    <summary>Dependencias</summary>

    ```java
    import jakarta.json.Json;
    import jakarta.json.JsonArray;
    import jakarta.json.JsonArrayBuilder;
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
    import java.io.OutputStream;
    import java.util.Arrays;
    import java.util.Optional;
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
  ```
  
  <details>
    <summary>Código contextual</summary>

    ```java
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

  </details>

  ```java
  @WebServlet("/download/*")
  public class FileDownloadServlet extends HttpServlet {
  
      private static final int BUFFER_SIZE = 8192; // Buffer size for file reading
      private String uploadFolderPath;
  
      @Override
      public void init(ServletConfig config) throws ServletException {
        ...
      }

      @Override
      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
          String pathInfo = request.getPathInfo();
  
          // If no specific file is requested, return the list of all available files
          if (pathInfo == null || pathInfo.equals("/")) {
              sendFileListResponse(response);
              return;
          }
  
          // Extract the filename from the URL, removing the leading slash
          String filename = pathInfo.substring(1);
          File requestedFile = new File(uploadFolderPath, filename);
  
          // Check if the requested file exists; if not, send a 404 error response
          if (!requestedFile.exists()) {
              sendErrorResponse(response, "File not found", HttpServletResponse.SC_NOT_FOUND);
              return;
          }
  
          // Send the requested file back to the client
          sendFileResponse(response, requestedFile);
      }
  ```

  <details>
    <summary>Código contextual</summary>

    ```java
        private void sendFileListResponse(HttpServletResponse response) throws IOException {
            JsonArray fileListJson = getUploadedFilesJson();

            response.setContentType("application/json");
            response.setCharacterEncoding("UTF-8");
            response.setStatus(HttpServletResponse.SC_OK);
    
            // Use try-with-resources to ensure the OutputStream is properly closed
            try (OutputStream out = response.getOutputStream()) {
                out.write(fileListJson.toString().getBytes());
            }
        }
    
        private JsonArray getUploadedFilesJson() {
            // Retrieve the list of filenames from the uploads directory, or an empty list if none are found
            File uploadDir = new File(uploadFolderPath);
            String[] filenames = Optional.ofNullable(uploadDir.list()).orElse(new String[0]);
            return convertArrayToJson(filenames);
        }
    
        private JsonArray convertArrayToJson(String[] filenames) {
            // Stream through filenames to efficiently build a JSON array
            JsonArrayBuilder arrayBuilder = Json.createArrayBuilder();
            Arrays.stream(filenames).forEach(arrayBuilder::add);
            return arrayBuilder.build();
        }
    
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
    }
    ```

  </details>

## Código de cumplimiento en Java Jakarta

* El siguiente fragmento de código utiliza un *middleware* para permitir la carga de archivos y el acceso a los mismos exclusivamente a usuarios autenticados:

  <details>
    <summary>Dependencias</summary>

    ```java
    import jakarta.json.Json;
    import jakarta.json.JsonObject;
    import jakarta.servlet.*;
    import jakarta.servlet.annotation.WebFilter;
    import jakarta.servlet.http.HttpServletRequest;
    import jakarta.servlet.http.HttpServletResponse;
    
    import java.io.IOException;
    import java.io.OutputStream;
    ```

  </details>

  ```java
  @WebFilter(urlPatterns = {"/upload", "/download/*"})
  public class AuthFilter implements Filter {
  
      @Override
      public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException {
          HttpServletRequest httpRequest = (HttpServletRequest) request;
          HttpServletResponse httpResponse = (HttpServletResponse) response;

          try {
              HttpSession session = httpRequest.getSession();

              // Get User object
              User user = (User) session.getAttribute("user");

              if (user != null) 
                  chain.doFilter(request, response);
              else
                httpResponse.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Unauthorized access");
          } catch (IOException | ServletException e) {
              JsonObject errorJson = Json.createObjectBuilder().add("message", "Something went wrong").build();

              httpResponse.setContentType("application/json");
              httpResponse.setCharacterEncoding("UTF-8");
              httpResponse.setStatus(500);

              try (OutputStream out = httpResponse.getOutputStream()) {
                  out.write(errorJson.toString().getBytes());
              }
          }
      }
  }
  ```

  * Se puede observar cómo el middleware garantiza que únicamente los usuarios autenticados (aquellos con una sesión activa que contenga un objeto `User`) puedan acceder a las rutas `/upload` y `/download/*`, devolviendo en caso contrario un estado `401 Unauthorized`.

## Ejercicio para practicar :writing_hand:

* La siguiente aplicación, a pesar de las apariencias, carece de mecanismos de control de acceso, ya que no existen medidas en el servidor para evitar que usuarios anónimos carguen o descarguen archivos.
* Como puede demostrarse abriendo el editor de código mediante el botón `Open Code Editor` e iniciando la terminal integrada, cualquiera puede ejecutar los siguientes comandos para cargar y descargar un archivo, siendo `APP_URL` una variable de entorno que apunta a la ruta base de la aplicación web:

  ```bash
  curl -F "formFile=@landscape.png" $APP_URL/upload
  ```

  ```bash
  curl $APP_URL/download/landscape.png -o landscape.png
  ```

* Asimismo, cualquier usuario registrado en la aplicación puede utilizar libremente las funciones de carga y descarga sin restricciones una vez iniciada la sesión, como por ejemplo:
  * `jackson01` (rol: `admin`, contraseña: `dX2%V5h|s5>C}]V`).
  * `johndoe` (rol: `moderator`, contraseña: `7j@H!3p%!&8l^S2`).
  * `alice99` (rol: `member`, contraseña: `u^#B&2y!F7@d$E9`).
* El objetivo aquí es editar el código fuente para aplicar una política de control de acceso en el servidor, limitando la subida de archivos a los usuarios autenticados (aquellos con una sesión activa) y permitiendo únicamente a los usuarios con el rol `admin` o `moderator` la descarga de archivos. Las peticiones exitosas deberían devolver un estado `200 OK`, mientras que los intentos no autorizados deberían resultar en un estado `401 Unauthorized`.
  * Más concretamente, las modificaciones de código deben realizarse en los archivos `AuthFilter.java` y `AuthPrivFilter.java`, situados en `/home/coder/app/src/main/java/io/ontablab/`.
* Una vez realizados los cambios, se debe pulsar el botón `Verify Completion` para confirmar que se ha completado el ejercicio.

  @@ExerciseBox@@
