# What is Open Redirect?

* An open redirect is a problem where hackers can trick the website into sending you to a different site than intended. They do this by changing the URL to include instructions to go to a different site. This is a common problem in many websites.
* Imagine you're playing a game and someone gives you a map with a route to follow. If you follow the map, it leads you to a nice park. An open redirect is like someone giving you a map (URL) that looks like it goes to the park (a safe website), but they change the route so it takes you to a dangerous place instead (a malicious website).
* Sometimes, certain websites (like search engines) are supposed to give you maps to different places. This is normal and safe if they do it correctly. But, if a website isn't supposed to redirect you anywhere, an open redirect can be a big problem.
* Open redirect issues happen because the website doesn't properly check where it's sending you. Hackers can use this to steal your information, send you to fake websites, and do other bad things.
* Cross-Site Redirect, Cross-Domain Redirect are the alternate names for Open Redirect.
* Open redirect is classified into two types:
  * **Header-Based Open Redirect**: this type of open redirect leverages HTTP response headers to redirect users to another location or resource. One common example is the Location header, which, while intended to direct users to a legitimate URL, can be manipulated by attackers to redirect users to malicious websites. This exploitation typically occurs after the authentication process, making phishing attacks more convincing.
  * **Javascript-based Open Redirect**: all the web applications are ultimately relying on javascript. If the application allows the user to control the redirect process then this type of vulneriblity can occur. This can occur at both client and server side.

## How Open Redirect works?

![Workflow of Open Redirect][1]

* **Identification of vulnerable parameter**: the attacker identifies a parameter in a trusted website that controls the redirection URL (e.g., `url`).

* **Crafting a malicious URL**: the attacker creates a URL that includes the trusted domain and the vulnerable parameter, setting the parameter to a malicious website (e.g., `example.com/?url=malicious-site.com`).

* **Trust exploitation**: the URL starts with the trusted domain, which makes users trust it without scrutinizing the entire URL. The URL's length is significant, reducing the likelihood that users will notice the malicious end part.

* **User interaction**: the attacker distributes the crafted URL to potential victims through phishing emails, social media, or other communication channels. The user, seeing the trusted domain, clicks on the URL.

* **Redirection process**: the web application processes the URL and redirects the user to the site specified in the vulnerable parameter (`url`).

* **Phishing execution**: the user is redirected to the malicious website, which mimics the appearance and behavior of the legitimate site. The malicious site asks for sensitive information such as usernames, passwords, credit card details, etc.

* **Data theft**: the user, believing the site to be legitimate, enters their sensitive information. The attacker captures this information, gaining unauthorized access to the user's accounts or personal data and may direct again to the original website.

## What could be achieved with Open Redirect?

* Many people underestimate the significance of addressing open redirection vulnerabilities, assuming it merely allows redirecting users to different websites. However, this vulnerability can be exploited by hackers for far more harmful activities.

* When a hacker identifies and exploits this vulnerability, it goes beyond simple redirection. They can leverage it to carry out **phishing attacks**, **cross-site scripting (XSS) attacks**, and even **server-side request forgery (SSRF)** attacks. Let's explore each of these in detail.

## Phishing attacks

* Open redirect vulnerabilities can be exploited to conduct phishing attacks, making malicious links appear more legitimate by leveraging the trust associated with the original domain.

### Example scenario (OAuth Flow Exploit)

* An attacker crafts a URL using the open redirect vulnerability of a legitimate site.
* The victim clicks the link and is redirected to a legitimate service for OAuth authentication (e.g., example, Facebook).
* After entering their credentials, the victim is redirected back to a phishing site that mimics the original service, asking them to re-enter their information due to an incorrect username or password.
* The attacker captures the credentials when the victim re-enters them on the bogus site.
* Services like Facebook mitigate this by ensuring that the `redirect_uri` parameter matches a pre-configured URL, denying mismatched requests.

### Bypassing Server Side Request Forgery (SSRF) protections

* Open redirects can be used to bypass SSRF protections, allowing attackers to exploit internal systems behind firewalls or filters.

#### Example scenario

* An attacker exploits an open redirect vulnerability to direct a server-side request from a trusted domain to an internal system.
* The open redirect URL could look like: `https://trusted.org/redirect?url=https://internal-system.local`.
* The request appears to come from the trusted domain, bypassing the SSRF protections and allowing the attacker to interact with internal resources.

## Cross-Site scripting attacks

* Open redirect can allow attackers to execute javascript payloads from URL parameters.
* Here are two common payloads used to achieve this:

  * `javascript:alert(1)`:
    * This payload uses the javascript: scheme, which allows the insertion of JavaScript code directly in the URL.
    * If a vulnerable URL looks like `https://example.org/redirect?url=`, an attacker could craft a malicious URL such as `https://example.org/redirect?url=javascript:alert(1)`.
    * When the user is redirected, the browser interprets the javascript: scheme and executes the code alert(1), which displays an alert box with the number 1.
    * While this example uses a harmless alert, attackers can execute more harmful scripts to steal cookies, capture user input, or redirect to other malicious sites.
  * `javascript://%20alert(1)`:
    * This payload is a variation that uses URL encoding to evade basic input validation or filtering.
    * With the same vulnerable URL structure, the attacker could use `https://example.org/redirect?url=javascript://%20Aalert(1)`.
    * Here, `%20` is the encoded representation of empty space. When the browser processes this URL, it decodes the space and executes alert(1).
    * Similar to the previous payload, this one can bypass some filters or defenses that do not correctly handle encoded characters, allowing the execution of potentially malicious scripts.

* Open redirects can also bypass XSS auditors in web browsers, allowing attackers to execute cross-site scripting (XSS) attacks by leveraging the redirect functionality.

### Example scenario(XSS Bypass exploit)

* The attacker crafts a URL that uses an open redirect to include a script from a trusted domain.
* The script URL might be: `<script src="https://vulnerable.org/redirect?url=https://malicious.org/payload.js"></script>`.
* The XSS auditor, seeing the script as originating from a trusted domain, does not block it, allowing the malicious script to execute.

## Common example of Open Redirect vulnerability in Login or Registration

* A common example of an open redirect vulnerability can be found in the login or registration processes of web applications. Consider the following scenario where the user is directed to `example.org` after completeting the login/registration from `domain.org`.

### Example URL

* **Legitimate URL**: `https://domain.org/signup?redirectUrl=https://example.org`
* **Malicious URL**: `https://domain.org/signup?redirectUrl=https://malicious-site.org`

### Step-by-Step exploit

* A user signs up for an account on `domain.org` and is supposed to be redirected to a URL specified by the `redirectUrl` parameter after registration.
* The application does not properly validate the `redirectUrl` parameter, allowing any URL to be passed through.
* An attacker identifies this vulnerability and crafts a malicious URL:` <https://domain.org/signup?redirectUrl=https://malicious-site.org>`. The attacker distributes this URL through phishing emails, social media, or other channels.
* The victim clicks the malicious link and completes the sign-up process on `domain.org`. After sign-up, the application redirects the victim to `https://malicious-site.org` instead of a legitimate URL.
* The malicious site may mimic a legitimate login page, asking the victim to enter additional information, such as login credentials or personal data, under the pretense of needing to complete the registration process.
* The attacker captures the entered credentials or data.

[1]: /static/images/open-redirect.png
