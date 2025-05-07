# How to remove Server response header in Apache 2.4

* The response header `Server` often reveal unnecessary technical information that are not required for application functionality and can be removed to improve security.
* Apache allows the removal of headers through the `mod_security` module. To enable this module, run the following commands on the server and restart Apache:

  ```bash
  apt install libapache2-mod-security2 -y
  sudo service apache2 restart
  ```

* Once the module is enabled, the `Server` header can be removed by adding the directive to the Apache configuration `/etc/apache2/conf-available/security.conf` file:

  ```apacheconf
  SecServerSignature " "
  ```

* This directive ensures that the Server header is not included in the HTTP response, reducing the amount of information exposed.

## Exercise to practice :writing_hand:

* The application below does returns the response header `Server` which discloses the web server and its version.
* The goal here is to modify the `security.conf` file using the code editor accessed via the `Open Code Editor` button and implement a custom error page.
* **It is important to note that, in this case, there is no need to install or enable the `mod_security` module, as it is already installed and enabled.**
* After implementing the changes and redeploying the app, use `curl` to send requests and review the HTTP response headers for manual validation:

  ```bash
  curl -I $APP_URL
  ```

* Once done, press the `Verify Completion` button to confirm the exercise has been successfully completed.

  @@ExerciseBox@@
