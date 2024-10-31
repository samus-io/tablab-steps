# Syntax validation overview

* `Syntax validation` serves as a first layer of defense by ensuring that data conforms to expected format rules, thus preventing malformed data from entering an application.
* It involves verifying that data adheres to predefined rules or patterns, ensuring its integrity and security.

![Syntax validation sample][2]

* By enforcing syntactic rules, it helps to maintain consistency and reliability in data processing and storage.
* While it acts as an initial barrier against some injection attacks, such as SQL injection, Cross-Site Scripting (XSS) or XML External Entities (XXE), syntax validation should be combined with other security measures to provide comprehensive protection.

## Benefits of syntax validation

* **Prevents malformed inputs** by ensuring that incoming data adheres to the expected format, reducing the risk of errors and security vulnerabilities.
* **Enhances data integrity** validating input data before it is processed or stored, preserving the integrity and reliability of the system's information.
* **Improves user experience** by catching errors early, helping to provide a smoother user interaction with the system by preventing problematic inputs from causing failures or unexpected behaviors later.

## Syntax validation methods

* There are multiple techniques for implementing syntax validation, each tailored to specific data types and applications, and the most frequently used are referred below.

### Type checking

* Ensures that each input matches the expected data type and context-specific constraints. For example, verifying that a numerical field, like `age` or as it can be `id`, does not receive alphabetical input.
* For an e-commerce site where product IDs (e.g., `3281`) are passed as `id` parameter, the application should validate if that `id` is a number it falls within expected ranges, and if isn't, The request should be rejected and the user should be informed that it is not a number.
* Depending on the programming language, type checking can be implemented through casting or the definition of interfaces or classes, and the instantiation of these entities.

  > :older_man: Casting is the conversion process of one data type into another (e.g., `string` to `int`).

### Using Regular Expressions (RegEx)

* Regex provides powerful pattern-matching capabilities, allowing developers to define complex validation rules for data formats, such as email addresses, phone numbers or filenames. This method allows for the definition of precise criteria that input data must meet.

@@TagStart@@java

#### Code snippet in Java

* As a simple illustration, the static method `isAlphanumeric` employs RegEx to ensure the `str` parameter is restricted to alphanumeric characters:

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

#### Code snippet in Node.js

* As a simple illustration, the function `isAlphanumeric` employs RegEx to ensure the `str` parameter is restricted to alphanumeric characters:

  ```javascript
  const ALPHANUMERIC_PATTERN = "^[a-zA-Z0-9]*$";

  function isAlphanumeric(str) {
    return ALPHANUMERIC_PATTERN.test(str);
  }
  ```

@@TagEnd@@

### Applying JSON validation

* For API endpoints receiving JSON data, the application needs to first confirm that the user-provided data is a valid JSON document. Following this, the application should ensure, using JSON Schema or similar tools, that the JSON data conforms to the expected schema, particularly the required keys and the types of associated values (e.g., integers, strings, arrays), including date or emails fields.
* Using [JSON Schema][1], it is possible to guarantee the conformance of a JSON document to its schema in an extremely easy way in many languages.
* If the JSON document does not adhere to the required specifications, an error will occur.

@@TagStart@@java

#### Code snippet in Java

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

#### Code snippet in Node.js

  ```javascript
  const validate = validatorLibrary.compile(jsonSchema);

  function validateJSON(jsonData) {
    return validate(jsonData);
  }
  ```

@@TagEnd@@

## Handling validation errors

* Proper error handling is a crucial component of syntax validation, designed to manage situations where user inputs fail to meet validation criteria. This approach ensures that when errors occur, they are dealt with gracefully, enhancing user experience and maintaining security.
* To achieve this, error messages should be informative yet straightforward, guiding users to correct their inputs without confusing them with technical jargon or exposing internal system details that could be exploited by attackers.
* For instance, instead of technical feedback like `Input fails regex [a-z]{1,15}`, a user-friendly message such as `Username should be alphanumeric and its length should be between 1 and 15 characters` should be provided.
  * This not only helps users understand exactly what is expected but also avoids giving potential attackers clues about the underlying validation mechanisms.

@@TagStart@@java

### Code snippet in Java

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

### Code snippet in Node.js

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
