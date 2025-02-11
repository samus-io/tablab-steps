# Finding privilege escalation

* Privilege escalation vulnerabilities can be identified using manual and automated techniques to detect broken access control in web applications.
* Both vertical and horizontal privilege escalation can occur if role validation, authentication, or access controls are not properly enforced.

## Manual exploitation

* Manually navigate different URLs of the application, especially those that may contain sensitive functionalities such as administrative panels or user management pages, and try to access without the proper permissions.

## Automated scanning

* Using automated tools like OWASP ZAP or Burp Suite can help scan for access control weaknesses by crawling the application and analyzing responses.
* Automated scanners can detect hidden endpoints, exposed APIs, unprotected admin panels, and misconfigured authentication mechanisms.

## Source code analysis

* Analyze the source code of the application to identify any unprotected endpoints or functionalities that may have been overlooked during development.
* In many frameworks, middleware is responsible for enforcing authorization. If an endpoint bypasses middleware, it may lack proper access control.

## Authentication and authorization testing

* Create unit test for testing the application's authentication and authorization mechanisms to identify any weaknesses that could allow unauthorized access to unprotected functionalities.
* These tests have to attempt to access different endpoints of the application as different existing user roles and as unauthenticated users.

## API documentation review

* If it is available, review the application's API documentation to identify any endpoints or functionalities that are exposed but not adequately protected by authentication or authorization mechanisms.

## Parameter-based access control

* Modifying parameter values in requests, such as changing `role=1` to `role=admin`, can reveal weak access control if the system grants unauthorized access to privileged functionalities.
* Role-based access control parameters may also be found in cookies, and if these values are editable without backend validation, an attacker could modify them to gain higher privileges.

## Referrer header manipulation

* Some web applications use the `Referer` header as a weak access control mechanism without verifying authentication, assuming that requests from trusted pages are legitimate.
* Removing or forging the `Referer` header (pointing to internal domains or administrative endpoints) in HTTP requests can allow unauthorized access to restricted sections of a web application.

## Broken access control by URL mismatching

* Accessing URLs using different letter cases, such as `/admin` vs. `/ADMIN`, can sometimes bypass access controls if the system is case-insensitive but access control mechanisms are not.
* Alternative encodings, such as using URL encoding (`/admin%2Fpanel` instead of `/admin/panel`), can sometimes trick access control filters into allowing unauthorized access.
* Some web applications treat `/admin` and `/admin/` as the same endpoint, while access control mechanisms may not, leading to inconsistent restrictions between variations.

## Horizontal privilege escalation

### Finding Insecure Direct Object Reference (IDOR)

* Modify parameters in URLs or form submissions to access resources or perform actions intended for other users.
* If an application exposes customer accounts using predictable numerical identifiers, such as:

  ```
  https://example.tbl/customerAccount?id=123
  ```

* An attacker can modify the `id` parameter to attempt access to another user's account:

  ```
  https://example.tbl/customerAccount?id=124
  ```

### File enumeration

* Attempting to access static files or user-specific resources by modifying predictable paths can help identify improperly restricted content.
* Considering the case where the web application stores user's orders on PDFs in the following endpoint:

  ```
  https://example.com/orders/users/123.pdf
  ```

* An attacker can change the user identifier to access other user's orders:

  ```
  https://example.com/orders/users/124.pdf
  ```
