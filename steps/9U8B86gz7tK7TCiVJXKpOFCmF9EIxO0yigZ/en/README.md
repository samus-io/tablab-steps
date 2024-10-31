# Unicode normalization

## What is input normalization?

* `Input normalization` is the procedure used to transform incoming data into a uniform or standardized format. This transformation is crucial for maintaining data integrity and ensuring consistent data handling across various components of a software system.
* In web applications, it helps in mitigating security risks by standardizing user input to prevent unexpected behavior or exploitation, such as injection attacks.
  * Within this context, input normalization typically consists of converting data to any normal form (alphabetizing, or reverse alphabetizing, or stripping non-ASCII characters).

  > :warning: `Input normalization` must be the first line of defense in web application security, as neglecting this step could lead to other vulnerabilities or allow other security measures to be bypassed.

## What about Unicode normalization?

* Unicode normalization is a process that ensures different binary representations of texts that are equivalent, meaning they appear identical, will be reduced to the same sequence of code points, thus resulting in the same binary value.
* This process is essential in dealing with strings in programming and data processing since it is not only useful for security reasons, but also for functionality.

  > :older_man: Ensuring that user inputs are normalized to a canonical form in Unicode constitutes a security practice for web applications.

### Unicode normalization forms

* The Unicode standard distinguishes between two types of character equivalence:
  * `Canonical equivalence` is when characters that have the same visual appearance and meaning are considered equivalent.
  * `Compatibility equivalence` is a weaker type of equivalence, where characters may have a different visual appearance but represent the same concept (e.g., font variants like `ℌ` and `H`).
* To address these equivalences there are four standard normalization forms, each one implementing canonical and compatibility techniques differently:

  |Acronym|Term|Usage|Character `ᴷ` as example| Character `é` as example|
  |:--:|:--:|:--:|:--:|:--:|
  |`NFC`|Normalization Form Canonical Composition|Often used when a predictable and human-readable form of text is necessary, such as when displaying text in user interfaces or when storing text that must appear consistent to end-users|Remains the same|Stored as `é` (code `U+00E9`)|
  |`NFD`|Normalization Form Canonical Decomposition|Valuable in scenarios where text needs to be analyzed or processed at a character level, such as in search algorithms and text comparison operations, where diacritics and other modifiers need to be considered separately from their base characters|Remains the same|Stored as `e´` (codes `U+0065` and `U+0301`)|
  |`NFKC`|Normalization Form Compatibility Composition|Particularly useful in instances where a form of the text is required that is compatible across different systems, while still retaining the maximum amount of information possible. It's used in systems where compatibility is more important than textual accuracy, such as in keyword generation for search engines|Transformed into `K` to ensure compatibility across different systems|Stored as `é` (code `U+00E9`)|
  |`NFKD`|Normalization Form Compatibility Decomposition|Crucial for text analysis where compatibility and the most detailed decomposition are required, such as in cryptographic operations, indexing, and any application needing the most atomic form of characters|Transformed into `K` to ensure compatibility across different systems|Stored as `e´` (codes `U+0065` and `U+0301`)|

* These forms help in ensuring that Unicode characters are represented consistently in the database, during processing, and even when interfacing with other systems.
* Strings in a Unicode normalized form ensure that equivalent strings maintain a unique binary representation, naturally within the same normalization form applied.
  * For instance, in `NFC`, all characters are first decomposed, and then all combining sequences are systematically recomposed in a specific order as defined by the standard.

#### Which form should be used by default?

* The most common one is `NFC`. It is often recommended as the default choice because it is widely used and compatible with many systems and protocols.
  * It is actually considered the *normal* form of Unicode text on the web and in other computing environments, making it a safe default for general use.
* Alternatively, to avoid odd characters such as `＜` or `ⓩ`, the `NFKC` form can be applied, which replaces these characters with their standard equivalents (`<` and `z`).

## What potential security vulnerabilities are associated with Unicode normalization?

* Below are mentioned actual implications of vulnerabilities caused by a deficient Unicode normalization process.

### Account takeover

* In those web applications where users can sign up using usernames that appear identical but have different representations, they might lead to account takeover scenarios.
* For instance, the username `Amélie` can be represented in, at least, two different ways using the Unicode encoding standard:
  * The `é` character can be represented by the `U+00E9` code, providing a complete representation for `Amélie` as `\u0041\u006D\u00E9\u006C\u0069\u0065`.
  * The `é` can also be represented by breaking it down into an equivalent base letter `e`, with code `U+0065`, and combining acute accent `´`, with code `U+0301`, providing a complete representation for `Amélie` as `\u0041\u006D\u0065\u0301\u006C\u0069\u0065`.
  * These two characters, `é` and `é`, look the same, but do not compare as equal, and the strings have different lengths. In JavaScript:

    ```javascript
    console.log("\u00E9"); // => é
    console.log("\u0065\u0301"); // => é
    console.log("\u00E9" == "\u0065\u0301"); // => false
    console.log("\u00E9".length); // => 1
    console.log("\u0065\u0301".length); // => 2
    ```

* In this scenario, achieving a proper normalization of the string `Amélie` into a *canonical form* helps to avoid such discrepancies by ensuring that visually identical strings are treated as equivalent.
  * Using the previous example based on the `é` character, but with normalization applied, the outcome would be:

    ```javascript
    const str = "\u0065\u0301";
    console.log(str == "\u00E9"); // => false
    const normalized = str.normalize("NFC");
    console.log(normalized == "\u00E9"); // => true
    console.log(normalized.length); // => 1
    ```

### SQL injection filter bypass

* Taking as example a web application that constructs SQL queries using the character `'` along with user inputs, includes a security measure to remove all `'` characters from the input, and then applies Unicode normalization to the inputs after that deletion and before generating the queries, this scenario could inadvertently lead to a SQL injection vulnerability.
* A malicious user could insert a different Unicode character equivalent to `'` such as the fullwidth apostrophe `＇`, with code `U+FF07`, and when the input gets normalised, a single quote `'` is created, conducting to the SQL injection flaw.

### Cross-Site Scripting (XSS) filter bypass

* Another simple case where Unicode can be used to bypass security filters is changing the HTML brackets for Unicode brackets.
* For example, the HTML tag `<script>`, which used to inject javascript code by malicious users, can be replaced by `＜script＞` that uses the characters `＜`, with code `U+FF1C`, and `＞`, with code `U+FF1E`. Without an appropriate Unicode normalization process, both `<script>` and `＜script＞` can be considered equivalent at some point in the application, which can circumvent the security measures specified against the HTML tag `<script>`.

## Practical scenario

* Below is a code snippet demonstrating a use case sample.

### User changing its username

* It can be considered a web application that allows its users to change their own username as long as they do not choose a username that has already been taken by another user.

@@TagStart@@java

#### Code snippet in Java

* The `Normalizer` class provides the method `normalize` which transforms Unicode text into an equivalent composed or decomposed form, specified as the second parameter:

  ```java
  import java.text.Normalizer;

  public void changeUsername(String username){
    String normalizedUsername = Normalizer.normalize(username, Normalizer.Form.NFC);

    // Update logic here
  }
  ```

@@TagEnd@@
@@TagStart@@node.js

#### Code snippet in Node.js

* Since ES2015 JavaScript includes the built-in `String.prototype.normalize([form])` method which is supported in Node.js and all modern web browsers.
* The optional `form` argument specifies the string identifier of the normalization form to be used, defaulting to `NFC` if not passed.

  ```javascript
  function changeUsername(username) {
    const normalizedUsername = username.normalize();

    // Update logic here
  }
  ```

@@TagEnd@@

## What is the difference between normalization and canonicalization?

* Both methods aim to simplify the comparison of different representations of the same object, but one method takes a more in-depth approach.
* Normalization refers to the process of converting any representation of an object into a set of acceptable forms, known as normal forms. A normal form simply specifies the structure of the object, without the requirement of uniqueness.
  * This allows for comparison through a flexible process, accommodating variations that are considered equal within a context.
  * As an example, a certain normalization process might simply involve removing any non-alphabetic characters and substituting spaces with hyphens for all filenames that are provided by a user when uploading a file to a web application.
  * Considering the potential filenames `my document.pdf` and `MY DOCUMENT.pdf`, this would make both `my-document.pdf` and `MY-DOCUMENT.pdf` as resulting valid filenames, or even `My-Document.PDF` if the user provides `My Document.PDF`:
  ![Normalization process sample][1]
* Canonicalization is the process of turning any representation of an object into a sole, definitive version known as the canonical form, which is unique to each object.
  * Taking the same filenames `my document.pdf` and `MY DOCUMENT.pdf`, a canonicalization process could involve creating a unique version by not only removing any non-alphabetic characters and substituting spaces with hyphens, but also converting the entire filenames to lowercase, resulting `my-document.pdf` as the only acceptable filename, even when the user provides `My Document.PDF`:
  ![Canonicalization process sample][2]
  * In this case, to determine if two representations are of the same object, it's enough to compare their canonical forms for equality.
* Canonicalization provides a direct way to compare objects but can be challenging to apply uniformly, whereas normalization is more flexible for complex objects. For this reason, normalization might be preferable when it's difficult to consistently implement canonical forms.

## Quiz to consolidate :rocket:

* Complete the questionnaire by choosing the correct answer for each question.
  @@ExerciseBox@@

[1]: /static/images/learning/normalization-process-sample.png
[2]: /static/images/learning/canonicalization-process-sample.png
