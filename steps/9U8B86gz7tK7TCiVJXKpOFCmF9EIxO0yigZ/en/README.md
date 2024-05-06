# Input Normalization

* `Input normalization` is the procedure used to transform incoming data into a uniform or standardized format. This transformation is crucial for maintaining data integrity and ensuring consistent data handling across various components of a software system.
* In web applications, it helps in mitigating security risks by standardizing user input to prevent unexpected behavior or exploitation, such as injection attacks.

  > :warning: The `Input Normalization` must be done the first measure to be taken, otherwise it can arise other vulnerabilities or security measures can be bypassed.

## Unicode normalization forms

* Unicode provides several forms of normalization, such as `NFC`, `NFD`, `NFKC`, and `NFKD`, to meet different data processing needs. These forms help in ensuring that Unicode characters are represented consistently in the database, during processing, and even when interfacing with other systems.
* This consistency is vital not just for security purposes but also for functionality.
* If one is not sure which Unicode normalization form to use, `NFC` is often recommended as the default choice because it is widely used and compatible with many systems and protocols.
  * It is often considered the "normal" form of Unicode text on the web and in other computing environments, making it a safe default for general use.

### Normalization Form Canonical Composition (NFC)

* `NFC` is often used when a predictable and human-readable form of text is necessary, such as when displaying text in user interfaces or when storing text that must appear consistent to end-users.

### Normalization Form Canonical Decomposition (NFD)

* `NFD` is valuable in scenarios where text needs to be analyzed or processed at a character level, such as in search algorithms and text comparison operations, where diacritics and other modifiers need to be considered separately from their base characters.

### Normalization Form Compatibility Composition (NFKC)

* The `NFKC` is particularly useful in instances where a form of the text is required that is compatible across different systems, while still retaining the maximum amount of information possible. It's used in systems where compatibility is more important than textual accuracy, such as in keyword generation for search engines.

### Normalization Form Compatibility Decomposition (NFKD)

* `NFKD` is crucial for text analysis where compatibility and the most detailed decomposition are required, such as in cryptographic operations, indexing, and any application needing the most atomic form of characters.

## File Upload use case

* It can be considered a web application that have a file upload. In order to standardize the file name of the uploaded file, the following implementation should be followed.

### Implementation

* Implementation in Node.js:

```javascript
function handleFileUpload(filename) {
  normalizedFilename = filename.normalize("NFC");

  // Additional security measures

  // File upload logic
}
```

* Implementation in Java:

```java
public void handleFileUpload(String filename){
  String normalizedFilename = Normalizer.normalize(filename, Normalizer.Form.NFC);
  // Additional security measures

  // File upload logic
}
```
