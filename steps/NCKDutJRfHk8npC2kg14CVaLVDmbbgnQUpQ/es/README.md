# Saneamiento de nombres de archivo

* El saneamiento de nombres de archivo es un proceso esencial destinado a garantizar que los nombres de archivo sean seguros y compatibles con el sistema en el que se van a utilizar.
* Consiste en validar y potencialmente modificar los nombres originales de los archivos recibidos para prevenir amenazas de seguridad o fallos operativos que puedan comprometer la integridad del sistema.

## Lista de control de las medidas de seguridad

* Siempre que sea posible, se deben utilizar nombres de archivo únicos y aleatorios al almacenar los ficheros (e.g., adoptando UUID). Si las restricciones de lógica de la organización impiden este enfoque, entonces se recomienda:

  * [ ] Establecer un límite de longitud del nombre de archivo.
  * [ ] Limitar los caracteres permitidos (e.g., únicamente considerar `A-Z`, `a-z`, `0-9`, `-`, y `.` como caracteres válidos).
  * [ ] Tratar los nombres de archivo sin distinguir mayúsculas de minúsculas.
  * [ ] Restringir los nombres reservados en Windows.
  * [ ] Evitar los archivos ocultos y los puntos y espacios finales (e.g., `.htaccess`).

## Generación de nombres de archivo únicos y aleatorios

* La creación de nombres de archivo únicos y aleatorios al almacenar los archivos cargados evita las colisiones de nombres de archivo, mitiga los ataques path traversal, oculta los nombres de archivo originales que podrían exponer detalles sensibles, mejora la seguridad contra la ejecución de archivos maliciosos reduciendo el riesgo de que un atacante pueda localizar y ejecutar dichos archivos, y evita los ataques de enumeración de archivos.
* Una forma fiable de crear nombres de archivo impredecibles y no sobrescribibles es utilizar `Universally Unique Identifier (UUID)` o `Globally Unique Identifier (GUID)`.
* Este enfoque es especialmente útil en situaciones en las que no es necesario conservar los nombres de archivo originales proporcionados por los usuarios.

## Límites de longitud de los nombres de archivo

* Los distintos sistemas de archivos imponen límites variables a la longitud de los nombres de archivo, lo que puede afectar a la compatibilidad y la seguridad. Por ejemplo, el sistema de archivos `MS-DOS FAT` establece el formato de nombre de archivo `8.3`, que solo admite 8 caracteres para el nombre y 3 para la extensión, con el fin de mantener la compatibilidad con el software heredado.
* Los sistemas de archivos modernos como `NTFS` pueden soportar nombres de archivo más largos, aunque Windows ha impuesto tradicionalmente un límite `MAX_PATH` de 260 caracteres. Superar este límite puede provocar errores de truncamiento o de acceso a archivos, aunque las nuevas versiones de Windows permiten eliminar este límite mediante los ajustes de configuración adecuados.
* Tener en cuenta los límites de longitud de los nombres de archivo es esencial para evitar problemas como errores de acceso a los archivos, truncamientos o riesgos de seguridad debidos a una mala interpretación del sistema de archivos.
