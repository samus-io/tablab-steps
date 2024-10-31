# Introducción a la validación de datos de entrada

* La `validación de datos de entrada` es el proceso de asegurar que entradas de datos no confiables se ajustan a unos criterios predefinidos antes de ser procesados o almacenados.
* Consiste en examinar y validar las entradas de datos no confiables para garantizar que cumplen los requisitos y las restricciones especificadas.
* Se puede comparar la validación de datos de entrada con un portero de la puerta de un edificio, ya que actúa filtrando los datos no válidos o maliciosos para salvaguardar la integridad de la aplicación y evitar posibles daños.

![Insecure input validation overview][1]

## ¿Qué se considera una entrada de datos no confiable?

* Una entrada de datos no confiable es cualquier dato proporcionado por una fuente externa, refiriéndose a cualquier dato no producido o controlado por la aplicación, como por ejemplo:
  * Datos proporcionados por el usuario.
  * Respuestas de API externas.
  * Contenido de ficheros.

  > :older_man: Validar todas las variables de una aplicación es una tarea que consume tiempo, tanto desde el punto de vista del desarrollo como del rendimiento. Una buena directriz es validar únicamente los datos de las fuentes externas de la aplicación.

## Qué se puede conseguir con la validación de datos de entrada

* **Saneamiento y estandarización de los datos** mediante la aplicación de reglas y formatos específicos, como la supresión de espacios en blanco, la conversión de datos a un modelo coherente o la eliminación de caracteres prohibidos, asegurándose de que los datos que entran en el sistema están limpios y son uniformes.
  * Esto favorece la integridad de los mismos y simplifica su tratamiento y análisis posterior.
* **Mayor calidad y precisión** al verificar la integridad y corrección de los datos suministrados por los usuarios, reduciendo la probabilidad de errores, incoherencias e imprecisiones en los conjuntos de datos del sistema.
  * Esto fomenta la confianza en la fiabilidad de los resultados de la aplicación y facilita la toma de decisiones basadas en datos precisos.
* **Cumplimiento de los requisitos normativos** como `GDPR`, `HIPAA` o `PCI DSS` adhiriéndose a las prácticas de validación obligatorias, salvaguardando la información sensible, la privacidad del usuario y evitando sanciones debidas a infracciones o incumplimientos.
* **Prevención de ataques de inyección** como inyecciones SQL o cross-site scripting (XSS) mediante la validación de la entrada con patrones y el bloqueo de caracteres o comandos dañinos, protegiendo así los datos existentes y manteniendo la confidencialidad e integridad del sistema.
* **Reducción del impacto de los ataques de denegación de servicio (DoS)** limitando el tamaño y la complejidad de la entrada. Establecer restricciones razonables, como la longitud máxima de un campo o los límites de solicitud por usuario, evita que los actores maliciosos abrumen el sistema con datos excesivos o malformados.
* **Protección contra fallos de la lógica empresarial** mediante la aplicación de reglas de validación alineadas con la lógica de la aplicación, lo que impide que los usuarios introduzcan datos no válidos, incorrectos o inesperados que podrían interrumpir procesos críticos o provocar errores.
  * Esto garantiza que la aplicación funcione según lo previsto, ofreciendo resultados coherentes y alineados con los objetivos corporativos.

## Estrategias de validación de datos de entrada

* Las estrategias de validación se clasifican en validación sintáctica y validación semántica.

### Validación sintáctica

* Se centra en las características superficiales de los datos, asegurándose de que cumplen las expectativas de estructura y de formato predefinidas. Este tipo de validación verifica la corrección en términos de sintaxis sin tener en cuenta el significado de los datos.
  * Es como una revisión gramatical de los datos, la cual comprueba si se ajustan a las reglas sintácticas.
* Actúa como primera línea de defensa, rechazando rápidamente los datos con formato incorrecto antes de que se infiltren en las capas más profundas de la aplicación.

#### Casos de uso

* Tipos de datos: garantizar que los campos numéricos realmente contengan números, los campos de texto contengan caracteres alfabéticos, las direcciones de correo electrónico se ajusten al formato estándar (e.g., `user@example.tbl`) o una fecha esté en un formato específico (e.g., `DD-MM-YYYY`).
* Límites de longitud: comprobar si las longitudes de entrada se encuentran dentro de los límites aceptables para evitar desbordamientos de búfer o problemas de truncamiento.
* Restricciones de formato: validación de datos en función de patrones predeterminados, como números de tarjetas de crédito, números de teléfono o códigos postales.

### Validación semántica

* Profundiza más allá de la validación sintáctica, examinando el significado y el contexto de los datos en lugar de únicamente su apariencia superficial.
  * Se trata de garantizar que los datos tengan sentido y se ajusten a las expectativas de la aplicación.
* Actúa como juez interpretando los hechos de un caso, evaluando los datos para asegurarse de que no sólo parecen correctos, sino que también encajan bien en el contexto general del objetivo de la aplicación.

#### Casos de uso

* Comprobación de rangos: verificar si las entradas numéricas se encuentran dentro de los rangos permitidos, por ejemplo, si la edad de un usuario está comprendida entre 18 y 100 años.
* Reglas empresariales: aplicación de restricciones lógicas específicas, como la validación de la cantidad de un producto con respecto a las existencias disponibles, la comprobación de si una reserva se efectua dentro del horario operativo o la verificación de que un dominio de correo electrónico se encuentra entre los permitidos, existe y puede recibir correos electrónicos.
* Validación cruzada de campos: examinar las relaciones entre varios campos, tales como verificar que una fecha de inicio precede a una fecha final o simplemente garantizar la coherencia entre campos relacionados.

## Desafíos de la validación de datos de entrada

* Seguidamente se enumeran algunos de los escenarios más desafiantes a la hora de aplicar técnicas de validación de datos de entrada.

### Validación de contenido enriquecido

* Los contenidos enriquecidos abarcan una amplia gama de tipos y formatos de datos, como texto, imágenes, vídeos, documentos y otros. Garantizar la integridad y seguridad de estos contenidos generados por los usuarios resulta esencial, pero complicado.
* Las técnicas tradicionales de validación diseñadas para estructuras de datos más sencillas pueden tener dificultades para abordar adecuadamente las complejidades de la validación de contenidos enriquecidos.
* Los desarrolladores deben lidiar con el análisis sintáctico, el saneamiento y la validación de diversos formatos para evitar vulnerabilidades como Cross-Site Scripting (XSS), ataques de inyección y corrupción de datos.

### Validación del lado del cliente frente a validación del lado del servidor

* El eterno debate entre la validación del lado del cliente y del lado del servidor gira en torno a las compensaciones entre la experiencia del usuario y la seguridad.

#### Validación del lado del cliente

* La validación del lado del cliente, ejecutada en el navegador del usuario, ofrece información instantánea y una interfaz adaptable con capacidad de respuesta, lo que mejora la experiencia del usuario y la interactividad al detectar preventivamente errores incluso antes de enviar datos al servidor.
* Sin embargo, es susceptible de ser eludida y manipulada por agentes maliciosos, lo que la hace insuficiente como única línea de defensa contra los ataques.

#### Validación del lado del servidor

* La validación del lado del servidor, por su parte, emerge como el baluarte de defensa contra los ataques maliciosos y las alteraciones de la integridad de los datos, dando prioridad a la seguridad y la fiabilidad.
* Actúa como árbitro final, examinando rigurosamente los datos entrantes para hacer cumplir las normas empresariales, sanear las entradas y mitigar los riesgos de seguridad.
* A diferencia de la validación en el lado del cliente, que puede evitarse o desactivarse, la validación en el lado del servidor opera fuera del control del usuario, garantizando la integridad y fiabilidad de los datos de la aplicación.

  > :older_man: Al combinar la validación en el lado del cliente para mejorar la usabilidad con la validación en el lado del servidor para reforzar la seguridad, los desarrolladores tienen que encontrar un delicado equilibrio entre la experiencia del usuario y la integridad y seguridad de la aplicación, ofreciendo un paradigma de interacción con el usuario sin fisuras pero, a su vez, fortificado.

[1]: /static/images/learning/insecure-input-validation-overview.png
