# How to implement headers in Apache 2.54.X

* Setting headers in Apache is quite simple, first you need to enable the `mod_headers` module. To do this, run the following command on the server and restart Apache:

  ```bash
  sudo a2enmod headers
  sudo service apache2 restart
  ```

* To specify the headers you want to set, you will need to edit the Apache configuration file and add the following content

  ```
  Header always set Content-Security-Policy "default-src 'none'"
  ```

* This example specifies that the server sends the `Content-Security-Policy` response header with the value `default: none`.
* After making these changes, it is important to restart Apache or reload the configuration:

  ```bash
  sudo service apache2 reload
  ```
