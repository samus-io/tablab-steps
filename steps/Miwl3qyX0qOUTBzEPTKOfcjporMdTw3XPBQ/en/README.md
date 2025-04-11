# Enforcing file extension restrictions through allow-list validation in Node.js

* An allow-list validation strategy involves creating a list of approved values or characters considered as safe, rejecting any input that doesn't conform to the list in order to maintain data integrity and security.

## Exercise to practice :writing_hand:

* The existing application enables users to upload any file type. The goal here is to modify the source code by clicking the `Open Code Editor` button and to implement a server-side allow-list validation strategy that limits uploads to files with the extensions `.jpg`, `.jpeg`, and `.png`.
* More precisely, the `/upload` POST endpoint of the Express application in `app.js` should have code modifications to support this functionality.
* The application should return a `400` status code response when a user uploads a file with an extension other than `.jpg`, `.jpeg`, and `.png`.
  @@ExerciseBox@@
