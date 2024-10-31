# How to remove response headers in Apache 2.54.X

* To remove headers in Apache, you must first enable the `mod_headers` module. To do this, run the following command on the server and then restart Apache

  ```bash
  sudo a2enmod headers
  sudo service apache2 restart
  ```

* Sometimes there are some response headers that do not need to be sent, such as the `Server` response header.
* To remove the response headers, you need to add the following statement to the appropriate configuration file:

  ```apacheconf
  Header always unset Server
  ```
