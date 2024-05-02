# Regular Expression (RegEx) validation

* Regular expressions (RegEx) are a fundamental tool in software development for pattern matching and validation.
* In Node.js, RegEx is extensively used for input validation tasks, ensuring that user-provided data meets specific criteria.

## Common RegEx validations

* **Email validation** is crucial for ensuring that users provide a valid email address. However, validating email addresses with RegEx can be complex due to the various formats allowed.
  * Here's a detailed RegEx pattern for validating email addresses

    ```js
    const emailRegex = `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`;
    ```

  * This RegEx pattern breaks down as follows:

    * ^[^\s@]+: Matches one or more characters at the start of the string that are not whitespace or "@".
    * @: Matches the "@" symbol.
    * [^\s@]+: Matches one or more characters after "@" that are not whitespace or "@".
    * \.: Matches the dot "." symbol.
    * [^\s@]+: Matches one or more characters after "." that are not whitespace or "@".

* **IPV4 Address Validation** is essential for network-related applications.
  * IPv4 addresses are commonly validated using the following RegEx pattern

    ```js
    const ipRegex = `/^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/`;
    ```

  * This RegEx pattern verifies that an IP address consists of four sets of numbers (0-255) separated by periods.

* **Port validation** ensures that the provided port number is within the valid range (1-65535).
  * Here's a RegEx pattern for port validation

    ```js
    const portRegex = `^((6553[0-5])|(655[0-2][0-9])|(65[0-4][0-9]{2})|(6[0-4][0-9]{3})|([1-5][0-9]{4})|([0-5]{0,5})|([0-9]{1,4}))$`;
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

* **Alphanumeric Characters(without space)** - `/^[a-zA-Z0-9]*$/`
* **Date (YYYY-MM-dd )** -  `/([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))/`
* **Phone Number(with country codes)** - `\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$`
* **URL** - `/(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/ `
* **HH:MM (12-HOUR)** - `/^(0?[1-9]|1[0-2]):[0-5][0-9]$/`
* **IBAN** - `^([A-Z]{2}[ '+'\\\\'+'-]?[0-9]{2})(?=(?:[ '+'\\\\'+'-]?[A-Z0-9]){9,30}\$)((?:[ '+'\\\\'+'-]?[A-Z0-9]{3,5}){2,7})([ '+'\\\\'+'-]?[A-Z0-9]{1,3})?\$`
* **DNI** - `^[0-9]{8}[A-z]$`
* **Credit Card** - `(?<!\d)\d{16}(?!\d)|(?<!\d[ _-])(?<!\d)\d{4}(?:[_ -]\d{4}){3}(?![_ -]?\d)`
