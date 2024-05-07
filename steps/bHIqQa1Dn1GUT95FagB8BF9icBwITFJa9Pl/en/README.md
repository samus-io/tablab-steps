# Allow-List Validation (Whitelisting)

* `Allow-list Validation` is a fundamental security practice used to explicitly specify acceptable inputs while rejecting all the others.
* It involves defining a list of permitted values or characters that are considered safe or valid.
* Any input that does not match the items on the Allow-list is rejected to ensure data integrity and security.
* This approach helps mitigate various security risks, including injection attacks and unauthorized access.

## Understanding Allow-List Validation

* **Explicit Acceptance**: Allow-list Validation operates on the principle of explicit acceptance, so instead of trying to identify and reject malicious inputs, it focuses on defining a set of permissible inputs and deny others.
* **Security Benefits**: By explicitly specifying what is allowed, Allow-list Validation helps mitigate a wide range of security risks, including injection attacks, command injection, and unauthorized access.

## Implementation Strategies

### Array-Based Whitelists

* By using arrays to define lists of permitted values or characters is a straightforward approach. Inputs are validated by checking if they exist in the predefined array. Let's consider a common example of Allow-list Validation:
  * Implementation in Node.js:

    ```javascript
    // Example: Allow-list validation for email domains
    const allowedDomains = ['gmail.com', 'yahoo.com', 'hotmail.com'];

    function validateEmailDomain(email) {
        const domain = email.split('@')[1];
        return allowedDomains.includes(domain);
    }

    // Test the validation function
    const validEmail = 'user@gmail.com';
    const invalidEmail = 'user@example.com';

    console.log('Email domain validation (valid):', validateEmailDomain(validEmail));
    console.log('Email domain validation (invalid):', validateEmailDomain(invalidEmail));
    ```

    * Implementation in Java:

    ```java
    public class EmailValidator {
      
      // Set of allowed email domains
      private static final Set<String> allowedDomains = new HashSet<>(Set.of("gmail.com", "yahoo.com", "hotmail.com"));

      // Method to validate the domain of an email
      public static boolean validateEmailDomain(String email) {
          String domain = email.substring(email.indexOf('@') + 1);
          return allowedDomains.contains(domain);
      }

      // Main method to test the validation function
      public static void main(String[] args) {
          String validEmail = "user@gmail.com";
          String invalidEmail = "user@example.com";

          System.out.println("Email domain validation (valid): " + validateEmailDomain(validEmail));
          System.out.println("Email domain validation (invalid): " + validateEmailDomain(invalidEmail));
      }
    }
    ```

  * In this example, we define an array `allowedDomains` containing permissible email domains.
  * The `validateEmailDomain` function extracts the domain part from the email address and checks if it exists in the Allow-list of domains.
  * This ensures that only emails with whitelisted domains are considered valid.

### Allow-list RegEx validation

* This implementation involves defining a Regular Expression pattern that explicitly permits specific values while rejecting all others.
* Let's consider an example of RegEx pattern that allows only specific US state abbreviations.

#### Implementation in Node.js

```javascript
// Allow-list RegEx pattern for US state abbreviations
const stateAbbreviationsPattern = /^(AA|AE|AP|AL|AK|AS|AZ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)$/;

// Function to validate US state abbreviation
function validateStateAbbreviation(abbreviation) {
    return stateAbbreviationsPattern.test(abbreviation);
}

// Example usage
const validAbbreviation = 'NY';
const invalidAbbreviation = 'XYZ';

console.log('State abbreviation validation (valid):', validateStateAbbreviation(validAbbreviation));
console.log('State abbreviation validation (invalid):', validateStateAbbreviation(invalidAbbreviation));
```

#### Implementation in Java

```java
public class StateAbbreviationValidator {

    // Regular expression pattern for US state abbreviations
    private static final Pattern stateAbbreviationsPattern = Pattern.compile("^(AA|AE|AP|AL|AK|AS|AZ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)$");

    // Method to validate a US state abbreviation
    public static boolean validateStateAbbreviation(String abbreviation) {
        Matcher matcher = stateAbbreviationsPattern.matcher(abbreviation);
        return matcher.matches();
    }

    // Main method to test the validation function
    public static void main(String[] args) {
        String validAbbreviation = "NY";
        String invalidAbbreviation = "XYZ";

        System.out.println("State abbreviation validation (valid): " + validateStateAbbreviation(validAbbreviation));
        System.out.println("State abbreviation validation (invalid): " + validateStateAbbreviation(invalidAbbreviation));
    }
}
```

* In this example, the `stateAbbreviationsPattern` represents an Allow-list created with RegEx for US state abbreviations.
* The `validateStateAbbreviation` function checks whether a given abbreviation matches the Allow-list pattern, returning `true` if it does and `false` otherwise.

## File Upload use case

### Scenario

* In an application, users can upload files to the server.
* To maintain security, we want to ensure that only files with specific extension types are accepted for upload.

### Implementation stages

* **Define Permitted Extensions**: Create an array containing the allowed file extensions, such as `.jpg`, `.png`, `.pdf`, etc.
* **Validate Uploaded File**: When a file is uploaded, extract its extension and check if it exists in the list of permitted extensions.
* **Reject Invalid Files**: If the uploaded file's extension is not in the allow-list, reject the upload and provide feedback to the user.

### Implementation

* In this example, `validateFileExtension` checks if the uploaded filename's extension exists in the Allow-list of permitted extensions.
* Only files with extensions listed in allowedExtensions are considered valid for upload.

#### Implementation in Node.js

```javascript
// Define permitted file extensions
const allowedExtensions = ['.jpg', '.jpeg', '.png', '.pdf'];

// Function to validate file extension
function validateFileExtension(filename) {
  const lastDotIndex = filename.lastIndexOf('.');
  if (lastDotIndex === -1) return false; // No extension found

  const extension = filename.slice(lastDotIndex);
  return allowedExtensions.includes(extension);
}

// Example usage
const validFilename = 'document.pdf';
const invalidFilename = 'script.js';

console.log('File extension validation (valid):', validateFileExtension(validFilename));
console.log('File extension validation (invalid):', validateFileExtension(invalidFilename));
```

#### Implementation in Java

```java
public class FileExtensionValidator {

    // Define permitted file extensions
    private static final Set<String> allowedExtensions = new HashSet<>(Set.of(".jpg", ".jpeg", ".png", ".pdf"));

    // Method to validate the file extension of a filename
    public static boolean validateFileExtension(String filename) {
        int lastDotIndex = filename.lastIndexOf('.');
        if (lastDotIndex == -1) return false; // No extension found

        String extension = filename.substring(lastDotIndex);
        return allowedExtensions.contains(extension);
    }

    // Main method to test the validation function
    public static void main(String[] args) {
        String validFilename = "document.pdf";
        String invalidFilename = "script.js";

        System.out.println("File extension validation (valid): " + validateFileExtension(validFilename));
        System.out.println("File extension validation (invalid): " + validateFileExtension(invalidFilename));
    }
}
```
