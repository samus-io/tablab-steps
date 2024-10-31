# Introducción a la validación sintáctica

* La `validación sintáctica o validación de sintaxis` sirve como primera capa de defensa al garantizar que los datos se ajustan a las reglas de formato esperadas, evitando así que datos mal formados entren en una aplicación.
* Consiste en verificar que los datos se ajustan a normas o patrones predefinidos, garantizando su integridad y seguridad.

![Syntax validation sample][2]

* Al aplicar reglas sintácticas, se permite mantener la coherencia y fiabilidad en el tratamiento y almacenamiento de datos.
* Si bien actúa como barrera inicial contra algunos ataques de inyección, como la inyección SQL, el Cross-Site Scripting (XSS) o las entidades externas XML (XXE), la validación de sintaxis debe combinarse con otras medidas de seguridad para ofrecer una protección completa.

## Beneficios de la validación sintáctica

* **Evita las entradas malformadas** garantizando que los datos recibidos se ajustan al formato esperado, lo que reduce el riesgo de errores y vulnerabilidades de seguridad.
* **Mejora la integridad de los datos** validando estos en la entrada y antes de procesarlos o almacenarlos, preservando la integridad y fiabilidad de la información del sistema.
* **Mejora la experiencia del usuario** al detectar los errores en una fase temprana, lo que ayuda a que la interacción del usuario con el sistema sea más fluida al evitar que las entradas problemáticas provoquen fallos o comportamientos inesperados más adelante.

## Métodos de validación sintáctica

* Existen múltiples técnicas para implementar validación sintáctica, cada una adaptada a tipos de datos y aplicaciones específicas. A continuación, se hace referencia a las más utilizadas.

### Comprobación de tipo

* Garantiza que cada entrada coincide con el tipo de datos esperado y las restricciones específicas del contexto. Por ejemplo, consta en verificar que un campo numérico, como `age` o como puede ser `id`, no recibe una entrada alfabética.
* Para un sitio e-commerce en el que los ID de producto (por ejemplo, `3281`) se pasan como parámetro `id`, la aplicación debe validar si ese `id` es un número que entra dentro de los rangos esperados, y si no lo es, la solicitud debe ser rechazada y el usuario debe ser informado al respecto.
* Dependiendo del lenguaje de programación, la comprobación de tipos puede implementarse mediante *casting* o la definición de interfaces o clases y la instanciación de estas entidades.

  > :older_man: *Casting* es el proceso de conversión de un tipo de datos a otro (por ejemplo, de `string` a `int`).

### Uso de expresiones regulares (RegEx)

* RegEx proporciona potentes capacidades de concordancia de patrones, lo que permite a los desarrolladores definir reglas complejas de validación para formatos de datos, como direcciones de correo electrónico, números de teléfono o nombres de archivo. Este método permite definir criterios precisos que deben cumplir los datos de entrada.

@@TagStart@@java

#### Fragmento de código en Java

* Como demostración simple, el método estático `isAlphanumeric` emplea RegEx para garantizar que el parámetro `str` esté restringido a caracteres alfanuméricos.:

  ```java
  import java.util.regex.Pattern;
  import java.util.regex.Matcher;
  
  public static Boolean isAlphanumeric(String str) {
      Pattern pattern = Pattern.compile("^[a-zA-Z0-9]*$");
      Matcher matcher = pattern.matcher(str);
  
      return matcher.matches();
  }
  ```

@@TagEnd@@
@@TagStart@@node.js

#### Fragmento de código en Node.js

* Como ilustración sencilla, la siguiente función de JavaScript `isAlphanumeric` emplea RegEx para garantizar que el parámetro `str` está restringido a caracteres alfanuméricos:

  ```javascript
  const ALPHANUMERIC_PATTERN = "^[a-zA-Z0-9]*$";

  function isAlphanumeric(str) {
    return ALPHANUMERIC_PATTERN.test(str);
  }
  ```

@@TagEnd@@

### Aplicar validación de datos JSON

* En el caso que los *endpoints* de una API reciban datos JSON, la aplicación debe confirmar en primer lugar que los datos proporcionados por el usuario son un documento JSON válido y, seguidamente, debe asegurarse, utilizando JSON Schema o herramientas similares, que los datos JSON se ajustan al esquema esperado, en particular los atributos requeridos y los tipos de valores asociados, ya sean enteros, cadenas o matrices, o también valores de fecha o de correo electrónico.
* Utilizando [JSON Schema][1], es posible garantizar la conformidad de un documento JSON con un esquema predefinido de una forma extremadamente sencilla en muchos lenguajes.
* Si los datos en formato JSON no cumplen con las especificaciones requeridas, se producirá un error.

@@TagStart@@java

#### Fragmento de código en Java

  ```java
  public void validateJson(JsonNode json) {
      JsonSchema jsonSchema = schemaFactory.getSchema(SchemaLocation.of(schemaPath), config);

      // Validate JSON data
      Set<ValidationMessage> assertions = jsonSchema.validate(json);
      if (!assertions.isEmpty()) {
          System.out.println("JSON is not valid. Errors: ");
          assertions.forEach(vm -> System.out.println(vm.getMessage()));
      }
  }
  ```

@@TagEnd@@
@@TagStart@@node.js

#### Fragmento de código en Node.js

  ```javascript
  const validate = validatorLibrary.compile(jsonSchema);

  function validateJSON(jsonData) {
    return validate(jsonData);
  }
  ```

@@TagEnd@@

## Tratamiento de errores de validación

* El tratamiento adecuado de los errores es un componente crucial en procesos de validación de sintaxis, diseñado para gestionar situaciones en las que las entradas del usuario no cumplen los criterios de validación. Este enfoque garantiza que, cuando se produzcan errores, se traten con elegancia, mejorando la experiencia del usuario y manteniendo la seguridad.
* Para lograrlo, los mensajes de error deben ser informativos pero directos, y guiar a los usuarios para que corrijan sus entradas sin confundirlos con jerga técnica ni exponer detalles internos del sistema que puedan ser explotados por atacantes.
* Por ejemplo, en lugar de un mensaje técnico como `Input fails regex [a-z]{1,15}`, debería proporcionarse un mensaje fácil de usar como `Username should be alphanumeric and its length should be between 1 and 15 characters`.
  * Esto no sólo ayuda a los usuarios a entender exactamente lo que se espera, sino que también evita dar pistas a posibles atacantes sobre los mecanismos de validación subyacentes.

@@TagStart@@java

### Fragmento de código en Java

  ```java
  import java.util.regex.Pattern;
  import java.util.regex.Matcher;
  
  public static boolean isValidUsername(String username) throws IllegalArgumentException {
      Pattern ALPHANUMERIC_PATTERN = Pattern.compile("^[a-zA-Z0-9]*$");
  
      if (username == null || username.isEmpty()) {
          throw new IllegalArgumentException("Username should not be empty.");
      }
  
      if (!ALPHANUMERIC_PATTERN.matcher(username).matches()) {
          throw new IllegalArgumentException("Username should be alphanumeric.");
      }
  
      if (username.length() > 15) {
          throw new IllegalArgumentException("Username length should be between 1 and 15 characters.");
      }
  
      return true;
  }
  ```

@@TagEnd@@
@@TagStart@@node.js

### Fragmento de código en Node.js

  ```javascript
  const ALPHANUMERIC_PATTERN = /^[a-zA-Z0-9]*$/;

  function isValidUsername(username) {
    const isAlphanumeric = ALPHANUMERIC_PATTERN.test(username);
    const isValidLength = username.length > 0 && username.length <= 15;

    return isAlphanumeric && isValidLength;
  }

  if (!isValidUsername(username))
    throw new Error(
      "Username should be alphanumeric and its length should be between 1 and 15 characters"
    );
  ```

@@TagEnd@@

[1]: https://json-schema.org/
[2]: /static/images/learning/syntax-validation-sample.png
