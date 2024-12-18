# Best practices to prevent CSRF vulnerabilities

* Implementing a `Defense-in-Depth (DiD)` strategy is crucial to effectively prevent Cross-Site Request Forgery (CSRF) vulnerabilities. Applying multiple layers of security reduce the chances of successful exploitation.

## Do not use GET for state-changing operations

* Avoid using GET method for requests that modify data or change application state.
* GET requests are intended solely for retrieving information and should not trigger actions like updating user details, deleting data, or making payments.
* Browsers often prefetch or automatically trigger GET requests (e.g., when loading an image or following a link). If a GET request is used for state-changing operations, attackers can craft malicious URLs to trick users into performing unintended actions.

## Request for authentication before state-changing operations

* When performing critical state-changing operations, such as modifying user data, transferring funds, or processing payments, require additional authentication from the user.
* For example, prompt the user to re-enter their password or verify using their 2FA method.
* This will not only help prevent CSRF attacks, but will also help mitigate the impact of other potential vulnerabilities.

## Anti CSRF tokens

* An anti-CSRF token (also called a CSRF token) is a security mechanism designed to protect web applications from Cross-Site Request Forgery (CSRF) attacks.
* It works by ensuring that requests to a web application are legitimate and intentional, preventing maliciously forged requests initiated by attackers.
* When a user interacts with a website—for example, submitting a form to change a password—the server generates a unique, random token and embeds it in the form. This token acts like a secret passcode shared between the web application and the user's browser.
* When the form is submitted, the server-side application verifies the token included in the request. If the token is missing, incorrect, or invalid, the server rejects the request.

### Synchronizer token pattern

* The synchronizer token pattern is a widely used anti-CSRF technique where the web application generates a unique token for each user session and embeds it in all forms and requests requiring user action. This token is validated on the server side to ensure the request originates from the legitimate user.
* Anti-CSRF tokens must meet the following criteria:
  * Nonce (number used once): The token must be unique for each session or request and cannot be reused.
  * Unpredictable: Tokens should be random and difficult for attackers to guess.
  * Session-tied: Each token should be associated with a specific user session.
  * Strictly validated: The server must validate the token before executing the associated action.
* When rendering a form for the user, the web application should follow these steps:
  1. Generate a unique token
  1. Include the token as a hidden input field within the HTML form:

    ```html
    <input type="hidden" name="csrf-token" value="z0UtF3Ck4GBHZFTG3tjzMfX22PkAQk8f" />
    ```

  1. When the form is submitted, the server-side application checks that:
      * The token matches the one previously generated and associated with the session.
      * The token has not expired or been tampered with.

### Double-Submit cookie pattern

* If maintaining the state for CSRF token on the server is problematic, you can use an alternative technique known as the double submit cookie pattern. This technique is easy to implement and is stateless.
* The most secure implementation of the Double Submit Cookie pattern is the Signed Double-Submit Cookie, which uses a secret key known only to the server.

#### How it works

* The double-submit cookie pattern works by ensuring that the client (browser) sends two copies of a CSRF token—one as a cookie and the other as a request parameter (e.g., in a form field or header). The server validates that both values match to confirm the legitimacy of the request.
* This is the workflow of this pattern:
  1. When a user logs in or starts a session, the server generates a CSRF token and set it as a cookie (without `httpOnly` flag).
  1. When the user submits a form to the server, the browser will send the CSRF token cookie.
  1. Also, the form will include the same token as a request parameter
  1. Finally, the server compares the CSRF cookie with the CSRF token sended in the form. If they do not match (or one is missing), the server rejects the request.

* This type of protections take advantage that only the same domain can access to the cookies.

## SameSite attribute

* The `SameSite` cookie attribute is a security measure that restricts how cookies are sent with cross-site requests. Its primary purpose is to mitigate the risk of cross-origin information leakage and reduce the likelihood of CSRF attacks.
* However, it is important to note that the `SameSite` attribute does not completely prevent CSRF on its own, it only reduces the attack surface by controlling when cookies are included in requests.
* The `SameSite` attribute instructs browsers when to send cookies, depending on whether the request originates from the same site or a cross-site source. The attribute can have the following values:
  * `Strict`: Cookies are sent only with same-site requests; cross-site requests do not include cookies.
  * `Lax`: Cookies are sent with same-site requests and user-initiated cross-site navigation (e.g., clicking a link), but not with embedded content (e.g., images, iframes).
  * `None`: Cookies are sent with both same-site and cross-site requests, but the `Secure` attribute must also be set to ensure transmission over HTTPS.
