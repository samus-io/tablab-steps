# What is Open Redirect?

* An open redirect is a vulneribility where attackers can trick the website into sending users to a different site than intended. They do this by changing the URL to include instructions to go to a different site.
* Imagine a person playing a game and someone gives a map with a route to follow to that person. If the person follows the map, it leads to a nice park. An open redirect is like someone giving a map (URL) that looks like it goes to the park (a safe website), but they change the route so it takes to a dangerous place instead (a malicious website).
* However, whether an open redirect constitutes a vulnerability depends on the intended behavior of the application. For instance, certain services might intentionally provide redirects to arbitrary URLs as part of their functionality. In such cases, the open redirect may not be considered a security flaw.
* Open redirect issues happen because the website doesn't properly check where it's sending the user. Attackers can use this to steal user's information by sending the user to fake websites.
* Cross-Site Redirect, Cross-Domain Redirect are the alternate names for Open Redirect.

## Types of Open Redirect

### Header-Based Open Redirect

* This type of open redirect leverages HTTP response headers to redirect users to another location or resource.
* One common example is the `Location` header, which, while intended to direct users to a legitimate URL, can be manipulated by attackers to redirect users to malicious websites.
* This exploitation typically occurs after the authentication process, making phishing attacks more convincing.

### Javascript-based Open Redirect

* Switching from server-side restrictions to JavaScript-based checks on your web pages increases their vulnerability to redirect attacks, as attackers can easily disable client-side checks.
* When attackers successfully execute JavaScript-based redirects, the potential for exploitation becomes limitless. This is why attackers often exploit open redirect vulnerabilities through JavaScript-based methods during phishing attacks.

## How Open Redirect works?

![Workflow of Open Redirect][1]

* **Identification of vulnerable parameter**: the attacker identifies a parameter in a trusted website that controls the redirection URL (e.g., `url`).

* **Crafting a malicious URL**: the attacker creates a URL that includes the trusted domain and the vulnerable parameter, setting the parameter to a malicious website (e.g., `domain.tbl/?url=attacker.tbl`).

* **Trust exploitation**: the URL starts with the trusted domain, which makes users trust it without scrutinizing the entire URL. The URL's length is significant, reducing the likelihood that users will notice the malicious end part.

* **User interaction**: the attacker distributes the crafted URL to potential victims through phishing emails, social media, or other communication channels. The user, seeing the trusted domain, clicks on the URL.

* **Redirection process**: the web application processes the URL and redirects the user to the site specified in the vulnerable parameter (`url`).

* **Phishing execution**: the user is redirected to the malicious website, which mimics the appearance and behavior of the legitimate site. The malicious site asks for sensitive information such as usernames, passwords, credit card details, etc.

* **Data theft**: the user, believing the site to be legitimate, enters their sensitive information. The attacker captures this information, gaining unauthorized access to the user's accounts or personal data and may direct again to the original website.

## What could be achieved with Open Redirect?

* Many people underestimate the significance of addressing open redirection vulnerabilities, assuming it merely allows redirecting users to different websites. However, this vulnerability can be exploited by attackers for far more harmful activities.

* When a attacker identifies and exploits this vulnerability, it goes beyond simple redirection. They can leverage it to carry out **phishing attacks**, **cross-site scripting (XSS) attacks**, and even **server-side request forgery (SSRF)** attacks. Let's explore each of these in detail.

## Phishing attacks

* Open redirect vulnerabilities can be exploited to conduct phishing attacks, making malicious links appear more legitimate by leveraging the trust associated with the original domain.

### Example scenario (OAuth Flow Exploit)

* An attacker crafts a URL using the open redirect vulnerability of a legitimate site.
* The victim clicks the link and is redirected to a legitimate service for OAuth authentication (e.g., example, Facebook).
* After entering their credentials, the victim is redirected back to a phishing site that mimics the original service, asking them to re-enter their information due to an incorrect username or password.
* The attacker captures the credentials when the victim re-enters them on the bogus site.
* Services like Facebook mitigate this by ensuring that the `redirect_uri` parameter matches a pre-configured URL, denying mismatched requests.

## Bypassing Server Side Request Forgery (SSRF) protections

* Open redirects can be used to bypass SSRF protections, allowing attackers to exploit internal systems behind firewalls or filters.
* When an attacker combines SSRF with an open redirect, they can use the open redirect to bypass internal protections.
* This means they can trick the server into accessing internal systems by making the server follow a redirect to a malicious site.

### Example for bypassing SSRF

* Imagine a company's internal system (e.g., an internal API) is only accessible from within the company's network.
* An attacker finds an SSRF vulnerability on a public-facing server of the company. They use this to make the server request an internal API endpoint.
* The attacker discovers an open redirect vulnerability on the company's server. For instance, the server takes a URL parameter and redirects to that URL without proper validation.
* The attacker can craft a malicious URL that uses the open redirect to point to an internal system. The SSRF vulnerability allows the attacker to make the server request this URL, which then gets redirected to the internal system.

## Cross-Site scripting attacks

* Open redirect can allow attackers to execute javascript payloads from URL parameters.
* Here are two common payloads used to achieve this:

  * `javascript:alert(1)`:
    * This payload uses the javascript: scheme, which allows the insertion of JavaScript code directly in the URL.
    * If a vulnerable URL looks like `https://domain.tbl/redirect?url=`, an attacker could craft a malicious URL such as `https://domain.tbl/redirect?url=javascript:alert(1)`.
    * When the user is redirected, the browser interprets the `javascript:` scheme and executes the code `alert(1)`, which displays an alert box with the number 1.
    * While this example uses a harmless alert, attackers can execute more harmful scripts to steal cookies, capture user input, or redirect to other malicious sites.
  * `javascript://%20alert(1)`:
    * This payload is a variation that uses URL encoding to evade basic input validation or filtering.
    * With the same vulnerable URL structure, the attacker could use `https://domain.tbl/redirect?url=javascript://%20Aalert(1)`.
    * Here, `%20` is the encoded representation of empty space. When the browser processes this URL, it decodes the space and executes `alert(1)`.
    * Similar to the previous payload, this one can bypass some filters or defenses that do not correctly handle encoded characters, allowing the execution of potentially malicious scripts.

## Bypassing XSS Auditors

* XSS (Cross-Site Scripting) auditors are security mechanisms in browsers that attempt to detect and block XSS attacks by inspecting JavaScript code in web pages.
* These auditors are designed to mitigate XSS vulnerabilities by preventing malicious scripts from executing in the context of a webpage.
* Bypassing XSS auditors is often part of a broader strategy to exploit vulnerabilities across multiple sites or components within a web application.

### Example for Bypassing XSS Auditors

* `domain.tbl` has an open redirect vulnerability that allows an attacker to craft URLs like `http://domain.tbl/redirect?url=http://attacker.tbl`.
* Normally, XSS auditors in browsers might detect and block these attacks.
However, by using the open redirect vulnerability on `domain.tbl`, the attacker can redirect users to a URL like `http://domain.tbl/redirect?url=http://attacker.tbl/%3Cscript%3Ealert(1)%3C/script%3E`.
* Here, `%3Cscript%3Ealert(1)%3C/script%3E` represents `<script>alert(1)</script>` encoded to bypass XSS auditors.
* The user is redirected to `attacker.tbl` with the encoded XSS payload.
* `attacker.tbl` processes the URL and executes the JavaScript payload, bypassing XSS auditors and potentially compromising user data or performing unauthorized actions.

## Common example of Open Redirect vulnerability in Login or Registration

* A common example of an open redirect vulnerability can be found in the login or registration processes of web applications. Consider the following scenario where the user is directed to `example.tbl` after completeting the login/registration from `domain.tbl`.

### Example URL

* **Legitimate URL**: `https://domain.tbl/signup?redirectUrl=https://example.tbl`
* **Malicious URL**: `https://domain.tbl/signup?redirectUrl=https://attacker.tbl`

### Step-by-Step exploit

* A user signs up for an account on `domain.tbl` and is supposed to be redirected to a URL specified by the `redirectUrl` parameter after registration.
* The application does not properly validate the `redirectUrl` parameter, allowing any URL to be passed through.
* An attacker identifies this vulnerability and crafts a malicious URL like ` https://domain.tbl/signup?redirectUrl=https://attacker.tbl`. The attacker distributes this URL through phishing emails, social media, or other channels.
* The victim clicks the malicious link and completes the sign-up process on `domain.tbl`. After sign-up, the application redirects the victim to `https://attacker.tbl` instead of a legitimate URL.
* The malicious site may mimic a legitimate login page, asking the victim to enter additional information, such as login credentials or personal data, under the pretense of needing to complete the registration process.
* The attacker captures the entered credentials or data.

[1]: /static/images/open-redirect.png
