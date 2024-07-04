# Unicode normalization

## What is input normalization?

* `Input normalization` is the procedure used to transform incoming data into a uniform or standardized format. This transformation is crucial for maintaining data integrity and ensuring consistent data handling across various components of a software system.
* In web applications, it helps in mitigating security risks by standardizing user input to prevent unexpected behavior or exploitation, such as injection attacks.
  * Within this context, the input normalization process typically consists of converting data to any normal form (alphabetizing, or reverse alphabetizing, or stripping non-ASCII characters).

  > :warning: `Input normalization` must be the initial security measure implemented, as neglecting this step could lead to other vulnerabilities or allow other security measures to be bypassed.

## What vulnerabilities could arise when input normalization is not applied?

* Below are mentioned two actual implications of vulnerabilities derived from input data normalization.

### Account takeover

* In those web applications where users can sign up using usernames that appear identical but have different representations, they might lead to account takeover scenarios.
* For instance, the username `Amélie` can be represented in two different ways using the Unicode encoding standard:
  * The `é` character can be represented by the `U+00E9` code, providing a complete representation for `Amélie` as `\u0041\u006d\u00e9\u006c\u0069\u0065`.
  * The `é` can also be represented by breaking it down into an equivalent base letter `e`, with code `U+0065`, and combining acute accent ` ́`, with code `U+0301`, providing a complete representation for `Amélie` as `\u0041\u006d\u0065\u0301\u006c\u0069\u0065`.
* In this scenario, input normalization helps to avoid such discrepancies by ensuring that visually identical strings are treated as equivalent.

### Cross-Site Scripting (XSS)

* Another simple case where Unicode can be used to bypass security filters is changing the HTML brackets for Unicode brackets.
* For example, the HTML tag `<script>`, which used to inject javascript code by malicious users, can be replaced by `＜script＞` that uses the characters `＜`, with code `U+FF1C`, and `＞`, with code `U+FF1E`. Without proper input normalization they can be considered equivalent at some point in the application, which can circumvent the security measures specified only against the HTML tag `<script>`.

## Understanding Unicode normalization

* Unicode normalization is a process that ensures different binary representations of texts that are equivalent will be reduced to the same sequence of code points, thus resulting in the same binary value.
* This process is essential in dealing with strings in programming and data processing. It is not only useful for security reasons, but also for functionality.
* The Unicode standard distinguishes between two types of character equivalence:
  * Canonical Equivalence: characters that look and mean the same when displayed are considered equivalent.
  * Compatibility Equivalence: a less strict form of equivalence, where characters may look different but represent the same concept.
* To address these equivalences, four normalization algorithms are used, each one implementing canonical and compatibility techniques differently.

### Normalization Form Canonical Composition (NFC)

* `NFC` is often used when a predictable and human-readable form of text is necessary, such as when displaying text in user interfaces or when storing text that must appear consistent to end-users.

### Normalization Form Canonical Decomposition (NFD)

* `NFD` is valuable in scenarios where text needs to be analyzed or processed at a character level, such as in search algorithms and text comparison operations, where diacritics and other modifiers need to be considered separately from their base characters.

### Normalization Form Compatibility Composition (NFKC)

* The `NFKC` is particularly useful in instances where a form of the text is required that is compatible across different systems, while still retaining the maximum amount of information possible. It's used in systems where compatibility is more important than textual accuracy, such as in keyword generation for search engines.
* Using the `NFKC` form, the tag `＜script＞` will be converted to `<script>` and the security filters will block this input.

### Normalization Form Compatibility Decomposition (NFKD)

* `NFKD` is crucial for text analysis where compatibility and the most detailed decomposition are required, such as in cryptographic operations, indexing, and any application needing the most atomic form of characters.

## Unicode normalization forms

* Unicode provides several forms of normalization, such as `NFC`, `NFD`, `NFKC`, and `NFKD`, in order to meet different data processing needs. These forms help in ensuring that Unicode characters are represented consistently in the database, during processing, and even when interfacing with other systems.
* Strings in a unicode normalized form, they can be assured that equivalent strings have a unique binary representation.

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

## What is the difference between normalization and canonicalization?

* Both methods aim to simplify the comparison of different representations of the same object, but one method takes a more in-depth approach.
* Normalization refers to the process of converting any representation of an object into a set of acceptable forms, known as normal forms. A normal form simply specifies the structure of the object, without the requirement of uniqueness.
  * This allows for comparison through a flexible process, accommodating variations that are considered equal within a context.
  * As an example, a certain normalization process might simply involve removing any non-ASCII characters and substituting spaces with hyphens for all filenames that are provided by a user when uploading a file. Considering the potential filenames `my profile picture.png` and `MY PROFILE PICTURE.png`, this would make both `my-profile-picture.png` and `MY-PROFILE-PICTURE.png` as resulting valid filenames, or even `My-Profile-Picture.PNG` if the user provides `My Profile Picture.PNG`.
* Canonicalization is the process of turning any representation of an object into a sole, definitive version known as the canonical form, which is unique to each object.
  * Taking the same filenames `my profile picture.png` and `MY PROFILE PICTURE.png`, a canonicalization process could involve creating a unique version by not only removing any non-ASCII characters and substituting spaces with hyphens, but also converting the entire filenames to lowercase, resulting `my-profile-picture.png` as the only acceptable filename, even when the user provides `My Profile Picture.PNG`.
  * In this case, to determine if two representations are of the same object, it's sufficient to compare their canonical forms for equality.
* Canonicalization provides a direct way to compare objects but can be challenging to apply uniformly, whereas normalization is more flexible for complex objects. For this reason, normalization might be preferable when it's difficult to consistently implement canonical forms.
