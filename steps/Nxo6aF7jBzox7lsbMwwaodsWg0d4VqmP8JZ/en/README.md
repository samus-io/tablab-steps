# Best practices to prevent CSRF vulnerabilities

* Preventing CSRF vulnerabilities effectively requires a `Defense-in-Depth (DiD)` strategy, which applies layered security measures to reduce the likelihood of successful attacks.

## Security measures checklist

* [ ] Require additional authentication before executing critical state-changing operations.
* [ ] Verify whether the web framework in use includes built-in CSRF protection and enable it.
* [ ] In the absence of built-in CSRF protection, implement a CSRF defense mechanism by using the synchronizer token pattern for stateful applications and the double submit cookie pattern for stateless applications.
  * [ ] In both cases, use JavaScript to insert the CSRF token into a custom HTTP request (e.g., `x-csrf-token`) header instead of placing it in a hidden form field, as requests with custom headers are inherently restricted by the `Same-Origin Policy (SOP)`.
* [ ] Set the `SameSite` attribute for session cookies to `Lax` or `Strict` mode.
* [ ] Avoid using GET for state-changing operations, as it may enable CSRF under the `SameSite=Lax` cookie configuration and expose CSRF tokens through browser history, log files, network utilities that log HTTP request headers, the `Referer` header when linking to external sites.
* [ ] Review CORS configuration to ensure it does not allow cross-origin requests while dynamically reflecting the origin (`Access-Control-Allow-Origin: https://attacker.com`) and permitting credentialed requests (`Access-Control-Allow-Credentials: true`), as this would enable cross-origin JavaScript to access HTTP responses from an authenticated session.

## Request for authentication before critical state-changing operations

* When performing critical state-changing operations, such as modifying user data, transferring funds, or processing payments, require additional authentication to verify the user's intent and double confirm their identity.
* Common additional authentication mechanisms include requiring users to re-enter their password, primarily for modifying account details, and verifying actions through `Two-Factor Authentication (2FA)`, often used for fund transfers and payment processing.
* This authentication requirement effectively mitigates CSRF attacks by preventing unauthorized actions and verifying user intent while also acting as an important security control against other potential vulnerabilities.

## Use built-in CSRF protections

* Implementing an anti-CSRF token mechanism can lead to a complex and detail-oriented task, requiring significant effort to ensure each request properly includes and validates the CSRF token. Leveraging an established framework provides developers with prebuilt, comprehensive, and up-to-date security features, reducing the risk of errors and vulnerabilities.
* Employing a framework also ensures that the web application adheres to industry best practices, allowing developers to focus on other aspects of the application while maintaining strong CSRF protection.
* As example, built-in CSRF protection middleware is available in frameworks such as Django (Python) and Laravel (PHP), where it is automatically enabled by default.

## Employ anti-CSRF tokens

* An anti-CSRF token, also simply known as a CSRF token, is a security feature that safeguards web applications against CSRF attacks by ensuring that all requests are legitimate and intentional, preventing attackers from executing unauthorized actions on behalf of authenticated users.
* When a user performs an action on a web application (e.g., submitting a email change form), the server generates a distinct, random token that is delivered to the frontend application in the user's browser, functioning as a shared secret between the application and the user's browser.
* As part of form submission, the frontend application ensures that the token is attached to the HTTP request, allowing the server to validate it. If the token is missing, incorrect, or manipulated, the request is rejected to prevent unauthorized actions.
* Anti-CSRF tokens must adhere to the following criteria to ensure effective protection against CSRF attacks:
  * Nonce (a number used once and then discarded): each token must be unique for every user's session to ensure they cannot be reused.
  * Unpredictable: tokens must be generated randomly, making them impossible to guess.
  * Session-tied: each token must be uniquely generated for a session and remain valid only within that session.
  * Strictly validated: the server must validate the token before executing the associated action.

### Synchronizer token pattern

* The synchronizer token pattern has been the most commonly used technique for implementing anti-CSRF protection. In this approach, a unique token is generated for each user session and traditionally embedded in every form requiring state-changing operations. When the frontend application sends the corresponding HTTP request, the server retrieves the token from the request body and validates it to confirm that the request originates from the legitimate user.

#### Synchronizer token pattern in SSR applications

* When rendering a form in applications using `Server-Side Rendering (SSR)`, the web application should ensure the proper implementation of the synchronizer token pattern by following these steps:
  1. Generate the CSRF token for each user session and store it securely (e.g., in a database or server-side session storage).
  1. Include the token as a hidden input field within the HTML form:

      ```html
      <input type="hidden" name="csrf-token" value="z0UtF3Ck4GBHZFTG3tjzMfX22PkAQk8f" />
      ```

  1. When the form is submitted, the server-side application should ensure that the received token exactly matches the one previously generated and is properly associated with the correct session.

#### Synchronizer token pattern in SPA applications

* In `Single Page Applications (SPAs)`, implementing the synchronizer token pattern for requires a different approach than traditional SSR applications. Since SPAs primarily rely on JavaScript for rendering and making API requests, CSRF tokens must be managed and transmitted securely through API calls.
* Ensuring the correct implementation of the synchronizer token pattern in an SPA involves adhering to these steps:
  1. Generate the CSRF token for each user session and store it securely (e.g., in a database or server-side session storage).
  1. Provide an endpoint to call and retrieve the CSRF token (e.g., `/api/csrf-token`):

      ```javascript
      app.get("/api/csrf-token", authMiddleware, (req, res) => {
        const csrfToken = generateToken(req); // Generate and store token in session
        res.json({ csrfToken });
      });
      ```
  
  1. Fetch and attach the CSRF token in every state-changing request (e.g., `POST`, `PUT`, `DELETE`):

      ```javascript
      const csrfToken = await fetch("/api/csrf-token", { credentials: "include" })
        .then((response) => response.json())
        .then((data) => data.csrfToken);
      ```

      ```javascript
      const response = await fetch("/api/change-email", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              "x-csrf-token": csrfToken
          },
          body: JSON.stringify({ email: newEmail }),
          credentials: "include"
      });
      ```

      The CSRF token can be retrieved by the SPA only once, when the user authenticates.

      > :older_man: There is a slight difference between including the token in the request body and placing it in a custom HTTP header, as requests with custom headers are inherently restricted by the `Same-Origin Policy (SOP)`, which represents an additional protection layer.
  
  1. When the form is submitted, the server-side application should ensure that the received token exactly matches the one previously generated and is properly associated with the appropriate session.

### Double-submit cookie pattern

* In cases where managing CSRF token state on the server-side is not feasible, the double-submit cookie pattern offers an alternative. This approach is stateless, eliminating token storage on the server, and is relatively simple to integrate.
* The strongest implementation of this pattern is the **signed** double-submit cookie, which ensures token authenticity using a server-side secret key.
* The double-submit cookie pattern operates by requiring the frontend application in the user's browser to send two copies of the CSRF token — one as a cookie and the other as a custom HTTP header or request parameter (e.g., in a form field). The server then verifies that both values are identical to confirm the request's validity.
  * This process inherently ensures that only JavaScript running under the legitimate origin can retrieve the cookie value and include it as a custom header or request parameter, while other origins are restricted from doing so due to the `Same-Origin Policy (SOP)` enforced by web browsers, even when the cookie `httpOnly` flag is not set.

#### Double-submit cookie pattern in SPA applications

* These steps outline the operation of the double-submit cookie pattern in verifying requests and preventing CSRF attacks:
  1. When a user logs in or initiates a session, the server creates a unique CSRF token and sets it as a cookie without the `httpOnly` flag, allowing JavaScript code to access the cookie value containing the CSRF token:

      ```http
      Set-Cookie: csrfToken=abcdef1234567890; Path=/; Secure; SameSite=Strict
      ```

  1. When a user submits a form or performs a state-changing operation, the frontend application should explicitly include the token as a custom HTTP header or a request parameter (e.g., such as in a hidden input field), while the browser automatically sends the CSRF token cookie along with the request as part of its default behavior:

      ```javascript
      // Ensure js-cookie is available
      import Cookies from "js-cookie";

      // Retrieve CSRF token from cookie
      const csrfToken = Cookies.get("csrfToken");
      ```

      ```javascript
      const response = await fetch("/api/change-email", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              "x-csrf-token": csrfToken
          },
          body: JSON.stringify({ email: newEmail }),
          credentials: "include"
      });
      ```

  1. As the final step, the server validates the request by ensuring that the CSRF token in the cookie corresponds with the token in the `x-csrf-token` HTTP header, rejecting it if the values do not match or if a token is missing.

* As observed, this pattern relies on the `Same-Origin Policy (SOP)`, which restricts cookie access to the legitimate origin.

  > :older_man: When a cookie is set without specifying the `domain` attribute, the browser automatically restricts the cookie to the exact domain that issued the `Set-Cookie` header. As a result, the cookie is only sent to the issuing domain and not to its subdomains. However, if the server explicitly sets a domain (e.g., `Domain=example.tbl`), the cookie is sent to both `example.tbl` and all its subdomains (e.g., `*.example.tbl`, `*.sub.example.tbl`) - no matter how deep.

* To generate stateless CSRF tokens without requiring server-side storage, tokens can be created as a series of values that are either hashed or encrypted. Using the `Hash-based Message Authentication Code (HMAC)` algorithm is strongly recommended, as it is less computationally intensive than encryption and decryption processes while still ensuring strong security.

## Set the `SameSite` cookie attribute

* The `SameSite` cookie attribute is a security mechanism that regulates how cookies are transmitted with cross-site requests, aiming to mitigate CSRF attacks.

  > :older_man: A *site*, in the context of `SameSite` cookies, consists of the registered domain and public suffix (e.g., `example.tbl`), meaning all subdomains (e.g., `sub.example.tbl`) are considered part of the same site, while separate registered domains (e.g., `example.com`) are considered cross-site. URL schemes (e.g., `http://`, `https://`) and ports do not affect site classification.

* The `SameSite` attribute defines browser behavior for sending cookies based on whether a request originates from the same site or a cross-site source. Its values dictate different levels of cross-site cookie restrictions:
  * `Strict`: the cookie is sent only with requests that originate from the same site that set the cookie. On requests from cross-site sources, the browser does not include the cookie.
  * `Lax`: the cookie is sent in same-site requests, similar to `Strict` mode, but also in top-level, user-initiated navigations (e.g., clicking a link) when the request uses a safe method (`GET`, `HEAD`, `OPTIONS`, `TRACE`). It is excluded from background requests initiated by scripts, iframes, references to images, and other resources, as well as from requests using unsafe methods (`POST`, `PUT`, `DELETE`, `PATCH`).
  * `None`: the cookie is sent with all same-site and cross-site requests, which removes the built-in CSRF protection that `Lax` or `Strict` provide. This setting also mandates the `Secure` cookie attribute, restricting cookie transmission to HTTPS.

* It is essential to understand that `Lax` enforcement provides a reasonable defense-in-depth measure against CSRF attacks that use unsafe HTTP methods, but does not constitute a complete defense against CSRF attacks as a general security concern:
  * Cookies are still sent for top-level, user-initiated navigations using safe methods, allowing attackers to open a new window, trigger a forced navigation, or trick users into clicking a malicious link to bypass this restriction. CSRF attacks can still be performed through GET requests, which remain as a potential attack vector.
  * Features like `<link rel="prerender">` allow browsers to load pages in the background before a user actually navigates to them. If a site prerenders a page with sensitive actions, an attacker could exploit this to send an automatic "legitimate" request that appears same-site.
* According to OWASP, the `sameSite` attribute should not replace an anti-CSRF token mechanism, but should be used alongside it to strengthen security.

## Avoid using GET for state-changing operations except in particular cases

* GET requests should primarily be used for retrieving information and should not perform actions that alter data or modify the application state, such as updating user details, deleting data, or processing payments.
* Although it is technically possible to include an anti-CSRF token as a GET parameter, it is not recommended due to significant security risks:
  * URLs containing CSRF tokens may be logged by web servers, proxies, or analytics tools. Moreover, if a user follows a link or visits an insecure page, the token might be leaked via the `Referer` header.
  * The presence of CSRF tokens in URLs may allow attackers to intercept or recover them, enabling them to bypass CSRF protection.
* However, in specific cases, such as when an application sends a confirmation email with an activation link after user sign-in to activate the user's account, using the GET method for state-changing operations provides a seamless and user-friendly experience.
