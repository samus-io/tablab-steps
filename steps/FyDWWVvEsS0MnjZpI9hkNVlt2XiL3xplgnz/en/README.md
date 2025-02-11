# Horizontal privilege escalation

* Horizontal privilege escalation occurs when a user gains unauthorized access to resources or functionalities belonging to other users within the same privilege level.
* This vulnerability allows attackers to move laterally across the application's user base, accessing other users' data or performing actions they are not authorized to execute.
* Exploiting horizontal privilege escalation can lead to unauthorized data exposure, account manipulation, or disruption of services.

## Referer-based access control

* Some applications use the HTTP `Referer` header to determine whether a request is allowed based on its origin. If access control is enforced solely through `Referer` validation, it becomes vulnerable to manipulation.
* If an application restricts access to certain files or APIs based on `Referer` validation, an attacker could send a crafted request without a `Referer` header or modify it to bypass access controls.
* Consider a web application that grants access to user information based on whether the request originates from the company's intranet.
* The application relies on the `Referer` header to determine if a request comes from a trusted internal system, allowing access to sensitive data without requiring additional authentication.
* If the request contains a `Referer` header from the internal network, such as:

  ```
  Referer: https://internal.example.tbl/
  ```

* Then the access control will assume that the user is authorized and provides access to restricted information.
* An attacker outside the network can exploit this by modifying or forging the `Referer` header to appear as if their request is coming from the intranet.
* This can lead to data leaks, allowing the attacker to retrieve confidential records or personal details of other users.

## Location-based access control

* Some applications restrict access to content or functionalities based on a user's geographical location. If location-based access control is improperly implemented, attackers can manipulate their location to bypass restrictions.
* An attacker can use a VPN, proxy, or GPS spoofing techniques to disguise their actual location and access content or features meant for users in specific regions.
* If an application relies only on IP-based location checks without additional verification, an attacker can access geo-restricted services, potentially exposing sensitive data meant for specific regions.

## Insecure Direct Object References (IDOR)

* IDOR vulnerabilities occur when an application fails to properly enforce access controls, allowing attackers to manipulate parameters or directly reference objects (such as database records or files) to access unauthorized data.
* Attackers can modify a URL parameter to access another user's profile page or a sensitive data without proper authorization from database. In the following example, an attacker can change `userId=123` to `userId=456`:

  ```
  https://example.tbl/profile?userId=123
  ```

* If the system does not validate whether the user is authorized to view `userId=456`, the attacker can gain access to another user's profile.
* IDOR is not limited to user profiles and can expose financial records, invoices, order details, among others, if access controls are missing or improperly implemented.
