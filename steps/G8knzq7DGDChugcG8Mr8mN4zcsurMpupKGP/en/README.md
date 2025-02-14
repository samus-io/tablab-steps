# Preventing CSRF using synchronizer token pattern in Node.js 20 with Express.js and csrf-sync

* The [`csrf-sync` npm package][1] is a lightweight and straightforward library designed to mitigate `Cross-Site Request Forgery (CSRF)` attacks by implementing the synchronizer token pattern. This package simplifies the process of integrating CSRF protection into Express.js applications by generating and validating CSRF tokens that are stored on the server-side and must be included in client requests to perform sensitive actions.
* By utilizing `csrf-sync`, applications can ensure that only legitimate requests originating from authenticated users are processed, effectively blocking unauthorized CSRF attempts.

## Specifying particular configuration settings

* When initializing the `csrfSync` object, multiple configuration options can be specified, including:

  ```javascript
  const { generateToken, csrfSynchronisedProtection, invalidCsrfTokenError } = csrfSync({
    ignoredMethods: ["GET", "HEAD", "OPTIONS"],
    getTokenFromState: (req) => req.session.csrfToken,
    getTokenFromRequest: (req) => req.headers["x-csrf-token"],
    storeTokenInState: (req, token) => (req.session.csrfToken = token),
    size: 128
  });
  ```

  * `ignoredMethods`: defines the HTTP methods to exclude from CSRF protection, such as safe methods (`GET`, `HEAD`, `OPTIONS`).
  * `getTokenFromState`: retrieves the CSRF token from the server's state (i.e., user session).
  * `getTokenFromRequest`: extracts the CSRF token from the client's request headers (i.e., `x-csrf-token`).
  * `storeTokenInState`: stores the generated CSRF token in the server state (i.e., attaches it to the user's session).
  * `size`: specifies the size of the generated tokens in bits (128 bits is secure and sufficient).

## Exercise to practice :writing_hand:

* The application below is vulnerable to CSRF attacks, as there is no protection that prevents a malicious site forcing a logged-in user to send a request to change their email to any arbitrary address.
* To demonstrate this scenario, log in to the application with valid credentials (i.e., username `johndoe` and password `faBk;bhj7>QL`). Once logged in, check the current email address in the user's profile page, and then visit the *attacker website* tab in the simulated browser, which includes certain code that tries to change the user's email. Afterwards, confirm the email modification by reviewing the profile again.
* The purpose of this exercise is to edit the source code using the `Open Code Editor` button to implement a CSRF protection based on the synchronizer token pattern via the `csrf-sync` npm package. More specifically, the following steps must be accomplished to correctly support this functionality:
  * Add a GET endpoint under the `/csrf-token` route that returns the CSRF token associated with the user's session. This endpoint should permit only authenticated users and respond with `401 Unauthorized` status code response for unauthorized attempts. Legitimate requests should return a JSON object such as `{ "csrfToken": "<csrf_token_value>" }` that provides the CSRF token attached to the user's session.
  * Update the PATCH endpoint `/change-email` to include protection against CSRF attacks, ensuring it returns a `403 Forbidden` status code if the HTTP request sent by the client does not include a valid CSRF token in the `x-csrf-token` header, which must match the token stored on the server-side.
  * Be aware that the frontend client application automatically attempts to retrieve a CSRF token from the `/csrf-token` endpoint and, if successful, adds it to the `x-csrf-token` header before sending the PATCH request to update the email, thus eliminating the need for any frontend modification.
* After applying the changes, click the `Verify Completion` button to validate the exercise has been completed.

  @@ExerciseBox@@

[1]: https://www.npmjs.com/package/csrf-sync
