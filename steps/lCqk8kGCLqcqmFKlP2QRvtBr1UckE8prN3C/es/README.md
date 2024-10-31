# Conceptos basicos de la configuración de Apache 2.54.X

## Instalación y gestión del servicio Apache

* Primero de todo se debe de instalar Apache, para hacerlo en Linux Debian hay que ejecutar el siguiente comando:

  ```bash
  sudo apt-get install apache2
  ```

* Si se quiere iniciar, reiniciar, apagar o reiniciar la configuración de Apache puede ejecutarse los siguientes comandos:

  ```bash
  sudo systemctl start apache2
  sudo systemctl restart apache2
  sudo systemctl stop apache2
  sudo systemctl reload apache2
  ```

## Archivos de configuración de Apache

* Para configurar Apache se puede realizar desde distintos archivos de configuración, dependiendo del sistema operativo puede ser el fichero `apache2.conf` o `httpd.conf`. Estos pueden estar en el directorio `/etc/httpd`, `/etc/apache2` en Linux o en Windows `C:\Program Files (x86)\Apache Group\Apache2`.
  * Normalmente la ruta predefina para el archivo de configuración global es `/etc/apache2/apache2.conf`, el cual se utilizará en los siguientes ejercicios, de todas formas aunque el nombre del archivo cambie, la configuración es la misma.
* En el caso que se utilize el Virtual Host para crear distintas aplicaciones web en un mismo servidor, hay que tener en cuenta que los cambios realizados en estos archivos afectaran a todas las aplicaciones web.  
  * Si solo se quisiera modificar una aplicación web hay que modificar el archivo de configuración correspondiente que se encuentra en el directorio `sites-available` del directorio principal de Apache, este directorio indica qué aplicaciones web están activas.
* También es posible configurar Apache desde los archivos `.htaccess` con el mismo formato que los otros archivos de configuración pero estos solo tendrán efecto en el directorio que este guardado.

## Recomendaciones de configuración de Apache

* Se recomienda utilizar `apache2.conf` para establecer una configuración que se quiera adoptar en todos los servidores activos y luego utilizar cada archivo de Virtual Host para establecer opciones de configuración especifica. Las opciones especificadas en el archivo global de apache son sobrescritas por los archivos de Virtual Host, pero solo en las opciones que son equivalentes.
* Por ejemplo, si tenemos una regla en `apache2.conf` que permite enviar la cabecera de respuesta `Server` y luego en un archivo de configuración de Virtual Host se especifica lo contrario, este último tendrá preferencia.
* Para las opciones de seguridad, en el caso que se utilice Virtual Host, se recomienda utilizar el archivo `apache2.conf` para evitar dejar un servidor desprotegido a vulnerabilidades y utilizar los archivos de configuración del Virtual Host solo para algunas opciones de seguridad que son especificas de cada aplicación web.
* Es importante recordar que delante cualquier modificación de los archivos de configuración hay que reiniciar el servidor web.
