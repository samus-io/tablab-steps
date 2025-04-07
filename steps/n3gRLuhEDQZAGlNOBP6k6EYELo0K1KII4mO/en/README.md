# How to implement Referrer-Policy in Apache 2.54.X

## Apache configuration files

* The configuration of Apache can be managed from different configuration files, depending on the operating system it can be the file `apache2.conf` or `httpd.conf`.
* In Linux systems, these files are typically found in `/etc/apache2` or `/etc/httpd`, while in Windows they may be under `C:\Program Files (x86)\Apache Group\Apache2`.
  * The default global configuration file is usually located at `/etc/apache2/apache2.conf` on most Linux distributions
* When using Virtual Hosts to run multiple web applications on a single server, changes to the global configuration files will affect all applications
  * If the configuration should only apply to one specific web application, it is better to modify the appropriate file inside the `sites-available` directory, which holds the configuration files for individual applications.
* It is also possible to configure Apache using `.htaccess` files in the same format as the other configuration files, but these will only take effect in the directory in which they are stored.

## Implementing Referrer-Policy header

* Setting headers in Apache is quite simple through the `mod_headers` module. To enable this module, run the following commands on the server and restart Apache:

  ```bash
  sudo a2enmod headers
  sudo service apache2 restart
  ```

* Once the module is enabled, headers can be configured by editing the appropriate Apache configuration file.
* In this example, to add the `Referrer-Policy` response header, include the following directive in the configuration file:

  ```apacheconf
  Header always set Referrer-Policy "no-referrer"
  ```

* This configuration instructs the server to send the `Referrer-Policy` header with the value `no-referrer`.
* After applying the changes, restart or reload Apache to apply the updated configuration

  ```bash
  sudo service apache2 reload
  ```
