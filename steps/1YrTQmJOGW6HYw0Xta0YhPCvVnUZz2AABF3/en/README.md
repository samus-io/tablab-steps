# Information disclosure via response headers

* Web servers and backend frameworks often append headers automatically, such as Apache including `Server` and PHP appending `X-Powered-By`, which may reveal sensitive implementation details.
* Revealing environment details through headers can aid attackers in identifying exploitable weaknesses linked to specific software versions.

## Recommended security approaches

* It is advisable to configure servers and frameworks to remove these headers entirely, thereby minimizing the risk of targeted attacks.
* With the `-I` flag, tools like `curl` allow straightforward inspection of response headers from a web application, as demonstrated below:

  ```bash
  curl -I http://domain.tbl
  ```
  
  A common response may include headers such as the following:

  ```http
  HTTP/1.1 200 OK
  Date: Tue, 01 Apr 2025 11:15:23 GMT
  Server: Apache/2.4.62 (Debian)
  X-Powered-By: PHP/8.2.5
  Content-Length: 1039
  Content-Type: text/html;charset=UTF-8
  Vary: Accept-Encoding
  ```

  * In this example, this response reveals that Apache `2.4.62` is running on Debian and using PHP version `8.2.5`, which could assist attackers in identifying known vulnerabilities.
* Reducing this kind of technical detail in responses limits opportunities for attackers to perform server fingerprinting.
