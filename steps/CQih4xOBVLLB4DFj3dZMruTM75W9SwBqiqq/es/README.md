# Conceptos básicos de la configuración de Nginx 1.25.X

## Instalación y gestión del servicio Nginx

* Primero de todo para instalar Nginx en Linux Debian se tiene que ejecutar el siguiente comando:

  ```bash
  sudo apt install nginx
  ```

* Para iniciar, reiniciar, apagar de Nginx se puede ejecutar los siguientes comandos:

  ```bash
  sudo systemctl start nginx
  sudo systemctl restart nginx
  sudo systemctl stop nginx
  ```

## Archivos de configuración de Nginx

* Nginx tiene un archivo de configuración principal que contiene la configuración global para todo el servidor. Este archivo esta alojado en la ruta `/etc/nginx/nginx.conf` o `C:\nginx\conf\nginx.conf` dependiendo del sistema operativo.
  * En algunas distribuciones de Nginx puede cambiar la estructura de archivos, en ese caso se puede utilizar el comando `nginx -t` para saber donde se encuentra el archivo de configuración.
* Igual que Apache, Nginx tiene el directorio `sites-enabled` donde se encuentran los archivos de configuración para cada aplicación web en el caso que se utilice Virtual Host. También en caso que alguna opción del archivo de configuración del Virtual Host entre en conflicto con la configuración global, la configuración del directorio `sites-enabled` tendrá prioridad sobre esta.

## Recomendaciones de configuración de Nginx

* Para las opciones de seguridad, en el caso que se utilice Virtual Host, se recomienda utilizar el archivo `nginx.conf` para evitar dejar un servidor desprotegido a vulnerabilidades y utilizar los archivos de configuración del Virtual Host solo para algunas opciones de seguridad que son especificas de cada aplicación web, como podría ser la `Content Security Policy`.
* Es importante recordar que delante cualquier modificación de los archivos de configuración hay que reiniciar el servidor web.
