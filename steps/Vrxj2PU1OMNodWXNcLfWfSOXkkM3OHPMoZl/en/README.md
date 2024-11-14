# General best security practices when uploading files

* A `Defense-in-Depth (DiD)` strategy is essential to ensure a secure file upload function tailored to specific business requirements. Multiple security techniques should be applied, as there is no universal measure to fully protect this functionality.

  > :warning: When implementing file upload functionalities, ensure uploaded files successfully complete all security inspections before any processing steps are taken. If a file breaches any security conditions, discard the file and the request returning an error message.

## Security measures checklist

* [ ] Ensure that any existing general input validation process is performed prior to other validation steps listed below.
* [ ] Set a file name length limit and restrict the allowed characters or use an application-generated file name when storing the file if feasible.
* [ ] Define a list of allowed file extensions, ensuring only safe and business-required extensions are permitted.
* [ ] Set a file size limit.
* [ ] Validate the file type based on its actual data, not trusting the `Content-Type` header or the magic number, as both can be easily spoofed.
* [ ] Test the file for malicious content by running it through an antivirus or sandbox to ensure it doesn't contain harmful data.
* [ ] Ensure that file uploads are restricted to authorized users whenever possible.
* [ ] Store the files on a different server or service, but if that isn't an option, store them outside the webroot.
* [ ] In the case of public access to the files, prevent path/URL guessing (e.g., using random file names or an internal mapping system).
* [ ] Protect the file upload from `Cross-Site Request Forgery (CSRF)` attacks.
* [ ] Verify that the libraries used are securely configured and regularly updated.

## Security measures adopted

### File name sanitization

* When storing files, the application should generate a random name instead of relying on the user's file name. If the original name is required for functionality, ensure it contains no special characters to prevent security vulnerabilities like path traversal by using an allow-list.
* The best practice is to replace the user-provided file name with a consistent, randomly generated string by the web application, such as using the UUID format to prevent collisions that could result in overwriting existing files.
* If the web application needs to retain the user's original file name, it is recommended to implement the following security measures:
  * Restrict the allowed characters (e.g., permit only alphanumeric characters), and exclude special characters from the list (except `-` or `_`).
  * Set a maximum length (e.g., 200 characters).
  * To prevent file name collisions, verify that the file name does not already exist before saving it.
  * Avoid reserved file names in Windows (`CON`, `PRN`, `AUX`, `NUL`, `COM0-COM9`, `LPT0-LPT9`).

### File extension validation

* File extension validation should guarantee that only the file extensions needed for the application and business requirements are allowed, while blocking all others.
* When the upload feature is designed for a single file type (such as only PDFs), the best practice is to define the allowed extension on the server-side, avoiding dependence on the user's input.
* If it's not feasible to control the extension in the backend, a commonly used approach is to check the extension against an approved allow-list.
  * Careful consideration is essential for this verification, as various techniques can be employed to bypass a deficient comparison (e.g., ensure that the file has only one extension while blocking files with more than one extension).
* Additionally, files without extensions should generally not be allowed, as they could potentially be used to upload web server configuration files.

### File content validation

* Uploaded files may include malicious, inappropriate, or illegal content.
* Scanning file contents is often time-consuming and complex due to the diversity of file types or the potential presence of embedded malware. Therefore, the best solution is to rely on third-party frameworks or services.
* In addition, certain Web Application Firewalls (WAFs) include tools to check files for malware when they are uploaded via web application submission forms.

### File storage location and filesystem permissions

* Files should remain in memory or a temporary storage area during processing and be moved to a permanent location only once they've completed and passed the validation checks.
* Whenever possible, files should be stored on a separate service or dedicated server to handling file storage to minimize the impact of potential vulnerabilities.
  * If this isn't feasible, then store the files outside the webroot to prevent direct access via URL.
  * In cases where files need to be publicly accessible, use a handler to map file names inside the application.
* Permissions on the file storage should be limited to control what users can do with uploaded files, typically allowing only read and write access for files such as images or documents, and blocking execute permissions.
  * In all circumstances, especially when execution is required, scanning the file prior to storage is advised as a best practice to detect and prevent macros, hidden scripts, or any form of malware.

### Enforcing authentication and authorization

* File upload capabilities should be protected with authentication and authorization whenever possible, ensuring that only authorized users can access them.
* If granting read permissions on uploaded files to corporate users is required, it is advised to implement authorization controls to restrict access to authorized users, instead of relying solely on superficial parameters like internal IPs.

### Using proven frameworks for handling file upload preprocessing

* Implementing a secure file upload mechanism is a complex task that requires careful attention to numerous details and potential vulnerabilities and can be time-consuming. By using an established framework, the application can benefit from comprehensive and up-to-date security features, and ensure that the web application adheres to best practices.
* These frameworks may offer a variety of built-in validation features, such as file name sanitization, file type checks, content validation, and more, designed to address a wide range of security requirements.
* While the idea of manually building validation mechanisms may be tempting, leveraging established frameworks is often a better approach.

## Quiz to consolidate :rocket:

* Complete the questionnaire by choosing the correct answer for each question.
  @@ExerciseBox@@
