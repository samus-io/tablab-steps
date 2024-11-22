# Leveraging FortiWeb Cloud 24.3 to scan files on upload

* FortiWeb Cloud is a `Web Application Firewall (WAF)` designed to protect web applications from a wide range of threats, including those associated with file uploads. File uploads can potentially serve as vectors for malicious activities, and FortiWeb Cloud provides comprehensive scanning mechanisms to detect and mitigate potential risks.
* When properly configured, FortiWeb Cloud can perform scans on files being uploaded to detect various types of malware, greyware, malicious scripts, and other harmful content. This includes detecting viruses, trojans, and potentially dangerous scripts written in server-side languages such as PHP or ASP, often used in executing server-side attacks.

## Scanning mechanisms in FortiWeb Cloud

* FortiWeb Cloud employs a multi-layered scanning approach, combining both signature-based detection and behavioral analysis to ensure comprehensive protection.

### Signature-based detection

* Signature-based detection, also known as static detection, involves comparing the characteristics of an uploaded file to a database containing signatures of known malware, including trojans and other threats. FortiWeb Cloud leverages up-to-date virus definitions and threat intelligence to ensure reliable detection.
* In addition to identifying common malware, it also identifies files containing scripts in languages like PHP, ASP, and JavaScript, which attackers could potentially use to gain unauthorized access or control over web servers.
* This signature-based detection forms an essential primary line of defense against recognized threats.

  > :warning: Due to caching limits, signature-based detection currently only processes files smaller than 5 MB.

### Behavioral analysis through FortiSandbox

* In addition to static file analysis, FortiWeb Cloud utilizes FortiSandbox to provide dynamic, behavioral analysis. Files are executed within an isolated, controlled environment to monitor their behavior in real-time.
* This method is crucial for detecting advanced threats such as zero-day malware or sophisticated attacks that may not be detected through traditional signature-based methods. By simulating the execution of files in a real environment, FortiSandbox can uncover hidden malicious behavior, such as attempts to access unauthorized resources or execute harmful commands.

  > :older_man: Sandbox file evaluation is performed in the same region where the FortiWeb Cloud cluster is located, ensuring compliance with various data regulations such as GDPR.

## How to submit files for scanning upon upload

* Files must be submitted in supported formats to be scanned by FortiWeb Cloud. The following are the methods available for file submission.

### File upload via `multipart/form-data`

* The `multipart/form-data` format is the most common and suggested approach for file uploads, as it efficiently handles binary data. FortiWeb Cloud can process and scan files directly from this format, requiring no additional steps.
* Below is an example of an HTTP request that sends a file in a `multipart` form:

  ```text
  POST /upload HTTP/2
  Host: domain.tbl
  User-Agent: Mozilla/5.0 (compatible; MSIE 11.0; Windows; Windows NT 6.2; Win64; x64; en-US Trident/7.0)
  Accept-Encoding: gzip, deflate, br, zstd
  Content-Type: multipart/form-data; boundary=---------------------------41762806061171117218568726803
  Content-Length: 656499
  Connection: keep-alive
  
  -----------------------------41762806061171117218568726803
  Content-Disposition: form-data; name="email"

  johndoe@domain.tbl
  -----------------------------41762806061171117218568726803
  Content-Disposition: form-data; name="file"; filename="landscape.png"
  Content-Type: image/png
  
  [binary file data]
  
  -----------------------------41762806061171117218568726803--
  ```

* The following JavaScript code employs the `axios` package to create an HTTP request similar to the one above:

  ```javascript
  const sendFile = (formFile) => {
    const formData = new FormData();
    formData.append("file", formFile);

    return axios.post("/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    });
  };
  ```

### File upload via `application/json` and base64

* Files can be uploaded via JSON and scanned, but with certain limitations. When using JSON for file uploads, the property name holding the base64-encoded file in the JSON object must be manually set in the FortiWeb Cloud application and placed in the JSON object's root.
* Using a property name other than the one specified in the FortiWeb Cloud application configuration will cause the file not to be scanned.

  > :warning: FortiWeb Cloud's support for file uploads within a JSON object is currently limited to one file per HTTP request.

* Below is an example of an HTTP request that sends a base64-encoded file within a JSON object and using the parameter name `file`:

  ```text
  POST /upload HTTP/2
  Host: domain.tbl
  User-Agent: Mozilla/5.0 (compatible; MSIE 11.0; Windows; Windows NT 6.2; Win64; x64; en-US Trident/7.0)
  Accept-Encoding: gzip, deflate, br, zstd
  Content-Type: application/json
  Content-Length: 875047
  Connection: keep-alive
  
  {
    "file": "WDVPIVAlQEFQWzRcUFpYNTQoUF4pN0NDKTd9JEVJQ0FSLVNUQU5EQVJELUFOVElWSVJVUy1URVNULUZJTEUhJEgrSCo="
  }
  ```

* Below is JavaScript code that uses `axios` to create an HTTP request similar to the one above:

  ```javascript
  const sendFile = async (formFile) => {
    const readFileAsBase64 = (file) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = () => {
          const base64File = reader.result.split(",")[1]; // Extract the Base64 part
          resolve(base64File);
        };

        reader.onerror = (error) => reject(error);
        reader.readAsDataURL(file);
      });
    };

    const base64File = await readFileAsBase64(formFile);

    // Create a JSON object with the Base64 encoded file
    const jsonPayload = {
      file: base64File
    };

    return axios.post("/upload", jsonPayload, {
      headers: {
        "Content-Type": "application/json"
      }
    });
  };
  ```

## How to confirm whether a file is being scanned by FortiWeb Cloud

* An EICAR test file can be used to verify that file upload mechanisms are correctly implemented and that FortiWeb Cloud is effectively detecting and blocking malware.
* This validates FortiWeb Cloud's scanning capabilities without putting the system at risk from real malware.

### What is an EICAR test file?

* The EICAR test file is a non-malicious computer file that was developed by the `European Institute for Computer Antivirus Research (EICAR)` to safely test antivirus and security systems.
* It is intended to activate antivirus and security system responses as a real malware file would, but without any risk of actual harm.
* The EICAR file contains a simple ASCII text file with a specific character sequence that antivirus programs recognize as a malicious file. The simplest version of the EICAR file content is as follows:

  ```text
  X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
  ```

* To create a EICAR test file, copy and paste the character sequence above into a text editor and save it with a `.txt` extension. Alternatively, it can be downloaded directly from the official [EICAR website][1].

### Testing FortiWeb Cloud scanning

* As a security practice, once file upload functionality is in place, it's essential to verify if FortiWeb Cloud properly identifies and blocks potentially harmful files.
* With proper FortiWeb Cloud configuration, it should intercept the EICAR file upload, blocking the HTTP request before it reaches the server. In this scenario, FortiWeb will return a `403 Forbidden` HTTP status code response to the client, indicating the file was blocked due to potential security risks, with the following content shown:

![FortiWeb Cloud EICAR file block page][2]

[1]: https://www.eicar.org/download-anti-malware-testfile/
[2]: /static/images/fortiweb-eicar-alert.png
