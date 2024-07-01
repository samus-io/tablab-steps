# Input Normalization

* `Input normalization` is the procedure used to transform incoming data into a uniform or standardized format. This transformation is crucial for maintaining data integrity and ensuring consistent data handling across various components of a software system.
* In web applications, it helps in mitigating security risks by standardizing user input to prevent unexpected behavior or exploitation, such as injection attacks.
* Strings in a normalized form, they can be assured that equivalent strings have a unique binary representation.

  > :warning: The `Input Normalization` must be done the first measure to be taken, otherwise it can arise other vulnerabilities or security measures can be bypassed.

## Unicode normalization forms

* Unicode provides several forms of normalization, such as `NFC`, `NFD`, `NFKC`, and `NFKD`, to meet different data processing needs. These forms help in ensuring that Unicode characters are represented consistently in the database, during processing, and even when interfacing with other systems.
* This consistency is vital not just for security purposes but also for functionality.

### Normalization Form Canonical Composition (NFC)

* `NFC` is often used when a predictable and human-readable form of text is necessary, such as when displaying text in user interfaces or when storing text that must appear consistent to end-users.

### Normalization Form Canonical Decomposition (NFD)

* `NFD` is valuable in scenarios where text needs to be analyzed or processed at a character level, such as in search algorithms and text comparison operations, where diacritics and other modifiers need to be considered separately from their base characters.

### Normalization Form Compatibility Composition (NFKC)

* The `NFKC` is particularly useful in instances where a form of the text is required that is compatible across different systems, while still retaining the maximum amount of information possible. It's used in systems where compatibility is more important than textual accuracy, such as in keyword generation for search engines.

### Normalization Form Compatibility Decomposition (NFKD)

* `NFKD` is crucial for text analysis where compatibility and the most detailed decomposition are required, such as in cryptographic operations, indexing, and any application needing the most atomic form of characters.

### Differences between normalization forms

* Each normalization form represents characters differently, affecting how they are stored and displayed. Let’s take the character `ᴷ` as an example:
  * `NFC` and `NFD` the character `ᴷ` will remain the same.
  * `NFKC` and `NFKD` the character `ᴷ` will be transformed into `K` to ensure compatibility across different systems.
* On the other hand, the character `é` will appear the same across all four normalization forms, but internally, the storage format differs:
  * In `NFC` and `NFKC` the character will be stored as `é` (Unicode character `U+00E9`).
  * In `NFD` and `NFKD` the character will be stored as `e´` (Unicode characters `U+0065` and `U+0301`).

### Which form to use?

* If one is not sure which Unicode normalization form to use, `NFC` is often recommended as the default choice because it is widely used and compatible with many systems and protocols.
  * It is often considered the "normal" form of Unicode text on the web and in other computing environments, making it a safe default for general use.
* On the other hand, if you want to avoid strange characters such as `﹤` or `ⓩ`, you can use the `NFKC` form, which will replace this character for its equivalent (`<` and `z`).

## What vulnerabilities can arise from not applying input normalization?

* It depends on the systems in between and how they interact with Unicode.
* There may be situations where it is not a problem, but there may be other contexts where the Unicode is interpreted or manipulated by the backend and can be used to exploit vulnerabilities or bypass security filters.

### Account takeover

* In some cases, when a user registers on a web application, usernames that look identical can be registered but are represented different, can be used to account takeover.
* For instance, the username `Amélie` can be write in two different forms:
  * In this case, the `é` is the `U+00E9` character: `\u0041\u006d\u00e9\u006c\u0069\u0065`.
  * Here, the `é` is `U+0065` and `U+0301`: `\u0041\u006d\u0065\u0301\u006c\u0069\u0065`.
* Normalization prevents such discrepancies, ensuring that visually identical strings are treated equivalently.

### Cross-Site Scripting

* Another case where Unicode can be used to bypass security filters is changing the HTML brackets for Unicode brackets.
* For example, the HTML tag `<script>` can be converted to `＜script＞`.
* Using the `NFKC` form, the tag `＜script＞` will be converted to `<script>` and the security filters will block this input.

## File Upload use case

* It can be considered a web application that have a file upload. In order to standardize the file name of the uploaded file, the following implementation should be followed.

### Implementation

#### Implementation in Node.js

```javascript
function handleFileUpload(filename) {
  normalizedFilename = filename.normalize("NFC");

  // Additional security measures

  // File upload logic
}
```

#### Implementation in Java

```java
public void handleFileUpload(String filename){
  String normalizedFilename = Normalizer.normalize(filename, Normalizer.Form.NFC);
  // Additional security measures

  // File upload logic
}
```

## Canonicalization vs normalization

* Canonicalization converts any representation of an object into one unique form, making it easy to compare objects by ensuring they all look the same.
* On the other hand, normalization, transforms an object into a set of acceptable forms rather than one single form. This allows for comparison through a flexible process, accommodating variations that are still considered equal.
* Canonicalization is straightforward but can be hard to implement consistently, while normalization is more adaptable for complex objects. Both methods aim to simplify the comparison of different representations of the same object.
* Having as an example the file `Image.Png`, to convert it to the canonical form, it could become `image.png`.
* On the other hand, to convert it to the normalized form, it could keep the extension in lowercase and allow uppercase letters in the name, transforming the filename to `Image.png`.
