# Basic configuration concepts of Nginx 1.25.X

## Installation and management of the Nginx service

* To install Nginx on Debian Linux, you must first run the following command:

  ```bash
  sudo apt install nginx
  ```

* To start, restart, or shutdown Nginx, you can execute the commands:

  ```bash
  sudo systemctl start nginx
  sudo systemctl restart nginx
  sudo systemctl stop nginx
  ```

## Nginx configuration files

* Nginx has a main configuration file that contains the global configuration for the entire server. This file is located in `/etc/nginx/nginx.conf` or `C:\nginx\conf\nginx.conf` depending on your operating system.
  * In some Nginx distributions you can change the file structure, in this case you can use the `nginx -t` command to find out where the configuration file is located.
* Like Apache, Nginx has a `sites-enabled` directory which contains the configuration files for each web application when using virtual hosting. Also, if an option in the virtual host configuration file conflicts with the global configuration, the configuration in the `sites-enabled` directory will take precedence over the global configuration.

## Nginx configuration recommendations

* For security options, if Virtual Host is used, it is recommended to use the `nginx.conf` file to avoid leaving a server unprotected against vulnerabilities, and to use the Virtual Host configuration files only for some security options that are specific to each web application, such as the `Content Security Policy`.
* It is important to remember that the web server must be restarted before any changes are made to the configuration files.
