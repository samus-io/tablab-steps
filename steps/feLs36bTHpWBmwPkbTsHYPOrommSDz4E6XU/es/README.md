# Integración de arquitecturas de software y seguridad de 3-niveles tradicionales

* A continuación se muestra una representación gráfica de cómo integrar la arquitectura de software de 3 niveles tradicional (niveles de Presentación, Aplicación y Datos) con la arquitectura de seguridad de 3 niveles tradicional (niveles Desmilitarizado, Confianza y Privado).

![Integración de arquitecturas de software y seguridad de 3-niveles][1]

* Es importante destacar que los servidores web no tocan directamente los servidores de bases de datos.
  * Las capas de lógica de negocio deben descargarse de los servidores web a servidores dedicados al procesamiento de datos y es aquí donde se produce el procesamiento de datos real, incluyendo la adición de información a la base de datos, la recuperación y manipulación de datos y la ejecución de tareas y trabajos programados.
  * Estas capas de lógica de negocio también deben asumir la responsabilidad de implementar la mayoría de las medidas de seguridad de los datos, garantizando la integridad de los mismos.
  * Los servidores web interactuan con los servidores de procesamiento de datos a través de un protocolo menos benigno, como HTTP o HTTPS, y estas aplicaciones son las que se codifican para realizar llamadas SQL a los servidores de bases de datos internos.
  * Estos servidores backend del Nivel de Confianza nunca serán expuestos directamente a Internet.
* Este enfoque de 3 niveles se observa en las infraestructuras on-premises tradicionales y todavía puede considerarse hoy en día para aplicaciones web sencillas o para el desarrollo unificado de aplicaciones on-premises y en la nube.

## Proceso de integración

### El Nivel de Presentación se ubica en el Nivel Desmilitarizado

* El Nivel de Presentación, que contiene sólo la lógica de visualización de la aplicación y otros servicios para el soporte de visual, debe colocarse en el Nivel Desmilitarizado.

### El Nivel de Aplicación se divide entre el Nivel Desmilitarizado y el Nivel de Confianza

* Los componentes del Nivel de Aplicación necesarios para satisfacer las peticiones de la interfaz de usuario deben colocarse en el Nivel Desmilitarizado.
* Los servidores de aplicaciones que contienen toda la lógica de negocio deben colocarse en el Nivel de Confianza, haciéndolos accesibles a través de comunicaciones designadas desde el Nivel Desmilitarizado.

### El Nivel de Datos se ubica en el Nivel Privado

* El Nivel Privado debe contener los servidores de bases de datos, que idealmente sólo serán consultados por servidores en el Nivel de Confianza con acceso específico permitido y limitado.

### Desafíos

* Si no se diseña correctamente, es fácil acabar creando un nivel intermedio que se limita a realizar operaciones CRUD en la base de datos, lo que añade latencia adicional sin proporcionar ningún valor añadido.
* Al dividir una aplicación en distintas capas o servicios, existe el riesgo potencial de que la comunicación entre servicios provoque una latencia inaceptable o congestione la red.

### Buenas prácticas

* Utilizar el autoescalado para gestionar los cambios en la carga de trabajo.
* Considerar el uso de mensajería asíncrona para desacoplar los niveles.
* Instalar un cortafuegos de aplicaciones web (WAF) para analizar el tráfico entrante de Internet.
* Restringir el acceso al Nivel de Datos permitiendo solicitudes sólo desde el Nivel de Confianza.

## Pros y contras

### Beneficios

* Menor curva de aprendizaje para los desarrolladores.
* Abierto a entornos heterogéneos (Windows/Linux).
* Portabilidad entre la nube e infraestructuras on-premises, y entre plataformas en la nube.
* Proteger las capas de lógica de negocio de la exposición directa a Internet puede reducir la necesidad de actualizaciones frecuentes de su pila tecnológica, permitiendo intervalos más largos para abordar vulnerabilidades identificadas.

### Inconvenientes

* La frecuencia de actualización es baja.
* Puede aumentar la gestión de la seguridad de la red en un sistema de gran tamaño.
* El diseño monolítico restringe el despliegue independiente de funciones individuales y específicas.

## Consideraciones adicionales de seguridad

* Los servidores públicos nunca deben tener acceso directo a las redes o recursos internos.
  * Se puede considerar la posibilidad de añadir un controlador de dominio de sólo lectura (RODC) en el Nivel de Confianza para gestionar las autenticaciones de usuarios externos si es necesario.
* Los usuarios nunca deben tocar directamente los servidores web que sirven contenido.
  * Todas las solicitudes entrantes de Internet deben atravesar un proxy inverso para llegar a los distintos servicios web.
  * Estos proxies HTTP inversos deben mantenerse en sus propias subredes, separadas de las subredes de otros servidores web.
* Siempre que sea posible, los recursos deben limitarse a un único segmento de red para evitar que sean accesibles en **puertos de servicio** a través de múltiples interfaces de red.

[1]: /static/images/learning/three-tier-software-and-secure-architecture-integration.png
