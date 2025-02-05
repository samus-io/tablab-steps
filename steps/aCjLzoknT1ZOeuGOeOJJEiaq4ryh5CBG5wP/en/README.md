# Types of IDOR

* Malicious actors exploit IDOR vulnerabilities in web applications by abusing insufficient access controls and insecure handling of object references, often associated with:
  * Database keys.
  * Query parameters.
  * User or session IDs.
  * Filenames.
* Altering exposed object references can allow malicious actors to access or modify unauthorized information, potentially leading to:
  * **Horizontal privilege escalation**, when accessing or modifying another user's data.
  * **Vertical privilege escalation**, when accessing or modifying data belonging to higher-privilege accounts or restricted resources.
* Exploiting IDOR vulnerabilities generally involves a similar approach, with slight differences in the nature of object references and the ways attackers access or manipulate them.

## Leveraging direct references tied to identifiers

* In this scenario, the object reference acts as an identifier in back-end database queries, and simply modifying its value allows the viewing or manipulation of other unauthorized records.
* For attackers, understanding the structure of identifiers is crucial, as the absence of this knowledge may force them into time-consuming enumeration tasks to discern a predictable pattern.

### Via URL tampering

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

### Via body manipulation

* In this context, malicious user alter the object reference within the HTTP request body, rather than the URL. This typically occurs in applications using POST or PUT methods, where data is sent within the request body.
* Original request example with a numerical identifier:

  ```text
  POST /user/change-email
  {
    "userId": "123",
    "newEmail": "attacker@attacker.tbl"
  }
  ```

  Potentially manipulated request:

  ```text
  POST /user/change-email
  {
    "userId": "124",
    "newEmail": "attacker@attacker.tbl"
  }
  ```

* Modifying hidden form values and other form parameters is the most common example of such scenarios.

### Via HTTP headers manipulation

* This might include altering the object reference within a cookie before it is sent back to the server or decoding and modifying headers that may contain object references, such as changing a user ID found in the `Authorization` header.
* For instance, certain web applications might store a user ID within a cookie when a user logs in. Original cookie example with a numerical identifier:

  ```http
  Cookie: userId=123; HttpOnly; Secure
  ```

  Potentially manipulated cookie:

  ```http
  Cookie: userId=124; HttpOnly; Secure
  ```

### Via other manipulations

* APIs can be susceptible to IDOR vulnerabilities when malicious users manipulate API endpoints to access or modify data or perform unauthorized actions. This is often seen in RESTful APIs where resource identifiers are manipulated, such as enforcing the use of a deprecated version over the current one.
* Database-based applications can also be susceptible to IDOR vulnerabilities when malicious actors can alter SQL queries or database parameters to access, modify or delete records that they are not authorized to access, which can lead to data leakage or manipulation.

### Via blind scenarios

* Blind IDOR refers to cases where unauthorized actions are carried out, but the server response does not directly indicate that the exploitation was successful.
* This situation could involve a malicious user making changes to another user's private data without having access to it.
* Considering a web application where users can modify their profile settings via an HTTP PUT call to an endpoint like `api.domain.tbl/users/124`, an attacker might tamper with the user ID in the request to alter another user's profile settings without actually seeing their data.

## Leveraging direct references tied to static files

* Resource path manipulation stands out as a distinct form of IDOR vulnerability, as it enables direct access to file system resources rather than database records. In this particular scenario, a malicious user can view files within the application's scope without proper permission by visiting a specific URL.
* Original URL example with a specific file path:

  ```url
  GET /uploads/photo123.jpg
  ```

  Potentially manipulated URL:

  ```url
  GET /uploads/photo124.jpg
  ```

### Leading to a LFI vulnerability

* An IDOR vulnerability can lead to a `Local File Inclusion (LFI)` vulnerability if the application uses an input parameter as a file path. This often happens when user input is improperly sanitized and directly used in file paths.
  > :older_man: `Local File Inclusion (LFI)` is a web vulnerability that allows malicious actors to access, view, or include files stored within the document root folder of a web server's file system.

* Original request example with an input parameter serving as a resource locator:

  ```url
  GET /download?file=photo123.jpg
  ```

  Potentially manipulated URL:

  ```url
  GET /download?file=photo124.jpg
  ```

* While the IDOR impact is typically limited to unauthorized access to files within the application's intended scope, an LFI vulnerability allows access to arbitrary files on the server, often outside the application's managed directory when combined with `Path traversal` attacks, such as sensitive system files or application configuration files.
* This way, through the successful exploitation of a path traversal attack, a malicious user could gain access to sensitive file system resources such as the `/etc/passwd` file by manipulating the user input parameter (in this case, simply changing the URL) to navigate to that resource instead of `photo124.jpg`:

  ```url
  GET /download?file=../../../etc/passwd
  ```
