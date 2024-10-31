# Basic configuration concepts of IIS 10.0

* To modify the default IIS configuration, you must modify the web application configuration file `web.config`. This file is located at `C:\inetpub\wwwroot\Application\web.config`, where `Application` is the name of the web application.
* Note that this location may change depending on the server configuration and how IIS is installed.
* If you do not know where this file is located, you can use the following commands in Windows CMD to find it

  ```cmd
  cd C:\inetpub\wwwroot
  dir /s web.config
  ```

* Note that the `web.config` file only modifies the web application in which it resides, so if you have more than one web application hosted on the same server, each web application will have its own `web.config` file.
* It is also possible to configure the IIS server through the graphical interface, but it is recommended to use the `web.config` files as they provide a greater granularity in addition to a better understanding of the configuration.
* It is important to remember that the web server must be restarted before any changes are made to the configuration files.
