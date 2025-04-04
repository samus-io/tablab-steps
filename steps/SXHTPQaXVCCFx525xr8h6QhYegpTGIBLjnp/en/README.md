# Enforcing access control to file upload functionalities in Java Jakarta

* When applying access control to file upload functionalities, it's essential to consider both access to the file upload feature of the web application and access to the actual uploaded files.
* Generally, the file upload feature of the application might be open to the public or restricted to users, whereas file access could be public, restricted to certain users, or entirely disallowed.
* Authentication, authorization and access control are the terms involved in this process:
  * Authentication is the process of verifying the identity of a user or system.
  * Authorization is the process of specifying which actions or resources are allowed to a user or system.
  * Access control refers to the mechanisms that enforce both authentication and authorization, determining who can access which resources and under what circumstances.
* Putting these concepts in place help prevent unauthorized file uploads, data breaches, and access to sensitive information.

## Non-compliant code in Java Jakarta

* The code snippet below lacks access control mechanisms, exposing the web application to broken access control and potential information disclosure, as it allows anyone to upload or download files:

  <details>
    <summary>Dependencies</summary>

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
    <summary>Contextual code</summary>

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
    <summary>Contextual code</summary>

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

## Compliant code in Java Jakarta using a middleware

* The following code snippet uses a middleware to restrict file upload and file access to authenticated users exclusively:

  <details>
    <summary>Dependencies</summary>

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

  * Notice how the middleware ensures that only authenticated users (those with an active session containing a `User` object) can access the `/upload` and `/download/*` routes, otherwise returning a `401 Unauthorized` status.

## Exercise to practice :writing_hand:

* The following application, despite appearances, lacks access control mechanisms, as there are no server-side measures to prevent anonymous users from uploading or downloading files.
* As can be demonstrated by opening the code editor via the `Open Code Editor` button and launching the integrated terminal, anyone can run the following commands to upload and download a file, considering the `APP_URL` as an environment variable pointing to the web application's base path:

  ```bash
  curl -F "formFile=@landscape.png" $APP_URL/upload
  ```

  ```bash
  curl $APP_URL/download/landscape.png -o landscape.png
  ```

* Additionally, any user registered to the application can freely use the upload and download features without restrictions once logged in, such as:
  * Username: `jackson01`, password: `3YD8v=Smlv=!CAMe`, role: `admin`.
  * Username: `johndoe`, password: `pJI+zM2k-qZdOzwz`, role: `moderator`.
  * Username: `alice99`, password: `W-KTJ_!3r*8HwRE^`, role: `member`.
* The goal here is to edit the source code to enforce a server-side access control policy, limiting **file uploads to authenticated users** (those with an active session) and allowing only **users with the `admin` or `moderator` role to download files**. Successful requests should return a `200 OK` status, while unauthorized attempts should result in a `401 Unauthorized` status.
  * More precisely, the modifications should be made in the `AuthFilter.java` and `AuthPrivFilter.java` files, located in `/home/coder/app/src/main/java/io/ontablab/`.
* After making the changes, press the `Verify Completion` button to confirm that the exercise has been completed.

  @@ExerciseBox@@
