# How to remove Server response header in Apache 2.4

* The `Server` response header frequently exposes technical details that are not essential to functionality and should be removed to enhance security. A typical response including the `Server` header is shown below:
  
  ```http
  HTTP/1.1 200 OK
  Date: Tue, 01 Apr 2025 11:15:23 GMT
  Server: Apache/2.4.62 (Debian)
  Vary: Accept-Encoding
  Content-Length: 1039
  Content-Type: text/html;charset=UTF-8
  ```

  * Note how it discloses that Apache version `2.4.62` is running on a Debian-based system.

* Apache allows the removal of headers through the `mod_security` module. This module can be enabled by running the listed command on the server followed by an Apache restart:

  ```bash
  apt install libapache2-mod-security2 -y
  sudo service apache2 restart
  ```

* Once the module is activated, the `Server` header can be removed by adding the following directive to the Apache configuration `/etc/apache2/conf-available/security.conf` file:

  ```apacheconf
  SecServerSignature " "
  ```

  * This directive ensures that the `Server` header is not included in HTTP responses, reducing the amount of information exposed.
