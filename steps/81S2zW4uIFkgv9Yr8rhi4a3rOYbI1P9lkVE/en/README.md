# How to remove response headers in Nginx 1.25.X

* Sometimes there are some headers that do not need to be sent, such as the `Server` response header.
* To remove headers in Nginx, you must first install the Openresty [Headers More Nginx][1] module.
* Once the module is installed, simply use the `more_clear_headers` directive as in the following example:

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
    # Remove Server Header
    more_clear_headers Server;
    ...
  }
  ```

[1]: https://github.com/openresty/headers-more-nginx-module.git
