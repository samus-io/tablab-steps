# Saneamiento de nombres de archivo

* El saneamiento de nombres de archivo es un proceso esencial destinado a garantizar que los nombres de archivo sean seguros y compatibles con el sistema en el que se van a utilizar.
* Consiste en validar y potencialmente modificar los nombres originales de los archivos recibidos para prevenir amenazas de seguridad o fallos operativos que puedan comprometer la integridad del sistema.

## Lista de control de las medidas de seguridad

* Siempre que sea posible, se deben utilizar nombres de archivo únicos y aleatorios al almacenar los ficheros (e.g., adoptando UUID). Si las restricciones de lógica de la organización impiden este enfoque, entonces se recomienda:

  * [ ] Establecer un límite de longitud del nombre de archivo.
  * [ ] Limitar los caracteres permitidos (e.g., únicamente considerar `A-Z`, `a-z`, `0-9`, `-`, y `.` como caracteres válidos).
  * [ ] Tratar los nombres de archivo sin distinguir mayúsculas de minúsculas.
  * [ ] Restringir los nombres reservados en Windows y Linux.
  * [ ] Evitar los archivos ocultos y los puntos y espacios finales (e.g., `.htaccess`).

## Generar de nombres de archivo únicos y aleatorios

* La creación de nombres de archivo únicos y aleatorios al almacenar los archivos cargados evita las colisiones de nombres de archivo, mitiga los ataques path traversal, oculta los nombres de archivo originales que podrían exponer detalles sensibles, mejora la seguridad contra la ejecución de archivos maliciosos reduciendo el riesgo de que un atacante pueda localizar y ejecutar dichos archivos, y evita los ataques de enumeración de archivos.
* Una forma fiable de crear nombres de archivo impredecibles y no sobrescribibles es utilizar `Universally Unique Identifier (UUID)` o `Globally Unique Identifier (GUID)`.
* Este enfoque es especialmente útil en situaciones en las que no es necesario conservar los nombres de archivo originales proporcionados por los usuarios.

## Límites de longitud de los nombres de archivo

* Los distintos sistemas de archivos imponen límites variables a la longitud de los nombres de archivo, lo que puede afectar a la compatibilidad y la seguridad. Por ejemplo, el sistema de archivos `MS-DOS FAT` establece el formato de nombre de archivo `8.3`, que solo admite 8 caracteres para el nombre y 3 para la extensión, con el fin de mantener la compatibilidad con el software heredado.
* Los sistemas de archivos modernos como `NTFS` pueden soportar nombres de archivo más largos, aunque Windows ha impuesto tradicionalmente un límite `MAX_PATH` de 260 caracteres. Superar este límite puede provocar errores de truncamiento o de acceso a archivos, aunque las nuevas versiones de Windows permiten eliminar este límite mediante los ajustes de configuración adecuados.
* Tener en cuenta los límites de longitud de los nombres de archivo es esencial para evitar problemas como errores de acceso a los archivos, truncamientos o riesgos de seguridad debidos a una mala interpretación del sistema de archivos.

## Aplicar validación de entrada a los nombres del archivo

* Cuando se permiten nombres de archivo definidos por el usuario, es crucial validar exhaustivamente las entradas para prevenir vulnerabilidades como *path traversal* o ataques de inyección, así como para evitar errores operativos.
* *Path traversal* se refiere al proceso de manipulación de rutas de archivos para acceder a ubicaciones no deseadas fuera del directorio designado. Los usuarios maliciosos incluyen secuencias como `../` en los nombres de archivo para atravesar directorios y almacenar archivos en ubicaciones no deseadas. Por ejemplo, un nombre de archivo como `../../../../var/www/html/index.php` colocaría el archivo en *web root*, reemplazando potencialmente el contenido del archivo principal de una aplicación web PHP.
* Los nombres de archivo también pueden utilizarse para explotar vulnerabilidades relacionadas con la forma en que la aplicación procesa y gestiona el mismo. Por ejemplo, un nombre de archivo como `sleep(20)-- -.jpg` podría desencadenar una inyección SQL, `<svg onload=alert("XSS")>` podría conducir a XSS, y `; sleep 20;` podría dar lugar a una inyección de comandos.
* Permitir únicamente un conjunto seguro de caracteres, como caracteres alfanuméricos, guiones y puntos, es la práctica de seguridad más eficaz para evitar *path traversal* y ataques de inyección en los nombres de archivo.

## Distinción entre mayúsculas y minúsculas

* Para evitar conflictos como la sobreescritura involuntaria de archivos o problemas de acceso, es importante que los nombres de archivo no distingan entre mayúsculas y minúsculas. Utilizar convenciones de nomenclatura coherentes y validar sin diferenciar entre mayúsculas y minúsculas puede ayudar a mitigar los riesgos.
* Omitir este comportamiento puede llevar a la sobreescritura de archivos o a accesos no autorizados, especialmente en entornos que dependen del tratamiento de archivos son sensibles a mayúsculas y minúsculas.
* Por defecto, los sistemas de ficheros de Windows no distinguen entre mayúsculas y minúsculas, lo que significa que `Image.png`, `IMAGE.PNG` e `image.png` se consideran idénticos.

## Limitaciones de caracteres específicos del sistema para nombrar archivos

* Los distintos sistemas de ficheros aplican restricciones específicas a determinados caracteres en nombres de archivo para preservar la integridad del sistema y evitar errores de parseo de rutas de archivo.
* Intentar guardar un archivo utilizando nombres reservados o caracteres restringidos puede provocar errores inesperados e interrupciones del servicio.

### Caracteres restringidos y nombres reservados en Windows

* En Windows, los caracteres especiales `<`, `>`, `:`, `"`, `/`, `\`, `|`, `?`, `*`, `\x00` no están permitidos en los nombres de archivo.
* Adicionalmente, ciertos nombres como `AUX`, `COM1`, `COM2`, `COM3`, `COM4`, `COM5`, `COM6`, `COM7`, `COM8`, `COM9`, `CON`, `LPT1`, `LPT2`, `LPT3`, `LPT4`, `LPT5`, `LPT6`, `LPT7`, `LPT8`, `LPT9`, `NUL` y `PRN` están reservados por el sistema para dispositivos o recursos del mismo y no pueden utilizarse como nombres de fichero o directorio.
* Por otra parte, los [caracteres de control ASCII][1] comprendidos entre 0 y 31 tampoco están permitidos en los nombres de archivo.

### Caracteres restringidos y nombres reservados en Linux

* En Linux, los caracteres restringidos en los nombres de archivo son `/`, utilizado como separador de directorios, y el carácter nulo `\x00`, también conocido como terminador nulo, que se utiliza en muchos sistemas, incluido Linux, como terminador de cadenas.
* Los nombres reservados en sistemas tipo UNIX son `.` y `..`.

## Evitar archivos ocultos y que terminen con un punto o un espacio

* Empezar un nombre de archivo con un punto (e.g., `.htaccess`) está ampliamente aceptado y se utiliza habitualmente para crear archivos ocultos, especialmente en sistemas tipo UNIX, donde el punto indica que el archivo debe quedar oculto de los listados de directorios estándar, e incluso ser omitido en los análisis de seguridad automatizados. Los atacantes pueden aprovechar estos archivos para eludir controles de seguridad, ocultar scripts maliciosos o modificar configuraciones del servidor.
* Los archivos que terminan con un punto o un espacio pueden aprovecharse de las incoherencias en la forma en que los distintos sistemas operativos y sistemas de ficheros gestionan los nombres de archivo, lo que provoca errores de acceso a los mismos, problemas de compatibilidad en el Explorador de Windows o problemas con otras aplicaciones, incluso cuando el sistema de ficheros subyacente los admite.

[1]: https://www.ascii-code.com/