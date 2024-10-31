# How to implement the Cookie HttpOnly attribute in Nginx 1.25.X

* In Nginx, to add the `HttpOnly` attribute, you must first install the Openresty [Headers More Nginx][1] module.
* Once the module is installed, use the `more_set_headers` directive:

  ```nginx
  User nginx;
  worker_processes auto;

  error_log /var/log/nginx/error.log note;
  pid /var/run/nginx.pid;

  # load modules
  load_module modules/ngx_http_headers_more_filter_module.so;

  ...

  http { ...
    ...
    # Set HttpOnly flag
    more_set_headers 'Set-Cookie: $sent_http_set_cookie; HttpOnly';
    ...
  }
  ```

* In this example, the `$sent_http_set_cookie` parameter is the value of the cookie sent by the backend, including the attributes sent by the backend.
* This configuration modifies the cookie by adding the `HttpOnly` attribute. Note that you can modify the `Set-Cookie` response header as you like, even adding other attributes such as `Secure` or `SameSite`.
* If you want to add dynamic attributes like the `expires` attribute, you have to do it directly from the backend at programming level.

[1]: https://github.com/openresty/headers-more-nginx-module.git
