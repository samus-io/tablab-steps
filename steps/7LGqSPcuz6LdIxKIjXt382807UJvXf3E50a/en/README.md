# Finding Vertical Privilege Escalation

* You can uncover Vertical Privilege Escalation vulnerabilities resulting from Broken Access Control using multiple methods, including the following.

## For Unprotected functionalities

* **Manual exploitation**:
  * **URL enumeration**: Manually explore different URLs of the application, especially those that may contain sensitive functionalities such as administrative panels or user management pages.
  * **Link Crawling**: Follow links within the application to discover hidden or unlinked pages that may contain unprotected functionalities.
* **Automated scanning**:
  * **Web vulnerability scanners**: Use automated web vulnerability scanners like OWASP ZAP, Burp Suite, or Nikto to crawl the application and identify unprotected functionalities based on patterns or signatures.
  * **Fuzzing**: Utilize fuzzing techniques to systematically test different endpoints and parameters for potential vulnerabilities.
* **Source code analysis**:
  * **Static code analysis**: Analyze the source code of the application to identify any unprotected endpoints or functionalities that may have been overlooked during development.
  * **Manual code review**: Conduct manual code reviews to identify potential security flaws, including unprotected functionalities that may not be immediately apparent.
* **API documentation review**: Review the application's API documentation, if available, to identify any endpoints or functionalities that are exposed but not adequately protected by authentication or authorization mechanisms.
* **Browser developer tools**: Use browser developer tools to inspect network requests and responses while interacting with the application. Look for endpoints or functionalities that are accessible without proper authentication or authorization.
* **Authentication and Authorization testing**: Test the application's authentication and authorization mechanisms to identify any weaknesses or bypass techniques that could allow unauthorized access to unprotected functionalities.
* **Data analysis**: Analyze application logs and access records to identify any unusual or unexpected access patterns that may indicate access to unprotected functionalities.

## For Parameter-based access control

* **Parameter manipulation**:
  * **Manual testing**: Modify parameter values (e.g., role=1) to higher privilege levels (e.g., role=admin) and observe if access is granted to functionalities or resources reserved for privileged users.
  * **Automated Fuzzing**: Use automated tools or scripts to systematically test different parameter values, including higher privilege levels, to identify discrepancies in access control enforcement.
* **Cookie Tampering**:
  * **Manual testing**: Manipulate cookie values (e.g., admin=false to admin=true) using browser developer tools or proxy tools like Burp Suite and observe if access controls are bypassed, granting unauthorized access to privileged functionalities.
  * **Automated testing**: Use automated testing frameworks or tools to modify cookie values and assess if higher privilege levels can be achieved, potentially leading to unauthorized access.
* **Session Management testing**:
  * **Session Fixation**: Test for session fixation vulnerabilities where an attacker can set the session ID to a known value and hijack the session of a privileged user, gaining access to their privileges.
  * **Session Replay**: Assess if session tokens or cookies are susceptible to replay attacks, allowing attackers to reuse valid session information to gain unauthorized access to privileged functionalities.
* **Authorization bypass techniques**:
  * **Insecure Direct Object References (IDOR)**: Test for IDOR vulnerabilities where attackers manipulate parameters or cookies to access resources or functionalities belonging to other users, including those with higher privilege levels.
  * **Forced Browsing**: Attempt to access restricted URLs directly by guessing or enumerating URLs associated with higher privilege levels, bypassing access controls implemented based on parameters or cookies.
* **Browser extension testing**: Use browser extensions such as Cookie Editor or Tamper Data to manipulate parameters or cookies and observe if access controls can be bypassed to escalate privileges.

## For Broken Access Control resulting from platform misconfiguration

* Add or modify HTTP headers to attempt accessing protected resources.
* Common headers to test include `X-Original-URL` and `X-Rewrite-URL` which might be used by the server to route requests.

## For Broken Access Control resulting from URL-matching discrepancies

* Access URLs in varying cases (e.g., `/admin` vs. `/ADMIN`) to check if the access control varies.
* Use alternative encodings or unexpected formats to try bypassing URL filters.
* Configure web application firewalls to detect and block suspicious or unauthorized access attempts that exploit URL-matching discrepancies for privilege escalation. WAFs can provide an additional layer of defense against such vulnerabilities.
