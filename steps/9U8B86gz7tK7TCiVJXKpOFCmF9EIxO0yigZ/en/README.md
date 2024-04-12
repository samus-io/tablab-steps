# Input Normalization to UTF-8:

- `Input normalization to UTF-8` refers to the process of ensuring that textual data is encoded using the UTF-8 character encoding scheme.
- `UTF-8` is a variable-width character encoding capable of representing all Unicode characters.
- Normalizing input to UTF-8 is essential for consistency and compatibility across different systems and applications.

### Node.js and UTF-8 Normalization:

- In the realm of Node.js, libraries like `iconv-lite` provide utilities to facilitate the normalization process.
- By utilizing these tools, developers can seamlessly transform incoming text data into a standardized UTF-8 format, fostering interoperability and consistency within their applications.

## Validate Free-Form Unicode Text:

- `Validating free-form Unicode text` involves verifying that the text conforms to certain criteria or constraints, such as permissible characters, length limitations, or specific patterns.
- This validation ensures that the text is well-formed and does not contain any illegal or unexpected characters that could potentially cause issues during processing or storage.
- To validate free-form Unicode text in Node.js, define validation rules based on the application requirements.
- For example, to might restrict the allowed characters to a certain range or disallow specific characters that could pose security risks or compatibility issues.
  - Then, use appropriate validation mechanisms to ensure that the input text meets these criteria before further processing.

## File Upload use case: Restricting allowed characters for filename

**Scenario**

- Imagine developing a file upload feature for a web application, and to ensure that filenames uploaded by users adhere to specific character restrictions.
- This is crucial for maintaining compatibility across different operating systems and preventing potential security vulnerabilities.

**Implementation**

- In this scenario, input validation is implemented to restrict the allowed characters for the filename before storing the uploaded file on the server.

**Character Restriction Rules**

- Define a set of allowed characters for filenames, such as alphanumeric characters (A-Z, a-z, 0-9), underscores (\_), hyphens (-), and periods (.) and control characters like newline and null.
- Exclude special characters and symbols like `/, \, :, *, ?, ", <, >, |` that may pose security risks or cause compatibility issues with file systems.

**Input Normalization**

- Normalize user input using the `normalize()` function in JavaScript, which converts Unicode characters to their equivalent composed or decomposed forms.
- This step ensures that all user input is in a standardized format, reducing the risk of security vulnerabilities and ensuring consistency.

**Input Validation Process**

- After normalization, validate the filename against the predefined character restriction rules.
- Reject filenames that contain disallowed characters or do not meet the specified criteria.
- Provide feedback to the user indicating which characters are not allowed in the filename.

**Use Case**

- Suppose a user attempts to upload a file named `"document$%&.txt"`
- Normalize the filename using the normalize() function to convert any Unicode characters to their equivalent composed or decomposed forms.
- The input validation process detects the presence of special characters `($, %, &)` in the filename.
- As per the character restriction rules, these special characters are not allowed.
- The file upload feature rejects the filename and notifies the user that only alphanumeric characters, underscores, hyphens, and periods are permitted in filenames.

**Implementing Filename Validation**

- Intercept the file upload process and extract the filename from the uploaded file.
- Validate the filename against a whitelist of allowed characters using regular expressions or character comparison.

**Example**

```bash
// Normalize user input using the normalize() function
const normalizedFilename = userInput.normalize();

// Define allowed characters for filenames
const allowedCharactersRegex = /^[a-zA-Z0-9_.-]+$/;

// Validate normalized filename
if (!allowedCharactersRegex.test(normalizedFilename)) {
    console.log("Filename contains disallowed characters.");
} else {
    // Proceed with file upload
}

```

- In this example, the normalize() function converts any Unicode characters in the user input to their equivalent composed or decomposed forms.
- The normalized filename is then validated against the defined character restriction rules. If the filename fails the validation, a message is logged indicating which characters are not allowed.

**Benefits**

- Enhances security by preventing injection attacks or path traversal vulnerabilities.
- Ensures compatibility with various file systems and operating systems.
- Improves user experience by providing clear feedback on filename requirements.
