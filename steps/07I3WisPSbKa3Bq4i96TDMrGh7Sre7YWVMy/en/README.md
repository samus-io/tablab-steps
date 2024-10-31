# How to prevent Path Traversal in Java Jakarta 10.0

## Normalization of user input

* This code fragment implements the normalization of the requested file name using the canonical form NFC (Normalization Composition):

    ```java
    String filename = request.getParameter("filename");
    Normalizer.normalize(filename, Normalizer.Form.NFC);
    ```

* This practice is essential to standardize different representations of Unicode characters that may be visually identical but digitally different.
* Standardization prevents evasion techniques that exploit these variations to circumvent security controls, thus ensuring that all characters are evaluated consistently.
  * This measure should be applied immediately upon receipt of the filename as part of the request, prior to any further validation or processing.

## Implementing a list of allowed files (whitelist)

* By adding the following code, it is possible to allow only predefined files to be consulted in the code:

    ```java
    final Set<String> ALLOWED_FILES = Set.of("info", "policy", "cookies");
    
    String filename = request.getParameter("filename");
    if (!ALLOWED_FILES.contains(filename)){
        // Reject request
    }
    ```

* In this case, the code uses a list of predefined files, but these could be obtained from a database or other information sources.
  * If the allowed files are obtained from a database, for example, it must be ensured that the user cannot arbitrarily change the contents of the list.

## Validating alphanumeric characters

* By using the following regular expression, it is guaranteed that the file name is exclusively alphanumeric and allows at most one dot:

    ```java
    String filename = request.getParameter("filename");
    if (!filename.matches("^[a-zA-Z0-9]+(\\.[a-zA-Z0-9]+)?$")){
        // Reject request
    }
    ```

* This code prevents the inclusion of special characters such as `/`, `/`, `...`, and others that could be exploited in a Path Traversal attack.
* If the extension is controlled by the application and not by the user, the regular expression should be the following:

    ```java
    String filename = request.getParameter("filename");
    if (!filename.matches("^[a-zA-Z0-9]+$")){
        // Reject request
    }
    ```

## Restriction on file extension control

* Limiting the file extensions that can be requested to a predefined set of safe types (in this case, `png`, `jpg`, `jpeg`) reduces the risk of serving malicious or sensitive files that should not be accessible. To get this behavior in Java, one of the possible solutions could be:

    ```java
    public static String getFileExtension(String filename) {
        if (filename == null || !filename.contains(".")) {
            return "";
        }
        return filename.substring(filename.lastIndexOf(".") + 1);
    }
    ...

    String filename = request.getParameter("filename");
    final Set<String> ALLOWED_EXTENSIONS = Set.of("png", "jpg", "jpeg");
    
    if (!ALLOWED_EXTENSIONS.contains(getFileExtension(filename))){
        return;
    }
    ```

## Path validation and normalization

* The following code is the last check to be performed, it converts the path of the requested file to its canonical form, verifies that it starts with the specified base directory, and confirms its existence:

    ```java
    final String BASE_DIRECTORY = "/var/www/files";
    String filename = request.getParameter("filename");
    File file = new File(BASE_DIRECTORY, filename);
    if (!file.getCanonicalPath().startsWith(BASE_DIRECTORY) || !file.exists()){
        return;
    }
    ```

* Checking that the canonical path of the requested file starts with the expected base directory (`/var/www/files`) prevents access to files outside that directory.
* Using `getCanonicalPath()` resolves any symbols such as `..`, ensuring that the final path is absolute and not relative, thus preventing exploitation of parent directory references.

## Use cases

* These two examples cover the different cases of setting the different security features on an endpoint when reading files from the server.
* In these examples, if a user attempts to access a file that does not meet the established security criteria, the method will terminate prematurely, returning an empty response.
* This error handling approach of terminating execution and returning a blank page may not be the most appropriate in all contexts. The optimal way to handle such situations varies greatly depending on the particular specifications and needs of each application. In another `Lab` we will explain how to handle such exceptions correctly.
* For the sake of simplicity in this example, the most direct and simple error handling strategy has been chosen.

### Access to predefined files with a single extension

```java
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.*;
import java.text.Normalizer;
import java.util.Set;

@WebServlet("/getFile")
public class FileServlet extends HttpServlet {
    private static final Set<String> ALLOWED_FILES = Set.of("info", "policy", "cookies");
    private static final String BASE_DIRECTORY = "/var/www/files";

    private static String normalizeString(String s) {
        return Normalizer.normalize(s, Normalizer.Form.NFC);
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String filename = request.getParameter("filename");
        if (filename == null || filename.isEmpty()) {
            return;
        }
        // Normalize input
        filename = normalizeString(filename);

        // Files whitelist
        if (!ALLOWED_FILES.contains(filename)){
            return;
        }
        
        // Set the txt extension
        filename = filename.concat(".txt");

        // Get file
        File file = new File(BASE_DIRECTORY, filename);
        if (!file.getCanonicalPath().startsWith(BASE_DIRECTORY) || !file.exists()){
            return;
        }

        // Process file
        FileInputStream fileInputStream = new FileInputStream(file);
        BufferedInputStream bufferedInputStream = new BufferedInputStream(fileInputStream);
        BufferedOutputStream out = new BufferedOutputStream(response.getOutputStream());

        byte[] buffer = new byte[1024];
        int length;
        while ((length = bufferedInputStream.read(buffer)) > 0) {
            out.write(buffer, 0, length);
        }

        bufferedInputStream.close();
        out.close();
    }
}
```

### Access to alphanumeric files with multiple extensions

```java
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.*;
import java.text.Normalizer;
import java.util.Set;

@WebServlet("/getFile")
public class FileServlet extends HttpServlet {
    private static final Set<String> ALLOWED_EXTENSIONS = Set.of("png", "jpg", "jpeg");
    private static final String BASE_DIRECTORY = "/var/www/files";

    private static String normalizeString(String s) {
        return Normalizer.normalize(s, Normalizer.Form.NFC);
    }

    public static String getFileExtension(String filename) {
        if (filename == null || !filename.contains(".")) {
            return "";
        }
        return filename.substring(filename.lastIndexOf(".") + 1);
    }

    public static boolean isFileAlphanumeric(String input) {
        // Allows files with alfanumeric characters, including one dot
        return input.matches("^[a-zA-Z0-9]+(\\.[a-zA-Z0-9]+)?$");
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String filename = request.getParameter("filename");
        if (filename == null || filename.isEmpty()) {
            return;
        }
        // Normalize input
        filename = normalizeString(filename);

        // Alfanumeric characters
        if (!isFileAlphanumeric(filename)){
            return;
        }

        // Extensions whitelist
        if (!ALLOWED_EXTENSIONS.contains(getFileExtension(filename))){
            return;
        }

        // Get file
        File file = new File(BASE_DIRECTORY, filename);
        if (!file.getCanonicalPath().startsWith(BASE_DIRECTORY) || !file.exists()){
            return;
        }

        // Process file
        FileInputStream fileInputStream = new FileInputStream(file);
        BufferedInputStream bufferedInputStream = new BufferedInputStream(fileInputStream);
        BufferedOutputStream out = new BufferedOutputStream(response.getOutputStream());

        byte[] buffer = new byte[1024];
        int length;
        while ((length = bufferedInputStream.read(buffer)) > 0) {
            out.write(buffer, 0, length);
        }

        bufferedInputStream.close();
        out.close();
    }
}
```
