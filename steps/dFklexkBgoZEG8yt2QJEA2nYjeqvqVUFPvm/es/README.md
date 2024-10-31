# Introducción a la carga insegura de archivos

* La carga insegura de archivos hace referencia a una vulnerabilidad de seguridad que se produce cuando una aplicación permite a los usuarios cargar archivos sin verificar correctamente sus propiedades, como el nombre, el tipo, el contenido o el tamaño del archivo, lo que supone un riesgo potencial para el sistema.
* Cuando estas comprobaciones no se aplican correctamente, una simple función de carga de archivos podría ser explotada para cargar archivos maliciosos, incluyendo scripts del lado del servidor que pueden permitir a los atacantes ejecutar código arbitrario en el propio servidor o incluso en los dispositivos de los usuarios o empleados cuando estos acceden y abren estos archivos.

## Qué se podría conseguir con una subida de archivos insegura

* Los usuarios malintencionados pueden cargar malware que puede ejecutarse en el servidor o en los dispositivos de los usuarios, dando lugar al robo de datos, acceso no autorizado o compromiso total del sistema.
* Los archivos subidos ejecutados o interpretados por el servidor pueden permitir la ejecución de código arbitrario, dando a los atacantes el control sobre el servidor.
* Los archivos cargados con scripts maliciosos pueden ser servidos a los usuarios durante la interacción con la aplicación, dando lugar a ataques XSS.
* No sanear correctamente los nombres de archivo puede exponer el sistema a vulnerabilidades de inyección de comandos o SQL.
* Las cargas de archivos de gran tamaño o muy recurrentes pueden saturar los recursos del servidor, provocando una degradación del servicio o la denegación del mismo.
* La información sensible incrustada en los archivos cargados podría ser exfiltrada por usuarios maliciosos.
* Los archivos cargados pueden utilizarse para alterar el contenido de un sitio web, lo que puede provocar desfiguraciones y daños a la reputación.

### Ejecución remota de código

* Los archivos cargados incorrectamente validados pueden ser ejecutados directamente por el servidor, permitiendo a los atacantes ejecutar código arbitrario y potencialmente obtener el control total del sistema.
* Otro método para lograr la ejecución de código es a través de una vulnerabilidad de `Local File Inclusion (LFI)`. Si la aplicación web permite a los usuarios subir archivos a un directorio público, un usuario malicioso puede subir un archivo aparentemente inofensivo (como una imagen) que contenga código incrustado. El atacante puede entonces explotar la LFI para ejecutar el código dentro del archivo subido.
  > :older_man: `Local File Inclusion (LFI)` es una vulnerabilidad web que se produce cuando una aplicación web permite a los usuarios incluir archivos del sistema de ficheros del servidor. Cuando un archivo de este tipo se incluye en una página web, su contenido no sólo se lee, sino que también se interpreta como código.
  * Por ejemplo, los pasos podrían ser:
    1. El atacante carga un archivo llamado `image.png` con código incrustado en el directorio público de subidas (e.g., `/uploads`).
    1. Seguidamente, el atacante explota la vulnerabilidad LFI navegando a una URL como `https://domain.tbl/index?page=uploads/image.png`.
    1. El servidor incluye y ejecuta el archivo `image.png`, procesando el código incrustado.

### Cross-Site Scripting (XSS)

* Los archivos subidos pueden contener código JavaScript que se ejecuta en el contexto del navegador del usuario. Esto es especialmente peligroso con tipos de archivos como HTML, SVG o, en algunos casos, imágenes que puedan tener HTML incrustado.
* Los archivos que contienen scripts maliciosos incrustados que ejecutan código JavaScript en los navegadores de los usuarios pueden robar las sesiones del usuario, acceder a cualquier dato al que pueda acceder el usuario, realizar keylogging, desfigurar virtualmente el sitio web, redirigir a los usuarios a sitios web maliciosos o incluso tomar el control del navegador o instalar malware aprovechando vulnerabilidades del propio navegador web.

### Inyección SQL (SQLi)

* Si el nombre del archivo se utiliza en las consultas SQL sin un saneamiento adecuado, puede introducir vulnerabilidades de inyección SQL.
* Considerando que una aplicación almacena nombres de archivos en una base de datos en la cual un atacante puede cargar un archivo con el nombre `'); DROP TABLE users;--.jpg`. Si la aplicación construye consultas SQL de forma insegura, este nombre de archivo puede terminar la consulta existente y ejecutar el comando malicioso, eliminando la tabla users.

### Denegación de Servicio (DoS)

* Los atacantes pueden cargar archivos excesivamente grandes o un gran número de archivos en un corto periodo de tiempo, agotando recursos del servidor como la CPU, la memoria y el espacio en disco, lo que puede provocar la indisponibilidad del servicio.

### Path traversal

* Los nombres de archivo manipulados para incluir secuencias como `../`, tal como `../index.html`, pueden permitir a usuarios malintencionados acceder a archivos fuera del directorio de subida previsto o bien sobrescribir otros archivos.
* En este sentido, algunos nombres de archivo pueden ser manipulados para sobrescribir archivos críticos en el servidor, provocando la pérdida de datos o comprometiendo el sistema.

## Componentes involucrados en la carga de archivos que pueden utilizarse como vectores de ataque

### Nombre de archivo

* Los atacantes pueden manipular el nombre del archivo para incluir secuencias de path traversal (e.g., `../../`) para acceder a archivos sensibles en el servidor.
* Se puede utilizar el path traversal para guardar el archivo en una ruta diferente a la esperada.
  * Un atacante podría cargar un archivo con un nombre cuidadosamente diseñado que coincida con el nombre de un archivo crítico en el servidor, sobrescribiéndolo.
* Cuando se utilizan nombres de archivo en comandos del sistema sin el saneamiento adecuado, puede permiter a los usuarios maliciosos inyectar comandos adicionales.

### Extensión de archivo

* Permitir la carga de **archivos ejecutables** (e.g., `.exe`, `.elf`) puede conducir a la ejecución directa de malware en el servidor o en los dispositivos cliente.
* **Los archivos de código fuente** (e.g., `.js`, `.php`, `.py`) pueden ser interpretados por el servidor cuando se cargan en el mismo y dar lugar a la ejecución de código.
* **Los archivos comprimidos** (e.g., `.zip`, `.rar`, `.tar`) pueden contener múltiples archivos maliciosos o exploits dirigidos a las herramientas de descompresión.

### Contenido del archivo

* Archivos como PDF o documentos de Office pueden contener **scripts o macros incrustadas** que realizan acciones maliciosas al ser abiertos por un usuario, como la descarga de malware o el robo de datos.
* **Los archivos binarios** (e.g., ejecutables, DLLs) pueden explotar vulnerabilidades en el software de procesamiento de archivos, potencialmente conduciendo a la ejecución remota de código.
* Algunos archivos pueden contener **cargas útiles ofuscadas** dentro de documentos aparentemente inofensivos mediante técnicas de ofuscación, lo que dificulta su detección durante el escaneado.
* Los archivos cargados pueden utilizarse para **phishing**, camuflados como documentos legítimos pero diseñados para engañar a los usuarios para que revelen información sensible, como credenciales de inicio de sesión, a través de contenidos engañosos.
* **Los archivos multimedia** (e.g., imágenes, vídeos) pueden ser manipulados para explotar vulnerabilidades en las bibliotecas de procesamiento multimedia, permitiendo a los atacantes ejecutar código o causar una denegación de servicio (DoS) cuando estos archivos son visualizados o procesados.

### Tamaño del archivo

* Los archivos de gran tamaño pueden provocar el **agotamiento de recursos**, como la RAM y la CPU, degradando el rendimiento y la disponibilidad, lo que los atacantes pueden aprovechar subiendo repetidamente archivos de gran tamaño.
* Las cargas de archivos de gran tamaño pueden consumir un considerable **ancho de banda**, afectando al rendimiento de la red para otros usuarios.
* La gestión de cargas grandes o numerosas complica la **gestión del almacenamiento**, lo que requiere una supervisión y un mantenimiento diligentes.
Los archivos de gran tamaño también pueden hacer que las **copias de seguridad** sean más complejas y aumentar los tiempos de recuperación en situaciones de catástrofe.

## Consideraciones de seguridad

### Autenticación en la carga de archivos

* Al gestionar las funcionalidades carga de archivos, siempre que sea posible, se recomienda asegurarse de que estén protegidos con sólidos mecanismos de autenticación y autorización.
* Es esencial validar a los usuarios antes de concederles acceso a un servicio de carga de archivos, garantizar que sólo puedan acceder al servicio los usuarios autenticados para gestionar las cargas y, si es necesario, aplicar controles adecuados para restringir el acceso a los archivos a los usuarios autorizados.
* Un usuario malicioso puede abusar de la falta de autenticación para explotar diferentes vulnerabilidades, como DoS o divulgación de información, o aumentar el riesgo de una vulnerabilidad existente.

### Almacenamiento de archivos y permisos del sistema de ficheros

* Una gestión adecuada del almacenamiento de los archivos cargados puede reducir significativamente el riesgo de divulgación de información y la explotación de vulnerabilidades en una aplicación web.
* Para mejorar la seguridad, se deben tener en cuenta las siguientes buenas prácticas a la hora de decidir dónde y cómo almacenar los archivos subidos por los usuarios:
  * Siempre que sea posible, se deben almacenar los archivos cargados en un servicio exclusivo o servidor separado de la aplicación web principal. De esta forma se reduce el riesgo de que un atacante acceda a datos confidenciales o aproveche otras vulnerabilidades del servidor de aplicaciones.
  * Si no es posible almacenar los archivos en un servicio o servidor independiente, es necesario asegurarse de que los archivos cargados se almacenan fuera del directorio webroot. Esto impide el acceso directo a los archivos a través del servidor web.
  * Si la aplicación necesita mostrar archivos subidos a los usuarios, hay que evitar permitir el acceso directo a estos archivos a través del servidor web. En su lugar, se debe implementar un gestor del lado del servidor que sirva los archivos. Este gestor puede asignar internamente los archivos a un ID único, que luego se utiliza para acceder al archivo. Este enfoque proporciona una capa adicional de seguridad al evitar que los atacantes accedan directamente a las rutas de los archivos.

### Límites de carga y descarga

* Establecer límites de carga y descarga ayuda a evitar que el servidor se vea desbordado por transferencias de datos excesivas, garantizando un rendimiento estable del servicio.
* Los atacantes o usuarios malintencionados podrían aprovechar las cargas o descargas sin restricciones para inundar el servidor de datos, provocando ralentizaciones o caídas.
* Otro tipo de vulnerabilidad que puede ocurrir sin los límites adecuados es una condición de carrera, que podría explotar debilidades basadas en el tiempo o vulnerabilidades que existieran dentro de un marco de tiempo específico.

### Eliminación de metadatos

* Los metadatos pueden **revelar involuntariamente información personal** como nombres de usuario, direcciones de correo electrónico o detalles de dispositivos.
* Las imágenes y los vídeos pueden llevar incrustados **datos de geolocalización**, que pueden revelar la ubicación física del usuario o de la organización.
