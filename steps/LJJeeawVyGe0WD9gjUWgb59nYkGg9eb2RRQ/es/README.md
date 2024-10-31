# Definición de JSON Schema

* Los [JSON Schema][1] permiten describir la estructura, las restricciones y las reglas de validación de datos que se encuentran en formato JSON. Se utilizan en diversos escenarios, como en la validación de datos enviados por el cliente en servicios web o bien para garantizar la coherencia en el almacenamiento de datos.
* Un esquema JSON es una especificación para un formato concreto de datos JSON que define la estructura aceptable y el tipo de cada elemento en un documento u objeto de este tipo. Sirve como modelo para determinar qué datos están permitidos y cómo deben estructurarse.

  > :warning: Los esquemas JSON no deben exponerse públicamente, ya que pueden dar a los usuarios malintencionados información detallada sobre cómo interactuar con los sistemas de *backend*. La única excepción son las API públicas diseñadas para ser utilizadas por otros desarrolladores.

## Beneficios del uso de esquemas JSON

* Garantiza que todos los datos JSON se adhieren a un conjunto predefinido de reglas, promoviendo **la coherencia en toda la aplicación**.
* Ofrece un modelo claro para la estructura de los datos que pueda ser fácilmente comprendido y **utilizado como documentación** por los desarrolladores.
* Proporciona **escalabilidad** facilitando una estructura clara para los datos JSON que pueda evolucionar con el tiempo sin romper las restricciones existentes.
* Detecta errores en el formato de los datos en una fase temprana del ciclo de desarrollo, **reduciendo los errores en tiempo de ejecución**.

## Entendiendo el proceso de creación de un esquema JSON

* Desarrollar un esquema JSON implica identificar las propiedades de un determinado objeto JSON en cuestión y especificar los tipos de datos que deben contener estas propiedades.
* Es por este motivo que para ilustrar más claramente la creación de un esquema JSON, se parte del siguiente objeto JSON:

  ```json
  {
    "username": "johndoe",
    "age": 25,
    "isVerified": true,
    "contact": {
      "email": "johndoe@domain.tbl",
      "phoneNumbers": ["123-4567", "456-7890"]
    },
    "language": "en"
  }
  ```

  * El primer paso, en este caso, es determinar la estructura del atributo `username`, exigiendo que esté formado únicamente por caracteres alfanuméricos y tenga entre 5 y 50 caracteres de longitud.
  * El atributo `age` debe comprender un número entre 18 y 100, mientras que `isVerified` es una condición booleana que solamente debe acceptar valores `true` o `false`.
  * La propiedad `contact` incluye un atributo `email` y una serie de valores de números de teléfono en el campo `phoneNumbers` que constan de tres dígitos, un guión y cuatro dígitos adicionales.
  * Los idiomas se soportan a través del atributo `language` y los valores a incluir son `en`, `es`, `fr`, `de`, `it` y `pt`.
* Una vez definidos los parámetros, se puede comenzar con la generación del esquema JSON. Este enfoque metódico garantiza que el esquema sea sólido, funcional y se adapte a las necesidades específicas de la aplicación o el sistema.

## Creación de un esquema JSON

* La creación de un esquema JSON comienza definiendo el nivel raíz de este, especificando la versión, un título y el tipo de la estructura de datos raíz.
* La siguiente muestra es una inicialización de un esquema JSON:

  ```json
  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "User Profile",
    "description": "JSON Schema that validates the update of User Profile",
    "type": "object"
  }
  ```

  * El atributo `schema` especifica a qué borrador del estándar de esquema JSON se adhiere.
    * El borrador de esquema JSON más recomendado en la actualidad es el borrador 2020-12.
  * Las propiedades `title` y `description` indican la intención del esquema.
  * El atributo `type` especifica el tipo de datos para un esquema, cuyo valor puede ser `string`, `number`, `integer`, `boolean`, `null`, `array` u `object`.
  * También existe una palabra clave `$comment` para añadir comentarios, la cual no se ha utilizado en este ejemplo y no tiene ningún efecto sobre la validación del esquema.

### Agregar propiedades simples

* Una vez inicializado el esquema JSON, la siguiente etapa consiste en definir las propiedades más sencillas.
* En este ejemplo, el esquema exige que `username` sea alfanumérico, requiere que la `age` esté comprendida entre 18 y 100 años y define `isVerified` como un valor booleano que debe ser siempre verdadero:

  ```json
  {
    ...
    "type": "object",
    "properties": {
      "username": {
        "type": "string",
        "pattern": "^[a-zA-Z0-9]+$",
        "minLength": 5
      },
      "age": {
        "type": "integer",
        "minimum": 18,
        "maximum": 100
      },
      "isVerified": {
        "type": "boolean",
        "const": true
      }
    }
  }
  ```

  * El atributo `properties` define las propiedades de un tipo `object`, donde cada propiedad puede ser a su vez un esquema JSON permitiendo así reglas de validación anidadas.

### Agregar propiedades complejas

* Un esquema JSON también admite propiedades más complejas, como objetos anidados y matrices.
* En el documento JSON de ejemplo se define la propiedad `contact` como un objeto que incluye un `email`, el cual debe coincidir con un formato específico, y una lista de números de teléfono bajo `phoneNumbers` que se adhieren a un patrón particular. También requiere una enumeración para restringir el campo `language` a una lista predefinida de idiomas. Teniendo en cuenta todas estas condiciones, el esquema JSON podría proceder de la siguiente forma:

  ```json
  {
    ...
    "type": "object",
    "properties": {
      ...
      "contact": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email"
          },
          "phoneNumbers": {
            "type": "array",
            "items": {
              "type": "string",
              "pattern": "^[0-9]{3}-[0-9]{4}$"
            }
          }
        }
      },
      "language": {
        "enum": ["en", "es", "fr", "de", "it", "pt"]
      }
    }
  }
  ```

  * El atributo `items` especifica el esquema de los elementos de una matriz. Puede ser un único esquema que aplique a todos sus elementos, o bien una serie de esquemas, para que cada uno aplique a una posición específica de la matriz.

### Agregar propiedades de seguridad

* El siguiente esquema que se muestra está mejorado con propiedades de seguridad para salvaguardar mejor el proceso de validación. Se añaden atributos como `minLength`, `maxLength`, `uniqueItems`, `required` y `additionalProperties` para reforzar el esquema frente a posibles vulnerabilidades y garantizar el cumplimiento de las normas de gobernanza de datos. Con esto concluye el ejemplo demostrativo:

  ```json
  {
      "$schema": "https://json-schema.org/draft/2020-12/schema",
      "title": "User Profile",
      "description": "JSON Schema that validates the update of User Profile",
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "pattern": "^[a-zA-Z0-9]+$",
          "minLength": 5,
          "maxLength": 50
        },
        "age": {
          "type": "integer",
          "minimum": 18,
          "maximum": 100
        },
        "isVerified": {
          "type": "boolean"
        },
        "contact": {
          "type": "object",
          "properties": {
            "email": {
              "type": "string",
              "format": "email",
              "maxLength": 255 
            },
            "phoneNumbers": {
              "type": "array",
              "items": {
                "type": "string",
                "pattern": "^[0-9]{3}-[0-9]{4}$",
                "minLength": 9,
                "maxLength": 50
              },
              "uniqueItems": true
            }
          },
          "required": ["email", "phoneNumbers"],
          "additionalProperties": false
        },
        "language": {
          "enum": ["en", "es", "fr", "de", "it", "pt"]
        }
      },
      "required": ["username", "age", "isVerified", "contact", "language"],
      "additionalProperties": false
  }
  ```

  * `required`: especifica una matriz de *strings* que enumera los nombres de las propiedades que se requieren dentro de un objeto.
  * `additionalProperties`: controla si un objeto puede tener propiedades distintas de las definidas en la palabra clave `properties`. Puede definirse como un valor booleano o como un esquema al que deben ajustarse todas las propiedades adicionales.

## Consideraciones adicionales

* Cada `type` puede poseer sus propias palabras clave para establecer reglas específicas de su campo. Por ejemplo, el tipo `string` tiene las palabras clave `minLenght` y `maxLenght` que pueden utilizarse para establecer la longitud de la cadena. También admite la palabra clave `pattern` que se utiliza para restringir la cadena a una expresión regular determinada.
* Para evitar la creación de expresiones regulares, se puede utilizar la palabra clave `format`. Esta palabra clave permite validar ciertos tipos de valores de cadena utilizados habitualmente. El atributo `format` puede contener valores como `email`, `date`, `hostname`, `uuid`, `ipv4`, y `uri`.
* Para más información sobre cada palabra clave, se puede consultar [JSON Schema Reference][2].
* En JSON y JSON Schemas, las barras invertidas sirven como caracteres especiales para escapar, requiriendo que las mismas deban ser escapadas con una barra invertida doble (`\\`).

### Limitaciones de un esquema JSON

* JSON Schema no puede realizar validaciones como comprobar si la edad de una persona se encuentra dentro de un rango específico o bien confirmar que una fecha es anterior a la fecha actual. Estas validaciones deben codificarse manualmente.

## Cómo validar datos en formato JSON con respecto a un esquema JSON

* Se dispone de varios validadores para contrastar datos JSON con respecto a esquemas JSON. Además de las herramientas de línea de comandos y navegador, existen herramientas de validación en una amplia gama de lenguajes, como JavaScript, Java, Python, .NET y muchos otros. Para elegir el validador adecuado para un proyecto, se puede obtener una buena oritentación en la guía [validators tools][3].
* En la mayoría de los casos, el mecanismo funcional de estos validadores es prácticamente idéntico: comparan los datos con el esquema y la validación se realiza correctamente si los datos cumplen todos los requisitos definidos en el esquema.

@@TagStart@@java

### Fragmento de código en Java

  ```java
  public void validateJSON(JsonNode json) {
      JsonSchema jsonSchema = schemaFactory.getSchema(SchemaLocation.of(schemaPath), config);
      
      // Validate JSON data
      Set<ValidationMessage> assertions = jsonSchema.validate(json);
      if (!assertions.isEmpty()) {
          System.out.println("JSON not valid. Errors:");
          assertions.forEach(vm -> System.out.println(vm.getMessage()));
      }
  }
  ```

@@TagEnd@@
@@TagStart@@node.js

### Fragmento de código en Node.js

  ```javascript
  const Ajv = require("ajv");
  const ajv = new Ajv();

  const schema = {
    type: "object",
    properties: {
      foo: {type: "integer"},
      bar: {type: "string"},
    },
    required: ["foo"],
    additionalProperties: false,
  };

  const data = {
    foo: 1,
    bar: "abc",
  };

  const validate = ajv.compile(schema);
  const valid = validate(data);
  if (!valid) console.log(validate.errors);
  ```

@@TagEnd@@

[1]: https://json-schema.org/
[2]: https://json-schema.org/understanding-json-schema/reference
[3]: https://json-schema.org/implementations
