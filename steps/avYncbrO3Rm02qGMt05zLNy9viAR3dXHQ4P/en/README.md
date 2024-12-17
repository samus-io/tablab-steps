# Enforcing access control to password change functionalities in Node.js

* An IDOR vulnerability arises when an attacker can use a direct reference to access or alter an unauthorized object. A common example involves web applications that allow viewing or altering sensitive data via simple requests. In such cases, failure to verify the requester's permissions can allow unauthorized users to access or manipulate account information.

## Exercise to practice :writing_hand:

* The following application lacks proper access control, as no server-side protections exist to mitigate an IDOR vulnerability that lets an authenticated user change other users' passwords, potentially resulting in account takeover.
* In this particular application, a malicious user could use `curl` in the terminal to authenticate to the application with valid credentials (i.e., username `johndoe` and password `VcW;seD8qYEn`) sending a request to the `/login` endpoint and considering `$APP_URL` an environment variable that represents the base path of the application:

  ```bash
  curl -s -i -X POST \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode 'username=johndoe' \
    --data-urlencode 'password=VcW;seD8qYEn' \
    $APP_URL/login | sed -n -e '/^HTTP\/[0-9.]* [0-9]*/p' -e '/^set-cookie:.*sessionId=/Ip'
  ```

  After obtaining a response, the `sessionId` cookie can be retrieved. If the response indicates success with an HTTP `200 OK` status code, this cookie can be used to interact with authenticated-only endpoints.

  Malicious users will be able then send a PATCH request to the `/change-password` endpoint, providing the new password value for the specified username and including the `sessionId` cookie obtained earlier:

    ```bash
    curl -s -i -X PATCH \
      -H 'Content-Type: application/json' \
      -d '{ "username": "johndoe", "newPassword": "123456" }' \
      -b 'sessionId=<session_cookie_value>' \
      $APP_URL/change-password | sed -n '/^HTTP\/[0-9.]* [0-9]*/p'
    ```

  Due to an IDOR vulnerability, providing a direct reference to an existing username in the database, like `jackson01`, `jennifer`, `alice99`, or `dianak`, would result in changing their password and permitting login with the updated credentials.
* The purpose of this exercise is to modify the source code using the `Open Code Editor` button to implement server-side access control, ensuring users can only change their own password and returning a `401 Unauthorized` status code for unauthorized attempts.
  * More precisely, the `/change-password` PATCH endpoint of the Express application in `app.js` should have code modifications to support this functionality.
* After making the changes, press the `Verify Completion` button to confirm that the exercise has been completed.

  @@ExerciseBox@@
