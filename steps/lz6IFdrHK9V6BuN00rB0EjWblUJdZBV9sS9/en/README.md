# Preventing CSRF using double-submit cookie pattern in Node.js 20 with Express.js

* TODO

## Exercise to practice :writing_hand:

* The application below is vulnerable to CSRF attacks, as there is no protection that prevents a malicious site forcing a logged-in user to send a request to change their email to any arbitrary address.
* To demonstrate this scenario, log in to the application with valid credentials (i.e., username `johndoe` and password `a?S06Lx+SB[D`). Once logged in, check the current email address in the user's profile page, and then visit the *attacker website* tab in the simulated browser, which includes certain code that tries to change the user's email. Afterwards, confirm the email modification by reviewing the profile again.
* The purpose of this exercise is to edit the source code using the `Open Code Editor` button to implement a CSRF protection based on the double-submit cookie pattern via the `csrf-csrf` npm package. More specifically, the following steps must be accomplished to correctly support this functionality:
  * Make sure the POST `/login` endpoint sends a cookie named `csrfToken` in the HTTP response, containing a valid CSRF token associated with the user's session upon successful login. The cookie must be configured with the following attributes:
    * `httpOnly` set to `false`, so its value can be accessed by the application's frontend JavaScript.
    * `secure` set to `true` and `sameSite` set to `none`, as these flags are mandatory for setting cookies via an iframe, where the exercise is actually embedded. The `iframeCookieOptions` variable can be utilized for this purpose.
  * Update the PATCH endpoint `/change-email` to include protection against CSRF attacks, ensuring it returns a `403 Forbidden` status code if the HTTP request sent by the client does not include a valid CSRF token in the `x-csrf-token` header, which must match the token stored in the `csrfToken` cookie also sent in the request.
  * Be aware that the frontend client application automatically attempts to retrieve a CSRF token from the `csrfToken` cookie and, if successful, adds it to the `x-csrf-token` header before sending the PATCH request to update the email, thus eliminating the need for any frontend modification.
* After applying the changes, click the `Verify Completion` button to validate the exercise has been completed.

  @@ExerciseBox@@
