# Regular Expression (RegEx) validation

* Regular expressions (RegEx) are a fundamental tool in software development for pattern matching and validation.
* In Node.js, RegEx is extensively used for input validation tasks, ensuring that user-provided data meets specific criteria.

## Common RegEx validations

* **Email validation** is crucial for ensuring that users provide a valid email address. However, validating email addresses with RegEx can be complex due to the various formats allowed.
  * Here's a detailed RegEx pattern for validating email addresses

    ```js
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    ```

  * This RegEx pattern breaks down as follows:

    * ^[^\s@]+: Matches one or more characters at the start of the string that are not whitespace or "@".
    * @: Matches the "@" symbol.
    * [^\s@]+: Matches one or more characters after "@" that are not whitespace or "@".
    * \.: Matches the dot "." symbol.
    * [^\s@]+: Matches one or more characters after "." that are not whitespace or "@".

* **IP Address Validation** is essential for network-related applications.
  * IPv4 addresses are commonly validated using the following RegEx pattern

    ```js
    const ipRegex = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/;
    ```

  * This RegEx pattern verifies that an IP address consists of four sets of numbers (0-255) separated by periods.

* **Port validation** ensures that the provided port number is within the valid range (1-65535).
  * Here's a RegEx pattern for port validation

    ```js
    const portRegex = /^(6553[0-5]|655[0-2]\d|65[0-4]\d{2}|6[0-4]\d{3}|[1-5]\d{4}|\d{1,4})$/;
    ```

  * This RegEx pattern allows port numbers from 1 to 65535, covering the entire valid port range.


## Mitigating ReDoS Attacks

* `Regular Expression Denial of Service (ReDoS)` attacks occur when malicious input causes the RegEx engine to execute inefficiently, leading to denial of service. 
* To mitigate ReDoS risks, consider the following strategies:

  * Limit the complexity of regular expressions.
  * Use input length limits.
  * Implement early exit conditions.

* Example

    ```js

  function isValidEmail(email) {
      const basicStructureRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!basicStructureRegex.test(email)) {
          return false;
      }

      if (email.length > 254) {
          return false;
      }

      const complexRegex = /^((?![.!#$%&'*+/=?^_`{|}~()-])[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~()-]{1,64})@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
      return complexRegex.test(email);
  }

    ```

  * This function validates email addresses by checking their basic structure, length, and complexity while mitigating ReDoS risks.

## Common RegEx patterns

  | Pattern | Description |
  | :---:   | :---: |
  | Credit Card  | /^\d{4}-\d{4}-\d{4}-\d{4}$/   |
  | URL  | /^(https?   |
  | Zip Code  | /^\d{5}(?:[-\s]\d{4})?$/   |
  | Phone Number  | /^+\d{1,2}\s?\d3\d3\s?\d{3}-\d{4}$/   |
  | Date (MM/DD/YYYY)   | /^(0[1-9]  |

## Conclusion

* Regular expressions are powerful tools for validating various types of input in Node.js applications. 
* By understanding common RegEx patterns and considering challenges like ReDoS attacks, developers can implement robust input validation mechanisms to enhance the security and reliability of their applications.
