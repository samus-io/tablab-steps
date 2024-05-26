# Insecure File Upload in NodeJS 20

## What is Insecure File Upload?

* Insecure File Upload is a security vulneribility that occurs whenever the server accepts the uploaded file without validating it or keeping a control over it.
* This allows attacker to upload malicious or unauthorized code via the file into the server.

## What are the factors in file upload that can serve as attack vectors?

* Every field received from the client can be exploited by attackers if not properly handled.
* Fields from client which can cause the vulneribility are listed below.

### Filename

* Attackers can manipulate the filename to include directory traversal sequences (e.g., `../../`) to access sensitive files on the server.
* If filenames are used in system commands without proper sanitization, attackers can inject additional commands.
* An attacker can upload a file with a name that overwrites an existing critical file.
* Using filenames directly in file paths without validation can lead to path injection attacks.

### File Content

* Uploaded files can contain malicious scripts or code that, when executed, can compromise the server or clients. The below are the different problems due to file content:
  * **Embedded Scripts:** Files such as PDFs or office documents can contain embedded scripts or macros that execute malicious actions when opened by a user.
  * **Binary Exploits:** Binary files (e.g., executables, DLLs) can exploit vulnerabilities in file processing software, potentially leading to remote code execution.
  * **Obfuscated Payloads:** Malicious content can be hidden within seemingly benign files through obfuscation techniques, making it harder to detect during scanning.
  * **Phishing Content:** uploaded files could be designed to look like legitimate documents but actually contain phishing content to deceive users into disclosing sensitive information.

### File Size

* Large files can exhaust server resources such as memory and storage, leading to service outages.
* Attackers can upload excessively large files repeatedly, causing the server to crash or slow down.
* The below are the problems due to improper file size:
  * **Resource Exhaustion:** very large files can deplete server resources such as RAM and CPU, impacting overall server performance and availability.
  * **Network Bandwidth:** large file uploads can consume significant bandwidth, affecting the performance of the network and other users.
  * **Storage Management:** managing storage space becomes challenging with large or numerous uploads, requiring careful monitoring and maintenance.
  * **Backup and Recovery:** larger files can complicate backup processes and increase recovery times during disaster recovery scenarios.

### File Type

* Certain file types, especially executables or scripts, can be used to exploit server vulnerabilities.
* The below are the problems caused, if it is exploited:
  * **Executable Files:** allowing uploads of executable files (.exe, .sh) can lead to direct execution of malicious code on the server or client systems.
  * **Scripts:** Files like .js, .php, .py can be interpreted by the server if mishandled, leading to code execution.
  * **Archives:** Compressed files (.zip, .rar) might contain multiple malicious files or exploits targeting decompression tools.
  * **Media Files:** maliciously crafted media files (e.g., images, videos) can exploit vulnerabilities in media processing libraries.

### File Path

* Storing files in publicly accessible directories can lead to unauthorized access or data leakage.
* Impacts due to file path manipulation:
  * **Path Injection:** User-controlled file paths can be manipulated to traverse directories and access restricted areas of the file system.
  * **Relative Paths:** misuse of relative paths can lead to unpredictable file access behavior, potentially exposing sensitive files.
  * **Symbolic Links:** Attackers might upload files that create symbolic links to sensitive files or directories, enabling unauthorized access.

### Metadata

* Metadata within files cause the vulneribility is various ways, like:
  * **Privacy Violations:** Metadata in files can inadvertently reveal personal information such as user names, email addresses, and device details.
  * **Data Leakage:** Metadata can include details about the internal structure of the system or network, which can be useful for attackers.
  * **Geolocation Data:** Files like images and videos can contain geolocation data, potentially exposing the physical location of the user or organization.
  * **Document History:** Document files can retain a history of changes and comments, potentially leaking sensitive or proprietary information.

## What is the impact of an insecure file upload?

* Insecure file upload can have severe consequences for the security and integrity of a system:
  * Attackers can upload files containing malware, which can then be executed on the server or client systems, leading to data theft, unauthorized access, and system compromise.
  If an uploaded file is executed or interpreted by the server, it can allow attackers to run arbitrary code on the server, leading to full control over the server.
  * Malicious files can cause the server to make unintended requests to internal or external systems, potentially exposing internal networks and services.
  * Uploaded files containing malicious scripts can be served to users, leading to XSS attacks that steal cookies, session tokens, or redirect users to malicious sites.
  * Large or numerous file uploads can consume excessive server resources, leading to service degradation or complete denial of service.
  * Sensitive information can be included in uploaded files and then exfiltrated by the attacker.
  * Uploaded files can exploit server vulnerabilities to escalate privileges, allowing attackers to gain higher-level access than intended.
  * Unauthorized file uploads can lead to unauthorized access to restricted areas of the application.
  * Improper handling of uploaded files can reveal sensitive information unintentionally.
  * Uploaded files can be used to modify website content, leading to defacement and reputational damage.

## What vulnerabilities can arise from insecure file upload?

### Cross-Site Scripting (XSS)

* **Script Injection:** uploaded files can contain embedded scripts that execute in the context of the user's browser. This is particularly dangerous for files like HTML, SVG, or even images with embedded scripts.
* **Stored XSS:** Malicious scripts in uploaded files can be stored on the server and served to other users, leading to persistent XSS attacks that affect multiple users over time.
* For example, an attacker uploads a profile picture that is actually an SVG file containing malicious JavaScript. When another user views the attacker’s profile, the script executes, stealing their session cookie and sending it to the attacker’s server.

### SQL Injection (SQLi)

* **Filename Manipulation:** if the filename or file metadata is used in SQL queries without proper sanitization, it can introduce SQL injection vulnerabilities.
* **Metadata Exploitation:** File metadata such as EXIF data in images can contain strings that are interpreted as part of SQL queries, leading to injection attacks.
* For example, an application stores filenames in a database. An attacker uploads a file with the name `'); DROP TABLE users;--.jpg`. If the application constructs SQL queries unsafely, this filename can terminate the existing query and execute the malicious command, dropping the users table.

### Cross-Site Request Forgery (CSRF)

* **Unauthorized Uploads:** CSRF can be exploited to trick authenticated users into uploading files without their consent, potentially leading to the server storing unwanted or malicious files.
* **File Processing:** if the upload endpoint lacks proper CSRF protection, an attacker can make a user upload a file that performs harmful actions when processed by the server.
* For eaxmple, an attacker creates a hidden form on their website that, when visited by an authenticated user of another site, triggers a file upload to that site. This form uploads a file with malicious content, exploiting the lack of CSRF protection on the upload endpoint.

### Denial of Service (DoS)

* **Resource Exhaustion:** Attackers can upload very large files or numerous files in a short period, exhausting server resources such as CPU, memory, and disk space, leading to service unavailability.
* **File Processing:** maliciously crafted files can exploit vulnerabilities in file processing libraries, causing the server to crash or become unresponsive during processing.
* For example, an attacker scripts the upload of large files repeatedly to a server, quickly filling up disk space and causing the server to run out of resources, resulting in a denial of service for legitimate users.

### Path Traversal

* **Directory Traversal:** by manipulating the filename to include sequences like `../`, attackers can traverse directories and access files outside the intended upload directory.
* **File Overwriting:** Malicious filenames can be crafted to overwrite critical files on the server, leading to data loss or system compromise.
* For example, an attacker uploads a file with the name `../../../../etc/passwd`. If the application concatenates this filename with the upload directory path without proper validation, it might overwrite or disclose the contents of the `/etc/passwd` file, exposing sensitive system information.

## How can Local File Inclusion(LFI) and Publicly Accessible Uploaded Files Lead to Code Execution Vulnerabilities?

If a web application is vulnerable to Local File Inclusion (LFI) and allows users to upload files to a public directory, an attacker can exploit this to execute malicious code. Here's how this can happen:

* **LFI Vulnerability**: occurs when a web application includes files based on user input without proper validation or sanitization, allowing attackers to manipulate the file path. Attackers can include and execute files from the server's filesystem, potentially accessing sensitive files or executing arbitrary code.

* **Public Directory for Uploads**: uploaded files are stored in a publicly accessible directory, making them accessible via a direct URL. If these files are not properly validated and sanitized, malicious files can be uploaded and later included via LFI.

* **Malicious File Upload**: an attacker uploads a file with a malicious payload, ensuring it has an extension that the server processes (e.g., `.pdf`, `.php`). By manipulating the LFI vulnerability, the attacker can include the path to the uploaded malicious file, causing it to be executed by the server.

### Example

1. **Upload Malicious File**: the attacker uploads a file named `malicious.pdf` containing embedded  code to the public upload directory.

2. **Trigger LFI**: the attacker exploits the LFI vulnerability by navigating to a URL like `http://example.org/index?page=uploads/malicious.pdf`.

3. **Execute Malicious Code**: the server includes and executes the `malicious.pdf` file, processing the embedded code. The attacker can then execute arbitrary commands by passing parameters (e.g., `http://example.org/index?page=uploads/malicious.pdf&cmd=ls`).
