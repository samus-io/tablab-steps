# Types of IDOR

* Malicious actors exploit IDOR vulnerabilities in web applications by abusing insufficient access controls and insecure handling of object references, which are often connected to:
  * Database keys.
  * Query parameters.
  * User or session IDs.
  * Filenames.
* Through altering exposed object references, a malicious user may access or modify unauthorized information, potentially achieving:
  * **Horizontal privilege escalation**, when accessing or modifying another user's data.
  * **Vertical privilege escalation**, when accessing or modifying data belonging to higher-privilege accounts or restricted resources.

## Common IDOR attacks

* All IDOR exploitation processes share a common approach, although there are minor differences in how object references are accessed and altered by malicious users.

### Exploiting direct references to identifiers

* In this scenario, the object reference acts as an identifier in back-end database queries, and simply modifying its value allows the viewing or manipulation of other unauthorized records.
* For attackers, understanding the structure of identifiers is crucial, as the absence of this knowledge may force them into time-consuming enumeration tasks to discern a predictable pattern.

#### URL tampering

* The simplest method to exploit an IDOR vulnerability is through URL tampering, which usually needs very minimal or no technical expertise. In this case, a malicious user simply modifies the object reference value visible in the browser's address bar.
* Original request example with a numerical identifier:

  ```http
  GET /user/profile?id=123
  ```

  Potentially manipulated request:

  ```http
  GET /user/profile?id=124
  ```

* Original request example with a string-based identifier:

  ```http
  GET /profile?username=johndoe
  ```

  Potentially manipulated request:

  ```http
  GET /profile?username=admin
  ```

* In general, URL tampering might involve incrementing or decrementing numerical IDs, substituting alternative strings, or attempting to guess hidden URLs.

#### Body manipulation

* In this context, the malicious user alters the object reference within the HTTP request body, rather than the URL. This typically occurs in applications using POST or PUT methods, where data is sent within the request body.
* Original request example with a numerical identifier:

  ```text
  POST /user/change-email
  {
    "userId": "123",
    "email": "attacker@attacker.tbl"
  }
  ```

  Potentially manipulated request:

  ```text
  POST /user/change-email
  {
    "userId": "124",
    "email": "attacker@attacker.tbl"
  }
  ```

* Modifying hidden form values and other form parameters is the most common example of such scenarios.

#### HTTP headers manipulation

* This might include altering the object reference within a cookie before it is sent back to the server or decoding and modifying headers that may contain object references, such as changing a user ID found in the `Authorization` header.
* For instance, certain web applications might store a user ID within a cookie when a user logs in.
* Original cookie example with a numerical identifier:

  ```http
  Set-Cookie: userId=123; HttpOnly; Secure
  ```

  Potentially manipulated cookie:

  ```http
  Set-Cookie: userId=124; HttpOnly; Secure
  ```

#### Other manipulations

* APIs can be susceptible to IDOR vulnerabilities when malicious users manipulate API endpoints to access or modify data or perform unauthorized actions. This is often seen in RESTful APIs where resource identifiers are manipulated, such as enforcing the use of a deprecated version over the current one.
* Database-based applications can also be susceptible to IDOR vulnerabilities when malicious actors can alter SQL queries or database parameters to access, modify or delete records that they are not authorized to access, which can lead to data leakage or manipulation.

### Exploiting direct references to files

* Resource path manipulation stands out as a distinct form of IDOR vulnerability, as it enables direct access to file system resources rather than database records. In this particular scenario, a malicious user can view files within the application's scope without proper permission by visiting a specific URL.
* Original URL example with a specific file path:

  ```url
  GET /uploads/photo123.jpg
  ```

  Potentially manipulated URL:

  ```url
  GET /uploads/photo124.jpg
  ```

#### Leading to a LFI vulnerability

* A `Local File Inclusion (LFI)` vulnerability occurs when an application uses an input parameter as a file path. This often happens when user input is improperly sanitized and directly used in file paths.
* Original request example with an input parameter serving as a resource locator:

  ```url
  GET /download?file=photo123.jpg
  ```

  Potentially manipulated URL:

  ```url
  GET /download?file=photo124.jpg
  ```

* While the IDOR impact is typically limited to unauthorized access to files within the application's intended scope, an LFI vulnerability allows access to arbitrary files on the server, often outside the application's managed directory when combined with `Path traversal` attacks, such as sensitive system files or application configuration files.
* This way, a malicious user could gain access to sensitive file system resources such as the `/etc/passwd` file by manipulating the user input parameter (in this case, simply changing the URL) to navigate to that resource instead of `photo124.jpg`:

  ```url
  GET /download?file=../../../etc/passwd
  ```

## Blind IDORs

* Blind IDOR refers to cases where unauthorized actions are carried out, but the server response does not directly indicate that the exploitation was successful.
* This situation could involve a malicious user making changes to another user's private data without having access to it. Considering a web application where users can modify their profile settings via an HTTP PUT call to an endpoint like `api.domain.tbl/users/124`, an attacker might tamper with the user ID in the request to alter another user's profile settings without actually seeing their data.