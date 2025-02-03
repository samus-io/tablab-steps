# Best practices to prevent CSRF vulnerabilities

* Implementing a `Defense-in-Depth (DiD)` strategy is crucial to effectively prevent CSRF vulnerabilities. This approach involves applying multiple layers of security to reduce the likelihood of successful exploitation.

## Do not use GET for state-changing operations

* GET requests should only be used for retrieving information and must not trigger actions that modify data or change the application state like updating user details, deleting data, or making payments.
* Browsers frequently prefetch or automatically trigger GET requests for various reasons, such as loading resources (e.g., images or scripts) or following hyperlinks. If a GET request is used for state-changing operations, attackers can exploit this by crafting malicious URLs that perform unintended actions when a user clicks them.
* Although it is technically possible to include a CSRF token as a GET parameter, it is not recommended due to significant security risks:
  * URLs containing CSRF tokens are often logged by web servers, proxies, or analytics tools. If a user clicks on a link or visits an insecure page, the token could be exposed via referrer headers.
  * Attackers could intercept or recover tokens embedded in URLs, enabling them to bypass CSRF protection.
* However, there are scenarios where using the GET method for state-changing operations is necessary for the application to function properly.
  * For instance, when a user signs in, the application might send a confirmation email containing an activation link. Clicking this link typically triggers a state-changing operation, such as activating the user's account.
  * In such cases, the GET method is often chosen because it allows seamless interaction and provides a user-friendly experience. However, extra security measures, such as using time-limited, one-time-use tokens in the activation link, should be implemented to mitigate potential risks.

## Request for authentication before state-changing operations

* When performing critical state-changing operations, such as modifying user data, transferring funds, or processing payments, require additional authentication from the user to ensure the action is intentional.

* Common examples of additional authentication mechanisms include:
  * Prompting the user to re-enter their password.
  * Verifying the action through Two-Factor Authentication (2FA), such as a one-time password (OTP) or authenticator app.
* By introducing a secondary verification step, the server ensures that the action is performed by the legitimate user, not a malicious request.
* This additional authentication step not only provides robust protection against CSRF attacks but also serves as a critical safeguard against other potential security vulnerabilities.

## Anti CSRF tokens

* An anti-CSRF token (also called a CSRF token) is a security mechanism designed to protect web applications from CSRF.
* It works by ensuring that requests to a web application are legitimate and intentional, preventing attackers from forging unauthorized requests on behalf of authenticated users.
When a user interacts with a web application (e.g., submitting a form to change their password), the server generates a unique, random token and embeds it in the form. This token serves as a secret passcode shared between the web application and the user's browser.
* Upon form submission, the server validates the token included in the request. If the token is missing, incorrect, or tampered with, the server rejects the request to prevent unauthorized actions.

### Synchronizer token pattern

* The synchronizer token pattern is one of the most widely used techniques for implementing anti-CSRF protection. In this method, the web application generates a unique token for each user session and embeds it in every form or request requiring user action. The token is validated on the server side to ensure the request originates from the legitimate user.
* Anti-CSRF tokens must meet the following criteria to effectively prevent CSRF attacks:
  * Nonce (number used once): each token must be unique for every session or request to ensure it cannot be reused by an attacker.
  * Unpredictable: tokens must be generated randomly, making them impossible to guess.
  * Session-tied: every token must be associated with a specific user session to ensure validity.
  * Strictly validated: the server must validate the token before executing the associated action.
* When rendering a form for a user, the web application should follow these steps to implement the synchronizer token pattern:
  1. Generate the CSRF token
  1. Include the token as a hidden input field within the HTML form:

    ```html
    <input type="hidden" name="csrf-token" value="z0UtF3Ck4GBHZFTG3tjzMfX22PkAQk8f" />
    ```

  1. When the form is submitted, the server-side application checks that:
      * The token matches the one previously generated and associated with the session.
      * The token has not expired or been tampered with.

### Double-submit cookie pattern

* If maintaining the state for CSRF tokens on the server is problematic, the double-submit cookie pattern provides an alternative technique. This method is stateless, meaning it does not require storing tokens on the server, and it is relatively simple to implement.
* The most secure implementation of this pattern is the signed double-submit cookie, which uses a secret key known only to the server for verifying the token's authenticity.

#### How it works

* The double-submit cookie pattern works by ensuring that the client (browser) sends two copies of a CSRF token, one as a cookie and the other as a request parameter (e.g., in a form field or header). The server validates that both values match to confirm the request's legitimacy.
* The following steps outline how the double-submit cookie pattern works to ensure the validity of requests and prevent CSRF attacks:
  1. When a user logs in or starts a session, the server generates a unique CSRF token and sets it as a cookie, which does not include the `httpOnly` flag to allow client-side access.
  1. When the user submits a form or performs a state-changing action, the browser automatically sends the CSRF token cookie along with the request as part of its standard behavior.
  1. The form or request also includes the same token explicitly as a request parameter, such as in a hidden input field or a custom header.
  1. Finally, the server validates the request by comparing the CSRF token from the cookie with the token from the request parameter, rejecting the request if the tokens do not match or one is missing.
* The pattern relies on the Same-Origin Policy (SOP), which ensures that only the domain that issued the cookie can access it.

#### Using HMAC CSRF tokens

* To create CSRF tokens that are stateless, eliminating the need for the server to store them, they can be generated as a series of values that are either hashed or encrypted.
* This approach ensures that attackers cannot forge or inject a valid CSRF token into a victim's authenticated session.
* The Hash-based Message Authentication Code (HMAC) algorithm is strongly recommended because it is less computationally intensive than encryption and decryption while maintaining high security. Similar to the synchronizer token pattern, the generated token must be tied to the user’s session.
* To generate HMAC CSRF tokens tied to a session, the system requires the following components:
  * A session-dependent value that changes with each login session to ensure uniqueness.
  * A secret cryptographic key known only to the server for token generation and validation.
  * A cryptographically random value to prevent collisions and improve token unpredictability.
* Unlike some other implementations, this approach does not require a timestamp, as the CSRF token must be regenerated with each new session, ensuring freshness.
* The following pseudocode is an example on how to generate HMAC CSRF tokens:

  ```
  // Gather the values to craft the CSRF token
  hmacSecret = readEnvironmentVariable("CSRF_SECRET") // HMAC secret key
  userSessionID = session.sessionID // Current authenticated user session
  randomValue = cryptographic.randomValue() // Cryptographic random value

  // Create the CSRF Token
  payload = userSessionID.length + ":" + userSessionID + ":" + randomValue.length + ":" + randomValue // HMAC payload
  hmacHash = generateHMAC("SHA256", hmacSecret, payload) // Generate the HMAC hash
  csrfToken = hmacHash + "." + randomValue // Combine the HMAC hash and random value to form the CSRF token

  // Set the CSRF token as a cookie without HttpOnly flag as the frontend will need to access the Cookie
  response.setCookie("csrf_token=" + csrfToken + "; Secure")
  ```

## SameSite cookie attribute

* The `SameSite` cookie attribute is a security feature designed to control how cookies are sent with cross-site requests. Its primary purpose is to mitigate the risk of cross-origin information leakage and reduce the likelihood of CSRF attacks.
* However, it is crucial to understand that the `SameSite` attribute does not completely prevent CSRF on its own. Instead, it reduces the attack surface by restricting the conditions under which cookies are included in requests.
* The `SameSite` attribute instructs browsers when to send cookies, depending on whether the request originates from the same site or a cross-site source. The attribute can have the following values:
  * `Strict`: cookies are sent only with requests originating from the same site that set the cookie. Requests from cross-site sources, even with the same domain but a different scheme or port, do not include cookies.
  * `Lax`: cookies are sent with same-site requests and user-initiated cross-site navigation (e.g., clicking a link), but they are excluded from requests initiated by embedded content (e.g., images, iframes).
  * `None`: cookies are sent with both same-site and cross-site requests, but this setting requires the `Secure` attribute to ensure that cookies are transmitted only over HTTPS connections.

## Delegating CSRF token handling to frameworks

* Implementing anti-CSRF tokens is a complex and detail-oriented task that requires significant effort to ensure every request includes and validates the CSRF token correctly.
* By leveraging an established framework, developers can benefit from prebuilt, comprehensive, and up-to-date security features, reducing the risk of errors and vulnerabilities.
* Using a framework also ensures that the web application adheres to industry best practices, allowing developers to focus on other aspects of the application while maintaining strong CSRF protection.
