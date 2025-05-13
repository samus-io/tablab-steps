# How to remove response headers in Apache 2.4

* Some HTTP response headers expose unnecessary server details, which can aid attackers in fingerprinting the underlying technologies. Apache allows these headers to be removed to improve security posture.

## Apache configuration files overview

* Apache configuration may be handled through various files, such as `apache2.conf` or `httpd.conf`, depending on the operating system.
  * In Linux systems, these files are usually located in `/etc/apache2` or `/etc/httpd`, and in Windows usually in `C:\Program Files (x86)\Apache Group\Apache2`.
  * The file `/etc/apache2/apache2.conf` usually serves as the default global configuration on many Linux systems.
* When virtual hosts are used to run multiple applications on a single web server, changes to global configuration files will impact all of them. Therefore, to target a specific web application, it's preferable to modify the relevant file in the `sites-available` directory, which contains individual application configurations.
* Apache can also be configured using `.htaccess` files, which follow the same format as other config files but apply only to they are located.

## How to remove response headers

* The `X-Powered-By` response header frequently exposes technical details that are not essential to functionality and should be removed to enhance security. A typical response including the `X-Powered-By` header is shown below:
  
  ```http
  HTTP/1.1 200 OK
  Date: Tue, 01 Apr 2025 11:15:23 GMT
  Server: Apache/2.4.62 (Debian)
  X-Powered-By: PHP/8.2.5
  Content-Length: 1039
  Content-Type: text/html;charset=UTF-8
  Vary: Accept-Encoding
  ```

  * This response reveals that Apache is running on Debian and using PHP version `8.2.5`, which could assist attackers in identifying known vulnerabilities.

* Apache allows the removal of headers through the `mod_headers` module. This module can be enabled by running the listed command on the server followed by an Apache restart:

  ```bash
  sudo a2enmod headers
  ```

  ```bash
  sudo service apache2 restart
  ```

* Once the module is activated, the `X-Powered-By` header can be removed by adding the following directive to the relevant Apache configuration file:

  ```apache
  Header unset X-Powered-By
  ```

  * This directive ensures that the `X-Powered-By` header is not included in the HTTP response, reducing the amount of information exposed.

## Exercise to practice :writing_hand:

* The application below includes the `X-Powered-By` header in HTTP responses, disclosing the PHP version.
* The goal here is to modify the `apache.conf` file using the code editor accessed via the `Open Code Editor` button, and remove the `X-Powered-By` header.
* **It is important to note that, in this case, there is no need to install or enable the `mod_headers` module, as it is already installed and enabled.**
* After implementing the changes and redeploying the app, use `curl` to send requests and review the HTTP response headers for manual validation:

  ```bash
  curl -I $APP_URL
  ```

* Once done, press the `Verify Completion` button to confirm the exercise has been successfully completed.

  @@ExerciseBox@@
