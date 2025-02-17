# Finding privilege escalation

* Privilege escalation vulnerabilities can be identified using manual and automated techniques to detect broken access control in web applications.
* Both vertical and horizontal privilege escalation can occur if role validation, authentication, or access controls are not properly enforced.

## Automated and manual exploitation

* Using automated tools like OWASP ZAP or Burp Suite can help scan for access control weaknesses by crawling the application and analyzing responses.
* Automated scanners can detect hidden endpoints, exposed APIs, unprotected admin panels, and misconfigured authentication mechanisms.
* Additionally, manually navigate different URLs of the application, especially those that may contain sensitive functionalities such as administrative panels or user management pages, and try to access without the proper permissions.

## Source code analysis

* Analyze the source code of the application to identify any unprotected endpoints or functionalities that may have been overlooked during development.
* In many frameworks, middleware is responsible for enforcing authorization. If an endpoint does not apply the access control middleware, it may lack proper access control.

### API documentation review

* If it is available, review the application's API documentation to identify any endpoints or functionalities that are exposed but not adequately protected by authentication or authorization mechanisms.

## Parameter-based access control

* Modifying parameter values in requests, such as changing `role=user` to `role=admin`, can reveal weak access control if the system grants unauthorized access to privileged functionalities.
* Role-based access control parameters may also be found in cookies, and if these values are editable without backend validation, an attacker could modify them to gain higher privileges.
* In the following example, the cookie `role` is used to identify the currently logged-in user role:

  ```http
  GET /
  Cookie: role=user
  ```

  If the application does not verify that the `role` corresponds to the authenticated user's session or permissions, an attacker can alter the cookie value to access to the admin panel:

  ```http
  GET /admin
  Cookie: role=admin
  ```

## Referrer header manipulation

* Some web applications use the `Referer` header as a weak access control mechanism without verifying authentication, assuming that requests from trusted pages are legitimate.
* Removing or forging the `Referer` header (pointing to internal domains or administrative endpoints) in HTTP requests can allow unauthorized access to restricted sections of a web application.
* For instance, an attacker could modify the `Referer` header to bypass the access control:

  ```http
  GET /admin
  Referer: https://internal.example.tbl
  ```

## Horizontal privilege escalation

### Finding Insecure Direct Object Reference (IDOR)

* Basic IDOR vulnerabilities often occur when applications use predictable identifiers to reference internal objects. For example, user profiles may be accessed by appending an ID to the URL:

  ```http
  GET /user/profile?id=123
  ```

  By simply modifying the `id` parameter, an attacker can attempt to access another user's profile:

  ```url
  GET /user/profile?id=124
  ```

  If the application does not verify whether the requesting user has authorization to access the modified resource, it may return unauthorized data, such as the profile of the user with `124` identifier.

#### Direct reference to static files

* Static files stored on the server can also be susceptible to IDOR vulnerabilities. For example, an application may store user-uploaded files in a shared directory without implementing proper access controls:

  ```http
  GET /uploads/123.pdf
  ```

  If the file names are sequential or predictable, an attacker can modify the file name in the request to access files uploaded by other users:

  ```url
  GET /uploads/124.pdf
  ```

  Without verifying whether the requesting user has permission to access the specified file, the server may expose sensitive or private data belonging to other users.
