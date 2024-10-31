# Conceptos básicos de la configuración de IIS 10.0

* Para modificar la configuración por defecto de IIS se tiene que modificar el archivo de configuración de la aplicación web `web.config`. Este archivo esta alojado en `C:\inetpub\wwwroot\Aplicacion\web.config` donde `Aplicacion` sera el nombre de la aplicación web.
* Hay que tener en cuenta que es posible que esta ubicación cambie, dependiendo de la configuración del servidor y como se haya instalado el IIS.
* Si no sabe donde puede estar alojado este archivo puede usar los siguientes comandos en la CMD de Windows para encontrarlo:

  ```cmd
  cd C:\inetpub\wwwroot
  dir /s web.config
  ```

* Cabe destacar que el archivo `web.config` solo modifica la aplicación web en la que esta ubicada, de esta forma cada aplicación web, en caso de tener mas de una alojada en el mismo servidor, tiene su propio archivo `web.config`.
* También es posible configurar el servidor IIS mediante la interficie gráfica pero se recomienda utilizar los archivos `web.config` ya que estos proporcionan una mayor granularidad, ademas de una mayor comprensión de la configuración.
* Es importante recordar que delante cualquier modificación de los archivos de configuración hay que reiniciar el servidor web.
