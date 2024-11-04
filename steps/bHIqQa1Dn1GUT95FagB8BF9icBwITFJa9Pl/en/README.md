# Allow-list validation

* `Allow-list validation`, previously known as `whitelist validation`, is a fundamental security practice used to explicitly specify acceptable inputs while rejecting anything not explicitly listed.

![Allow-list validation overview][1]

* It involves defining a list of permitted values or characters that are considered safe or valid. Any input that does not match the items on the allow-list is rejected to ensure data integrity and security.
* This approach can be used to mitigate various security risks, including injection attacks and unauthorized access.

## Understanding allow-list validation

* Allow-list validation operates on the principle of **explicit acceptance**, so instead of trying to identify and reject malicious inputs, it focuses on defining a set of permissible inputs and deny others.
* By explicitly specifying what is allowed, allow-list validation helps to mitigate a wide range of security risks, providing many **security benefits**.
* Ensures that input data **adheres to expected formats**, reducing the likelihood of malformed or incorrect data entering the system.

## Implementation strategies

* **Defining a list of values** is the straightforward method, which involves using lists of permissible values or characters to validate inputs by checking their existence on these lists.
* **Using regular expressions** offers an alternative approach by establishing a pattern that specifically approves certain values and excludes the rest.

## Practical scenarios

* Below there are a few code snippets illustrating various use cases.

### File extension restriction

* Ensuring only certain file types.

@@TagStart@@java

#### Code snippets in Java

* A set named `allowedFileExtensions` is defined, containing permissible file extensions. Then, the static method `isAllowedFileExtension` retrieves the file extension segment from a filename and verifies its presence in the allowed file extension list:

  ```java
  import java.util.Set;

  public class FileExtensionValidator {

      private static final Set<String> allowedFileExtensions = Set.of(".jpg", ".jpeg", ".png");

      public static boolean isAllowedFileExtension(String filename) {
          int lastDotIndex = filename.lastIndexOf('.');
          if (lastDotIndex == -1) return false; // No extension found

          String extension = filename.substring(lastDotIndex);

          return allowedFileExtensions.contains(extension);
      }
  }
  ```

* It can be used as shown below:

  ```java
  public static void main(String[] args) {
      String filename = "photo.webp";

      if (!FileExtensionValidator.isAllowedFileExtension(filename)) {
          System.out.println("File type not allowed.");
      }
  }
  ```

@@TagEnd@@
@@TagStart@@node.js

#### Code snippets in Node.js

* An array named `allowedFileExtensions` is defined, containing permissible file extensions. Then, the `isAllowedFileExtension` function retrieves the file extension segment from a filename and verifies its presence in the allowed file extension list:

  ```javascript
  const allowedFileExtensions = [".jpg", ".jpeg", ".png"];

  function isAllowedFileExtension(filename) {
    const lastDotIndex = filename.lastIndexOf(".");
    if (lastDotIndex === -1) return false; // No extension found

    const extension = filename.slice(lastDotIndex);

    return allowedFileExtensions.includes(extension);
  }
  ```

* It can be used as shown below:

  ```javascript
  const filename = "photo.webp";

  if (!isAllowedFileExtension(filename)) {
    console.log("File type not allowed.");
  }
  ```

@@TagEnd@@

### Email domain validation

* Allowing only specific email domains for registration or access to certain services.

@@TagStart@@java

#### Code snippets in Java

* A set named `allowedEmailDomains` is defined, containing permissible email domains. Then, the static method `isAllowedEmail` retrieves the domain segment from an email address and verifies its presence in the allowed domain list:

  ```java
  import java.util.Set;

  public class EmailValidator {

      private static final Set<String> allowedEmailDomains = Set.of("example.tbl", "domain.tbl", "trusted.tbl");

      public static boolean isAllowedEmail(String email) {
          String domain = email.substring(email.lastIndexOf("@") + 1);

          return allowedEmailDomains.contains(domain);
      }
  }
  ```

* It can be used as shown below:

  ```java
  public static void main(String[] args) {
      String email = "user@untrusted.tbl";

      if (!EmailValidator.isAllowedEmail(email)) {
          System.out.println("Email domain not allowed.");
      }
  }
  ```

@@TagEnd@@
@@TagStart@@node.js

#### Code snippets in Node.js

* An array named `allowedEmailDomains` is defined, containing permissible email domains. Then, the `isAllowedEmail` function retrieves the domain segment from an email address and verifies its presence in the allowed domain list:

  ```javascript
  const allowedEmailDomains = ["example.tbl", "domain.tbl", "trusted.tbl"];

  function isAllowedEmail(email) {
    const domain = email.split("@").pop();
    
    return allowedEmailDomains.includes(domain);
  }
  ```

* It can be used as shown below:

  ```javascript
  const email = "user@untrusted.tbl";

  if (!isAllowedEmail(email)) {
    console.log("Email domain not allowed.");
  }
  ```

@@TagEnd@@

### Limitation to a specific set of values ​​using regular expressions

* Let's consider an example where an app only allows specific US state abbreviations.

@@TagStart@@java

#### Code snippets in Java

* The `stateAbbreviationsPattern` represents an allow-list created with RegEx for US state abbreviations. Then, the static method `isAllowedStateAbbreviation` checks whether a given abbreviation matches the pattern, returning `true` if it does and `false` otherwise:

  ```java
  public class StateAbbreviationValidator {

    private static final Pattern stateAbbreviationsPattern = Pattern.compile("^(AA|AE|AP|AL|AK|AS|AZ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)$");
  
    public static boolean isAllowedStateAbbreviation(String abbreviation) {
        Matcher matcher = stateAbbreviationsPattern.matcher(abbreviation);

        return matcher.matches();
    }
  }
  ```

* It can be used as shown below:

  ```java
  public static void main(String[] args) {
      String abbreviation = "XYZ";

      if (!StateAbbreviationValidator.isAllowedStateAbbreviation(abbreviation)) {
          System.out.println("Abbreviation not allowed.");
      }
  }
  ```

@@TagEnd@@
@@TagStart@@node.js

#### Code snippets in Node.js

* The `stateAbbreviationsPattern` represents an allow-list created with RegEx for US state abbreviations. Then, the `isAllowedStateAbbreviation` function checks whether a given abbreviation matches the pattern, returning `true` if it does and `false` otherwise:

  ```javascript
  const stateAbbreviationsPattern = /^(AA|AE|AP|AL|AK|AS|AZ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)$/;

  function isAllowedStateAbbreviation(abbreviation) {
    return stateAbbreviationsPattern.test(abbreviation);
  }
  ```

* It can be used as shown below:

  ```javascript
  const abbreviation = "XYZ";

  if (!isAllowedStateAbbreviation(abbreviation)) {
    console.log("Abbreviation not allowed.");
  }
  ```

@@TagEnd@@

### Dynamic SQL queries with unparameterizable values

* According to OWASP, there may be rare cases where dynamic SQL queries must be defined and the values ​​required to be dynamic cannot be set as parameters, such as table names or the sort order indicator.

@@TagStart@@java

#### Code snippets in Java

* The static method `isAllowedTableName` checks whether a given table name matches one of the allowed ones, returning `true` if it does and `false` otherwise, and the static method `getAllowedSortOrder` ensures obtaining the appropriate sort value to incorporate into the SQL query:

  ```java
  public class QueryParamsValidator {
  
    public static boolean isAllowedTableName(String tableName) {
        switch (tableName) {
            case "Format":
            case "Level":
            case "Property":
                return true;
            default:
                return false;
        }
    }

    public static String getAllowedSortOrder(boolean sortOrder) {
        return sortOrder ? "ASC" : "DESC";
    }
  }
  ```

* Both can be used as shown below:

  ```java
  public static void main(String[] args) {
      String tableName = "Condition";
      boolean sortOrder = true;

      if (!QueryParamsValidator.isAllowedTableName(tableName)) {
          System.out.println("Table name not allowed.");
      }

      System.out.println("Order query results using '" + QueryParamsValidator.getAllowedSortOrder(sortOrder) + "'");
  }
  ```

@@TagEnd@@
@@TagStart@@node.js

#### Code snippets in Node.js

* The `isAllowedTableName` function checks whether a given table name matches one of the allowed ones, returning `true` if it does and `false` otherwise, and `getAllowedSortOrder` function ensures obtaining the appropriate sort value to incorporate into the SQL query:

  ```javascript
  function isAllowedTableName(tableName) {
    switch (tableName) {
      case "Format":
      case "Level":
      case "Property":
        return true;
      default:
        return false;
    }
  }

  function getAllowedSortOrder(sortOrder) {
    return sortOrder ? "ASC" : "DESC";
  }
  ```

* Both can be used as shown below:

  ```javascript
  const tableName = "Condition";
  const sortOrder = true;

  if (!isAllowedTableName(tableName)) {
    console.log("Table name not allowed.");
  }

  console.log(`Order query results using '${getAllowedSortOrder(sortOrder)}'`);
  ```

@@TagEnd@@

### Web application form inputs

* Limiting acceptable values for a html dropdown menu to predefined options promotes the submission of only valid selections, which is not safe from a security perspective but contributes to the process:

  ```html
  <select name="payment_method" required>
    <option value="credit_card">Credit Card</option>
    <option value="paypal">PayPal</option>
    <option value="bank_transfer">Bank Transfer</option>
  </select>
  ```

  > :warning: Frontend data input validation does not provide security benefits due to potential code tampering, but it supports further data normalization and validation tasks and typically leads to an improved user experience.

[1]: /static/images/allow-list-validation-overview.png
