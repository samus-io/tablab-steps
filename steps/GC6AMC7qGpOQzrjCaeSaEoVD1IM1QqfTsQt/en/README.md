# Vertical Privilege Escalation

* Vertical Privilege Escalation occurs when a user gains access to higher levels of privileges or resources than they are authorized to have within a system.
* In this an attacker attempts to gain more permissions or access with an existing account they have compromised. For example, an attacker takes over a regular user account on a network and attempts to gain administrative permissions or root access.
* This typically happens due to vulnerabilities such as missing access controls, parameter-based access controls, or Broken Access Control (BAC) resulting from URL mismatching.

## Missing Access Control

* In this scenario, the system fails to properly enforce access controls, allowing users to perform actions or access resources beyond their authorized level.
* For example, a regular user may exploit a vulnerability to gain administrative privileges and access sensitive functionalities or data intended only for administrators.
* Example: A Node.js application that lacks proper access control might have an endpoint for deleting user accounts that doesn't check if the requester has the necessary administrative privileges. Here's a simplified example:

```js
// Route for deleting user accounts (vulnerable to missing access control)
app.delete('/users/:id', (req, res) => {
    const userId = req.params.id;
    // Delete user account from the database (no access control check)
    User.findByIdAndDelete(userId, (err, deletedUser) => {
        if (err) {
            return res.status(500).send('Internal Server Error');
        }
        res.send('User account deleted successfully');
    });
});

```

* Anybody can delete the users just by requesting to `/users/<id>` with DELETE Method.
* To solve the missing access control problem in the Node.js application, we need to implement proper access control checks to ensure that only authorized users can perform certain actions.

```js
// Route for deleting user accounts (with access control)
app.delete('/users/:id', (req, res) => {
    const userId = req.params.id;
    const authenticatedUserId = req.user.id;user ID
    const isAdmin = req.user.isAdmin; // Anything like isAdmin property indicating admin status

    // Check if the authenticated user is an admin or is deleting their own account
    if (isAdmin || userId === authenticatedUserId) {
        // Proceed with deleting the user account from the database
        User.findByIdAndDelete(userId, (err, deletedUser) => {
            if (err) {
                return res.status(500).send('Internal Server Error');
            }
            res.send('User account deleted successfully');
        });
    } else {
        // If the authenticated user is neither an admin nor the account owner, deny access
        res.status(403).send('Access Denied');
    }
});
```

## Parameter-based Access Control

* Parameter-based Access Control vulnerabilities occur when access permissions are determined based on user-supplied parameters or inputs without proper validation or sanitization.
* In this an attacker can manipulate these parameters to bypass access controls and gain unauthorized access. For instance, an attacker may tamper with URL parameters or form inputs to escalate their privileges and access restricted resources.
* Example: Suppose an application allows users to view their own profile information using an endpoint like /profile. However, it doesn't properly validate the user ID parameter, allowing any user to access any profile by manipulating the parameter:

```js
// Route for accessing user profile (vulnerable to parameter-based access control)
app.get('/profile/:userId', (req, res) => {
    const requestedUserId = req.params.userId;

    // Fetch and send profile information for the authenticated user
    User.findById(requestedUserId, (err, user) => {
        if (err) {
            return res.status(500).send('Internal Server Error');
        }
        res.json(user);
    });
});
```

* Here we have no checks, if it is the authenticated user requesting for profile details.
* To solve the parameter-based access control problem in the Node.js application, we need to ensure that the endpoint properly validates the user ID parameter to ensure that the authenticated user can only access their own profile information. Here's how we can modify the code to address this issue:

```js
// Route for accessing user profile (with proper parameter-based access control)
app.get('/profile/:userId', (req, res) => {
    const requestedUserId = req.params.userId;
    const authenticatedUserId = req.user.id; // Try to implement a logic to fetch uthenticated user ID

    // Check if the requested user ID matches the authenticated user's ID
    if (requestedUserId !== authenticatedUserId) {
        return res.status(403).send('Access Denied');
    }

    // Fetch and send profile information for the authenticated user
    User.findById(authenticatedUserId, (err, user) => {
        if (err) {
            return res.status(500).send('Internal Server Error');
        }
        res.json(user);
    });
})
```

## BAC Resulting from URL Mismatching

* Broken Access Control resulting from URL-matching discrepancies occurs when the application's access control mechanisms inconsistently enforce access restrictions based on variations in URL casing, parameters, or other factors.
* Examples of broken access control resulting from URL-matching discrepancies:

  * **Case Sensitivity Issues:**
    The application enforces access controls for URLs in a case-sensitive manner. However, some endpoints are accessible using different casing variations (e.g., /Admin/DeleteUser vs. /admin/deleteUser). Attackers can exploit this discrepancy to bypass access controls by accessing the same endpoint with a different casing.
  * **Trailing Slash Discrepancies:**
    The application enforces access controls for endpoints with trailing slashes (e.g., /admin/deleteUser/). However, the same endpoint without a trailing slash (e.g., /admin/deleteUser) lacks proper access controls. Attackers can exploit this discrepancy to access unprotected endpoints and perform unauthorized actions.
  * **Parameter-Based Discrepancies:**
    The application enforces access controls based on URL parameters (e.g., /admin/deleteUser?id=123). However, similar endpoints with variations in parameter names (e.g., /admin/deleteUser?userId=123) do not have proper access controls. Attackers can manipulate parameter names to bypass access controls and perform unauthorized actions.
  * **URL Encoding Vulnerabilities:**
    The application fails to properly decode and normalize URL-encoded characters, leading to discrepancies in URL matching. Attackers can exploit this vulnerability by encoding characters differently (e.g., %2Fadmin/deleteUser vs. /admin/deleteUser) to bypass access controls and access unprotected endpoints.
  * **Route Alias Vulnerabilities:**
    The application allows route aliases or shortcuts for certain endpoints (e.g., /admin/deleteUser aliased to /admin/removeUser). However, access controls are only enforced for the original endpoint and not the aliased one. Attackers can exploit this discrepancy by accessing the aliased endpoint to bypass access controls and perform unauthorized actions.
* Mitigating these vulnerabilities requires ensuring consistent enforcement of access controls across all variations of URLs and addressing any discrepancies in URL matching and access control enforcement.

## Vertical Privilege Escalation for both Authenticated and Unauthenticated users

* Vertical Privilege Escalation for both authenticated and unauthenticated users can have significant security implications, potentially leading to unauthorized access to sensitive functionalities or data within a system.

  * Scenarios for Authenticated Users:

    * Role-Based Privilege Escalation: An authenticated user exploits a vulnerability in the system's access control mechanisms to escalate their privileges beyond their assigned role. For example, a regular user may manipulate parameters or bypass access controls to gain administrative privileges, allowing them to access and modify sensitive data or perform administrative actions.
    * Session Hijacking: An attacker gains unauthorized access to an authenticated user's session, either by intercepting the session token or through session fixation techniques. With control over the user's session, the attacker can impersonate the user and access functionalities or data reserved for the legitimate user's role, potentially leading to data breaches or unauthorized actions.
    * Exploiting Business Logic Flaws: Authenticated users exploit flaws in the application's business logic to escalate their privileges. For example, a customer may manipulate the ordering process to bypass payment authentication, allowing them to place orders without paying or accessing discounted prices intended for privileged users.

  * Scenarios for Unauthenticated Users:

    * Parameter Manipulation: An unauthenticated user manipulates parameters or URL structures to access functionalities or data intended for authenticated users. For example, an attacker may tamper with URL parameters to access administrative pages or perform privileged actions without proper authentication, leading to unauthorized access or data breaches.
    * Exploiting Default Credentials or Backdoors: The system includes default credentials or backdoor access points that are not properly secured. An attacker discovers and exploits these vulnerabilities to gain unauthorized access to privileged functionalities or data without the need for authentication, potentially compromising the security of the entire system.
    * Insecure Direct Object References (IDOR): The application fails to properly enforce access controls on sensitive resources, allowing unauthenticated users to directly reference or manipulate object identifiers to access restricted data. For example, an attacker may manipulate URLs to access other users' private information or sensitive files stored on the server.
