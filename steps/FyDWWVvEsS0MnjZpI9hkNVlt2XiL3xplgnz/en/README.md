# Horizontal privilege escalation

* Horizontal privilege escalation occurs when a user gains unauthorized access to resources or functionalities belonging to other users within the same privilege level.
* This vulnerability allows attackers to move laterally across the application's user base, accessing other users' data or performing actions they are not authorized to execute.
* Exploiting horizontal privilege escalation can lead to unauthorized data exposure, account manipulation, or disruption of services.

## Referer-based access control

* Some applications use the HTTP `Referer` header to determine whether a request is allowed based on its origin. If access control is enforced solely through `Referer` validation, it becomes vulnerable to manipulation.
* If an application restricts access to certain files or APIs based on `Referer` validation, an attacker could send a crafted request without a `Referer` header or modify it to bypass access controls.
* Consider a web application that grants access to user information based on whether the request originates from the company's internal website.
* The application relies on the `Referer` header to determine if a request comes from a trusted internal system, allowing access to sensitive data without requiring additional authentication:

```javascript
// Middleware for referer-based access control
function internalAccessControl(req, res, next) {
    const internalURL = 'https://internal.example.tbl';
    const referer = req.headers['referer'];

    if (!referer || !referer.startsWith(internalURL)) {
        return res.status(403).send('Access denied');
    }

    next();
}

// Protected route for internal requests only
app.get('/user/profile/:username', internalAccessControl, (req, res) => {
    User.findOne({ username: username }, (err, user) => {
        if (err) {
            return res.status(500).send('Internal Server Error');
        }
        if (!user) {
            return res.status(404).send('User not found');
        }
        res.json(user);
    });
});
```

* If the request contains a `Referer` header from the internal network, such as:

  ```http
  Referer: https://internal.example.tbl
  ```

* Then the access control will assume that the user is authorized and provides access to restricted information.
* An attacker outside the network can exploit this by modifying or forging the `Referer` header to appear as if their request is coming from the internal website.
* This can lead to data leaks, allowing the attacker to retrieve confidential records or personal details of other users.

## Location-based access control

* Some applications restrict access to content or functionalities based on a user's geographical location. If location-based access control is improperly implemented, attackers can manipulate their location to bypass restrictions.
* An attacker can use a VPN, proxy, or GPS spoofing techniques to disguise their actual location and access content or features meant for users in specific regions.
* If an application relies only on IP-based location checks without additional verification, an attacker can access geo-restricted services, potentially exposing sensitive data meant for specific regions.

## Insecure Direct Object References (IDOR)

* `Insecure Direct Object Reference (IDOR)` is a type of access control vulnerability in web applications that occurs when insufficient access controls allow malicious users to manipulate object references, such as identifiers or file names, to access restricted data or perform unauthorized actions.
* Direct references to resources in web applications and APIs are common sources of IDOR vulnerabilities, while compiled libraries are less susceptible, as they usually enforce strict access controls.
* As a simple illustrative example, the following request includes a numerical identifier referencing a user ID for displaying profile information:

  ```http
  GET /user/profile?id=123
  ```

* An IDOR vulnerability may arise when access control mechanisms are either absent or ineffective, enabling unauthorized disclosure of information from other user profiles by simply modifying the identifier:

  ```http
  GET /user/profile?id=124
  ```

* IDOR is not limited to user profiles and can expose financial records, invoices, order details, among others, if access controls are missing or improperly implemented.
