# Vulnerable code to Path Traversal in Java Jakarta 10.0

* The provided code snippet reveals a significant security flaw in handling user input, making it susceptible to Path Traversal attacks:

  ```java
    // Get parameters
    String filename = request.getParameter("filename");
    if (filename == null || filename.isEmpty()){
        return;
    }
    String path = "/var/www/files/" + filename;

    // Reading file using user input
    FileInputStream fileInputStream = new FileInputStream(path);
    BufferedInputStream bufferedInputStream = new BufferedInputStream(fileInputStream);
    BufferedOutputStream out = new BufferedOutputStream(response.getOutputStream());

    byte[] buffer = new byte[1024];
    int length;
    while ((length = bufferedInputStream.read(buffer)) > 0) {
        out.write(buffer, 0, length);
    }

    bufferedInputStream.close();
    out.close();
    ```

* This vulnerability arises because the application directly concatenates user-provided file names with a base directory path without validating or sanitizing the input. As a result, attackers can manipulate the path to access unauthorized files on the server.
* Here, the application constructs a file path by appending user-supplied input (`filename`) directly to a fixed directory path. Without proper validation, this operation opens the door to unauthorized file access.

    ```java
    String path = "/var/www/files/" + filename;
    ```
  
* This behavior causes a user who enters the string `../../../` to be taken to the root of the server.
* From here, you can target and include any operating system file as long as the application has read permissions, such as `/etc/passwd`, or try to find where the source code is stored.
