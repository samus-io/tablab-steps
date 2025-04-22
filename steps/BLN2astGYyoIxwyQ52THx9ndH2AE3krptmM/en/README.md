# Enforcing file name sanitization in Java Jakarta

* Sanitizing file names involves reviewing and potentially modifying incoming file names to prevent security threats or operational issues that could compromise system integrity.
* Using UUIDs or similar random identifiers for file storage eliminates the need for sanitizing file names. However, if business requirements prevent this, proper sanitization should be applied.

## Exercise to practice :writing_hand:

* The application below allows users to upload files without enforcing any control over the file name, directly using the `filename` value during storage.
* The goal here is to modify the source code by clicking the `Open Code Editor` button and integrate a strong, secure file name sanitization mechanism that fulfills the outlined criteria:
  * Disallow reserved names and strip unsafe characters, preserving only alphanumeric characters, dots, and hyphens (i.e., `A-Za-z0-9.-`).
  * Remove leading and trailing dots to avoid hidden files or path-related exploits.
  * Normalize file names by transforming casing to lowercase for uniformity across environments.
  * Set a file name length limit of 100 characters.
* The `doPost` function found in `src/main/java/io/ontablab/FileUploadServlet.java` is the main place where changes need to be implemented to enable this functionality.
* **It is important to note that, in this case, there is no need to implement any mechanism for handling file name collisions**.
* After making the changes, press the `Verify Completion` button to confirm that the exercise has been completed.

  @@ExerciseBox@@
