# How to remove response headers in Apache 2.4

## Apache configuration files

* The configuration of Apache can be managed from different configuration files, depending on the operating system it can be the file `apache2.conf` or `httpd.conf`.
* In Linux systems, these files are typically found in `/etc/apache2` or `/etc/httpd`, while in Windows they may be under `C:\Program Files (x86)\Apache Group\Apache2`.
  * The default global configuration file is usually located at `/etc/apache2/apache2.conf` on most Linux distributions
* When using Virtual Hosts to run multiple web applications on a single server, changes to the global configuration files will affect all applications
  * If the configuration should only apply to one specific web application, it is better to modify the appropriate file inside the `sites-available` directory, which holds the configuration files for individual applications.
* It is also possible to configure Apache using `.htaccess` files in the same format as the other configuration files, but these will only take effect in the directory in which they are stored.

## Remove response headers

* Response headers like `X-Powered-By` often reveal unnecessary technical information that are not required for application functionality and can be removed to improve security.
* Apache allows the removal of headers through the `mod_headers` module. To enable this module, run the following commands on the server and restart Apache:

  ```apache
  sudo a2enmod headers
  sudo service apache2 restart
  ```

* Once the module is enabled, headers can be removed by adding a directive to the relevant Apache configuration file:

  ```apache
  Header unset X-Powered-By
  ```

* This directive ensures that the `X-Powered-By` header is not included in the HTTP response, reducing the amount of information exposed.

## Exercise to practice :writing_hand:

* The application below does returns the response header `X-Powered-By` which discloses the web server and its version.
* The goal here is to modify the `apache.conf` file using the code editor accessed via the `Open Code Editor` button and implement a custom error page.
* **It is important to note that, in this case, there is no need to install or enable the `mod_security` module, as it is already installed and enabled.**
* After making the changes, press the `Verify Completion` button to confirm that the exercise has been completed.

@@ExerciseBox@@
