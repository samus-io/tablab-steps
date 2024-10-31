# Data validation in Node.js

* Node.js offers various tools and libraries for implementing syntax validation, such as regular expressions, built-in functions, and third-party packages like [validator.js][4].

* Lets's take an example of JSON validation in Node.js by using [Ajv][1] npm library.

  ```javascript
  const Ajv = require("ajv");
  const addFormats = require("ajv-formats");

  // Define JSON schema for survey response
  const schema = {
    type: "object",
    properties: {
      name: { type: "string" },
      age: { type: "number" },
      email: { type: "string", format: "email" }
    },
    required: ["name", "age", "email"]
  };

  // Validation function
  function validateJSON(data) {
    const ajv = new Ajv();
    // Add more formats (.e.g email)
    addFormats(ajv);
    const validate = ajv.compile(schema);

    const isValid = validate(data);
    if (!isValid) {
      console.error("JSON validation failed:", validate.errors);
      return false;
    } else {
      console.log("JSON is valid.");
      return true;
    }
  }

  // Example usage
  const jsonData = {
    name: "John Doe",
    age: 30,
    email: "john@example.tbl"
  };

  validateJSON(jsonData);
  ```

  * This example illustrates how we can perform syntax validation on JSON data in a Node.js environment, ensuring that the data meets the expected format requirements before further processing.
  * Other popular packages for JSON validation are : [JOI][2] and [JSON Validator][3].

## Validator.js library

* The [validator.js][4] library offers functions for validating various data types in JavaScript, some examples are:
  * `isEmail`: Validates email addresses.
  * `isURL`: Validates URLs.
  * `isAlphanumeric`: Checks if a string consists only of letters and numbers.
  * `isLength`: Validates string length.
  * `isNumeric`: Checks if a value is numeric.

## File Upload use case: Filename length limit

### Scenario

* Consider the development of a file upload feature for a web application.
* It's essential to ensure that filenames conform to specific syntax rules.
* One crucial aspect is enforcing a maximum length limit for filenames.
* This maintains compatibility across various file systems and mitigates security risks associated with excessively long filenames.

### Implementation

* Syntax validation ensures that user input follows predefined rules and formats.
* Here, the focus is on validating filenames during the file upload process and incorporate additional syntax validations.

### Filename Length Limit

* Define a maximum length limit for filenames to maintain compatibility and prevent security risks related to excessively long filenames.
* Reject filenames exceeding the specified length limit and provide feedback to users.

### Filename Extension Check

* Split the filename by dot (`.`) to ensure it has exactly one extension.
* Prevent filenames with multiple extensions or filenames lacking an extension.

### Alphanumeric Check

* Utilize the isAlphanumeric function from the `validator.js` library to verify if the filename is alphanumeric.
* This ensures filenames comprise only letters and numbers, enhancing security and compatibility.

### Code example

  ```javascript
  const validator = require("validator");

  // Validate Filename Syntax
  function validateFilenameSyntax(filename) {
    // Check Filename Length Limit
    if (filename.length > 255) {
      return false; // Reject filename exceeding length limit
    }

    // Single Extension Check
    const extensions = filename.split(".");
    if (extensions.length !== 2) {
      return false; // Reject filename with multiple extensions
    }

    // Alphanumeric Character Requirement
    if (!validator.isAlphanumeric(extensions[0])) {
      return false; // Reject filename with non-alphanumeric characters
    }

    return true; // Filename syntax is valid
  }

  // Example Filename
  const validFilename = "document.pdf";
  const invalidFilename = "image.jpg.php"; // Contains multiple extensions

  // Validate Filename Syntax
  console.log("Syntax Validation for valid filename:", validateFilenameSyntax(validFilename));
  console.log("Syntax Validation for invalid filename:", validateFilenameSyntax(invalidFilename));
  ```

* In this example, the validateFilename function performs multiple syntax validations:

  * Checks if the filename length exceeds the maximum limit.
  * Ensures the filename has exactly one extension.
  * Validates that the filename is alphanumeric using the isAlphanumeric function from the `validator.js` library.

[1]: https://www.npmjs.com/package/ajv
[2]: https://www.npmjs.com/package/joi
[3]: https://www.npmjs.com/package/json-validator
[4]: https://www.npmjs.com/package/validator
