# What is Insecure Direct Object Reference (IDOR)?

* `Insecure Direct Object Reference (IDOR)` is a type of access control vulnerability in web applications where the absence of proper access control allows malicious users to alter object references, such as identifiers or file names, to gain access to restricted data or perform unauthorized actions on the system.
* IDOR vulnerabilities typically involve horizontal privilege escalation, although they may also enable vertical privilege escalation.
* IDOR vulnerabilities are typically found in web applications and APIs, being significantly less common in libraries.

## How it works

* An insecure direct object reference vulnerability takes place when these three conditions are present:
  * The application exposes a direct reference pointing to an internal resource or operation.
  * The user is capable of modifying the URL or a form parameter to alter the direct reference.
  * The application provides access to the internal object without verifying if the user is authorized.
* A request containing a numerical identifier that displays user profile information can serve as a demonstrative example:

  ```http
  GET /user/profile?id=123
  ```

  When the lack of access control mechanisms allows information from other user profiles to be disclosed by simply altering the identifier:

  ```http
  GET /user/profile?id=124
  ```

## What could be achieved with an IDOR

* Exposed object references revealing direct database IDs can result in **unauthorized access to records containing sensitive data**, such as users' personal information (e.g., financial details, medical records, or private messages).
* Unvalidated user ID values, command names, or API keys may be exploited to **execute unauthorized operations**, including resetting other users' passwords and taking over accounts, performing admin actions to add users or upgrade privileges, or accessing restricted APIs.
* **Manipulate the application's internal state and data**, potentially enabling changes to business logic (e.g., altering prices in an online store), updates to critical settings (e.g., deactivating security features), or session manipulation to impersonate users.
* **Gain direct access to files** stored on the server, which, when combined with path traversal, may allow manipulation of file systems and alteration of other users' data.
