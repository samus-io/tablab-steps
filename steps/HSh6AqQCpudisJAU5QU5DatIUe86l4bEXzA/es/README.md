# Entorno de Ejecución (RTE)

* En el contexto del desarrollo de software, un entorno se refiere a un conjunto de sistemas dedicados a implementar una de las capas del proceso de lanzamiento de una aplicación.

## Tipos de RTE

* Las definiciones y distinciones precisas entre estos entornos pueden variar. La fase de Pruebas podría ser vista como parte del Desarrollo, mientras que las Pruebas de Aceptación podrían ubicarse dentro de la fase de Pruebas o existir de manera independiente, etc.

### Entorno de Desarrollo

* El `Entorno de Desarrollo` representa la etapa inicial en el desarrollo de software. En este espacio se lleva a cabo la codificación y las tareas relacionadas con la creación de software, abarcando desde las primeras líneas de código hasta las más nuevas.
* Como su nombre indica, es el lugar donde ocurre el desarrollo de software.
* Un componente esencial del Entorno de Desarrollo es el `Entorno de Desarrollo Integrado (IDE)`. Este paquete de software con sus amplias funcionalidades se utiliza para crear, construir, probar y depurar el código. Los desarrolladores de software suelen utilizarlo en sus estaciones de trabajo. Entre los IDE más conocidos se encuentran Microsoft Visual Studio, Eclipse, NetBeans y muchos otros.

### Entorno de Control de Calidad/Testing

* El `Entorno de Control de Calidad (QC) o de Testing` proporciona un espacio para que los ingenieros de testing evalúen el código nuevo y modificado, ya sea a través de medios automatizados o manuales.
* En este entorno, los testeadores se asegurarán de que la incorporación de código nuevo no afecte inadvertidamente a la funcionalidad existente.
* Además, son capaces de mantener la calidad del código identificando y revisando correcciones de errores.
* El enfoque principal aquí se centra en probar componentes individuales en lugar de toda la aplicación, garantizando la compatibilidad entre el código existente y el nuevo. Esta es la etapa donde generalmente se realizan las **pruebas unitarias**.
* Diferentes tipos de pruebas pueden requerir diferentes entornos de prueba, y algunos o todos estos entornos pueden ser virtualizados para agilizar los tests y habilitar su ejecución en paralelo.

### Entorno de Garantía de Calidad/Preproducción

* El `Entorno de Garantía de Calidad (QA) o de Preproducción` está diseñado para reflejar fielmente el entorno de producción, esforzándose por replicar las condiciones del mundo real para garantizar el funcionamiento correcto del software en este.
* El objetivo principal aquí es realizar pruebas exhaustivas de la aplicación o software en su totalidad, en un entorno que simula de manera más realista el entorno que utilizarán los usuarios en producción.
* En este entorno, se deben realizar pruebas para detectar y mitigar problemas potenciales que puedan surgir en producción, con un enfoque en minimizar cualquier impacto negativo en los usuarios. Los tipos de pruebas en este entorno pueden incluir pruebas **funcionales** y **pruebas de humo (smoke testing)**.
* Otra aplicación crucial del Entorno de Preproducción es la **prueba de rendimiento (performance testing)**, especialmente la **prueba de carga (load testing)**, ya que a menudo es sensible al entorno.
* Dependiendo de factores como requisitos regulatorios (por ejemplo, GDPR) y la capacidad de la organización para anonimizar datos, el Entorno de Preproducción puede incluir conjuntos de datos anonimizados o completos de producción para simular de cerca el entorno de producción real.
* El acceso al Entorno de Preproducción generalmente está restringido a un grupo selecto de personas. Solo aquellas con direcciones de correo electrónico autorizadas, direcciones IP especificadas y el equipo de desarrollo tienen permiso para acceder a la aplicación dentro de este entorno.
* Una práctica recomendada, aunque no obligatoria, implica aislar los Entornos de Preproducción y Producción en clústeres separados y **Redes Privadas Virtuales (VPCs)** para minimizar la posibilidad de complicaciones en el entorno de producción derivadas del Entorno de Preproducción.

#### Creación de un Entorno de Preproducción

* Crear un Entorno de Preproducción desde cero.
* Clonar el Entorno de Producción y crear un Entorno de Preproducción a partir de él.

#### Diferenciación entre Entornos de Testing y de Preproducción

* La distinción principal entre un Entorno de Preproducción y un Entorno de Testing radica en el grado de similitud con el entorno de producción.
* En un Entorno de Preproducción, todos los componentes se actualizan a las últimas versiones, replicando fielmente el entorno en produccion (a excepción de los cambios más recientes provenientes del Entorno de Desarrollo). Este enfoque garantiza que los nuevos cambios no interrumpan inesperadamente los elementos existentes al implementarlos en el entorno en vivo.
* En un Entorno de Testing, no es obligatorio seguir estrictamente esta coincidencia con el entorno en vivo. En su lugar, el enfoque se centra en probar cambios de código específicos, trabajando con suposiciones sobre el comportamiento del sistema. La ventaja de un Entorno de Testing es que permite pruebas más rápidas sin la necesidad de replicar completamente el entorno en vivo, como se hace en un Entorno de Preproducción.

### Entorno de Producción/En Vivo

* El `Entorno de Producción o En Vivo` es donde se produce el software y se ejecuta en un servidor de producción. Es el punto en el que el software se pone oficialmente a disposición de los usuarios reales.
* Al implementar una nueva versión en el Entorno de Producción, generalmente se realiza en etapas, liberándola inicialmente a una fracción de usuarios para evaluar su rendimiento, identificar y corregir posibles errores adicionales antes de implementarla para el resto de la base de usuarios.
