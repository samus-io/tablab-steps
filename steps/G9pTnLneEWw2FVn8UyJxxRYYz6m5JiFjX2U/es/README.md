# Introducción a Software Testing

* El principal objetivo del *software testing* es evaluar la funcionalidad, el rendimiento y la estabilidad del software. Este proceso implica ejecutar el software en diversas condiciones y casos de prueba o tests para detectar problemas, analizar el rendimiento y garantizar que se cumplen los requisitos de funcionalidad previstos.
* El software testing o pruebas de software se lleva a cabo en diferentes etapas del ciclo de vida del desarrollo, con objetivos diversos.

## Objetivos principales

* **Detección de errores**.
  * Ejecutar tests es la forma más productiva de identificar si una adición al código base no está causando comportamientos erróneos en otras funcionalidades.
  * Una vez detectado un error, las tests ayudan a aislarlo del resto del código, facilitando al desarrollador la localización y corrección del problema.
* **Confianza y eficacia para el desarrollador**.
  * Los tests proporcionan a los desarrolladores confianza y un conocimiento más sólido de su código, lo que les anima a realizar cambios sin temor a romper las funcionalidades existentes.
  * Cuando las funcionalidades se rompen, los tests reducen el tiempo y el esfuerzo que el desarrollador dedica a la depuración. En este sentido, las suites de testing automatizadas también ahorran tiempo al desarrollador y al equipo en comparación con la ejecución de pruebas manuales para garantizar que todo sigue funcionando.
* **Quality Assurance (QA) y User Acceptance**.
  * Las pruebas centradas en el usuario permiten al equipo identificar y abordar problemas de usabilidad, satisfacción del usuario y comportamiento.
  * Las pruebas de aceptación del usuario aportan una perspectiva única y valiosos conocimientos sobre las expectativas, hábitos y requisitos del usuario, contribuyendo así a una experiencia satisfactoria.

## Clasificación de tests

### Por Enfoque

#### `Black-Box Testing`

* Evalúa el comportamiento externo del software sin conocer su código y estructura interna.
* Se centra en la funcionalidad del software y la experiencia del usuario y no requiere formación técnica.

#### `White-Box Testing`

* Examina el código, la lógica y la arquitectura interna del software. Los *testers* tienen acceso al código y a la estructura, lo que les permite evaluar la calidad del código y solucionar posibles problemas, por lo que necesitan comprender el funcionamiento interno de la entidad probada.

### Por objetivo

#### `Tests funcionales`

* Principalmente evalúan si el software funciona según lo previsto teniendo en cuenta los requisitos especificados, comprobando que cada funcionalidad realiza su tarea designada de forma eficiente.
* Su objetivo es mejorar la calidad del código y la satisfacción del usuario mediante la validación de las funcionalidades própiamente, la garantía de calidad del código y la coherencia del comportamiento y los resultados de la aplicación.

#### `Tests no funcionales`

* Se centran en aspectos del software que van más allá de su funcionalidad básica; evalúan el rendimiento, la seguridad, la usabilidad, la escalabilidad y otras características no funcionales.
* Ofrecen información sobre posibles cuellos de botella, vulnerabilidades o áreas de optimización.

### Por método de ejecución

#### `Tests manuales`

* Los ejecuta un probador humano que interactúa con la aplicación como lo haría un usuario final. Proporcionan una perspectiva humana y mucha flexibilidad, especialmente en la satisfacción del usuario.

#### `Tests automatizados`

* La mayoría se centran en garantizar la calidad del código. A través de la repetición, es posible verificar que la funcionalidad permanece operativa y ahorrar tiempo que de otro modo se perdería ejecutando manualmente estas pruebas.
* Pueden integrarse en los procesos de release para garantizar una integración fluida del código a lo largo de todo el ciclo de desarrollo.

### Por ámbito

#### `Tests unitarios`

* Ocurren en el nivel más bajo del testing, donde una sola función, método o servicio (unidad) se puede probar de forma aislada para verificar que las partes individuales funcionan como se espera.

#### `Tests de integración`

* Tienen como objetivo asegurarse de que los componentes individuales se comportan como se espera cuando trabajan juntos. Prueban la funcionalidad de estas unidades de forma cohesiva para garantizar interacciones perfectas entre módulos.

#### `Tests de extremo a extremo/sistema`

* Tienen el alcance más amplio de las tres; se diferencian de las pruebas de integración en que prueban el sistema **como un todo**, incluyendo también aspectos *no funcionales*. En las pruebas E2E (End-to-End), esto se hace desde la perspectiva del usuario.

#### `Tests de humo`

* Sirven como rápidas "comprobaciones de humo" preliminares para determinar si las principales funcionalidades del software están intactas. Aunque menos fiables, su rápido tiempo de ejecución  significa una retroalimentación más frecuente, ya que los desarrolladores pueden utilizarlas como rápidas comprobaciones de operabilidad sin tener que esperar a suites de pruebas más lentas y robustas.
  > "Conectas una placa nueva y la enciendes. Si ves que sale humo de la placa, apágala y no tendrás que hacer más pruebas" de Kaner, Bach y Pettichord. *Lessons Learned in Software Testing*

## Consideraciones

* La mejor configuración de tests siempre será diferente según el proyecto y, en este sentido, equilibrar el tiempo dedicado a escribir (y reescribir) los mismos con la seguridad y confianza que brindan es a menudo el desafío más difícil para el *tester*.
