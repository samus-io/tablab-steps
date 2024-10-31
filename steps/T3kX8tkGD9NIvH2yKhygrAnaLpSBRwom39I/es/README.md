# Validación de datos en Java Jakarta utilizando JSON Schema

* El [JSON Schema validator de NetworkNT][1] es una librería Java que valida documentos JSON según las especificaciones [JSON Schema][2].
* Es compatible con varias versiones de las normas de esquemas, incluidos los borradores V4, V6, V7 y las versiones más recientes 2019-09 y 2020-12.
* La librería es conocida por su eficiencia en el rendimiento y puede gestionar los formatos JSON y YAML, lo que la hace versátil para diversos escenarios de desarrollo de software.

## Fragmento de código en Java

* La clase `JsonSchemaValidator` está diseñada para validar datos JSON contra un esquema JSON especificado, asegurando que los datos se ajustan a la estructura y restricciones definidas.
* Esta clase incluye el método `loadSchema` para cargar un esquema JSON desde una ruta especificada (como un archivo o una ubicación classpath) y el método `validateJson` para validar un objeto JSON, representado como un `JsonNode`, contra el esquema cargado.

  ```java
  import com.fasterxml.jackson.databind.JsonNode;
  import com.networknt.schema.JsonSchema;
  import com.networknt.schema.JsonSchemaFactory;
  import com.networknt.schema.SchemaValidatorsConfig;
  import com.networknt.schema.SpecVersion;
  import com.networknt.schema.SchemaLocation;
  import com.networknt.schema.JsonSchemaException;
  import com.networknt.schema.ValidationMessage;
  
  import java.io.IOException;
  import java.util.Set;
  
  public class JsonSchemaValidator {
  
      private final JsonSchema schema;
      public JsonSchemaValidator() throws IOException {
          // Load the JSON Schema from resources folder
          schema = loadSchema("classpath:schema.json");
      }
  
      public JsonSchemaValidator(String schemaPath) throws IOException {
          schema = loadSchema(schemaPath);
      }
  
      private JsonSchema loadSchema(String schemaPath) throws IOException {
          // Schema validator configuration
          SchemaValidatorsConfig.Builder builder = SchemaValidatorsConfig.builder();
          builder.nullableKeywordEnabled(true); // Set true to be compliance
          SchemaValidatorsConfig config = builder.build();
  
          // Specify the JSON Schema version
          JsonSchemaFactory schemaFactory = JsonSchemaFactory.getInstance(SpecVersion.VersionFlag.V202012);
          try {
              JsonSchema jsonSchema = schemaFactory.getSchema(SchemaLocation.of(schemaPath), config);
              jsonSchema.initializeValidators(); // Prevent potential issues related to concurrency
              return jsonSchema;
          }
          catch (JsonSchemaException e) {
              throw new IOException("Failed to load json schema", e);
          }
      }
  
      public void validateJson(JsonNode json) {
          // Validate JSON data
          Set<ValidationMessage> assertions = schema.validate(json, executionContext -> {
              // By default since Draft 2019-09 the format keyword only generates annotations and not assertions
              executionContext.getExecutionConfig().setFormatAssertionsEnabled(true);
          });
  
          if (!assertions.isEmpty()) {
              System.out.println("JSON is not valid. Errors:");
              assertions.forEach(vm -> System.out.println(vm.getMessage()));
          }
      }
  }
  ```

  * Esta validación garantiza que la estructura JSON y los tipos de datos se ajustan al formato esperado especificado en el esquema, lo que resulta crucial para mantener la integridad y coherencia de los datos en aplicaciones que dependen de la entrada de datos estructurados.

## Mensajes de error personalizados mediante el validador de esquemas JSON

* El propio esquema JSON no soporta de forma nativa mensajes de error personalizados. Sin embargo, algunas librerías extienden esta funcionalidad.
* Con el validador de JSON Schema de NetworkNT, los autores de esquemas pueden incluir mensajes de error personalizados dentro del esquema utilizando una palabra clave designada.
* Esto no está habilitado por defecto y para conseguir esta funcionalidad debe configurarse previamente:

  ```java
  SchemaValidatorsConfig config = SchemaValidatorsConfig.builder().errorMessageKeyword("errorMessage").build(); 
  ```

* Activando esta configuración, es posible especificar mensajes de error dentro del esquema JSON utilizando la palabra clave `errorMessage`:

  ```json
  {
    "type": "object",
    "properties": {
      "firstName": {
        "type": "string",
        "description": "The person's first name."
      },
      "foo": {
        "type": "array",
        "maxItems": 3
      }
    },
    "errorMessage": {
      "maxItems": "MaxItem must be 3 only",
      "type": "Invalid type"
    }
  }
  ```

### Limitaciones del esquema JSON

* JSON Schema no puede gestionar validaciones como comprobar si la edad de una persona está dentro de un rango específico basado en su fecha de nacimiento o asegurar que una fecha precede a la fecha actual. Estos tipos de validaciones requieren una lógica personalizada que debe implementarse manualmente en el código de la aplicación.

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

[1]: https://github.com/networknt/json-schema-validator
[2]: https://json-schema.org/
