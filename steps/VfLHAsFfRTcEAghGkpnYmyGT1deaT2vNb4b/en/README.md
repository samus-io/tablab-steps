# Add modules to Nginx 1.25.X

* Nginx modules are components that extend the functionality of the Nginx web server by providing additional features and capabilities. These modules can be either compiled directly into the Nginx binary during its build process or added dynamically as shared modules.

* There are two main types of modules in Nginx:
  * Core Modules: These modules are included in the Nginx core and are an integral part of the server. They provide essential functionalities such as handling HTTP requests, serving static content, and managing connections.
  * Third-Party Modules: These modules are developed separately from the Nginx core and can be added to the server to enhance its capabilities. They offer a wide range of features such as load balancing, caching, security enhancements, and more.
* For third-party modules, the installation process may vary depending on the module itself. In general, you'll need to download the source code of the module, compile it as a dynamic shared object (DSO) or a statically linked module, and then configure Nginx to load the module during runtime.

> :warning: Only install modules that are from trusted source. If the module isn't from a trusted source it can contain malware and infect the server.

## Local module installation

* To install a module on local, first download the source code. In this example we will use the module `Headers More Nginx` of Openresty:
  ```bash
  git clone --depth 1 --single-branch https://github.com/openresty/headers-more-nginx-module.git
  ```
* Change current directory to the repository and update the submodules of GitHub:
  ```bash
  cd ./headers-more-nginx-module
  ```
  ```bash
  git submodule update --init
  ```
* Download Nginx (you have to specify the version) and decompress: 
  ```bash
  wget -O - http://nginx.org/download/nginx-<nginx-version>.tar.gz | tar zxfv -
  ```
* Now we will configure the module as a dynamic module for the Nginx version that we had downloaded. In case that the module isn't compatible with the Nginx version, this command will throw an error:
  ```bash
  ./nginx/configure --with-compat --add-dynamic-module=./headers-more-nginx-module
  ```
* Finally we will build the module:
  ```bash
  make modules
  ```
* Copy the module where there are your Nginx modules and give it permissions:
  ```bash
  cp ./nginx/objs/ngx_http_headers_more_filter_module.so /usr/lib/nginx/modules
  ```
  ```bash
  chmod -R 755 /usr/lib/nginx/modules/ngx_http_headers_more_filter_module.so
  ```

## Docker module installation

* This is an example of a Dockerfile that download and install the module `Headers More Nginx`. The Dockerfile get the same results as the local installation but with the difference that is all automated:  
  ```Dockerfile
  ARG NGINX_VERSION=1.25.2
  ARG HEADERS_MORE_VERSION=v0.34

  FROM nginx:$NGINX_VERSION-alpine

  RUN apk --update --no-cache add \
          gcc \
          make \
          libc-dev \
          g++ \
          openssl-dev \
          linux-headers \
          pcre-dev \
          zlib-dev \
          libtool \
          automake \
          autoconf \
          git

  RUN cd /opt \
      && git clone --depth 1 --single-branch https://github.com/openresty/headers-more-nginx-module.git \
      && cd /opt/headers-more-nginx-module \
      && git submodule update --init \
      && cd /opt \
      && wget -O - http://nginx.org/download/nginx-$NGINX_VERSION.tar.gz | tar zxfv - \
      && mv /opt/nginx-$NGINX_VERSION /opt/nginx \
      && cd /opt/nginx \
      && ./configure --with-compat --add-dynamic-module=/opt/headers-more-nginx-module \
      && make modules

  FROM nginx:$NGINX_VERSION-alpine

  COPY --from=0 /opt/nginx/objs/ngx_http_headers_more_filter_module.so /usr/lib/nginx/modules

  RUN chmod -R 755 /usr/lib/nginx/modules/ngx_http_headers_more_filter_module.so

  COPY ./nginx.conf /etc/nginx/nginx.conf
  ```

## Nginx configuration

* After the module is installed, ensure to add it in the Nginx configuration file:
  ```nginx
  user  nginx;
  worker_processes  auto;

  error_log  /var/log/nginx/error.log notice;
  pid        /var/run/nginx.pid;

  # Load Modules
  load_module modules/ngx_http_headers_more_filter_module.so;

  ...
  ```

