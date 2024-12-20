# Bypassing common defenses against CSRF

* Defensive methods designed to prevent CSRF attacks can sometimes be bypassed in specific scenarios. It is important to be aware of these potential weaknesses when developing security solutions.

## Bypassing anti-CSRF tokens

### CSRF token depends on request method

* Sometimes, web applications correctly validate the CSRF token when processing requests specific HTTP methods, such as POST.
* However, they may inadvertently allow the same action to be performed using other HTTP method (.e.g., GET) without proper CSRF token validation. This oversight enables attackers to exploit CSRF vulnerabilities via these HTTP methods.

### CSRF token depends on token being present

* There are web applications that when token is omitted, the application still processes the request, rendering the anti-CSRF mechanism ineffective.

### CSRF token is not tied to the user session

* In certain cases, web applications do not validate that the token belongs to the same session as the user who is making the request.
* Instead, the application maintains a global pool of tokens that it has issued and validates requests using any token from this pool.
* An attacker can log in to the application with their own account, retrieve a valid CSRF token, and use that token to craft requests on behalf of the victim.

### CSRF token is tied to a non-session cookie

* If a CSRF token is tied to a non-session cookie rather than the user's session cookie, attackers can exploit this setup under certain conditions.
* This scenario is more challenging to exploit, as it requires the application to have a mechanism that allows attackers to set cookies in the victim's browser.
* The attacker can log in to the application with their own account to generate a valid token and associated cookie.
* Then, using a cookie-setting behavior in the application (e.g., a vulnerable endpoint or script injection), the attacker places their cookie into the victim’s browser and crafts a request using their token and tricks the victim into executing it.

### CSRF token can be predictable

* If the CSRF token generation process is not sufficiently random, the token may be predictable.
* For example, if the application generates tokens using sequential numbers or a small set of predefined values, attackers can apply brute force to guess or compute a valid token.
* Predictable tokens undermine the entire anti-CSRF mechanism, allowing attackers to bypass protections and perform unauthorized actions.

## Bypass SameSite cookie attribute

* The `SameSite` cookie attribute with the Lax value can be bypassed if the web application permits state-changing operations through GET requests.
* The `Lax` value allows the browser to send cookies for user-initiated cross-site navigation. This means that when a user clicks on a link from another site, the browser includes cookies in the request to the target application.

## Bypass Referer-based CSRF protections

* Some web applications attempt to defend against CSRF attacks by relying on the HTTP `Referer` header.
* This header is used to verify that the request originated from the application's domain.
* While this method offers a basic level of protection, it is generally considered less effective and prone to various bypass techniques.

### Referer header depends on header being present

* Certain web applications validate the Referer header only when it is present in the request. If the header is omitted, the application skips validation entirely, assuming the request is legitimate.
* In this scenario, an attacker can design a CSRF exploit that manipulates the victim's browser to omit the `Referer` header in the resulting request.
* For example, an attacker can include the following HTML code in a malicious domain to ensure that the `Referer` header is not sent with requests originating from their page:
  
  ```html
  <meta name="referrer" content="no-referrer">
  ```

### Non-strict validation on Referer header

* If the web application does not strictly validate the `Referer` header, attackers can bypass the protection by crafting requests from malicious domains that partially match the expected value.
* For example, if the application validates that the domain in the `Referer` starts with the value `victim.tbl`, then the attacker can place it as a subdomain of their own domain:

  ```
  https://victim.tbl.attacker.tbl/
  ```

## Bypass CSRF protections with CORS misconfiguration

* If the web application does not have CORS properly configured, this behaviour allows reading HTTP request responses via JavaScript.
* As it is possible to get the responses from a malicious domain, it is possible to get the CSRF tokens by first making a GET request.
* Once the CSRF token is obtained, the only thing left to do is to make a POST request to exploit the CSRF.

## Bypass CSRF protections with XSS

* Cross-Site Scripting (XSS) vulnerabilities can completely bypass CSRF protections because XSS allows an attacker to execute arbitrary JavaScript in the context of the victim's browser.
* Similar to the CORS misconfiguration scenario, XSS enables an attacker to make requests as the victim and access the server's responses. By analyzing the server’s responses, an attacker can extract CSRF tokens and use them to forge legitimate-looking requests.

### How it works

* Malicious JavaScript injected via XSS can issue authenticated requests on behalf of the victim. The script leverages the victim’s session cookies, authentication headers, or any other credentials that are automatically sent with requests to the same domain.
* These unauthorized requests can retrieve server responses that include sensitive information, such as CSRF tokens embedded in HTML forms or API responses. This allows the attacker to use the stolen token for subsequent state-changing requests.
* The following example demonstrates how an attacker could exploit an XSS vulnerability to retrieve a CSRF token and use it to perform unauthorized actions, such as changing a user’s email address:

```html
<script>
  // Step 1: Fetch the HTML containing the CSRF token
  fetch('/change/email', { credentials: 'include' })
    .then(response => response.text())
    .then(html => {
      // Step 2: Parse the HTML to extract the CSRF token
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const csrfToken = doc.querySelector('input[name="csrf-token"]').value;

      // Step 3: Use the extracted CSRF token to craft a malicious request
      fetch('/change/email', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `email=attacker@attacker.tbl&csrf-token=${csrfToken}`,
      });
    });
</script>
```

* The first fetch request retrieves the CSRF token from a protected endpoint while using the victim’s authentication context (via cookies and credentials).
* The JavaScript uses a `DOMParser` to parse the HTML and locate the hidden input field with the name `csrf-token`. The value of this field is extracted and stored in the `csrfToken` variable.
* The attacker uses the stolen CSRF token to craft a POST request to the `/change/email` endpoint, changing the victim's email address to `attacker.tbl`. This malicious request is sent with the victim's authenticated session cookies.
