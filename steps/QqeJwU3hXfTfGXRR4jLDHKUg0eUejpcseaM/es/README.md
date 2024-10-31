# Formato de redacción a seguir y restricciones de derechos de autor

* Crear un Step en [tablab.io][1] consiste en ofrecer una experiencia de aprendizaje concisa, clara y atractiva. Esta guía se centra en el formato y el estilo de redacción esenciales para crear un Step eficaz.

## Sigue nuestra convención de estilo de escritura

* Utiliza la sintaxis Markdown para dar estilo a todos los escritos.
* Describe los conceptos mediante listas de enumeración con frases cortas y concretas, como esta.
* Todas las frases deben empezar con un punto de enumeración.
* Evita frases largas. Si es necesario, divídelas por significado, concepto o contexto.
* Evita oraciones en primera persona al explicar un concepto, como "Imagina que estás ejecutando una plataforma en línea donde...". En su lugar, se debe utilizar el enfoque "Se puede considerar una plataforma en línea donde...".

### Definición de títulos

* No es necesario añadir dos puntos (`:`) al final de un título para introducir la enumeración.
* No se deben utilizar letras mayúsculas para palabras que no representan un concepto. Por ejemplo, el título "Casos de Uso" debería ser simplemente "Casos de uso". Sin embargo, al utilizar "Validación de Entrada" en un título, dado que representa un concepto, se debe optar por "Introducción a la Validación de Entrada" con mayúsculas, por ejemplo.

### Uso de emojis

* :writing_hand: (`:writing_hand:`): se utiliza para indicar al lector que a continuación se encuentra un ejercicio práctico.
* :older_man: (`:older_man:`): se utiliza para explicar algún concepto relacionado con el Step el cual no se trata específicamente.
* :warning: (`:warning:`): se utiliza cuando es aconsejable que el lector preste atención a una sección importante.

### Añadir una tabla

* Puedes añadir tablas cuando sea necesario. Para ello, ten en cuenta que este es el formato que procesa nuestro renderizador de Markdown:

  ```markdown
  |Column 1|Column 2|Column 3|
  |:--:|:--:|:--:|
  |Field 1|Field 2|Field 3|
  |Field 4|Field 5|Field 6|
  ```

### Añadir una imagen

* Cuando quieras añadir una imagen al contenido para explicar un concepto de forma más representativa, primero necesitas obtener la imagen en tu ordenador y luego colocarla como archivo estático en la carpeta `/static/images/` que encontrarás en este repositorio.
* Una vez hecho esto, puedes incrustar la imagen siguiendo el código Markdown como se muestra:

  ```markdown
  ![Image caption here][1]
  ```

  Después, solo tienes que hacer referencia a la imagen al final del archivo de la siguiente forma:

  ```markdown
  [1]: /static/images/your-selected-image.png
  ```

  Ten en cuenta que la ruta de la imagen `/static/images/your-selected-image.png` se refiere a la ruta absoluta donde supuestamente se ha colocado la imagen en este repositorio.
* Observe que los nombres de las imágenes deben seguir el siguiente patrón: `su-imagen.png`.
* **Aviso importante**: puedes añadir cualquier imagen que desees, aunque no la hayas creado tú mismo. Nosotros nos encargaremos de crear una nueva imagen que represente exactamente el mismo concepto pero en formato corporativo (estilos y colores) y evitando cualquier infracción de derechos de autor.

## Añadir un enlace

* Cuando añadas un enlace debes utilizar la misma convención que las imágenes.
* Primero, añade el enlace con su título usando este formato: `[tablab.io][1]`.
* Después, al final del código *markdown*, añade la URL:

  ```markdown
  [1]: https://tablab.io
  ```

### Añadir fragmentos de código

* Para insertar código en Steps, debe rodearlo con tres tildes (```` ``` ````) y especificar el lenguaje de programación inmediatamente después de las tildes de apertura para activar el resaltado de sintaxis.
* Asegúrate de que hay una línea en blanco antes y después del bloque de código para separarlo del texto que lo rodea.
* Si tu texto hace referencia directa al código, indenta el bloque de código para conectar visualmente el texto y el código, mejorando la legibilidad:

  ```html
  <h1>Hello World!</h1>
  ```

### Conceptos de programación

* Los siguientes conceptos deben ser envueltos en acentos(`` ` ``):
  * Cabeceras HTTP: `Content-Type`, `Server`, `Host`.
  * Métodos HTTP: `GET`, `PUT`, `DELETE`.
  * Endpoints o rutas: `/admin`, `/var/www/html`.
  * Parámetros web: `/users?id=123`, `id=123`.
* Utiliza Camel Case para los nombres de los endpoints o ficheros (por ejemplo, `/deleteUser`, `userInvoice.pdf`).
* Si necesitas mencionar un nombre de dominio como ejemplo, debes usar `ejemplo.org`. Además, los dominios deben ir entre acentos.
  * En el caso del dominio de un atacante, debe utilizarse `attacker.site` y `victim.site` para el dominio de la víctima.

### Uso de Visual Studio Code

* Aquellos que utilicen Visual Studio Code encontrarán en este mismo repositorio configuraciones para varios plugins diseñados para mejorar su experiencia de escritura en Markdown.
* Para instalar las extensiones recomendadas para este proyecto, sigue estos pasos en Visual Studio Code:
  1. Inicia Visual Studio Code cargando el repositorio [tablab-steps][2].
  1. Navega a la vista de *Extensions* pulsando `Ctrl+Shift+X` (o `Cmd+Shift+X` en macOS).
  1. Escribe `@recommended` en la barra de búsqueda.
  1. Haz clic en el botón de instalación situado junto a las extensiones enumeradas en *Workspace Recommendations*.

## Respeta los derechos de autor

* Como creador de contenido, es fundamental comprender y respetar las leyes de derechos de autor, asegurándote de no utilizar ni replicar frases o textos de otros sitios web.
* El mero intercambio de palabras con significados similares en una frase, sin modificar la estructura de la misma ni la gramática, sigue considerándose una forma de plagio.
* Las herramientas de IA pueden ayudarte en la creación de contenido, pero no se permiten textos producidos directamente por sistemas de inteligencia artificial en [tablab.io][1].

[1]: https://tablab.io
[2]: https://github.com/samus-io/tablab-steps
