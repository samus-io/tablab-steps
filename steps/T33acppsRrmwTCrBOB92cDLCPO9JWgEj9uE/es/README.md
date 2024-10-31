# Validación de datos en Node.js utilizando JSON Schema

* El paquete [Ajv][1] es conocido como el validador JSON más rápido para Node.js y el navegador.
* Es compatible con JSON Schema draft-06/07/2019-09/2020-12 y JSON Type Definition [RFC 8927][2].

## Fragmento de código en Node.js

* El código siguiente utiliza el paquete Ajv para validar un objeto JavaScript con respecto a un esquema JSON que contiene dos propiedades obligatorias, `productId` como una cadena de exactamente 5 caracteres alfanuméricos y `quantity` como un número entero positivo:

  ```javascript
  const Ajv = require("ajv");

  const ajv = new Ajv();

  const schema = {
    type: "object",
    properties: {
      productId: { 
        type: "string",
        pattern: "^[a-zA-Z0-9]{5}$"
      },
      quantity: {
        type: "integer",
        minimum: 1
      },
    },
    required: ["productId", "quantity"],
    additionalProperties: false,
  };

  const data = {
    productId: "a7gh2",
    quantity: 5
  };

  const validate = ajv.compile(schema);
  const isDataValid = validate(data);
  if (!isDataValid) console.log(validate.errors);
  ```

  * Esta validación garantiza que los datos se ajustan al formato especificado en el esquema, lo que es crucial para mantener la integridad y coherencia de los datos en aplicaciones que dependen de la entrada de datos estructurados.

### Limitaciones del esquema JSON

* JSON Schema no puede gestionar validaciones como comprobar si la edad de una persona está dentro de un rango específico basado en su fecha de nacimiento o asegurar que una fecha precede a la fecha actual. Estos tipos de validaciones requieren una lógica personalizada que debe implementarse en el código de la aplicación.

## Mensajes de error personalizados mediante Ajv

* El propio esquema JSON no soporta de forma nativa mensajes de error personalizados. Sin embargo, algunas paquetes extienden esta funcionalidad.
* Con Ajv los autores de esquemas pueden incluir mensajes de error personalizados dentro del esquema utilizando una palabra clave designada.
* Para lograrlo, es necesario instalar y configurar un paquete adicional llamado `ajv-errors`:

  ```javascript
  const Ajv = require("ajv");
  const addErrors = require("ajv-errors");

  const ajv = new Ajv({ allErrors: true });
  addErrors(ajv);
  ```

* Activando esta configuración, es posible especificar mensajes de error dentro del esquema JSON utilizando la palabra clave `errorMessage`:

  ```javascript
  const schema = {
    type: "object",
    properties: {
      productId: { 
        type: "string",
        pattern: "^[a-zA-Z0-9]{5}$",
        errorMessage: {
          type: "Product ID must be a string",
          pattern: "Product ID must be exactly 5 alphanumeric characters"
        }
      },
      quantity: {
        type: "integer",
        minimum: 1,
        errorMessage: {
          type: "Quantity must be an integer",
          minimum: "Quantity must be a positive integer"
        }
      },
    },
    required: ["productId", "quantity"],
    additionalProperties: false,
    errorMessage: {
      required: {
        productId: "Product ID is required",
        quantity: "Quantity is required"
      },
      additionalProperties: "No additional properties are allowed"
    }
  };
  ```

## Ejercicio para practicar :writing_hand:

* El siguiente formulario de registro acepta datos proporcionados por el usuario sin realizar ningún tipo de validación en el servidor.
* El objectivo aquí es abrir el editor de código a través del botón `Open Code Editor` y aplicar una estrategia de validación de entrada en el lado del servidor usando `JSON Schema`, con el objetivo de validar todos los datos introducidos en los campos del formulario.
* Más concretamente, es necesario modificar un esquema JSON ya existente, el cual se encuentra en `src/main/resources/register-form.schema.json`.
* Este ejercicio sólo se puede superar si la validación de datos del lado del servidor cumple los siguientes requisitos:
  * Los campos `firstName` y `lastName` sólo aceptan caracteres alfabéticos (es decir, A-Z o a-z) de entre 2 y 50 caracteres.
  * El campo `gender` sólo acepta uno de los valores de la lista explícitamente en minúsculas (es decir, `female`, `male`, `transgender`, `non-binary/non-conforming`, `other`).
  * El campo `birthday` sólo acepta una fecha válida en el formato `dd/mm/aaaa` (por ejemplo, 23/01/1990).
  * El campo `email` sólo acepta un correo electrónico en un formato válido común, con un dominio de nivel superior existente y que no supere los 254 caracteres (es decir, `johndoe@example.com`).
  * El campo `phoneNumber` sólo acepta un número de teléfono, sin prefijo, que consta exactamente de 9 dígitos.
  * El campo `password` sólo acepta valores entre 8 y 80 caracteres que contengan al menos una letra minúscula, una mayúscula, un número y un carácter especial (por ejemplo, `@`, `$`, `!`, `%`, `?`, `&`).
  * El campo `hasAcceptedTerms` sólo acepta el valor booleano `true`.
  * Ninguno de los campos anteriores puede dejarse vacío.
* ¿Serás capaz de adoptar una estrategia de validación de entrada adecuada? :slightly_smiling_face::muscle:
  @@ExerciseBox@@

[1]: https://www.npmjs.com/package/ajv
[2]: https://datatracker.ietf.org/doc/rfc8927/
