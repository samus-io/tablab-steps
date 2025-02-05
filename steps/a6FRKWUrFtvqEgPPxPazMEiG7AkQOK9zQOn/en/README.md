# What is Insecure Direct Object Reference (IDOR)?

* `Insecure Direct Object Reference (IDOR)` is a type of access control vulnerability in web applications that occurs when insufficient access controls allow malicious users to manipulate object references, such as identifiers or file names, to access restricted data or perform unauthorized actions.
* IDOR vulnerabilities commonly result in horizontal privilege escalation, allowing access to other users' data at the same privilege level. However, they can also lead to vertical privilege escalation, granting elevated privileges such as administrative access.
* Direct references to resources in web applications and APIs are common sources of IDOR vulnerabilities, while compiled libraries are less susceptible, as they usually enforce strict access controls.

## How it works

* An insecure direct object reference vulnerability takes place when these three conditions are present:
  1. The application exposes a direct reference pointing to an internal resource or operation (e.g., user IDs, file paths or database keys).
  1. The user is capable of modifying the URL or a form parameter to alter the direct reference.
  1. The application provides access to the internal object without properly verifying if the user is authorized.
* As a simple illustrative example, the following request includes a numerical identifier referencing a user ID for displaying profile information:

  ```http
  GET /user/profile?id=123
  ```

  An IDOR vulnerability may arise when access control mechanisms are either absent or ineffective, enabling unauthorized disclosure of information from other user profiles by simply modifying the identifier:

  ```http
  GET /user/profile?id=124
  ```

## What could be achieved by exploiting an IDOR vulnerability

* Exposed object references revealing direct database IDs can result in **unauthorized access to records containing sensitive data**, such as users' personal information (e.g., financial details, medical records, or private messages). This could lead to **data breaches**, identity theft, or misuse of private information.
* Unvalidated user ID values, command names, or API keys may be exploited to **execute unauthorized operations**, including resetting other users' passwords and **taking over accounts**, performing admin actions to add users or upgrade privileges, or accessing restricted APIs.
* **Manipulate the application's internal state and data**, potentially enabling changes to business logic (e.g., altering prices in an online store), updates to critical settings (e.g., deactivating security features), or session manipulation to impersonate users.
* Exploiting direct file access may allow attackers **unauthorized file acces**, which, when combined with path traversal techniques, can enable unauthorized file retrieval or modification, including overwriting or deletion.
