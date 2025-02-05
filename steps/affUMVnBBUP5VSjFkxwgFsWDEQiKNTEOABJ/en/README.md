# Finding and exploiting IDOR vulnerabilities

## Finding IDORs

* Identifying IDOR vulnerabilities requires careful analysis of how web applications handle object references and access controls. Start by inspecting all user-controllable input parameters, such as IDs, usernames, or file paths, to determine if they directly map to internal resources.
* Analyze API endpoints and web requests for parameters that reference objects (e.g., `id=123`, `user=johndoe`). Pay special attention to predictable patterns in these parameters, such as sequential or easily guessable values.
* Test whether modifying these parameters allows access to other users' resources without proper authorization. Tools like proxies (e.g., Burp Suite or OWASP ZAP) can assist in intercepting and modifying requests for manual testing.
* Check for variations in response behavior when parameter values are altered. Unauthorized access may return sensitive information, error messages, or subtle changes in response times that indicate potential access control issues.
* Additionally, as part of in-depth research, leverage a vulnerability scanner for automatic detection, inspect source code if accessible to review access control policies on the server side ensuring they validate user permissions for each resource, and perform SAST to uncover security risks.

## Exploiting basic IDORs

* Basic IDORs often involve straightforward scenarios where object references can be easily manipulated due to predictable or poorly implemented access control mechanisms.

### Via predictable identifiers

* Basic IDOR vulnerabilities often occur when applications use predictable identifiers to reference internal objects. For example, user profiles may be accessed by appending an ID to the URL:

  ```http
  GET /user/profile?id=123
  ```

  By simply modifying the `id` parameter, an attacker can attempt to access another user's profile:

  ```http
  GET /user/profile?id=124
  ```
  
  If the application does not verify whether the requesting user has authorization to access the modified resource, it may return unauthorized data, such as the profile of the user with `124` identifier.

### Via usernames

* Web applications sometimes use usernames or other unique textual identifiers instead of numeric IDs to reference user profiles. In such scenarios, an attacker can modify the username parameter to attempt unauthorized access to another user's data.
* For instance, a legitimate request to fetch the profile of the currently logged-in user might resemble this:

  ```http
  GET /user/profile?user=johndoe
  ```
  
  Without proper access controls, altering the `user` parameter to a different username (e.g., `janedoe`) could allow an attacker to retrieve another user's profile data:

  ```http
  GET /user/profile?user=janedoe
  ```

### Via direct reference to static files

* Static files stored on the server can also be susceptible to IDOR vulnerabilities. For example, an application may store user-uploaded files in a shared directory without implementing proper access controls:

  ```http
  GET /uploads/123.pdf
  ```
  
  If the file names are sequential or predictable, an attacker can modify the file name in the request to access files uploaded by other users:

  ```http
  GET /uploads/124.pdf
  ```
  
  Without verifying whether the requesting user has permission to access the specified file, the server may expose sensitive or private data belonging to other users.

### Via resource path manipulation

* Some web applications retrieve files dynamically based on parameters instead of serving them as static files. This method can also result in an IDOR vulnerability if proper authorization checks are not in place.
* For instance, a user might request an invoice by specifying its ID in the query string:

  ```http
  GET /invoices?id=123.pdf
  ```
  
  If the application fails to verify that the requesting user is authorized to access the specified file, an attacker can manipulate the `id` parameter to retrieve unauthorized invoices:

  ```http
  GET /invoices?id=124.pdf
  ```
  
  This may allow attackers to access sensitive documents associated with other users, such as invoices, reports, or other private resources, potentially exposing confidential data.

### Via cookie manipulation

* Cookies are commonly used by web applications for authentication and authorization. In some cases, a cookie may store a user-specific identifier to determine the current user. If this identifier is not properly validated, it can be exploited to achieve an IDOR vulnerability.
* In the following example, the cookie `userId` is used to identify the currently logged-in user:

  ```http
  GET /user/profile
  Cookie: userId=123
  ```

  If the application does not verify that the `userId` corresponds to the authenticated user's session or permissions, an attacker can alter the cookie value to access another user's data:

  ```http
  GET /user/profile
  Cookie: userId=124
  ```

## Exploiting IDORs via parameter pollution

* Parameter pollution is a technique used to exploit how applications handle multiple values for the same input parameter. This occurs when duplicate parameters are injected into a request, with the application's behavior depending on the underlying technology. It may:
  * Process only the first value.
  * Process only the last value.
  * Concatenate all values.
* For example, a legitimate request to retrieve a user profile might look like this:

  ```http
  GET /user/profile?id=123
  ```

  An attacker could modify the `id` parameter to include additional values:

  ```http
  GET /user/profile?id=123&id=124
  ```

  If the application uses the first value (i.e., `id=123`) for access control checks but the second value (i.e., `id=124`) to retrieve the resource, it could unintentionally expose unauthorized data. Similarly, if concatenation occurs or the last value is prioritized, unexpected behaviors or data leaks might result.
* Parameter pollution not only amplifies IDOR vulnerabilities but also provides a means to bypass poorly implemented authorization mechanisms. Testing for this issue is essential, as its exploitation relies on inconsistencies in how parameters are validated and processed.

## Exploiting IDORs via unexpected values

* Inadequate or nonexistent input validation can make IDOR vulnerabilities exploitable by allowing unexpected values to be introduced into application inputs. Such inputs can disrupt application logic by involving unusual or unanticipated data types.
* Testing for this involves experimenting with various input methods to bypass access controls. If the target accepts input through a JSON body, altering different fields can reveal how the endpoint processes and validates input. Modifying the expected data can lead to unintended behavior or security flaws, such as:
  * Submitting an array of IDs: `[123, 124]`.
  * Using a boolean value: `true` or `false`.
  * Applying wildcard characters like `*` or `%` (test carefully to avoid unintended effects).
  * Providing a large integer with leading zeros: `0000124`.
  * Using a negative ID: `-1`.
  * Inputting a decimal value: `124.0`.
  * Adding a string with delimiters: `"123,124"`.
* A request to update a user profile might typically include a standard input, such as:

  ```http
  PUT /api/users/profile
  {
    "userId": 123
  }
  ```

  A malicious user can test the application's behavior by modifying the input to include unexpected data, such as an array of values:

  ```http
  PUT /api/users/profile
  {
    "userId": [
      123,
      124
    ]
  }
  ```

* These inputs might exploit type coercion, validation flaws, or unanticipated application behavior, potentially leading to unauthorized access.

  > :older_man: Type coercion refers to the automatic conversion of a value from one data type to another during program execution, possible in dynamically or loosely typed languages such as JavaScript, Python, and PHP, where variables are not strictly tied to a specific type.

## Exploiting method-based IDORs

* Applications sometimes implement different access control mechanisms for different HTTP methods, which can result in bypass vulnerabilities. By altering the HTTP method of a request, it may be possible to bypass restrictions and perform unauthorized actions or access sensitive data.
* For example, a GET request might enforce access controls, but a corresponding POST request may lack these checks, creating a potential security gap. This behavior is often caused by misconfigured access control rules or incorrect assumptions about how requests are handled.
* Consider a scenario where an application provides endpoints to access user profiles. While a GET request enforces access controls, a POST request for the same resource lacks proper validation:

@@TagStart@@java

  ```java
  @RestController
  @RequestMapping("/api/users")
  public class UserProfileController {

      @GetMapping("/{userId}/profile")
      public ResponseEntity<?> getUserProfile(@PathVariable String userId, HttpSession session) {
          if (verifyAccess(session, userId)) {
              Object profile = getProfile(userId);
              return ResponseEntity.ok(profile);
          } else {
              return ResponseEntity.status(HttpStatus.FORBIDDEN).body("Unauthorized");
          }
      }

      @PostMapping("/{userId}/profile")
      public ResponseEntity<?> updateUserProfile(@PathVariable String userId, @RequestBody Map<String, String> body) {
          String name = body.get("name");
          String email = body.get("email");

          Object profile = getProfile(userId); // No access control checks here

          // Perform additional actions if allowed

          return ResponseEntity.ok(profile);
      }
  }
  ```

@@TagEnd@@
@@TagStart@@node.js

  ```javascript
  app.get("/api/users/:userId/profile", (req, res) => {
    const { userId } = req.params;
    let profile;

    if (verifyAccess(req.session, userId)) {
      profile = getProfile(userId);
    } else {
      res.status(403).send("Unauthorized");
      return;
    }

    res.send(profile);
  });

  app.post("/api/users/:userId/profile", (req, res) => {
    const { userId } = req.params;
    const { name, email } = req.body;

    const profile = getProfile(userId); // No access control checks here

    // Perform additional actions if allowed

    res.send(profile);
  });
  ```

@@TagEnd@@

  In this scenario, while the GET endpoint enforces robust access control using the `verifyAccess` function to restrict profile data access to authorized users, the POST endpoint lacks such checks, allowing unauthorized access and processing of profile data.

* To exploit this vulnerability, a malicious user could send the following request:

  ```http
  POST /api/users/124/profile
  ```

* This type of vulnerability arises because applications may treat HTTP methods differently, assuming certain methods (e.g., POST) do not require the same access controls as others (e.g., GET). Proper implementation of consistent access control checks across all endpoints is essential to prevent such exploits.

## Exploiting content-type-based IDORs

* Content-type-based IDORs can arise when underlying frameworks or libraries process requests differently depending on the `Content-Type` header. By modifying this header, it may be possible to bypass access controls, perform state-changing actions, or access sensitive data under certain conditions.
* For instance, a request with the `Content-Type` header set to `application/x-www-form-urlencoded` might be processed in an unintended manner:

  ```http
  GET /user/profile/123
  Content-Type: application/x-www-form-urlencoded

  id=124
  ```
  
* In such cases, the application could interpret the request differently due to the specified content type, potentially handling input in a way that bypasses access controls. This highlights the importance of validating input consistently and ensuring that access control mechanisms function correctly, regardless of the content type or request format used.

## Exploiting IDORs via depreciated API versions

* Public APIs often employ versioning systems to manage updates, new features, and security patches. However, if older versions of the API remain accessible, there is a possibility that these versions could still contain vulnerabilities, such as missing access control checks, that have been addressed in newer versions. Under such conditions, attackers might exploit these outdated endpoints to attempt unauthorized actions or access sensitive data.
* For instance, a legitimate request to a newer API version might look like this:

  ```http
  GET /api/v2/users/123/profile
  ```

  An attacker could test an older version of the API to determine if it lacks the same security measures:

  ```http
  GET /api/v1/users/124/profile
  ```
  
  In this scenario, if the older API version does not enforce proper access control, it may inadvertently expose unauthorized data.

## Exploiting IDORs in APIs that rely on static keywords

* Some APIs include static keywords such as `current` or `me` to represent the currently authenticated user. While this approach simplifies user-specific requests, there is a possibility that it could introduce IDOR vulnerabilities if the same endpoint also supports numerical user IDs.
* In such cases, replacing the static keyword with a numerical user ID may reveal whether the API correctly enforces access controls. For example, a typical request might look like this:

  ```http
  GET /api/users/me/profile
  ```

  A malicious user might attempt to replace the keyword `me` with a numerical user ID to check if unauthorized access is possible:

  ```http
  GET /api/users/124/profile
  ```
  
  If the API processes the modified request without validating the user's authorization, it could potentially expose sensitive data from another user's profile.

## Exploiting IDORs that require unpredictable IDs

* Some applications use UUIDs or other non-sequential identifiers to reduce the likelihood of IDOR exploitation.
* While these are harder to predict, they do not inherently eliminate the vulnerability, as they can still be exploited if an attacker discovers them via other means.
* For instance, UUIDs may be found in:
  * Publicly accessible user profile URLs.
  * Shared links generated by the application.
  * Password reset forms, invitation emails or unsubscribe forms.
  * Application metadata or API responses.
  * Search engines and archival tools, such as the [Wayback Machine][1].
* If UUIDs are exposed and access control is insufficient, attackers can still manipulate them to access unauthorized resources.

## Exploiting second-order IDOR vulnerabilities

* Second-order IDOR vulnerabilities function similarly to traditional IDORs but involve an additional layer of complexity. In these cases, the application uses user-provided input to indirectly reference a data object. The input is first kept in memory or stored and later retrieved to interact with the data object, potentially bypassing access controls during the second step.
* These vulnerabilities can be more challenging to identify, as the exploitation requires understanding how the application processes and uses stored data at different stages.
* In the following example, the application allows users to request the deletion of their account. The user provides a crafted `userId` through an external API request:

  ```http
  POST /api/users/actions/delete
  {
    "userId": "123/../124"
  }
  ```

  The application processes this request and then constructs an internal API call to delete the user's associated storage:

  ```http
  DELETE /internal/storage/users/123/../124
  ```

  If the `userId` parameter is not properly validated and sanitized, the manipulated input (`123/../124`) could be treated as a valid identifier. This might allow an attacker to target and delete another user's storage (`124`), bypassing access control checks and resulting in unauthorized data deletion.

* This demonstrates how insufficient validation and access control at the initial request phase can create IDOR vulnerabilities during subsequent operations.

## Exercise to practice :writing_hand:

* The following web application contains a basic IDOR vulnerability that enables authenticated users to view other users' personal information (username and address).
* The exercise task involves logging into the application with `johndoe`'s credentials (i.e., username: `johndoe`, password: `Zw+?YmIZlrZF`) and leveraging the IDOR vulnerability to gain access to the `admin` user's address information.

  @@ExerciseBox@@

[1]: https://web.archive.org
