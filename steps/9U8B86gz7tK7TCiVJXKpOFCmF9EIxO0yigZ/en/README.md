# Unicode normalization

## What is input normalization?

* `Input normalization` is the procedure used to transform incoming data into a uniform or standardized format. This transformation is crucial for maintaining data integrity and ensuring consistent data handling across various components of a software system.
* In web applications, it helps in mitigating security risks by standardizing user input to prevent unexpected behavior or exploitation, such as injection attacks.
  * Within this context, the input normalization process typically consists of converting data to any normal form (alphabetizing, or reverse alphabetizing, or stripping non-ASCII characters).

  > :warning: `Input normalization` must be the first line of defense in web application security, as neglecting this step could lead to other vulnerabilities or allow other security measures to be bypassed.

## What vulnerabilities could arise when input normalization is not applied?

* Below are mentioned two actual implications of vulnerabilities derived from input data normalization.

### Account takeover

* In those web applications where users can sign up using usernames that appear identical but have different representations, they might lead to account takeover scenarios.
* For instance, the username `Amélie` can be represented in two different ways using the Unicode encoding standard:
  * The `é` character can be represented by the `U+00E9` code, providing a complete representation for `Amélie` as `\u0041\u006D\u00E9\u006C\u0069\u0065`.
  * The `é` can also be represented by breaking it down into an equivalent base letter `e`, with code `U+0065`, and combining acute accent ` ́`, with code `U+0301`, providing a complete representation for `Amélie` as `\u0041\u006D\u0065\u0301\u006C\u0069\u0065`.
  * These two characters look the same, but do not compare as equal, and the strings have different lengths. In JavaScript:

    ```javascript
    console.log("\u00E9"); // => é
    console.log("\u0065\u0301"); // => é
    console.log("\u00E9" == "\u0065\u0301"); // => false
    console.log("\u00E9".length); // => 1
    console.log("\u0065\u0301".length); // => 2
    ```

* In this scenario, normalizing the string into the *canonical form* helps to avoid such discrepancies by ensuring that visually identical strings are treated as equivalent.

### Cross-Site Scripting (XSS)

* Another simple case where Unicode can be used to bypass security filters is changing the HTML brackets for Unicode brackets.
* For example, the HTML tag `<script>`, which used to inject javascript code by malicious users, can be replaced by `＜script＞` that uses the characters `＜`, with code `U+FF1C`, and `＞`, with code `U+FF1E`. Without proper input normalization both `<script>` and `＜script＞` can be considered equivalent at some point in the application, which can circumvent the security measures specified against the HTML tag `<script>`.

## Understanding Unicode normalization

* Unicode normalization is a process that ensures different binary representations of texts that are equivalent, meaning they appear identical, will be reduced to the same sequence of code points, thus resulting in the same binary value.
* This process is essential in dealing with strings in programming and data processing. It is not only useful for security reasons, but also for functionality.
* The Unicode standard distinguishes between two types of character equivalence:
  * Canonical Equivalence: characters that have the same visual appearance and meaning when displayed are considered equivalent.
  * Compatibility Equivalence: is a weaker type of equivalence, where characters may have a different visual appearance but represent the same concept.
* To address these equivalences there are four standard normalization forms, each one implementing canonical and compatibility techniques differently:

  |Acronym|Term|Usage|Character `ᴷ`| Character `é`|
  |:--:|:--:|:--:|:--:|:--:|
  |NFC|Normalization Form Canonical Composition|Often used when a predictable and human-readable form of text is necessary, such as when displaying text in user interfaces or when storing text that must appear consistent to end-users|Remains the same|Stored as `é` (code `U+00E9`)|
  |NFD|Normalization Form Canonical Decomposition|Valuable in scenarios where text needs to be analyzed or processed at a character level, such as in search algorithms and text comparison operations, where diacritics and other modifiers need to be considered separately from their base characters|Remains the same|Stored as `e´` (codes `U+0065` and `U+0301`)|
  |NFKC|Normalization Form Compatibility Composition|Particularly useful in instances where a form of the text is required that is compatible across different systems, while still retaining the maximum amount of information possible. It's used in systems where compatibility is more important than textual accuracy, such as in keyword generation for search engines|Transformed into `K` to ensure compatibility across different systems|Stored as `é` (code `U+00E9`)|
  |NFKD|Normalization Form Compatibility Decomposition (NFKD)|Crucial for text analysis where compatibility and the most detailed decomposition are required, such as in cryptographic operations, indexing, and any application needing the most atomic form of characters|Transformed into `K` to ensure compatibility across different systems|Stored as `e´` (codes `U+0065` and `U+0301`)|

* These forms help in ensuring that Unicode characters are represented consistently in the database, during processing, and even when interfacing with other systems.
* Strings in a unicode normalized form, they can be assured that equivalent strings have a unique binary representation.
* Considering the previous `é` character example again, but this time normalizing the string:

  ```javascript
  const str = "\u0065\u0301";
  console.log(str == "\u00e9"); // => false
  const normalized = str.normalize("NFC");
  console.log(normalized == "\u00e9"); // => true
  console.log(normalized.length); // => 1
  ```

### Which form should be used by default?

* The most common one is `NFC`. It is often recommended as the default choice because it is widely used and compatible with many systems and protocols.
  * It is actually considered the *normal* form of Unicode text on the web and in other computing environments, making it a safe default for general use.
* Alternatively, to avoid odd characters such as `﹤` or `ⓩ`, the `NFKC` form can be applied, which replaces these characters with their standard equivalents (`<` and `z`).
* Any form is acceptable, as long as consistency is maintained throughout the process, guaranteeing that the same input always leads to the same result.

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
  * As an example, a certain normalization process might simply involve removing any non-ASCII characters and substituting spaces with hyphens for all filenames that are provided by a user when uploading a file to the web application.
  * Considering the potential filenames `my document.pdf` and `MY DOCUMENT.pdf`, this would make both `my-document.pdf` and `MY-DOCUMENT.pdf` as resulting valid filenames, or even `My-Document.PDF` if the user provides `My Document.PDF`.
* Canonicalization is the process of turning any representation of an object into a sole, definitive version known as the canonical form, which is unique to each object.
  * Taking the same filenames `my document.pdf` and `MY DOCUMENT.pdf`, a canonicalization process could involve creating a unique version by not only removing any non-ASCII characters and substituting spaces with hyphens, but also converting the entire filenames to lowercase, resulting `my-document.pdf` as the only acceptable filename, even when the user provides `My Document.PDF`.
  * In this case, to determine if two representations are of the same object, it's sufficient to compare their canonical forms for equality.
* Canonicalization provides a direct way to compare objects but can be challenging to apply uniformly, whereas normalization is more flexible for complex objects. For this reason, normalization might be preferable when it's difficult to consistently implement canonical forms.
