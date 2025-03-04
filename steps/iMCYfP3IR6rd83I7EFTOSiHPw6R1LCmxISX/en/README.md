# Integrating malware scanning on file uploads with React and FortiWeb Cloud 24.3

* FortiWeb Cloud is a cloud-based Web Application Firewall (WAF) service provided by Fortinet, designed to protect web applications and APIs against various security threats such as SQL injection, Cross-Site Scripting (XSS), Denial-of-Service (DoS) attacks, and other common vulnerabilities, including those associated with file uploads.
* It is appropriate for organizations looking for robust, scalable, and easy-to-manage web application security, especially when managing multiple applications or services across different environments (cloud, on-premise, or hybrid).

## Exercise to practice :writing_hand:

* Behind this file upload form, there's backend code that mimics the conditions under which FortiWeb Cloud can scan a file based on the HTTP request format sent by the client.
* The goal here is to edit the source code opening the code editor via the `Open Code Editor` button and update the `sendFile` function in `app/src/send-file.js` to make a POST request via `axios`, returing the promise, to the `/upload` endpoint, with the purpose of uploading the file selected in the upload form after pressing the `Submit` button.
  * The backend code will send a `200 OK` status HTTP response if FortiWeb Cloud could have scanned the file, or a `400 Bad Request` status if it couldn't, along with a suitable message shown directly on the file upload form.
* **Note that updating the React application in the code editor requires recompiling the app and clicking the `reload` link in the form to load the newest JavaScript code in the browser.**
* To complete the exercise successfully, after entering the appropriate JavaScript code, use the form to upload one of the provided sample images.
  * This should send an HTTP request with the image under a parameter called `file` and receive a `200 OK` response, indicating that it could have been scanned by FortiWeb Cloud.

  @@ExerciseBox@@
