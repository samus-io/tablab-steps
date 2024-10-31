# How to implement the Cookie HttpOnly attribute in Apache 2.54.X

* In order to set the `HttpOnly` attribute you have to modify the Apache configuration file and add the following line:

  ```apacheconf
  Header edit Set-Cookie ^(.*)$ $1;HttpOnly;
  ```

* Apache will modify all `Set-Cookie` response headers where the value matches the regular expression `^(.*)$` (in this case, any value) and modify the header value to `$1;HttpOnly;` where `$1` is the original value of the `Set-Cookie` header.
