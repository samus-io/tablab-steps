# Regular Expression (RegEx) validation

* `Regular expressions (RegEx)` are a fundamental tool in software development for pattern matching and validation.
* RegEx is extensively used for input validation measures, ensuring that user-provided data meets specific criteria.

## ReDoS vulnerability

* When using **complex RegEx** be aware that it can rise a `Regular expression Denial of Service (ReDoS)` vulnerability, which occur when malicious input causes the RegEx engine to execute inefficiently, leading to denial of service.

## Common RegEx validations

* The page [ihateregex.io][1] is a web page that has several common RegEx used in web development. Before using it, it is recommended to test each RegEx to ensure that it works for the case.

### Email validation

* Validating the email is crucial for ensuring that users provide a valid email address. However, validating email addresses with RegEx can be complex due to the various formats allowed.
* Here's a detailed RegEx pattern for validating email addresses:

  ```regex
  ^[^\s@]+@[^\s@]+\.[^\s@]+$
  ```

* This RegEx pattern breaks down as follows:
  * `^[^\s@]+`: Matches one or more characters at the start of the string that are not whitespace or `@`.
  * `@`: Matches the `@` symbol.
  * `[^\s@]+`: Matches one or more characters after `@` that are not whitespace or `@`.
  * `\.`: Matches the dot `.` symbol.
  * `[^\s@]+`: Matches one or more characters after `.` that are not whitespace or `@`.

### IPv4 Address Validation

* IPv4 addresses are commonly validated using the following RegEx pattern:

  ```regex
  ^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$
  ```

* This RegEx pattern verifies that an IP address consists of four sets of numbers (0-255) separated by periods.

### URL

```regex
(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)
```

#### Port validation

* Ensures that the provided port number is within the valid range (1-65535).
* Here's a RegEx pattern for port validation:

  ```regex
  ^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$
  ```

* This RegEx pattern allows port numbers from 1 to 65535, covering the entire valid port range.

### Alphanumeric characters (without space)

```regex
^[a-zA-Z0-9]*$
```

### Positive integer input

```regex
^-?\d+$
```

### Date (YYYY-MM-dd)

```regex
([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))
```

### Date (DD/MM/YYYY) Format

TODO

### Phone number (with country codes)

```regex
\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$
```

### HH:MM (12 HOUR)

```regex
^(0?[1-9]|1[0-2]):[0-5][0-9]$
```

### IBAN

```regex
^([A-Z]{2}[0-9]{2})([A-Z0-9]{1,30})$
```

### Credit Card

```regex
(^4[0-9]{12}(?:[0-9]{3})?$)|(^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$)|(3[47][0-9]{13})|(^3(?:0[0-5]|[68][0-9])[0-9]{11}$)|(^6(?:011|5[0-9]{2})[0-9]{12}$)|(^(?:2131|1800|35\d{3})\d{11}$)
```

## Implementing RegEx

### Using RegEx in Java

```java
import java.util.regex.Pattern;
import java.util.regex.Matcher;

public static Boolean isValidEmail(String email){
  Pattern pattern = Pattern.compile("^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$");
  Matcher matcher = pattern.matcher(email);
  return matcher.matches();
}
```

> :warning: Remember that in Java you must escape the backslashes `\` in RegEx.

### Using RegEx in Node.js

```javascript
function isValidEmail(email){
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
```

[1]: https://ihateregex.io/
