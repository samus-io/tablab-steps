# Cómo eliminar cabeceras de respuesta en IIS 10.0

* Para eliminar cabeceras en IIS solo hay que eliminar el contenido del `web.config` que añade la cabecera.
* En algunos casos esto no será posible, ya que la cabecera la implementa el propio IIS como pasa con la cabecera `Server`. Es recomendable eliminar esta cabecera ya que proporciona información del servidor junto con la versión de este.
* Para eliminar la cabecera `Server` se tendrá que instalar el módulo de IIS `IIS URL Rewrite`. Este módulo reescribirá las peticiones de forma que no se envíe la cabecera.
* Para instalar el módulo, hay que descargar y ejecutar el instalador desde la página oficial de IIS [URL Rewrite][1].
* Una vez instalado el módulo, hay que reiniciar el servicio y añadir el siguiente contenido al archivo `web.config`:

  ```xml
  <rewrite>
    <outboundRules>
        <rule name="Remove Server header">
            <match serverVariable="RESPONSE_SERVER" pattern=".+" />
            <action type="Rewrite" value="" />
        </rule>
    </outboundRules>
  </rewrite>
  ```

* Esta configuración buscará la variable del servidor `RESPONSE_SERVER` y reescribirá su valor dejándolo vacío.

[1]: https://www.iis.net/downloads/microsoft/url-rewrite
