# Insecure file upload overview

* `Insecure file upload` refers to a web security vulnerability that occurs when an application allows users to upload files without correctly verifying the file's properties like the file's name, type, content, or size, posing a potential risk to the system.
* When these checks are not properly enforced, a simple file upload feature could be exploited to upload dangerous files, including server-side scripts that can allow attackers to execute malicious code on the server or even on the desktops of users or employees when they access these files.

![Insecure file upload overview][1]

## What could be achieved with an insecure file upload

* Malicious users can upload malware that may execute on the server or user devices, resulting in data theft, unauthorized access, or full system compromise.
* Uploaded files executed or interpreted by the server can enable arbitrary code execution, giving attackers control over the server.
* Uploaded files with malicious scripts can be served to users, leading to XSS attacks.
* Failing to sanitize file names correctly can expose the system to SQL or command injection vulnerabilities.
* Large or excessive file uploads can overwhelm server resources, causing service degradation or denial of service.
* Sensitive information embedded in uploaded files can be exfiltrated by attackers.
* Uploaded files can be used to alter website content, leading to defacement and reputational damage.

### Remote code execution

* Improperly validated uploaded files can be executed by the server, allowing attackers to run arbitrary code and potentially gain full control over the system.
* Another method of achieving code execution is through a `Local File Inclusion (LFI)` vulnerability. If the web application permits users to upload files to a public directory, an attacker can upload a seemingly harmless file (such as an image) containing embedded code. The attacker can then exploit the LFI to execute the code within the uploaded file.
  > :older_man: `Local File Inclusion (LFI)` is a web vulnerability that occurs when a web application allows users to load files from the server's filesystem. When such a file is included on a webpage, its contents are not only read but also interpreted as code.
  * For example, the steps might be:
    1. The attacker uploads a file named `image.png` with embedded code to the public upload directory (e.g., `/uploads`).
    1. Then the attacker exploits the LFI vulnerability by navigating to a URL like `https://example.tbl/index?page=uploads/image.png`.
    1. The server includes and executes the `image.png` file, processing the embedded code.

### Cross-Site Scripting (XSS)

* Uploaded files may contain JavaScript code that execute in the user's browser context. This is particularly dangerous with file types like HTML, SVG, or in some cases images that can have HTML embedded.
* Files containing embedded malicious scripts that execute JavaScript code in users' browsers can steal user sessions, access any data the user can access, perform keylogging, deface the website virtually, redirect users to malicious websites, or even take control of the browser or install malware by exploiting web browser vulnerabilities.

### SQL injection (SQLi)

* If the file name is used in SQL queries without proper sanitization, it can introduce SQL injection vulnerabilities.
* For example, an application stores file names in a database, an attacker can upload a file with the name `'); DROP TABLE users;--.jpg`. If the application constructs SQL queries unsafely, this file name can terminate the existing query and execute the malicious command, dropping the users table.

### Denial of Service (DoS)

* Attackers might upload excessively large or numerous files within a short time frame, depleting server resources such as CPU, memory, and disk space, which can result in service unavailability.

### Path traversal

* Manipulated file names to include sequences like `../` such as `../index.html` can allow malicious users to access files outside the intended upload directory or overwrite other files.
* Some file names can be crafted to overwrite critical files on the server, leading to data loss or system compromise.

## Components involved in file uploads that can be used as attack vectors

### File name

* Attackers can manipulate the file name to include path traversal sequences (e.g., `../../`) to access sensitive files on the server.
* Path traversal can be used to save the file on a different path than expected.
  * An attacker could upload a file with a carefully crafted name that matches the name of a critical file on the server, thereby overwriting it.
* When file names are used in system commands without adequate sanitization, it may allow attackers to inject additional commands.

### File extension

* Allowing uploads of **executable files** (e.g., `.exe`, `.elf`) can lead to direct execution of malware on the server or client systems.
* **Source code files** (e.g., `.js`, `.php`, `.py`) can be interpreted by the server when uploaded to the server, leading to code execution.
* **Compressed files** (e.g., `.zip`, `.rar`, `.tar`) might contain multiple malicious files or exploits targeting decompression tools.

### File content

* Files like PDFs or office documents may contain **embedded scripts** or macros that perform malicious actions when opened by a user, such as downloading malware or stealing data.
* **Binary files** (e.g., executables, DLLs) can exploit vulnerabilities in file processing software, potentially leading to remote code execution.
* Some files may contain **obfuscated payloads** within seemingly harmless documents through obfuscation techniques, making it harder to detect during scanning.
* Uploaded files can be used for **phishing**, disguised as legitimate documents but designed to trick users into revealing sensitive information, such as login credentials, through deceptive content.
* **Media files** (e.g., images, videos) can be crafted to exploit vulnerabilities in media processing libraries, allowing attackers to execute code or cause Denial of Service (DoS) when these files are viewed or processed.

### File size

* Large files can lead to **resource exhaustion**, such as RAM and CPU, degrading performance and availability, which attackers can exploit by repeatedly uploading oversized files.
* Large uploads can use up significant **bandwidth**, affecting network performance for other users.
* Handling large or numerous uploads complicates **storage management**, requiring diligent monitoring and maintenance.
* Large files can also make **backups** more complex and increase recovery times in disaster recovery situations.

## Security considerations

### Authentication on file upload

* When handling file uploads, whenever possible, ensure they are protected with robust authentication and authorization mechanisms.
* It is essential to validate users before granting access to a file upload service, ensuring that the service is accessible only to authenticated users to manage uploads, and, if necessary, implementing proper controls to restrict file access to authorized users.
* An attacker can abuse the lack of authentication to exploit different vulnerabilities, like DoS or information disclosure, or increase the risk of an existing vulnerability.

### File storage location and filesystem permissions

* Proper management of uploaded file storage can significantly reduce the risk of information disclosure and the exploitation of vulnerabilities in a web application.
* To enhance security, consider the following best practices when deciding where and how to store files uploaded by users:
  * Whenever possible, store uploaded files on a server separate from the main web application. This reduces the risk of an attacker gaining access to sensitive data or exploiting other vulnerabilities in the application server.
  * If storing files on a separate server is not feasible, ensure that uploaded files are stored outside of the webroot directory. This prevents direct access to the files via the web server.
  * If the application needs to display uploaded files to users, avoid allowing direct access to these files via the web server. Instead, implement a server-side handler that serves the files. This handler can map files internally to a unique ID, which is then used to access the file. This approach provides an additional layer of security by preventing attackers from directly accessing the file paths.
  
### Upload and download limits

* Setting upload and download limits helps prevent the server from being overwhelmed by excessive data transfers, ensuring stable service performance.
* Attackers or malicious users could exploit unrestricted uploads or downloads to flood the server with data, leading to slowdowns or crashes.
* Another type of vulnerability that can occur without proper limits is a race condition, which could exploit timing-based weaknesses or vulnerabilities that exist within a specific time frame.

### Metadata deletion

* Metadata can unintentionally **disclose personal information** like usernames, email addresses, or device details.
* Images and videos can have embedded **geolocation data**, potentially revealing the user's or organization's physical location.

[1]: /static/images/insecure-file-upload-overview.png
