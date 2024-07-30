# RegEx validation

* `Regular Expressions (RegEx)` are fundamental in software development for conducting pattern matching and validation, making them widely used in ensuring that user-provided data conforms to specific criteria.

## ReDos vulnerability perspective

* The use of complex RegEx should be approached with caution due to the potential risk of a `Regular expression Denial of Service (ReDoS)` vulnerability, which can occur when malicious input causes the RegEx engine to execute inefficiently, leading to a denial of service.

## Common RegEx validations

* The website [ihateregex.io][1] provides several common RegEx used in web development. Some of these are shown below.

### Password

* Minimum eight characters, at least one upper case letter, one lower case letter, one number and one special character:

  ```regex
  ^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$
  ```

### Email

* Presented below is a straightforward email regex effective in many cases, but it's important to note that email validation using RegEx can be complicated because of the various allowed formats:

  ```regex
  ^[^\s@]+@[^\s@]+\.[^\s@]+$
  ```

### IPv4 addresses

* Verifies that an IP address consists of 4 sets of numbers (0-255) separated by periods:

  ```regex
  ^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$
  ```

### TCP/UDP port

* Ensures that the provided port number lies between 1 and 65535:

  ```regex
  ^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$
  ```

### URL

* Matches URLs by optionally recognizing the "http" or "https" protocols followed by "www.", then captures domain names with valid characters and top-level domains (2-6 letters), including subsequent URL components like paths and query strings:

  ```regex
  (https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)
  ```

### Date (DD/MM/YYYY)

* Following the `DD/MM/YYYY` format, it checks that the day falls between 01 and 31, the month is within 01 to 12, and the year is a four-digit number starting with 19 or 20:

  ```regex
  \b(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)\d{2}\b
  ```

### HH:MM (12-hour)

* Checks a time in the 12-hour format, ensuring the hour is between 01 and 12 and the minutes are from 00 to 59. Leading zeros for single-digit hours are optional:

  ```regex
  ^(0?[1-9]|1[0-2]):[0-5][0-9]$
  ```

### Phone number with country code

* Validates an international phone number by confirming that the number begins with a plus sign, is followed by a valid country code, and consists of up to 15 digits:

  ```regex
  \+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$
  ```

### IBAN

* Matches an International Bank Account Number (IBAN), starting with a two-letter country code, followed by two check digits, and including up to 30 alphanumeric characters:

  ```regex
  ^([A-Z]{2}[0-9]{2})([A-Z0-9]{1,30})$
  ```

### Credit card

* Verifies credit card numbers issued by Visa, MasterCard, American Express, Diners Club, Discover, and JCB:

  ```regex
  (^4[0-9]{12}(?:[0-9]{3})?$)|(^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$)|(3[47][0-9]{13})|(^3(?:0[0-5]|[68][0-9])[0-9]{11}$)|(^6(?:011|5[0-9]{2})[0-9]{12}$)|(^(?:2131|1800|35\d{3})\d{11}$)
  ```

## How to use regular expressions

### Code snippet in Java

* The following example performs a check for a valid email format:

  ```java
  import java.util.regex.Pattern;
  import java.util.regex.Matcher;

  public static Boolean isValidEmail(String email) {
      Pattern pattern = Pattern.compile("^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$");
      Matcher matcher = pattern.matcher(email);

      return matcher.matches();
  }
  ```

  > :warning: In Java, backslashes `\` in RegEx must be escaped.

### Code snippet in Node.js

* The following example performs a check for a valid email format:

  ```javascript
  function isValidEmail(email) {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    return pattern.test(email);
  }
  ```

[1]: https://ihateregex.io/
