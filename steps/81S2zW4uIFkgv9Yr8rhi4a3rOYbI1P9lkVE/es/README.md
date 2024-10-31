# Cómo eliminar cabeceras de respuesta en Nginx 1.25.X

* En ocasiones hay algunas cabeceras que no se tienen que enviar, como podría ser la cabecera de respuesta `Server`.
* Para eliminar cabeceras en Nginx, primero hay que instalar el módulo [Headers More Nginx][1] de Openresty.
* Una vez instalado el módulo, únicamente hay que utilizar la instrucción `more_clear_headers` como en el siguiente ejemplo:

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
