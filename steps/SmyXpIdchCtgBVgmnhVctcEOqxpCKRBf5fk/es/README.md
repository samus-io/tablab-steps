# Explotando la vulnerabilidad Path Traversal

* La técnica más comúnmente empleada para explotar esta vulnerabilidad utiliza la secuencia `../` en sistemas basados en Unix/Linux o `..\` en sistemas Windows. Este método intenta "ascender" en la jerarquía de directorios para acceder a archivos o directorios fuera del ámbito permitido.
* Considerando una aplicación web que permite a los usuarios visualizar imágenes mediante un parámetro en la URL:

  ```
  https://example.tbl/getFile?img=image1.png
  ```

## Explotando el Path Traversal en servidores Linux

* Un adversario podría modificar el parámetro `img` para tratar de acceder a archivos más allá del directorio designado. Por ejemplo, para leer el archivo `/etc/passwd`, que alberga información crítica sobre los usuarios del sistema, el adversario podría manipular la URL de la siguiente manera:

  ```
  https://example.tbl/getFile?img=../../../../etc/passwd
  ```

* En esta imagen se puede observar como funciona exactamente el Path Traversal:

![Path Traversal Example][1]

* Primero, el adversario hace la petición contra `http://abc.com/?file=../../../etc/passwd`. Al recibir la petición el servidor, este interpreta qué archivo se esta intentando leer, accediendo a directorios anteriores hasta llegar al directorio raíz. Una vez allí, se procede a buscar el directorio `etc` y acceder al archivo `passwd`.

## Explotando el Path Traversal en servidores Windows

* En entornos Windows, el ataque se adapta utilizando secuencias de ruta diferentes (`..\`) para navegar por el sistema de archivos. Un ejemplo clásico sería intentar acceder al archivo de configuración `web.config` de una aplicación ASP.NET, que podría contener información sensible como credenciales de acceso a bases de datos:

  ```
  https://example.tbl/getFile?img=..\..\..\..\web.config
  ```

* En Windows, el adversario también podría intentar acceder a archivos del sistema o directorios críticos utilizando rutas absolutas o relativas para obtener información sensible o manipular el comportamiento de la aplicación.

## Técnicas avanzadas

* Además de esta técnica, existen otras para llegar a explotar esta vulnerabilidad. Por ejemplo, otra de las técnica mas utilizadas, es usar URL encoding para así evadir filtros de seguridad, convirtiendo la cadena `../` a `%2e%2e%2f`. De esta forma, si la aplicación no acepta la cadena `../`, en algunas aplicaciones, se conseguirá evadir la seguridad y explotar la vulnerabilidad.

## Practica

* :writing_hand: Esta aplicación web utiliza un parámetro para incluir imágenes en la página web, explota la vulnerabilidad accediendo al `/etc/passwd`:
@@ExerciseBox@@

[1]: /static/images/learning/path-traversal-example.png
