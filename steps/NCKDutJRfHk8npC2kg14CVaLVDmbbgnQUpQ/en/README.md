# File name sanitization

* File name sanitization is a crucial process aimed at ensuring that file names are safe and compatible with the system on which they will be used.
* This involves validating and potentially modifying the original names of the files received to prevent security threats or operational failures that could compromise system integrity.

![File name sanitization][2]

## Security measures checklist

* Whenever possible, use unique and random file names when storing the files (e.g., adopting UUID). If business logic constraints prevent this approach, then:

  * [ ] Set a file name length limit.
  * [ ] Restrict the allowed characters (e.g., only consider `A-Z`, `a-z`, `0-9`, `-`, and `.` as valid characters).
  * [ ] Handle file names as case-insensitive.
  * [ ] Restrict reserved names in Windows and Linux.
  * [ ] Avoid hidden files and trailing periods and spaces (e.g., `.htaccess`).

## Generating unique and random file names

* Creating unique and random file names when storing uploaded files prevents filename collisions, mitigates path traversal attacks, conceals original filenames that might expose sensitive details, enhances security against malicious file execution reduing the risk of an attacker being able to locate and execute such files, and prevents file enumeration attacks.
* A reliable way for creating unpredictable and non-overwritable file names is by utilizing `Universally Unique Identifier (UUID)` or `Globally Unique Identifier (GUID)`.
* This approach is particularly useful in scenarios where the original file names provided by users do not need to be retained.

## File name length limits

* Different file systems impose varying limits on file name lengths, which can affect compatibility and security. For instance, the `MS-DOS FAT` file system enforces the `8.3` file name format, allowing only 8 characters for the name and 3 for the extension to maintain compatibility with legacy software.
* Modern file systems like `NTFS` can support longer file names, yet Windows has traditionally imposed a `MAX_PATH` limit of 260 characters. Exceeding this limit may cause truncation or file access errors, but newer Windows versions allow this limit to be removed through proper configuration settings.
* Accounting for file name length limits is essential to avoid issues such as file access errors, truncation, or security risks due to file system misinterpretation.

## Applying input validation to the file name

* When user-defined file names are allowed, comprehensive input validation is crucial to prevent security vulnerabilities such as path traversal or injection attacks, as well as to avoid operational errors.
* Path traversal refers to the process of manipulating file paths to access unintended locations outside the designated directory. Malicious users include sequences like `../` in file names to traverse directories and store files in unintended locations. For instance, a file name such as `../../../../var/www/html/index.php` would place the file in the web root, potentially replacing the actual main file content of a web PHP application.
* File names can also be used to exploit vulnerabilities related to how the application processes and handles the file name. For example, a file name like `sleep(20)-- -.jpg` could trigger a SQL injection, `<svg onload=alert("XSS")>` might lead to XSS, and `; sleep 20;` might result in command injection.
* Allowing only a secure set of characters, such as alphanumeric characters, hyphens, and dots is the most effective security practice for preventing path traversal and injection attacks.

## Addressing case-sensitive

* To prevent conflicts like unintended file overwriting or access issues, always treat file names as case-insensitive. Using consistent naming conventions and applying case-insensitive validation can help mitigate risks.
* Omitting this behavior may lead to file overwriting or unauthorized access, especially in environments that rely on case-sensitive file handling.
* Windows file systems treat file names as case-insensitive by default, meaning that `Image.png`, `IMAGE.PNG`, and `image.png` are considered identical.

## System-specific character limitations for file naming

* Different file systems enforce specific restrictions on certain characters in file names to preserve system integrity and avoid file path parsing errors.
* Attempting to save a file using reserved names or restricted characters can trigger unexpected errors and cause service disruption.

### Restricted characters and reserved names in Windows

* In Windows, the special characters `<`, `>`, `:`, `"`, `/`, `\`, `|`, `?`, `*`, `\x00` are not allowed in file names.
* Additionally, certain names such as `AUX`, `COM1`, `COM2`, `COM3`, `COM4`, `COM5`, `COM6`, `COM7`, `COM8`, `COM9`, `CON`, `LPT1`, `LPT2`, `LPT3`, `LPT4`, `LPT5`, `LPT6`, `LPT7`, `LPT8`, `LPT9`, `NUL`, and `PRN` are reserved by the system for devices or system resources and cannot be used as file or directory names.
* Furthermore, the [ASCII control characters][1] ranging from 0 to 31 are also not permitted in file names.

### Restricted characters and reserved names in Linux

* In Linux, the characters restricted in file names are `/`, used as a directory separator, and the null character `\x00`, also known as the null terminator, which is used in many systems, including Linux, as a string terminator.
* UNIX-like systems reserved names are `.` and `..`.

## Avoid hidden files and files ending with a period or a space

* Starting a file name with a period (e.g., `.htaccess`) is widely accepted and commonly used to create hidden files, particularly in UNIX-like systems, where the period signals that the file should be hidden from standard directory listings, and even overlooked by automated security scans. Attackers could leverage these files to bypass security checks, hide malicious scripts, or modify server configurations.
* Files ending with a period or space can take advantage of inconsistencies in how different operating systems and file systems handle filenames, leading to file access errors, compatibility issues in Windows Explorer, or problems with other applications, even if the underlying file system supports them.

@@TagStart@@java

## Non-compliant code in Java Jakarta

* The code snippet below demonstrates an insecure file upload implementation in a Java Jakarta application, where the original file name received from the user is used without any validation, leading to risks such as file overwriting and file enumeration, among others:

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

## Non-compliant code in Node.js using `multer`

* The code snippet below demonstrates an insecure file upload implementation in an `Express.js` application using `multer`, where the original file name received from the user is used without any validation, leading to risks such as file overwriting and file enumeration, among others:

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

## Compliant code in Java Jakarta while generating a random file name

* The following code snippet illustrates how to handle file uploads in Java Jakarta and storing files in a specific folder with randomly generated names via UUID, ensuring the file names are both unique and unpredictable:

  ```java
  import java.util.UUID;
  ```

  ```java
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

  * In this scenario, the code is designed to consider only PDF file uploads to the application.

@@TagEnd@@

@@TagStart@@node.js

## Compliant code in Node.js using `multer` while generating a random file name

* The following code snippet illustrates how to handle file uploads using the `multer` middleware and storing files in a specific folder with randomly generated names via UUID, ensuring the file names are both unique and unpredictable:

  ```javascript
  const uuid = require("uuid");
  ```

  ```javascript
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

  * In this scenario, the code is designed to consider only PDF file uploads to the application.

@@TagEnd@@

@@TagStart@@java

## Compliant code in Java Jakarta while keeping the original file name

* The following code snippet demonstrates how to handle file uploads in Java Jakarta storing files in a specific folder while preserving the original file name sent by the user. It applies a custom file name length limit, restricts characters and reserved names, treats file names as case-insensitive, prevents hidden files or those ending with a period or space, and ensures no file name collisions:

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

  <details>
    <summary>Contextual code</summary>

    ```java
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
    ```

  </details>

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

## Compliant code in Node.js using `multer` while keeping the original file name

* The following code snippet demonstrates how to handle file uploads using the `multer` middleware and storing files in a specific folder while preserving the original file name sent by the user. It applies a custom file name length limit, restricts characters and reserved names using the `sanitize-filename` package, treats file names as case-insensitive, prevents hidden files or those ending with a period or space, and ensures no file name collisions:

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

  > :warning: As some of the security measures outlined may remove undesired characters, it is advisable to first apply file name sanitization and then verify the file extension.

@@TagEnd@@

[1]: https://www.ascii-code.com/
[2]: /static/images/file-name-sanitization.png
