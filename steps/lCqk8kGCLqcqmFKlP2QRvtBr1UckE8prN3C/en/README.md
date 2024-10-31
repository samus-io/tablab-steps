# Basic configuration concepts of Apache 2.54.X

## Installation and management of the Apache service

* First you need to install Apache, to do this on Linux Debian you need to run the following command

  ```bash
  sudo apt-get install apache2
  ```

* If you want to start, restart, shutdown, or reset the Apache configuration, you can run the following commands

  ```bash
  sudo systemctl start apache2
  sudo systemctl restart apache2
  sudo systemctl stop apache2
  sudo systemctl reload apache2
  ```

## Apache configuration files

* The configuration of Apache can be done from different configuration files, depending on the operating system it can be the file `apache2.conf` or `httpd.conf`. These can be located in `/etc/httpd`, `/etc/apache2` in Linux or `C:\Program Files (x86)\Apache Group\Apache2` in Windows.
  * Normally, the default path for the global configuration file is `/etc/apache2/apache2.conf`, which will be used in the following exercises, but even if the file name changes, the configuration is the same.
* If the Virtual Host is used to create different web applications on the same server, it is important to remember that changes made to these files will affect all web applications.
  * If you want to modify only one web application, you must modify the corresponding configuration file located in the `sites-available` directory of the Apache root directory, this directory indicates which web applications are active.
* It is also possible to configure Apache using `.htaccess` files in the same format as the other configuration files, but these will only take effect in the directory in which they are stored.

## Apache configuration recommendations

* It is recommended that you use `apache2.conf` to set a configuration that you want to apply to all active servers, and then use each Virtual Host file to set specific configuration options. The options specified in the global apache file will be overridden by the Virtual Host files, but only for options that are equivalent.
* For example, if we have a rule in `apache2.conf` that allows the `Server` response header to be sent, and then a Virtual Host configuration file specifies otherwise, the latter will take precedence.
* For security options, when using Virtual Host, it is recommended to use the `apache2.conf` file to avoid leaving a server unprotected against vulnerabilities, and to use the Virtual Host configuration files only for some security options specific to each web application.
* It is important to remember that the web server must be restarted before any changes are made to the configuration files.
