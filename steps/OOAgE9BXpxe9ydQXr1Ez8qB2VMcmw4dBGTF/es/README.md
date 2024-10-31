# Arquitectura de software de 3-niveles tradicional

* La arquitectura de software de 3 niveles es un patrón de arquitectura de software cliente-servidor en el que la interfaz de usuario (`Nivel de Presentación`), la lógica de negocio (`Nivel de Aplicación`), el almacenamiento de datos y su correspondiente acceso (`Nivel de Datos`) se desarrollan y mantienen como módulos independientes, la mayoría de las veces en plataformas separadas.

![Arquitectura de software de 3-niveles][1]

* Además de las ventajas comunes del software modular con interfaces bien definidas, la arquitectura de 3 niveles está diseñada para permitir la actualización o sustitución independiente de cualquiera de sus tres niveles en respuesta a cambios en los requisitos o la tecnología.
* Cada nivel se ejecuta en su propia infraestructura y puede existir sin el nivel superior, pero necesita el nivel inferior para funcionar.
* Todas las comunicaciones se realizan a través del nivel de aplicación. El nivel de presentación y el nivel de datos no pueden comunicarse directamente entre sí.

## Nivel vs Capa

* Aunque los conceptos de _capa_ y _nivel_ suelen utilizarse indistintamente, existe una diferencia importante.
* Una _capa_ se refiere a una división funcional del software, un mecanismo de estructuración lógico de los elementos conceptuales que componen una aplicación.
* En cambio, un _nivel_ se refiere a una división del software que se ejecuta en una infraestructura separada de las demás divisiones, es decir, un mecanismo físico o virtual de estructuración de los elementos de hardware que componen la infraestructura del sistema.
* La aplicación de contactos de un teléfono, por ejemplo, es una aplicación de tres capas pero de un solo nivel, dado que las tres capas se ejecutan en el propio teléfono.

## Nivel de Presentación

* El nivel de presentación es la interfaz de usuario del software, donde el usuario final interactúa con la aplicación.
* Su propósito principal es mostrar información al usuario y recoger información.
* Este nivel superior puede ejecutarse en un navegador web, como puede ser una aplicación React, o también como una aplicación de escritorio, por ejemplo.

## Nivel de Aplicación

* El nivel de aplicación, también conocido como nivel lógico, de negocio o intermedio, es el corazón de la aplicación.
* En este nivel, la información recopilada en el nivel de presentación se procesa en función de un conjunto específico de reglas de negocio.
* Este nivel es el principal responsable de las comprobaciones de validación de entradas y de las reglas de seguridad.
* Puede tratarse simplemente un servidor web que aloje la aplicación y sus componentes, y una API REST que procese las peticiones.

## Nivel de Datos

* El nivel de datos, a veces denominado nivel de base de datos o nivel de acceso a datos, es donde se almacena y gestiona la información procesada por la aplicación.
* Incluye los mecanismos de persistencia de datos (servidores de bases de datos, archivos compartidos, etc.) y la capa de acceso a estos.
* El nivel de acceso a datos debe proporcionar una API al nivel de aplicación que ofrezca métodos de gestión de los datos almacenados sin exponer ni crear dependencias de los mecanismos de almacenamiento de datos.
* Puede tratarse de un sistema de gestión de bases de datos relacionales como PostgreSQL, MySQL, MariaDB, Oracle, DB2, Informix o Microsoft SQL Server, o de un servidor de bases de datos NoSQL como Cassandra, CouchDB o MongoDB o incluso cualquier almacenamiento en la nube como Amazon S3 o Google Cloud Storage.
* Evitar dependencias de los mecanismos de almacenamiento permite realizar actualizaciones o cambios sin que los clientes del nivel de aplicación se vean afectados por el cambio o ni siquiera sean conscientes de él.

## Pros y contras

### Beneficios

* **Escalabilidad mejorada**: cada nivel puede escalarse de forma independiente en función de las necesidades. Además, cada nivel funciona en su propio hardware dedicado o servidor virtual, lo que permite personalizar y optimizar los servicios sin afectar a los demás.
* **Mayor fiabilidad**: es menos probable que un fallo en un nivel afecte a la disponibilidad o el rendimiento de los demás.
* **Mejora de la seguridad**: dado que el nivel de presentación y el nivel de datos no se comunican directamente, un nivel de aplicación bien estructurado puede actuar como cortafuegos interno, protegiendo contra inyecciones SQL y otros tipos de exploits maliciosos.
* **Desarrollo más rápido**: dado que cada nivel puede ser desarrollado simultáneamente por equipos independientes, la organización puede acelerar el plazo de lanzamiento al mercado de la aplicación. Además, los programadores pueden utilizar los lenguajes y herramientas más actuales y eficaces para cada nivel.

### Inconvenientes

* La arquitectura de 3 niveles está obsoleta y también se suele denominar arquitectura monolítica. Se desarrolló antes de la adopción generalizada de la nube pública y las aplicaciones móviles y, en este sentido, ha tenido dificultades para adaptarse eficazmente a los entornos de nube.
* A medida que una aplicación crece en tamaño y complejidad, puede resultar complicado implementar actualizaciones frecuentes.
* Además, mantener al menos tres niveles separados de hardware y software puede generar ineficiencias para una empresa.

[1]: /static/images/learning/three-tier-software-architecture.png
