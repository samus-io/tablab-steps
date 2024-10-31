# Añadir módulos a Nginx 1.25.X

* Los módulos Nginx son componentes que extienden la funcionalidad del servidor web, proporcionando características y capacidades adicionales. Estos módulos pueden compilarse directamente en el binario de Nginx durante su proceso de compilación o añadirse dinámicamente como módulos compartidos.

* Hay dos tipos principales de módulos en Nginx:
  * Módulos principales: Estos módulos están incluidos en el núcleo de Nginx y son una parte integral del servidor. Proporcionan funcionalidades esenciales como la gestión de peticiones HTTP, el servicio de contenido estático y la gestión de conexiones.
  * Módulos de terceros: Estos módulos se desarrollan por separado del núcleo de Nginx y pueden añadirse al servidor para mejorar sus capacidades. Ofrecen una amplia gama de funcionalidades como balanceo de carga, almacenamiento en caché, mejoras de seguridad, entre otras.
* En el caso de los módulos de terceros, el proceso de instalación puede variar en función del propio módulo. En general, se tendrá que descargar el código fuente del módulo, compilarlo como un objeto dinámico compartido (DSO) o un módulo enlazado estáticamente, y luego configurar Nginx para cargar el módulo durante el tiempo de ejecución.

> :warning: Sólo instale módulos que provengan de fuentes de confianza. Si el módulo no es de una fuente de confianza puede contener malware e infectar el servidor.

## Instalación local de módulos

* Para instalar un módulo en local, primero descargue el código fuente. En este ejemplo usaremos el módulo [Headers More Nginx][1] de Openresty:
  ```bash
  git clone --depth 1 --single-branch https://github.com/openresty/headers-more-nginx-module.git
  ```
* Cambia el directorio actual al repositorio y actualiza los submódulos de GitHub:
  ```bash
  cd ./headers-more-nginx-module
  ```
  ```bash
  git submodule update --init
  ```
* Descarga Nginx (especificando la versión) para poder crear el módulo dinámico y luego hay que descomprimir el binario: 
  ```bash
  wget -O - http://nginx.org/download/nginx-<nginx-version>.tar.gz | tar zxfv -
  ```
* Ahora hay que configurar el módulo como un módulo dinámico para la versión de Nginx que hemos descargado. En caso de que el módulo no sea compatible con la versión de Nginx, este comando lanzará un error:
  ```bash
  ./nginx/configure --with-compat --add-dynamic-module=./headers-more-nginx-module
  ```
* Finalmente construiremos el módulo:
  ```bash
  make modules
  ```
* Añade el módulo donde estén almacenados los módulos de Nginx y dale permisos:
  ```bash
  cp ./nginx/objs/ngx_http_headers_more_filter_module.so /usr/lib/nginx/modules
  ```
  ```bash
  chmod -R 755 /usr/lib/nginx/modules/ngx_http_headers_more_filter_module.so
  ```

## Instalación del módulo Docker

* Este es un ejemplo de un Dockerfile que descarga e instala el módulo `Headers More Nginx v0.34` en la versión de `Nginx 1.25.2`. El Dockerfile obtiene los mismos resultados que la instalación local pero con la diferencia de que está todo automatizado:
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

## Configuración de Nginx

* Una vez instalado el módulo, asegúrese de añadirlo en el archivo de configuración de Nginx:
  ```nginx
  user  nginx;
  worker_processes  auto;

  error_log  /var/log/nginx/error.log notice;
  pid        /var/run/nginx.pid;

  # Load Modules
  load_module modules/ngx_http_headers_more_filter_module.so;

  ...
  ```
* De esta forma el módulo ya esta cargado en Nginx y listo para funcionar. Solo quedaría añadir las configuraciones deseadas que dependen de cada módulo.

[1]: https://github.com/openresty/headers-more-nginx-module.git