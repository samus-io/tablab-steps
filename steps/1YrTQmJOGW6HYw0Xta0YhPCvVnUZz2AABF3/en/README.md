# Information disclosure through response headers

* Web servers, like `Apache`, often include response headers that reveals sensitive information by default, such as `Server` header. Other technologies, like programming languages or frameworks, may also add headers automatically, such as PHP including the `X-Powered-By` header.
* These headers can expose technical details about the web application's environment. Disclosing server types and versions helps attackers look for known exploits associated with specific versions.
* It's recommended to configure servers and frameworks to avoid leaking this technical information by removing these headers, reducing the risk of targeted attacks.
* Tools like `curl` can be used to inspect a web application's response headers with the following command:

  ```bash
  curl -I http://domain.tbl
  ```

* A common response might show headers like the following:

  ```http
  HTTP/1.1 200 OK
  Date: Tue, 01 Apr 2025 11:15:23 GMT
  Server: Apache/2.4.62 (Debian)
  Vary: Accept-Encoding
  Content-Length: 1039
  Content-Type: text/html;charset=UTF-8
  ```

* In this example, the `Server` header reveals that the application is running on Apache version 2.4.62 on Debian.
* Preventing this kind of information leakage helps minimize the risk of targeted attacks based on server fingerprinting.
