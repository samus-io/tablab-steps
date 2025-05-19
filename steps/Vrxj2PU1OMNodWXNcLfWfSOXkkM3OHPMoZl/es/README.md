# Mejores prácticas generales de seguridad al cargar archivos

* Una estrategia de defensa en profundidad (en inglés, `Defense-in-Depth (DiD)`) es esencial para conseguir una función de carga de archivos segura y adaptada a los requisitos específicos de una organización. Es necesario aplicar múltiples técnicas de seguridad, ya que no existe una medida universal para proteger completamente esta funcionalidad.

  > :warning: En la implementación de funcionalidades de carga de archivos, se debe garantizar que los archivos cargados superan con éxito todas las inspecciones de seguridad antes de realizar cualquier procesamiento. Si un archivo incumple alguna de las condiciones de seguridad, se recomienda descartar el archivo y la solicitud devolviendo un mensaje de error.

## Lista de control de las medidas de seguridad

* [ ] Garantizar que cualquier proceso de validación de datos de entrada general ya existente se aplique antes de los pasos de validación enumerados seguidamente.
* [ ] Establecer un límite de longitud de nombre de archivo y restringir los caracteres permitidos o utilizar un nombre de archivo generado por la aplicación al almacenar el archivo si es posible.
* [ ] Definir una lista de extensiones de archivo permitidas, garantizando que sólo se permiten las extensiones seguras y necesarias para la organización.
* [ ] Establecer un límite de tamaño de archivo.
* [ ] Validar el tipo de archivo basándose en sus datos reales, sin depender de la cabecera `Content-Type` ni del número mágico, ya que ambos pueden ser fácilmente manipulados.
* [ ] Examinar el archivo en busca de contenido malicioso ejecutándolo a través de un antivirus o sandbox para garantizar que no contiene elementos dañinos.
* [ ] Garantizar que la carga de archivos esté restringida a usuarios autorizados siempre que sea posible.
* [ ] Utilizar un servicio dedicado u otro servidor para el almacenamiento de archivos, si no es una opción, almacenarlos fuera de *webroot*.
* [ ] En caso de acceso público a los archivos, impedir que se pueda adivinar la ruta/URL (e.g., utilizando nombres de archivo aleatorios o un sistema de mapeo interno).
* [ ] Proteger la carga de archivos frente a ataques de `Cross-Site Request Forgery (CSRF)`.
* [ ] Comprobar que las librerías utilizadas están configuradas de forma segura y se actualizan periódicamente.

## Medidas de seguridad adoptadas

### Saneamiento de nombres de archivo

* Al almacenar archivos, la aplicación debe generar un nombre aleatorio en lugar de confiar en el nombre de archivo proporcionado por el usuario. Si el nombre original es necesario para la aplicación, se debe garantizar que no contenga caracteres especiales mediante validación de lista de permitidos para prevenir vulnerabilidades como *path traversal*.
* La mejor opción es sustituir el nombre de archivo proporcionado por el usuario por una cadena coherente y generada aleatoriamente por la propia aplicación web, por ejemplo, utilizando el formato UUID para evitar colisiones que podrían dar lugar a la sobreescritura de archivos existentes.
* Si la aplicación web necesita conservar el nombre de archivo original del usuario, entonces se recomienda implementar las siguientes medidas de seguridad:
  * Restringir los caracteres permitidos (e.g., permitir solo caracteres alfanuméricos), y excluir caracteres especiales de la lista (excepto `-`, `_` o `.`).
  * Establecer una longitud máxima (e.g., 200 caracteres).
  * Para evitar colisiones de nombres de archivo, se debe comprobar que el nombre del archivo no existe ya antes de guardarlo.
  * Evitar los nombres de archivo reservados en Windows (`CON`, `PRN`, `AUX`, `NUL`, `COM0-COM9`, `LPT0-LPT9`).

### Validación de extensiones de archivo

* La validación de extensiones de archivo debe garantizar que solo se permiten las extensiones de archivo necesarias para la aplicación y los requisitos de la organización, bloqueando todas las demás.
* Cuando la función de carga está diseñada para un único tipo de archivo (por ejemplo, únicamente PDF), la mejor práctica consiste en definir la extensión permitida en el lado del servidor, evitando depender de la entrada del usuario.
* Si no es factible controlar la extensión en el backend-side, un enfoque habitual es comparar la extensión con una lista de valores permitidos.
  * Para esta comprobación es esencial prestar especial atención, ya que se pueden emplear diversas técnicas para eludir una comparación deficiente (e.g., garantizar que el archivo solamente tiene una extensión mientras se bloquean los archivos con más de una extensión).
* Adicionalmente, los archivos sin extensiones generalmente no deben ser permitidos, ya que potencialmente podrían ser utilizados para cargar archivos de configuración del servidor web.

### Validación del contenido del archivo

* Los archivos cargados pueden incluir contenido malicioso, inapropiado o ilegal.
* El análisis del contenido de los archivos suele ser lento y complejo debido a la diversidad de tipos de archivos y a la posible presencia de malware incrustado. Por este motivo, la mejor solución es recurrir a *frameworks* o servicios de terceros.
* Adicionalmente, algunos cortafuegos de aplicaciones web (WAF) incluyen herramientas para comprobar si los archivos contienen malware cuando se suben a través de formularios web.

### Almacenamiento de archivos y permisos del sistema de ficheros

* Los archivos deben permanecer en memoria o en un área de almacenamiento temporal durante el procesamiento y trasladarse a una ubicación permanente únicamente cuando hayan completado y superado las comprobaciones de validación.
* Siempre que sea posible, los archivos deben almacenarse en un servicio dedicado o en un servidor separado para gestionar el almacenamiento de archivos con el fin de minimizar el impacto de posibles vulnerabilidades.
  * Si esto no es posible, se deben almacenar los archivos fuera de la raíz web para evitar el acceso directo a través de URL.
  * En los casos en los que los archivos deban ser accesibles públicamente, se puede utilizar un sistema de mapeo interno para asignar nombres de archivo identificativos en la aplicación.
* Los permisos en el almacenamiento de archivos deben ser limitados para controlar qué pueden hacer los usuarios con los archivos subidos, normalmente permitiendo solo acceso de lectura y escritura para archivos como imágenes o documentos, y bloqueando los permisos de ejecución.
  * En todos los casos, aunque especialmente cuando se requiera la ejecución, se aconseja escanear el archivo antes de almacenarlo como mejor práctica de seguridad para detectar y prevenir macros, scripts ocultos o cualquier forma de malware.

### Aplicación de autenticación y autorización

* Las funciones de carga de archivos deben protegerse con autenticación y autorización siempre que sea viable, garantizando que solamente los usuarios autorizados puedan acceder a las mismas.
* Si es necesario conceder permisos de lectura sobre los archivos cargados a los usuarios corporativos, se aconseja implementar controles de autorización para restringir el acceso únicamente a los usuarios autorizados básandose en su identidad y sesión, en lugar de simplemente en parámetros superficiales como las IP internas.

### Utilizar *frameworks* contrastados para gestionar el preprocesamiento de la carga de archivos

* Implementar un mecanismo seguro de carga de archivos es una tarea compleja que requiere prestar especial atención a numerosos detalles y posibles vulnerabilidades, lo que requiere una cantidad significativa de tiempo. Al utilizar un *framework* consolidado, la aplicación puede beneficiarse de funciones de seguridad completas y actualizadas, y garantizar que esta se adhiere a las mejores prácticas.
* Estos *frameworks* o librerías pueden ofrecen una gran variedad de funciones de validación integradas, como la limpieza de nombres de archivo, la comprobación de tipos de archivo o la validación de contenido, diseñadas para responder a una amplia gama de requisitos de seguridad.
* Aunque la idea de construir manualmente mecanismos de validación puede ser tentadora, aprovechar los *frameworks* o las librerías establecidas suele representar un mejor enfoque.

## Test para consolidar :rocket:

* Completa el cuestionario eligiendo la respuesta correcta para cada pregunta.
  @@ExerciseBox@@
