# Normalización Unicode

## ¿Qué es la normalización de los datos de entrada?

* La normalización de los datos de entrada es el procedimiento utilizado para transformar los datos entrantes en un formato uniforme o estandarizado. Esta transformación es crucial para mantener la integridad de los datos y garantizar su tratamiento coherente en los distintos componentes de un sistema informático.
* En las aplicaciones web, este proceso ayuda a mitigar los riesgos de seguridad estandarizando la entrada del usuario para evitar comportamientos inesperados o la explotación de vulnerabilidades, por ejemplo, mediante ataques de inyección.
  * En este contexto, la normalización de los datos de entrada suele consistir en la conversión de los datos a cualquier forma normal (como puede ser la alfabetización, la alfabetización inversa o la eliminación de caracteres no ASCII).

  > :warning: La normalización de los datos de entrada debe ser la primera línea de defensa en la seguridad de las aplicaciones web, ya que descuidar este paso podría dar lugar a otras vulnerabilidades o permitir que se eludan otras medidas de seguridad.

## ¿Qué es la normalización Unicode?

* La normalización Unicode es un proceso que garantiza que diferentes representaciones binarias de textos que son equivalentes, es decir, que parecen idénticos, se reducen a la misma secuencia de puntos de código, lo que da como resultado el mismo valor binario.
* Este proceso es esencial en el tratamiento de cadenas dentro del contexto de la programación y el tratamiento de datos, ya que no solamente es útil por razones de seguridad, sino también por motivos de funcionalidad.

  > :older_man: Garantizar que las entradas del usuario se normalizan a una forma canónica en Unicode constituye una práctica de seguridad para las aplicaciones web.

### Formas de normalización Unicode

* El estándar Unicode distingue entre dos tipos de equivalencia de caracteres:
  * La `equivalencia canónica` es cuando los caracteres que tienen el mismo aspecto visual y significado se consideran equivalentes.
  * La  `equivalencia de compatibilidad` es un tipo de equivalencia más débil, en la que los caracteres pueden tener un aspecto visual diferente pero representar el mismo concepto (por ejemplo, variantes de fuentes como `ℌ` y `H`).
* Para abordar estas equivalencias existen cuatro formas de normalización estándar, cada una de las cuales aplica de forma diferente las técnicas canónicas y de compatibilidad:

  |Acrónimo|Término|Uso|Carácter `ᴷ` como ejemplo| Carácter `é` como ejemplo|
  |:--:|:--:|:--:|:--:|:--:|
  |`NFC`|Normalization Form Canonical Composition|Se utiliza cuando se necesita una forma de texto predecible y legible, como cuando se muestra texto en interfaces de usuario o cuando se almacena texto que debe parecer coherente a los usuarios finales|Permanece igual|Almacenado como `é` (código `U+00E9`)|
  |`NFD`|Normalization Form Canonical Decomposition|Valioso en situaciones en las que el texto debe analizarse o procesarse a nivel de caracteres, como en algoritmos de búsqueda y operaciones de comparación de texto, en las que los diacríticos y otros modificadores deben considerarse por separado de sus caracteres base|Permanece igual|Almacenado como `e´` (códigos `U+0065` y `U+0301`)|
  |`NFKC`|Normalization Form Compatibility Composition|Especialmente útil en los casos en que se requiere una forma del texto que sea compatible en distintos sistemas, conservando al mismo tiempo la máxima cantidad de información posible. Se utiliza en sistemas en los que la compatibilidad es más importante que la precisión textual, como en la generación de palabras clave para motores de búsqueda|Transformado en `K` para garantizar la compatibilidad entre distintos sistemas|Almacenado como `é` (código `U+00E9`)|
  |`NFKD`|Normalization Form Compatibility Decomposition|Crucial para el análisis de textos en los que se requiere compatibilidad y la descomposición más detallada, como en operaciones criptográficas, indexación y cualquier aplicación que necesite la forma más atómica de los caracteres|Transformado en `K` para garantizar la compatibilidad entre distintos sistemas|Almacenado como `e´` (códigos `U+0065` y `U+0301`)|

* Estas formas ayudan a garantizar que los caracteres Unicode se representen de manera coherente en la base de datos, durante el procesamiento e incluso al interactuar con otros sistemas.
* Las cadenas de texto que se encuentran en una forma normalizada garantiza que las cadenas equivalentes mantengan una representación binaria única, naturalmente dentro de la misma forma de normalización aplicada.
  * Como ejemplo, en `NFC`, primero se descomponen todos los caracteres y, a continuación, se recomponen sistemáticamente todas las secuencias combinatorias en un orden específico definido por la forma.

#### ¿Qué forma debe utilizarse por defecto?

* La más común es `NFC`. A menudo se recomienda como la opción por defecto porque es ampliamente utilizada y compatible con muchos sistemas y protocolos.
  * De hecho, se considera la forma *normal* de texto Unicode en el mundo web y en otros entornos informáticos, haciendo que la elección sea segura para el uso general.
* Alternativamente, para evitar caracteres extraños como `＜` o `ⓩ`, se puede aplicar la forma `NFKC`, que sustituye estos caracteres por sus equivalentes estándar (`<` y `z`).

## ¿Qué posibles vulnerabilidades de seguridad están asociadas a la normalización Unicode?

* Seguidamente se mencionan implicaciones reales de vulnerabilidades, de entre otras existentes, causadas por un proceso de normalización de Unicode deficiente.

### Account takeover

* En aquellas aplicaciones web en las que los usuarios pueden registrarse utilizando nombres de usuario que parecen idénticos pero tienen representaciones diferentes, estas podrían dar lugar a escenarios de **toma de control de cuentas**.
* Por ejemplo, el nombre de usuario `Amélie` puede representarse, al menos, de dos formas distintas utilizando el estándar de codificación Unicode:
  * El carácter `é` puede representarse mediante el código `U+00E9`, lo que proporciona una representación completa de `Amélie` como `\u0041\u006D\u00E9\u006C\u0069\u0065`.
  * El carácter `é` también puede representarse descomponiéndola en una letra base equivalente `e`, con el código `U+0065`, y combinando el acento agudo `´`, con el código `U+0301`, lo que proporciona una representación completa para `Amélie` como `\u0041\u006D\u0065\u0301\u006C\u0069\u0065`.
  * Estos dos caracteres, `é` y `é`, parecen iguales, pero no se comparan como iguales, y las cadenas tienen longitudes diferentes. En JavaScript:

    ```javascript
    console.log("\u00E9"); // => é
    console.log("\u0065\u0301"); // => é
    console.log("\u00E9" == "\u0065\u0301"); // => false
    console.log("\u00E9".length); // => 1
    console.log("\u0065\u0301".length); // => 2
    ```

* En este escenario, conseguir una normalización adecuada de la cadena `Amélie` a una *forma canónica* ayuda a evitar tales discrepancias, garantizando que las cadenas visualmente idénticas sean tratadas como equivalentes.
  * Utilizando el ejemplo anterior basado en el carácter `é`, pero aplicando la normalización, el resultado sería:

    ```javascript
    const str = "\u0065\u0301";
    console.log(str == "\u00E9"); // => false
    const normalized = str.normalize("NFC");
    console.log(normalized == "\u00E9"); // => true
    console.log(normalized.length); // => 1
    ```

### Evasión de filtro para inyección SQL

* Tomando como ejemplo una aplicación web que construye consultas SQL utilizando el carácter `'` conjuntamente con las entradas del usuario, incluye una medida de seguridad para eliminar todos los caracteres `'` de la entrada, y luego aplica la normalización Unicode a las mismas justo después de dicha eliminación y antes de generar las consultas, este escenario podría conducir inadvertidamente a una vulnerabilidad de inyección SQL.
* Un usuario malintencionado podría insertar un carácter Unicode diferente pero equivalente a `'`, como el apóstrofo de ancho completo `＇`, con el código `U+FF07`, para que cuando la entrada sea normalizada se cree una comilla simple `'`, lo que puede conducir al fallo de inyección SQL.

### Evasión de filtro para Cross-Site Scripting (XSS)

* Otro caso sencillo en el que se puede utilizar Unicode para saltarse los filtros de seguridad es cambiar los corchetes HTML por corchetes Unicode.
* Por ejemplo, la etiqueta HTML `<script>`, utilizada para inyectar código javascript por usuarios malintencionados, puede ser sustituida por `＜script＞` que utiliza los caracteres `＜`, con código `U+FF1C`, y `＞`, con código `U+FF1E`. En un proceso de normalización Unicode deficiente, tanto `<script>` como `＜script＞` pueden considerarse equivalentes en algún punto de la aplicación, lo que puede eludir las medidas de seguridad especificadas contra la etiqueta HTML `<script>`.

## Escenario práctico

* A continuación se muestran un fragmentos de código que ilustra un caso de uso.

### Usuario cambiando su nombre de usuario

* Se puede considerar una aplicación web que permite a sus usuarios cambiar su propio nombre de usuario siempre que no elijan un nombre de usuario que ya haya sido tomado por otro usuario.

@@TagStart@@java

#### Fragmento de código en Java

* La clase `Normalizer` proporciona el método `normalize` que transforma el texto Unicode en una forma compuesta o descompuesta equivalente, especificada como segundo parámetro:

  ```java
  import java.text.Normalizer;

  public void changeUsername(String username){
    String normalizedUsername = Normalizer.normalize(username, Normalizer.Form.NFC);

    // Update logic here
  }
  ```

@@TagEnd@@
@@TagStart@@node.js

#### Fragmento de código en Node.js

* Desde ES2015 JavaScript incluye el método `String.prototype.normalize([form])` que es compatible con Node.js y todos los navegadores web modernos.
* El argumento opcional `form` especifica el identificador de cadena de la forma de normalización a utilizar, siendo por defecto `NFC` si no se proporciona.

  ```javascript
  function changeUsername(username) {
    const normalizedUsername = username.normalize();

    // Update logic here
  }
  ```

@@TagEnd@@

## ¿Cuál es la diferencia entre normalización y canonización?

* Ambos métodos pretenden simplificar la comparación de distintas representaciones de un mismo objeto, pero uno de ellos adopta un enfoque más profundo.
* La normalización se refiere al proceso de convertir cualquier representación de un objeto en un conjunto de formas aceptables, conocidas como formas normales. Una forma *normal* simplemente especifica la estructura del objeto, sin el requisito de unicidad.
  * Esto permite la comparación a través de un proceso flexible, dando cabida a variaciones que se consideran iguales dentro de un contexto.
  * Por ejemplo, un determinado proceso de normalización podría consistir simplemente en eliminar cualquier carácter no alfabético y sustituir los espacios por guiones en todos los nombres de archivo que proporcione un usuario al cargar un archivo en una aplicación web.
  * Teniendo en cuenta los posibles nombres de archivo `my document.pdf` y `MY DOCUMENT.pdf`, tanto `my-document.pdf` como `MY-DOCUMENT.pdf` serían nombres de archivo resultantes válidos, o incluso `My-Document.PDF` si el usuario proporciona `My Document.PDF`:
  ![Normalization process sample][1]
* La canonización es el proceso de convertir cualquier representación de un objeto en una versión única y definitiva conocida como forma canónica, que es única para cada objeto.
  * Tomando los mismos nombres de archivo `my document.pdf` y `MY DOCUMENT.pdf`, un proceso de canonización podría implicar la creación de una versión única no sólo eliminando cualquier carácter no alfabético y sustituyendo los espacios por guiones, sino también convirtiendo todos los nombres de archivo a minúsculas, dando como resultado `my-document.pdf` como único nombre de archivo aceptable, incluso cuando el usuario proporciona `My Document.PDF`:
  ![Canonicalization process sample][2]
  * En este caso, para determinar si dos representaciones son del mismo objeto, basta con comparar sus formas canónicas para comprobar si son iguales.
* La canonización proporciona una forma directa de comparar objetos, pero puede resultar difícil aplicarla de manera uniforme, mientras que la normalización es más flexible para objetos complejos. Por este motivo, la normalización puede ser preferible cuando resulta difícil aplicar de forma coherente las formas canónicas.

## Test para consolidar :rocket:

* Completa el cuestionario eligiendo la respuesta correcta para cada pregunta.
  @@ExerciseBox@@

[1]: /static/images/learning/normalization-process-sample.png
[2]: /static/images/learning/canonicalization-process-sample.png
