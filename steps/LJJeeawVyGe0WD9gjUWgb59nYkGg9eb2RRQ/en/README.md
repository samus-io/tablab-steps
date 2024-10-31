# Defining JSON Schema

* [JSON Schema][1] provide a way to describe the structure, constraints, and validation rules of JSON data. They are used in various applications such as validating client-submitted data in web services or ensuring consistency across data storage.
* A JSON Schema is a specification for JSON data format that defines the acceptable structure and type of each element in a JSON document. It serves as a blueprint for what data is permissible and how it should be structured.

  > :warning: JSON Schemas should not be publicly exposed since they can give attackers detailed insight into how to interact with backend systems. The only exception should be public APIs designed to be used by other developers.

## Benefits of using JSON Schema

* Ensure that all JSON data adheres to a predefined set of rules, promoting **consistency across the application**.
* Offer a clear model for the data's structure which can be easily understood and **used as documentation** by developers.
* Provide **scalability** by facilitating a clear structure for JSON data that can evolve over time without breaking existing restrictions.
* Catch errors in data format early in the development cycle, **reducing runtime errors**.

## Understanding the process of creating a JSON Schema

* Developing a JSON Schema involves identifying the properties in a JSON object and specifying the types of data these properties should contain.
* To illustrate the creation of a JSON Schema more clearly, consider the following JSON object that requires validation:

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

  * The initial step here is to determine the structure of the `username` property, requiring that it consists solely of alphanumeric characters and is between 5 and 50 characters long.
  * The `age` field should be a number between 18 and 100, while `isVerified` a boolean condition that accepts only `true` or `false` values.
  * The `contact` property includes an `email` attribute and a series of phone numbers values in the `phoneNumbers` field consisting of three digits, a hyphen and four additional digits.
  * Languages are supported through the `language` attribute and the values to be included are `en`, `es`, `fr`, `de`, `it` and `pt`.
* Once the parameters have been defined, the generation of the JSON Schema can begin. This methodical approach ensures that the schema is robust, functional, and tailored to the specific needs of the application or system.

## Creating a JSON Schema

* The creation of a JSON Schema starts by defining the root level of the schema, specifying the schema version, a title, and the type of the root data structure.
* The following is an initialization of a JSON Schema:

  ```json
  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "User Profile",
    "description": "JSON Schema that validates the update of User Profile",
    "type": "object"
  }
  ```

  * The `schema` attribute specifies which draft of the JSON Schema standard the schema adheres to.
    * The most commonly recommended JSON Schema draft as of now is Draft 2020-12.
  * The `title` and `description` state the intent of the schema.
  * The `type` specifies the data type for a schema, where its value can be `string`, `number`, `integer`, `boolean`, `null`, `array` or `object`.
  * There is also a `$comment` keyword for adding comments, which has not been used in this example and has no effect on the validation of the JSON Schema.

### Adding simple properties

* Once the JSON Schema is initialized, the next stage involves defining simple properties.
* In this example, the schema enforces that the `username` is alphanumeric, requires that `age` falls between 18 and 100 years, and defines `isVerified` as a boolean value that must always be set to true:

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

  * The `properties` attribute defines the properties of an `object` type, where each property can itself be a JSON Schema, allowing nested validation rules.

### Adding complex properties

* A JSON Schema also accommodates more complex properties such as nested objects and arrays.
* The JSON document taken as example defines the `contact` property as an object that includes an `email` that must match a specific format and a list of phone numbers under `phoneNumbers` that adhere to a particular pattern. It also requires an enum to restrict the `language` field to a predefined list of languages. Considering all these conditions, the JSON Schema could then proceed as follows:

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

  * The `items` attribute specifies the schema for elements within an array. It can be a single schema that applies to all items, or a series of schemas, each tailored to a specific position in the array.

### Adding security properties

* The next schema shown is enhanced with security properties to better safeguard the JSON validation process. Attributes such as `minLength`, `maxLength`, `uniqueItems`, `required`, and `additionalProperties` are added to strengthen the schema against potential vulnerabilities and ensure compliance with data governance standards. This concludes the example that has been demonstrated:

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

  * `required`: specifies an array of strings that lists the names of properties that are required within an object.
  * `additionalProperties`: controls whether an object can have properties other than those defined in the `properties` keyword. It can be set to a boolean value or a schema that all additional properties must adhere to.

## Additional considerations

* Each `type` can possess its own keywords to establish rules specific to its field. For example, the `string` type have the keywords `minLenght` and `maxLenght` which may be used to set the length of the string. It also supports the keyword `pattern` which is used to restrict the string to a particular regular expression.
* To avoid the creation of regular expressions, you can use the keyword `format`. This keyword allows validation of certain kinds of string values commonly used. The `format` attribute can take values such as `email`, `date`, `hostname`, `uuid`, `ipv4`, and `uri`.
* For additional insights into each keyword, refer to the [JSON Schema Reference][2].
* In JSON and JSON Schemas, backslashes serve as special characters for escaping, requiring them to be escaped with a double backslash (i.e., `\\`).

### JSON Schema limitations

* JSON Schema can't handle validations like checking if a person's age falls within a specific range or confirming that a date is before the current date. Such validations must be coded manually.

## How to validate JSON data against a JSON Schema

* There are several validators available for validating JSON data against JSON Schemas. In addition to command-line and browser tools, validation tools are available in a wide range of languages, including JavaScript, Java, Python, .NET, and many others. For choosing the right validator for a project, valuable help can be obtained from the [validators tools][3] guide.
* In most instances, the functional mechanism of these validators is virtually identical; they compare the data to the schema, and successful validation occurs if the data adheres to all the defined requirements in the schema.

@@TagStart@@java

### Code snippet in Java

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

### Code snippet in Node.js

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
