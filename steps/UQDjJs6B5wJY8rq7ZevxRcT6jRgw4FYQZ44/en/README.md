# Finding Horizontal Privilege Escalation

* There are multiple ways of finding Horizontal privilege escalation and the most encountered type of it called Insecure Direct Object References (IDOR). Some of them are included in the below list:

## Parameter manipulation

* Modify parameters in URLs or form submissions to access resources or perform actions intended for other users.
* An example is the URL used to access accounts like `/customerAccount?customerNumber=132355`, you can change the **customerNumber** parameter to **132356** to access another user's account.

## URL enumeration

* Enumerate through URLs to discover hidden or unlinked pages that may contain sensitive information or actions.
* Decide whether you want to use automated tools or manual methods for URL enumeration. Common tools include directory brute-forcing tools like DirBuster, Dirsearch, or Gobuster.
* One can perform manual enumeration using web browser developer tools or command-line tools like cURL.
* For instance, try accessing `/static/<file_name>` or `/user/<userId>` and discover if it contains sensitive information belonging to another user without requiring authentication.

## Referrer header manipulation

* Manipulate the Referer header to trick the application into granting access to unauthorized resources.
* For example, you can access a resource with a valid Referer header pointing to a legitimate page, but then change the Referer header to access another user's data.

## Brute Force or Guessing

* Guess or brute force object references to access resources or perform actions intended for other users.
* For example, Systematically try different identity numbers in URLs or parameters to find valid user accounts or sensitive data.

## API Testing

* Test application programming interfaces (APIs) to identify endpoints or parameters that may expose sensitive data or actions.
* Use tools like cURL or GUI tools like postman to test the endpoints of the application and verify if all the endpoints have the correct access control.
* For example, Let's say we have an API endpoint `/api/users` that retrieves a list of users. Here's how you can perform testing using cURL:

  ```bash
  # Send GET request to retrieve list of users
  curl -X GET http://api.example.org/api/users
  ```

## Error messages and responses

* Analyze error messages or response behaviors to identify instances where the application reveals sensitive information about other users.
* For instance, you can intentionally trigger errors or exceptions by manipulating parameters and observe if the application discloses details about other user's accounts or resources.

## Session Hijacking

* Hijack active user sessions to gain unauthorized access to other user's accounts or privileges.
* Check if it is possible to steal the Session ID through methods like Session Fixation, Cross-Site Scripting (XSS) or Session Side Jacking.
* For instance, you can force a valid session ID onto a victim, typically by tricking it into clicking on a specially crafted link containing a known session ID. Once the victim logs in using the fixed session ID, you can then use that session ID to gain unauthorized access. This is called **Session Fixation**.
