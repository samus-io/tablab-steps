# Finding and exploiting IDOR vulnerabilities

* Basic IDOR vulnerabilities often occur when applications use predictable identifiers to reference internal objects. For example, user profiles may be accessed by appending an ID to the URL:

  ```http
  GET /user/profile?id=123
  ```

  By simply modifying the `id` parameter, an attacker can attempt to access another user's profile:

  ```http
  GET /user/profile?id=124
  ```

* If the application does not verify whether the requesting user has authorization to access the modified resource, it will return unauthorized data, such as the profile of the user with `124` identifier.

## IDOR via username

* Web applications often use usernames or other unique textual identifiers instead of numeric IDs to reference user profiles.
* In such cases, an attacker can manipulate the username sent to the application to attempt accessing another user's information:
* For example, a legitimate request to retrieve the profile of the currently authenticated user might look like this:

  ```http
  GET /user/profile?user=johndoe
  ```

* If the application does not enforce proper access controls, changing the user parameter to another username (e.g., janedoe) may allow an attacker to retrieve the profile data of another user:

  ```http
  GET /user/profile?user=janedoe
  ```

## IDOR via direct reference to static files

* Static files stored on the server can lead to IDOR vulnerabilities. For example, an application may generate user invoices stored as PDFs:

  ```http
  GET /invoices/123.pdf
  ```

* An attacker can modify the file name in the request to access another user's invoice:

  ```http
  GET /invoices/124.pdf
  ```

## IDOR via resource path manipulation

* In some web applications, files are dynamically retrieved based on parameters rather than being served as static files.
* This approach can introduce an IDOR vulnerability if proper authorization checks are not in place.
* Considering the following request where a user retrieves an invoice by specifying its ID:

  ```http
  GET /invoices?id=123.pdf
  ```

* If the application does not validate whether the requesting user has the proper permissions to access the specified file, an attacker can manipulate the `id` parameter to retrieve unauthorized files:

  ```http
  GET /invoices?id=124.pdf
  ```

* This allows the attacker to access sensitive documents belonging to other users, such as invoices, reports, or other private resources.

## IDOR via cookie manipulation

* Cookies are commonly used by web applications for authentication and authorization. In some cases, a cookie may store a user-specific identifier to determine the current user. If this identifier is not properly validated, it can be exploited to achieve an IDOR vulnerability.
* In the following example, the cookie `user_id` is used to identify the currently logged-in user:

  ```http
  GET /user/profile
  Cookie: user_id=123
  ```

* If the application solely relies on the cookie value without verifying the user's identity or permissions, an attacker can modify the `user_id` value to access another user's data:

  ```http
  GET /user/profile
  Cookie: user_id=124
  ```

## IDOR via parameter pollution

* Parameter pollution can amplify IDOR vulnerabilities by injecting multiple values into a single parameter, exploiting the application's ambiguous handling of such parameters.

* For example, an attacker might craft a request with duplicate parameters:

  ```http
  GET /user/profile?id=123&id=124
  ```

* Depending on the underlying service or technology, the parameters will be handled in one way or another.
* Some frameworks prioritize the first parameter (`id=123`), while others use the last (`id=124`) or concatenate the values.
* If the first parameter is used for access control verification and the second parameter retrieves the resource, the application may inadvertently disclose unauthorized data.

## IDOR via method-based explotation

* Applications may implement different access controls for different HTTP methods, leading to bypass vulnerabilities.
* Modifying the request to use a different HTTP method, such as POST, might bypass access controls:

  ```http
  GET /user/profile?id=123
  ```

  ```http
  POST /user/profile
  Content-Type: application/x-www-form-urlencoded
  ...

  id=124
  ```

* This occurs because some applications treat GET and POST requests differently, either due to misconfigured access control rules or assumptions about request contexts.

## IDOR via unexpected values

* Applications that fail to validate input properly are vulnerable to IDOR exploitation using unexpected values. By sending unconventional input types, attackers can attempt to break application logic.
* For example, if the target accepts the following JSON body:

  ```json
  {
    "id": 123
  }
  ```

* An attacker might send various unexpected values to break the web application logic, such as:

  ```json
  {
    "id": -1
  }
  ```

  ```json
  {
    "id": 124.0
  }
  ```

  ```json
  {
    "id": [123, 124]
  }
  ```

  ```json
  {
    "id": true
  }
  ```

  ```json
  {
    "id": "123"
  }
  ```

* These inputs might exploit type coercion, validation flaws, or unanticipated application behavior, potentially leading to unauthorized access.

> :older_man: Type coercion is the process by which a programming language automatically converts a value from one data type to another during program execution. It occurs in dynamically typed or loosely typed languages like JavaScript, Python, or PHP, where variables are not strictly bound to a specific data type.

## Exploiting IDORs that require unpredictable IDs

* Some applications use UUIDs or other non-sequential identifiers to reduce the likelihood of IDOR exploitation.
* While these are harder to predict, they do not inherently eliminate the vulnerability, as they can still be exploited if an attacker discovers them via other means.
* For instance, UUIDs may be found in:
  * Publicly accessible user profile URLs.
  * Shared links generated by the application.
  * Password reset forms or invitation emails.
  * Application metadata or API responses.
  * Search engines (like Google and Bing)
* If UUIDs are exposed and access control is insufficient, attackers can still manipulate them to access unauthorized resources.

## Exercise to practice :writing_hand:

* The following web application contains an IDOR vulnerability that enables authenticated users to view other users' personal information (username and address).
* The exercise task involves logging into the application with `johndoe`'s credentials (username: `johndoe`, password: `Zw+?YmIZlrZF`) and leveraging the IDOR vulnerability to gain access to the `admin` user's address information.

  @@ExerciseBox@@
