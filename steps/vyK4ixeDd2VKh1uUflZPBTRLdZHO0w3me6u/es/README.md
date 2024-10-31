# Cómo implementar el atributo de las Cookie HttpOnly en Nginx 1.25.X

* Para poder añadir el atributo `HttpOnly` desde Nginx, primero hay que instalar el módulo [Headers More Nginx][1] de Openresty.
* Una vez instalado el módulo, hay que utilizar la instrucción `more_set_headers`:

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
    # Set HttpOnly flag
    more_set_headers 'Set-Cookie: $sent_http_set_cookie; HttpOnly';
    ...
  }
  ```

* En este ejemplo, el parámetro `$sent_http_set_cookie` es el valor de la Cookie enviada por el backend, incluyendo los atributos enviados por este.
* Con esta configuración, se modifica la Cookie añadiendo el atributo `HttpOnly`. Cabe destacar que se puede modificar la cabecera de respuesta `Set-Cookie` como se desee, incluso añadiendo otros atributos como `Secure` o `SameSite`.
* En el caso que se quiera añadir atributos dinámicos como el atributo `expires` se tendrá que hacer directamente desde el backend a nivel de programación.

[1]: https://github.com/openresty/headers-more-nginx-module.git
