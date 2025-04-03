# Information disclosure through sensitive query strings in URL using Express in Node.js and React Router

* This vulnerability is present when sensitive data such as usernames, passwords, session identifiers, tokens, or other potentially critical information is passed through the URL.

## Exercise to practice :writing_hand:

* The following application transmits the email via URL when a user accesses their profile page, resulting in an information disclosure vulnerability. This can be observed by logging into the application using valid credentials (i.e., username `johndoe` and password `LSu:IL95=ViU`).
* This exercise aims to modify the source code via the `Open Code Editor` button by updating the communication method with the `/profile` endpoint from a GET request to a POST request, and effectively addressing the issue of information disclosure via sensitive query strings in the URL.
* More specifically, the following steps must be accomplished to correctly support this functionality:
  * The frontend React application requires modification to send a POST request to the `/profile` API endpoint instead of a GET request. These updates involve applying changes to the `Profile.jsx` file at `/client/src/pages/Profile.jsx` and `Login.jsx` file at `/client/src/pages/Login.jsx`.
  * The `/profile` route in the Node.js Express backend should also be adjusted to support POST requests and obtain the email value from the body rather than the URL.
* **Note that any updates made to the React or Node.js code in the editor require a redeployment to take effect. In addition, the React frontend requires using the `reload` link found in the application to refresh the JavaScript code in the browser**.
* After applying the changes, click the `Verify Completion` button to validate the exercise has been completed.

  @@ExerciseBox@@
