# Preventing CSRF using double-submit cookie pattern in Node.js 20 with Express.js and csrf-csrf

* The [`csrf-csrf` npm package][1] is a utility designed to implement stateless CSRF protection in Express.js applications using the double-submit cookie pattern. This approach involves the server generating a CSRF token and setting it as a cookie in the client's browser. The client must then include this token in subsequent requests, typically within a custom header or form field. The server validates the token by comparing the value in the request with the value stored in the cookie.
* This method provides CSRF protection without the need for server-side session storage, making it suitable for stateless applications.
* By utilizing `csrf-csrf`, applications can ensure that only legitimate requests originating from authenticated users are processed, effectively blocking unauthorized CSRF attempts.

## Specifying particular configuration settings

* When initializing the `doubleCsrf` object, multiple configuration options can be specified, including:

  ```javascript
  const { doubleCsrfProtection, generateToken, invalidCsrfTokenError } = doubleCsrf({
    ignoredMethods: ["GET", "HEAD", "OPTIONS"],
    getSecret: () => "secret-for-hashing-here",
    getSessionIdentifier: (req) => req.session.id,
    cookieName: "csrfToken",
    cookieOptions: {
      httpOnly: false
    },
    getTokenFromRequest: (req) => {
      const rawToken = req.headers["x-csrf-token"]; // Extract the raw CSRF token from the request headers
      const decodedToken = decodeURIComponent(rawToken); // Decode the token to handle URL-encoded characters
      const [token, signature] = decodedToken.split("|"); // Separate the token and its signature for validation

      return token;
    },
    size: 128
  });
  ```

  * `ignoredMethods`: specifies HTTP methods to exclude from CSRF protection.
  * `getSecret`: defines the secret used for hashing CSRF tokens.
  * `getSessionIdentifier`: links tokens to a user's session.
  * `cookieName`: sets the name of the cookie where the CSRF token is stored.
  * `cookieOptions`: configures cookie attributes like security and HTTP-only behavior.
  * `getTokenFromRequest`: extracts and decodes the token from client headers (i.e., `x-csrf-token`).
  * `size`: specifies the size of the generated tokens in bits (128 bits is secure and sufficient).

## Exercise to practice :writing_hand:

* The application below is vulnerable to CSRF attacks, as there is no protection that prevents a malicious site forcing a logged-in user to send a request to change their email to any arbitrary address.
* To demonstrate this scenario, log in to the application with valid credentials (i.e., username `johndoe` and password `a?S06Lx+SB[D`). Once logged in, check the current email address in the user's profile page, and then visit the *attacker website* tab in the simulated browser, which includes certain code that tries to change the user's email. Afterwards, confirm the email modification by reviewing the profile again.
* The purpose of this exercise is to edit the source code using the `Open Code Editor` button to implement a CSRF protection based on the double-submit cookie pattern via the `csrf-csrf` npm package. More specifically, the following steps must be accomplished to correctly support this functionality:
  * Make sure the POST `/login` endpoint sends a cookie named `csrfToken` in the HTTP response, containing a valid CSRF token associated with the user's session upon successful login. The cookie must be configured with the following attributes:
    * `httpOnly` set to `false`, so its value can be accessed by the application's frontend JavaScript.
    * `secure` **set to** `true` **and** `sameSite` **set to** `none`, as these flags are mandatory for setting cookies via an iframe, where the exercise is actually embedded.
    * The `iframeCookieOptions` variable can be utilized for this purpose:

      ```javascript
      cookieOptions: {
        ...iframeCookieOptions,
        httpOnly: false
      }
      ```

  * Update the PATCH endpoint `/change-email` to include protection against CSRF attacks, ensuring it returns a `403 Forbidden` status code if the HTTP request sent by the client does not include a valid CSRF token in the `x-csrf-token` header, which must match the token stored in the `csrfToken` cookie also sent in the request.
  * Be aware that the frontend client application automatically attempts to retrieve a CSRF token from the `csrfToken` cookie and, if successful, adds it to the `x-csrf-token` header before sending the PATCH request to update the email, thus **eliminating the need for any frontend modification**:

    ```javascript
    const csrfToken = Cookies.get("csrfToken") || "";
    
    axios({
      url: "/change-email",
      method: "PATCH",
      headers: {
        "content-type": "application/json",
        "x-csrf-token": csrfToken
      },
      data: {
        username,
        currentEmail,
        newEmail
      }
    })
    ```

* After applying the changes, click the `Verify Completion` button to validate the exercise has been completed.

  @@ExerciseBox@@

[1]: https://www.npmjs.com/package/csrf-csrf
