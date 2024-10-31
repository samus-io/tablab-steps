# How to implement the Cookie Secure attribute in Nginx 1.25.X

* To add the secure attribute from Nginx, you must first install the Openresty [Headers More Nginx][1] module.
* Once the module is installed, use the `more_set_headers` command:

  ```nginx
  user  nginx;
  worker_processes  auto;

  error_log  /var/log/nginx/error.log notice;
  pid        /var/run/nginx.pid;

  # Load Modules
  load_module modules/ngx_http_headers_more_filter_module.so;

  ...

  http {
    ...
    # Set Secure flag
    more_set_headers 'Set-Cookie: $sent_http_set_cookie; Secure';
    ...
  }
  ```

* In this example, the parameter `$sent_http_set_cookie` is the value of the Cookie sent by the backend, including the attributes sent by the backend.
* With this configuration, the Cookie sent by the backend is modified by adding the attribute `Secure`. Note that you can modify the `Set-Cookie` response header as you wish, even adding other attributes such as `HttpOnly` or `SameSite`.
* If you want to add dynamic attributes such as the `expires` attribute, you will have to do it directly from the backend at the programming level.

[1]: https://github.com/openresty/headers-more-nginx-module.git
