# Data validation in Node.js using JSON Schema

* The [Ajv][1] package is known as the fastest JSON validator for Node.js and browser.
* It supports JSON Schema draft-06/07/2019-09/2020-12 and JSON Type Definition [RFC 8927][2].

## Code snippet in Node.js

* The code below employs the Ajv package to validate a JavaScript object against a JSON schema that contains two required properties, `productId` as a string of exactly 5 alphanumeric characters, and `quantity` as a positive integer:

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

  * This validation ensures that the data conform the expected format specified in the schema, which is crucial for maintaining data integrity and consistency in applications that rely on structured data input.

### JSON Schema limitations

* JSON Schema can't handle validations like checking if a person's age falls within a specific range based on their birthdate or ensuring that a date precedes the current date. These types of validations require custom logic that must be implemented in the application code.

## Custom error messages using Ajv

* JSON Schema itself does not natively support custom error messages. However, some packages extend this functionality.
* With Ajv, schema authors can include custom error messages within the schema using a designated keyword.
* To achieve this, an extra package named `ajv-errors` needs to be installed and configured:

  ```javascript
  const Ajv = require("ajv");
  const addErrors = require("ajv-errors");

  const ajv = new Ajv({ allErrors: true });
  addErrors(ajv);
  ```

* By enabling this configuration, it's possible to specify error messages within the JSON Schema using the `errorMessage` keyword:

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

## Exercise to practice :writing_hand:

* The following register form is accepting user-supplied data without conducting any kind of validation on the server-side.
* The purpose here is to open the code editor through the `Open Code Editor` button and apply an input validation strategy on the server-side using `JSON Schema`, with the goal of validating all data entered into the form fields.
* More specifically, it is needed to edit an already existing JSON schema, which is located in `schemas/register-form.schema.js`.
* This exercise can only be passed if the server-side data validation meets the following requirements:
  * The `firstName` and `lastName` fields only accept alphabetic characters (i.e., A-Z or a-z) between 2 and 50 characters.
  * The `gender` field only accepts one of the listed values explicitly in lowercase (i.e., `female`, `male`, `transgender`, `non-binary/non-conforming`, `other`).
  * The `birthday` field only accepts a valid date in the `dd/mm/yyyy` format (e.g., 23/01/1990).
  * The `email` field only accepts an email in a common valid format, with an existing top-level domain, and no longer than 254 characters (i.e., `johndoe@example.com`).
  * The `phoneNumber` field only accepts a phone number, with no prefix, consisting of exactly 9 digits.
  * The `password` field only accepts values between 8 and 80 characters containing at least one lowercase letter, one uppercase letter, one number, and one special character (i.e., `@`, `$`, `!`, `%`, `?`, `&`).
  * The `hasAcceptedTerms` field only accepts the boolean value `true`.
  * None of the above fields can be left empty.
* Will you be able to adopt an appropriate input validation strategy? :slightly_smiling_face::muscle:
  @@ExerciseBox@@

[1]: https://www.npmjs.com/package/ajv
[2]: https://datatracker.ietf.org/doc/rfc8927/
