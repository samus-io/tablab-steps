# ¿Qué es el Path Traversal?

* El `Path Traversal`, también conocido como `Directory Traversal`, es una vulnerabilidad crítica del lado del servidor que permite a un adversario acceder a archivos arbitrarios en el servidor.
* Esta vulnerabilidad surge de un manejo inseguro de las entradas de usuario utilizadas para referenciar rutas de archivos almacenados en el servidor. Al manipular estas entradas, un adversario puede incluir archivos no previstos por la aplicación.
* Es común que las aplicaciones web utilicen parámetros para referenciar archivos como imágenes, y posteriormente incluir dichas imágenes en la página web. Sin embargo, si la aplicación web no valida correctamente estas entradas, podría ser explotada para acceder a archivos sensibles.

## Impacto del Path Traversal

* **Lectura de archivos del sistema**: Como `/etc/passwd` en Linux o archivos de configuración críticos en Windows, proporcionando una lista de usuarios locales del sistema o información sensible de configuración.
* **Lectura de código fuente**: Permitiendo al adversario entender y potencialmente explotar la lógica de la aplicación web.
* **Ejecución remota de comandos**: En circunstancias específicas, dependiendo de la configuración del servidor y otros factores de seguridad.
* **Enumeración de puertos internos y servicios**: Revelando información sobre servicios internos y posiblemente infraestructura no expuesta directamente a Internet.
* **Detección de versiones del servidor y del kernel de Linux/Windows**: Facilitando la identificación de sistemas vulnerables o desactualizados.
