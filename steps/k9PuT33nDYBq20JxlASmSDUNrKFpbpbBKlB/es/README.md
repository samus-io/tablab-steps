# Arquitectura de seguridad de 3-niveles tradicional

* La arquitectura de seguridad de 3 niveles es un patrón de arquitectura que define un modelo compuesto por tres niveles denominados `nivel desmilitarizado`, `nivel de confianza` y `nivel privado`, en el que para cada uno de estos niveles de seguridad se establecen diferentes medidas de seguridad, acceso y políticas de actualización de recursos.

![Arquitectura de seguridad de 3-niveles][1]

* Los niveles están separados por cortafuegos y el tráfico entre ellos es inspeccionado por sistemas IDS/IPS.
  * Cada nivel tiene sus propios segmentos de red.
* En una arquitectura cerrada, todas las comunicaciones iniciadas en un nivel específico pueden llegar a un activo perteneciente a cualquier nivel superior, pero no al revés; las comunicaciones procedentes de un nivel sólo pueden llegar a un activo perteneciente al nivel inmediatamente inferior.
* La arquitectura de 3 niveles ha sido habitual en las infraestructuras *on-premises* tradicionales.

## Nivel desmilitarizado

* El nivel desmilitarizado es donde se alojan todos los servidores de acceso público y se ofrecen servicios a usuarios externos.
* Cuenta con medidas y políticas de seguridad muy estrictas, tales como procedimientos de actualización diarios o semanales.
* Tradicionalmente, el nivel desmilitarizado, en infraestructuras *on-premises*, suele contener una o varias redes DMZ.

  > :older_man: Una red DMZ, también conocida como red perimetral, es esencialmente una red física o lógica que contiene y presenta los servicios externos de una organización a una red mayor y normalmente no fiable, como Internet.

## Nivel de confianza

* El nivel de confianza, a veces también llamado nivel lógico o de transacción, incluye aquellos servicios que los servidores públicos utilizan para ofrecer las prestaciones específicas a los usuarios externos.
* Contiene la lógica de negocio real, así como enlaces a sistemas internos para capacidades de procesamiento adicionales.
* En este nivel se aplican la mayoría de las medidas de seguridad relacionadas con el tratamiento de los datos de entrada.
* Tradicionalmente, el nivel de confianza, en infraestructuras *on-premises*, contiene una o varias redes de transacción.

  > :older_man: Una red de transacción, también llamada red intermedia o gris, no es más que una red física o lógica que se sitúa entre las redes DMZ y las redes internas más profundas.

## Nivel privado

* El nivel privado se compone de los datos esenciales de los que depende la organización.
* Aquí es donde deben ubicarse generalmente los datos más críticos y sensibles de una organización.
  * No sólo en lo que respecta a los servidores de bases de datos, sino también a otros servicios sensibles como los servicios de dominio de Active Directory (AD DS) o el almacenamiento conectado en red (NAS).
* Tradicionalmente, en infraestructuras *on-premises*, contiene múltiples redes internas.

  > :older_man: Una red interna, a menudo denominada simplemente LAN, es una red privada y propietaria a la que sólo pueden acceder los empleados de una empresa concreta y en la que se ofrecen la mayoría de los servicios empresariales internos.

## Consideraciones adicionales de seguridad

* Al transicionar a un nivel inferior, el protocolo de comunicación debería ser diferente del utilizado para comunicarse desde el nivel superior al nivel actual.
* Es aconsejable emplear varios proveedores y soluciones de seguridad para analizar el tráfico entre niveles.
* Las reglas de seguridad deben aplicarse lo más cerca al origen posible.

[1]: /static/images/three-tier-secure-architecture.png
