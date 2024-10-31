# Leveraging FortiWeb Cloud 24.3 to scan uploaded files

* FortiWeb Cloud is a `Web Application Firewall (WAF)` designed to protect web applications from a wide range of threats, including those introduced through file uploads. As file uploads can serve as vectors for malicious activity, FortiWeb provides comprehensive scanning mechanisms to detect and mitigate potential risks.
* When properly configured, FortiWeb Cloud can scan uploaded files for various types of malware, malicious scripts, and other harmful content. This includes detecting viruses, Trojans, and potentially dangerous scripts written in server-side languages like PHP or ASP, which are often exploited to execute server-side attacks.

## Scanning mechanisms in FortiWeb Cloud

* FortiWeb Cloud employs a multi-layered scanning approach, combining both signature-based detection and behavioral analysis to ensure comprehensive protection.

### Static/Signature detection

* Signature-based detection works by comparing the characteristics of the uploaded file with a database of known malware signatures, Trojans, and other malware. FortiWeb leverages up-to-date virus definitions and threat intelligence to ensure accurate detection.
* In addition to common malware types, it identifies files that contain scripts in languages such as PHP, ASP, and JavaScript, which can potentially be exploited by attackers to gain unauthorized access or control over web servers.
* This signature-based detection provides an essential first line of defense against well-known threats.

### Behavioral analysis in FortiSandbox

* Beyond static file analysis, FortiWeb integrates with FortiSandbox to provide dynamic, behavioral analysis. Files are executed within an isolated, controlled environment (sandbox) to monitor their behavior in real-time.
* This method is crucial for detecting advanced threats such as zero-day malware or sophisticated attacks that may not be detected through traditional signature-based methods. By simulating file execution in a real-world environment, FortiSandbox can uncover hidden malicious behavior, including attempts to access unauthorized resources or execute harmful commands.

## Properly submitting files for scanning

* To ensure files are scanned accurately and thoroughly by FortiWeb, they must be submitted in supported formats. The following are the recommended methods for submitting files.

### File upload via `multipart/form-data`

* The most common method for file uploads is using the `multipart/form-data` format because it efficiently handles binary data. FortiWeb processes and scans the uploaded file directly from this format without requiring any additional steps from developers.
* Below is an example of an HTTP request where the file is sent in a multipart form:

  ```text
  POST /upload HTTP/2
  Host: domain.tbl
  User-Agent: Mozilla/5.0 (compatible; MSIE 11.0; Windows; Windows NT 6.2; Win64; x64; en-US Trident/7.0)
  Accept-Encoding: gzip, deflate, br, zstd
  Content-Type: multipart/form-data; boundary=---------------------------41762806061171117218568726803
  Content-Length: 656499
  Connection: keep-alive
  
  -----------------------------41762806061171117218568726803
  Content-Disposition: form-data; name="file"; filename="landscape.png"
  Content-Type: image/png
  
  <binary>
  
  -----------------------------41762806061171117218568726803--
  ```

### File upload via `application/x-www-form-urlencoded` and base64

* Files can be uploaded using Base64 encoding, which is often necessary when binary files need to be transmitted over text-based protocols. In these cases, FortiWeb automatically decodes the base64-encoded file and conducts a comprehensive scan to ensure no security threats are present.
* This is particularly useful for web applications that need to transmit binary data through non-binary channels while maintaining security.
* Below is an example of an HTTP request where the file is sent in Base64 with a simple POST:

  ```text
  POST /upload HTTP/2
  Host: domain.tbl
  User-Agent: Mozilla/5.0 (compatible; MSIE 11.0; Windows; Windows NT 6.2; Win64; x64; en-US Trident/7.0)
  Accept-Encoding: gzip, deflate, br, zstd
  Content-Type: application/x-www-form-urlencoded
  Content-Length: 933513
  Connection: keep-alive
  
  file=<base64-file>
  ```

### File upload via `application/json` and base64

* Files can also be uploaded using JSON, with a few specific limitations. When using JSON to upload files, both the file and the filename must be included in the root of the JSON object.

  > :warning: FortiWeb's support for JSON file uploads is limited to a single file per request, which may require developers to handle multiple files by batching requests.

* Below is an example of an HTTP request where the file is sent in Base64 with JSON:

  ```text
  POST /upload HTTP/2
  Host: domain.tbl
  User-Agent: Mozilla/5.0 (compatible; MSIE 11.0; Windows; Windows NT 6.2; Win64; x64; en-US Trident/7.0)
  Accept-Encoding: gzip, deflate, br, zstd
  Content-Type: application/json
  Content-Length: 875047
  Connection: keep-alive
  
  {
    "filename": "<filename>",
    "file": "<base64-file>"
  }
  ```

## Testing file upload implementation

* To find out if the implementation has been done in such a way that FortiWeb detects malware, an EICAR file can be used.

### What is an EICAR?

* The EICAR Anti-Virus Test File or EICAR test file is a computer file that was developed by the European Institute for Computer Antivirus Research (EICAR).
* Its purpose is to test the response of computer antivirus programs. Instead of using real malware, which could cause real damage, this test file allows to test anti-virus software without having to use a real computer virus.
* The content of the EICAR file its only a sequence of ASCII characters that Anti-Virus will always detect. The simplest EICAR file content is the following:

  ```
  X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
  ```

* The EICAR file can be created adding the above characters in a file using a text editor or it can be downloaded in the official [EICAR][1] website.

### Testing FortiWeb scanning

* When the file upload implementation is done, its possible to test if FortiWeb will detect correctly malware uploading the EICAR file.
* Once uploaded, if the file upload is implemented using some above methods, the server will not receive the file and FortiWeb will return the following 403 HTTP response:

![FortiWeb block page][2]

[1]: https://www.eicar.org/download-anti-malware-testfile/#:~:text=enabled%20protocol%20HTTPS-,EICAR.COM,-DOWNLOAD
[2]:
