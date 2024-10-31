# Data validation in Java Jakarta using JSON Schema

* The [JSON Schema validator from NetworkNT][1] is a Java library that validates JSON documents against [JSON Schema][2] specifications.
* It supports multiple versions of the schema standards, including drafts V4, V6, V7, and the more recent 2019-09 and 2020-12 versions.
* The library is known for its performance efficiency and can handle both JSON and YAML formats, making it versatile for various software development scenarios.

## Code snippet in Java

* The `JsonSchemaValidator` class is designed to validate JSON data against a specified JSON Schema, ensuring the data conforms to the defined structure and constraints.
* This class includes the `loadSchema` method to load a JSON Schema from a specified path (such as a file or classpath location) and the `validateJson` method to validate a JSON object, represented as a `JsonNode`, against the loaded schema.

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

  * This validation ensures that the JSON structure and data types conform the expected format specified in the schema, which is crucial for maintaining data integrity and consistency in applications that rely on structured data input.

## Custom error messages using JSON Schema validator

* JSON Schema itself does not natively support custom error messages. However, some libraries extend this functionality.
* With JSON Schema validator, schema authors can include custom error messages within the schema by using a designated keyword.
* This is not enabled by default and to achieve this functionality it must be configured previously:

  ```java
  SchemaValidatorsConfig config = SchemaValidatorsConfig.builder().errorMessageKeyword("errorMessage").build(); 
  ```

* By enabling this configuration, it's possible to specify error messages within the JSON Schema using the `errorMessage` keyword:

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

### JSON Schema limitations

* JSON Schema can't handle validations like checking if a person's age falls within a specific range based on their birthdate or ensuring that a date precedes the current date. These types of validations require custom logic that must be implemented in the application code.

## Exercise to practice :writing_hand:

* The following register form is accepting user-supplied data without conducting any kind of validation on the server-side.
* The purpose here is to open the code editor through the `Open Code Editor` button and apply an input validation strategy on the server-side using `JSON Schema`, with the goal of validating all data entered into the form fields.
* More specifically, it is needed to edit an already existing JSON schema, which is located in `src/main/resources/register-form.schema.json`.
* This exercise can only be passed if the server-side data validation meets the following requirements:
  * The `firstName` and `lastName` fields only accept alphabetic characters (i.e., A-Z or a-z) between 2 and 50 characters.
  * The `gender` field only accepts one of the listed values explicitly in lowercase (i.e., `female`, `male`, `transgender`, `non-binary/non-conforming`, `other`).
  * The `birthday` field only accepts a valid date in the `dd/mm/yyyy` format (e.g., 23/01/1990).
  * The `email` field only accepts an email in a common valid format, with an existing top-level domain, and no longer than 254 characters (i.e., `johndoe@example.com`).
  * The `phoneNumber` field only accepts a phone number with no prefix consisting of exactly 9 digits.
  * The `password` field only accepts values between 8 and 80 characters containing at least one lowercase letter, one uppercase letter, one number, and one special character (i.e., `@`, `$`, `!`, `%`, `?`, `&`).
  * The `hasAcceptedTerms` field only accepts the boolean value `true`.
  * None of the above fields can be left empty.
* Will you be able to adopt an appropriate input validation strategy? :slightly_smiling_face::muscle:
  @@ExerciseBox@@

[1]: https://github.com/networknt/json-schema-validator
[2]: https://json-schema.org/
