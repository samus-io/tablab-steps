# How to implement the Cookie Secure attribute in Apache 2.54.X

* To set the `Secure` flag, modify the Apache configuration file and add the following line

  ```apacheconf
  Edit Header Set-Cookie ^(.*)$ $1;Secure;
  ```

* With this configuration, Apache will modify all `Set-Cookie` response headers where the value matches the regular expression `^(.*)$` (in this case, any value) and change the header value to `$1;Secure;` where `$1` is the original value of the `Set-Cookie` header.
