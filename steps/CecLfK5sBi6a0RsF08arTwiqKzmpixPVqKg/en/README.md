# How to implement headers in Nginx 1.25.X

* To set headers in Nginx, you have to modify the configuration file corresponding to the server. Then, to be able to append a response header in Nginx, it is necessary to add the following content inside the `http` or `server` section

  ```nginx
  http {
    ...
    add_header content security policy "default-src 'none';";
    ...
    server { ...
        listen 80;
        server_name example.tbl;
        ...
    }
  }
  ```

* This example adds the `Content-Security-Policy` header with the value `default-src 'none'` to the Web application response headers.
* After making the appropriate changes to the configuration file, it is necessary to restart the server for them to take effect.
