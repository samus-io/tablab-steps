# How to set the Referrer-Policy header in Apache 2.4

* The `Referrer-Policy` header defines how much referrer information should be shared with external sites and can be configured directly in Apache settings.

## Apache configuration files overview

* Apache configuration may be handled through various files, such as `apache2.conf` or `httpd.conf`, depending on the operating system.
  * In Linux systems, these files are usually located in `/etc/apache2` or `/etc/httpd`, and in Windows usually in `C:\Program Files (x86)\Apache Group\Apache2`.
  * The file `/etc/apache2/apache2.conf` usually serves as the default global configuration on many Linux systems.
* When virtual hosts are used to run multiple applications on a single web server, changes to global configuration files will impact all of them. Therefore, to target a specific web application, it's preferable to modify the relevant file in the `sites-available` directory, which contains individual application configurations.
* Apache can also be configured using `.htaccess` files, which follow the same format as other config files but apply only to they are located.

## Setting the `Referrer-Policy` header

* Headers can be set easily in Apache using the `mod_headers` module. To activate it, execute the commands below on the server and restart Apache.

  ```bash
  sudo a2enmod headers
  sudo service apache2 restart
  ```

  * Once the module is enabled, headers can be configured by editing the appropriate Apache configuration file.
* To configure the Referrer-Policy header, insert the directive shown below into the appropriate configuration file:

  ```apacheconf
  Header always set Referrer-Policy "no-referrer"
  ```

  * This configuration instructs the server to send the `Referrer-Policy` header with the value `no-referrer`.
* Once the changes are made, Apache must be restarted to apply the new configuration:

  ```bash
  sudo service apache2 reload
  ```
