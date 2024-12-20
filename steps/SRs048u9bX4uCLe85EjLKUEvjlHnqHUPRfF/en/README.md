# Finding and exploiting CSRF vulnerabilities

## CSRF via GET method

* CSRF vulnerabilities can often be exploited using the GET HTTP method when endpoints allow state-changing operations without proper protections.
* GET requests are typically intended for retrieving data (read-only operations), but if a web application improperly uses GET for actions that modify state (e.g., changing user information or making updates), it creates a significant security risk.
* In this example, when the user clicks on the following link, its email will be changed to `attacker@attacker.tbl`, making the attacker to get the full control of the account:

    ```http
    https://victim.tbl/email/change?email=attacker@attacker.tbl
    ```

* If the victim clicks the link while authenticated to `victim.tbl`, their browser automatically sends the GET request to the vulnerable endpoint.
* Another way to exploit CSRF via the GET method is by embedding the malicious link in an image tag (`<img>`).
* When the victim visits a malicious website, the browser automatically renders the HTML and sends the GET request to the vulnerable endpoint without any user interaction:

    ```html
    <img src="https://victim.tbl/email/change?email=attacker@attacker.tbl">
    ```

* This request, which includes the victim's authenticated session cookies, triggers the state-changing operation, changing the user's email address to `attacker@attacker.tbl`, without the victim's knowledge or consent.
* Once the email is changed, the attacker can reset the victim's password using the new email address, thereby gaining full control of the account.

## CSRF via POST method

* CSRF attacks using the POST method are among the most common forms of CSRF. These attacks occur when a web application fails to implement security mechanisms (such as CSRF tokens) to protect against unauthorized requests.
* An attacker can exploit this by crafting malicious HTML content that automatically triggers a POST request as soon as the user's browser renders the page.
* Unlike GET-based CSRF, POST-based CSRF allows attackers to target endpoints that require more structured input and are typically used for state-changing operations.
* Since browsers allow automatic form submission, attackers can initiate POST requests without user interaction, provided the user is authenticated to the target site.
* Suppose a vulnerable web application has an endpoint `/email/change`, which allows a user to update their email address using a POST request and this endpoint requires only the parameter `email`. An attacker can craft the following HTML page to exploit the vulnerability:

    ```html
    <html>
        <body>
            <form action="https://victim.tbl/email/change" method="POST">
                <input type="hidden" name="email" value="attacker@attacker.tbl" />
            </form>
            <script>
                document.forms[0].submit();
            </script>
        </body>
    </html>
    ```

### How the attack works

1. The attacker creates the HTML form with a hidden input field specifying the new email (`attacker@attacker.tbl`).
1. The `<script>` tag automatically submits the form as soon as the page is loaded.
1. The attacker tricks the victim into visiting the malicious page, such as through phishing emails, malicious links, or compromised websites.
1. When the victim's browser renders the HTML, it sends the POST request to `https://victim.tbl/email/change`.
1. If the victim is authenticated (i.e., has an active session in `victim.tbl`), the server processes the request and updates the victim's email to `attacker@attacker.tbl`.
