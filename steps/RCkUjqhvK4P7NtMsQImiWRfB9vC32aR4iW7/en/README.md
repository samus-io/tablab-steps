# Regular Expression (RegEx) validation

* Regular expressions (RegEx) are a fundamental tool in software development for pattern matching and validation.
* RegEx is extensively used for input validation tasks, ensuring that user-provided data meets specific criteria.

## Common RegEx validations

* **Email validation** is crucial for ensuring that users provide a valid email address. However, validating email addresses with RegEx can be complex due to the various formats allowed.
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

* **IPV4 Address Validation** is essential for network-related applications.
  * IPv4 addresses are commonly validated using the following RegEx pattern

    ```regex
    ^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$
    ```

  * This RegEx pattern verifies that an IP address consists of four sets of numbers (0-255) separated by periods.

* **Port validation** ensures that the provided port number is within the valid range (1-65535).
  * Here's a RegEx pattern for port validation

    ```regex
    ^((6553[0-5])|(655[0-2][0-9])|(65[0-4][0-9]{2})|(6[0-4][0-9]{3})|([1-5][0-9]{4})|([0-5]{0,5})|([0-9]{1,4}))$
    ```

  * This RegEx pattern allows port numbers from 1 to 65535, covering the entire valid port range.

## Implementing RegEx

* Using RegEx in Node.js:

  ```js
  function isValidEmail(email){
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
  ```

* Using RegEx in Java:

  ```java
  public static Boolean isValidEmail(String email){
    Pattern pattern = Pattern.compile("^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$");
    Matcher matcher = pattern.matcher(email);
    return matcher.matches();
  }
  ```

> :warning: Remember that in Java you must escape the backslashes `\` in RegEx.

## Mitigating ReDoS Attacks

* `Regular Expression Denial of Service (ReDoS)` attacks occur when malicious input causes the RegEx engine to execute inefficiently, leading to denial of service.
* To mitigate ReDoS risks, consider the following strategies:
  * Limit the complexity of regular expressions.
  * Use input length limits.
  * Implement early exit conditions.

* Example

    ```js
    function isValidEmail(email) {
        if (email.length > 254) {
            return false;
        }

        const complexRegex = /^((?![.!#$%&'*+/=?^_`{|}~()-])[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~()-]{1,64})@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
        return complexRegex.test(email);
    }
    ```

  * This function validates email addresses by checking their basic structure, length, and complexity while mitigating ReDoS risks.

## Common RegEx patterns

### Alphanumeric characters(without space)

```regex
^[a-zA-Z0-9]*$
```

### Date (YYYY-MM-dd)

```regex
([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))
```

### Phone number (with country codes)

```regex
\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$
```

### URL

```regex
(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)
```

### HH:MM (12 HOUR)

```regex
^(0?[1-9]|1[0-2]):[0-5][0-9]$
```

### IBAN

```regex
^([A-Z]{2}[0-9]{2})([A-Z0-9]{1,30})$
```

### DNI

```regex
^[0-9]{8}[A-Z]$
```

### Credit Card

```regex
(^4[0-9]{12}(?:[0-9]{3})?$)|(^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$)|(3[47][0-9]{13})|(^3(?:0[0-5]|[68][0-9])[0-9]{11}$)|(^6(?:011|5[0-9]{2})[0-9]{12}$)|(^(?:2131|1800|35\d{3})\d{11}$)
```
