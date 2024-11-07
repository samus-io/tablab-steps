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

* To ensure that file upload mechanisms are properly implemented and that FortiWeb Cloud effectively detects and blocks malware, an EICAR test file can be used for testing purposes. This check validation of FortiWeb’s scanning capabilities without exposing the system to real malware.

### What is an EICAR?

* The EICAR Anti-Virus Test File, or EICAR test file, is a non-malicious file developed by the European Institute for Computer Antivirus Research (EICAR) to safely test antivirus and security systems.
* Its purpose is designed to trigger antivirus and security system responses as a real malware file would, without the risk of causing actual harm.
* The content of the EICAR file is a simple ASCII text file with a specific sequence of characters that antivirus software will detect as if it were a malicious file. The simplest form of the EICAR file content is as follows:

  ```
  X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
  ```

* The EICAR file can be created by copying and pasting the above character sequence into a text editor and saving it with a .txt extension. Alternatively, it can be downloaded directly from the official [EICAR website][1].

### Testing FortiWeb scanning

* After implementing file upload handling, it’s crucial to test if FortiWeb correctly identifies and blocks potentially harmful files, such as the EICAR test file.
* Attempt to upload the EICAR file using the application’s file upload functionality. This file simulates malware, and its detection will validate that FortiWeb’s security layer is active and configured correctly.
* If FortiWeb is configured properly, it should intercept the EICAR file upload and prevent the server from receiving it. In such cases, FortiWeb will return an HTTP 403 (Forbidden) response, indicating that the file has been blocked due to potential security risks:

![FortiWeb block page][2]

[1]: https://www.eicar.org/download-anti-malware-testfile/#:~:text=enabled%20protocol%20HTTPS-,EICAR.COM,-DOWNLOAD
[2]: /static/images/fortiweb-eicar-alert.png
