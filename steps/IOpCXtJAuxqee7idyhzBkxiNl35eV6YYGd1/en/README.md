# Preventing privilege escalation

* Incorporating the principles below into the application development process helps establish robust access controls and reduce the risk of privilege escalation vulnerabilities.

## Principle of least privilege

* The principle of least privilege advocates for granting users the minimum level of access or permissions required to perform their tasks effectively.
* Restricting privileges reduces the risk of security breaches, unauthorized access and potential damage caused by compromised accounts.
* During the design phase of a web application, defining trust boundaries, user roles, resources, and allowed operations is essential to maintain secure access control.
* Assigning excessive permissions can introduce security risks, making it crucial to carefully plan access levels to avoid unnecessary revocations later. Adding permissions is easier than removing them.
* Access control should be enforced at both horizontal and vertical levels to prevent unauthorized access to other user's data and privileged functionalities.
* Applying this principle strengthens security by minimizing the attack surface and ensuring that users can only perform actions relevant to their responsibilities.

### Practical example

* An example of the principle of least privilege would be a web application that has two primary roles:
  * A `User` which has basic permissions, such as managing their own profile and performing limited actions within the system.
  * An `Administrator` which has full control, including managing users, modifying system settings, and accessing sensitive data.
* Consider that there is one user that needs the ability to impersonate users to troubleshoot issues or assist customers.
* Assigning the `Administrator` role to the support agent would be too excessive, as it would grant them unnecessary permissions beyond impersonation.
* Increasing the `User` role privileges for all users would be too broad, potentially exposing impersonation capabilities to users who should not have it.
* Instead of misusing existing roles, a new role such as `Support Agent` or `Customer Service` should be created.
* This new role is assigned only the necessary permissions, allowing user impersonation but restricting access to system settings, security controls, or administrative features.
* This ensures that users receive only the permissions they need to perform their tasks, reducing security risks and preventing unauthorized access to sensitive system functions.

## Deny by default

* The deny by default principle ensures that access to resources is restricted unless explicitly granted, reducing the risk of unauthorized access and minimizing the attack surface.
* Access permissions should be explicitly defined rather than assumed, preventing unintended access due to misconfigurations or default settings.
* Justifying permissions before granting them helps maintain tight access control, ensuring that users and groups receive only the necessary privileges.
* A practical example of the deny by default principle would be a web application where access to all endpoints are initially restricted, preventing unauthorized users from accessing any functionality.

  <details>
    <summary>Dependencies</summary>

    ```javascript
    const express = require("express");
    const session = require("express-session");
    ```

  </details>

  ```javascript
  const app = express();

  // Configure session middleware
  app.use(session({
    secret: "sessionsecret",
    resave: false,
    saveUninitialized: false,
  }));

  // Authorization middleware that checks for allowed roles from the session
  const authMiddleware = (allowedRoles) => (req, res, next) => {
    const role = req.session?.user?.role; // Extract role from the session

    if (allowedRoles.includes("public") || (role && allowedRoles.includes(role))) {
      return next(); // Grant access if the role is authorized
    }
    return res.status(403).send("Access denied.");
  };
  ```

  ```javascript
  app.get("/", authMiddleware(["public"]), (req, res) => {
    res.send("Welcome!");
  });

  app.get("/login", authMiddleware(["public"]), (req, res) => {
    // Login logic
  });

  // Explicitly authorized routes
  app.get("/admin", authMiddleware(["admin"]), (req, res) => {
    res.send("Welcome, Admin!");
  });

  app.get("/user", authMiddleware(["user", "admin"]), (req, res) => {
    res.send("Welcome, User!");
  });
  ```

* By default, the web application will block all requests unless explicit access control rules are defined for specific roles or the definition that the endpoint is public.
* Applying this approach enforces a proactive security model, where access decisions are carefully evaluated rather than assumed, reducing exposure to potential threats.

## Verify permissions before processing requests

* Authorization checks should be the first step in request processing to ensure that only authorized users can access resources or perform actions.
* Performing access control verification at the beginning of request handling prevents unnecessary processing and protects sensitive data from unauthorized access.
* Using a global access control configuration helps maintain consistency across the entire application and reduces the risk of misconfigured permissions.
* An effective approach is to implement middleware in the web application to verify user permissions before executing the endpoint's logic.
* The following code snippet ensures that the `authMiddleware` is the first to process the request:

  ```javascript
  const customMiddleware = () => (req, res, next) => {
    // Custom middleware that applies application logic
    return next(); 
  };

  const authMiddleware = (allowedRoles) => (req, res, next) => {
    const role = req.session?.user?.role; // Extract role from the session

    if (allowedRoles.includes("public") || (role && allowedRoles.includes(role))) {
      return next(); // Grant access if the role is authorized
    }
    return res.status(403).send("Access denied.");
  };

  app.get("/profile", authMiddleware(["user", "admin"]), customMiddleware, (req, res) => {
    res.send("Welcome, User!");
  });
  ```

* If a user does not have the necessary privileges, the web application returns a `403 Forbidden` response without processing the request further.

## Enforce authorization checks on static resources

* Static resources that are not meant to be publicly accessible, such as user profile pictures, invoices, system logs, or private documents, must be protected by proper access control mechanisms to prevent unauthorized access and data leakage.
* Instead of serving static resources directly, the backend should enforce authentication and authorization checks before granting access.
* After verifying the user's identity, the backend checks whether they have the necessary permissions to access the requested file.
* If authorized, the backend retrieves the file from secure storage, such as a protected server directory, database, or cloud storage service, and serves it to the user.

  ```javascript
  // Secure route to serve private files with authorization checks
  app.get("/private/files/:filename", authMiddleware, (req, res) => {
    const filesDirectory = "/var/www/users/files/";
    const filename = req.params.filename;

    // Construct the full file path
    const filePath = path.join(filesDirectory, filename);

    // Check if the file exists
    if (!fs.existsSync(filePath)) {
      return res.status(404).send("File not found.");
    }

    // If authorized and file exists, serve the file
    return res.sendFile(filePath, (err) => {
      if (err) {
        console.error(err);
        return res.status(500).send("Error reading file.");
      }
    });
  });
  ```


## Create unit and integration test cases for authorization logic

* Testing authorization logic ensures that access controls are correctly enforced, preventing unauthorized access to sensitive resources.
* Identifying vulnerabilities or misconfigurations early in the development lifecycle reduces the risk of security breaches.
* Writing unit tests using testing frameworks helps validate authorization functions, middleware, and access control mechanisms in isolation.
* Unit tests should include different user roles, permissions, and scenarios to verify that access restrictions work as intended.
* For example, a test can confirm that a regular user cannot access admin-only routes while an administrator can perform privileged actions.

  ```javascript
  describe("authorize middleware (unit tests)", () => {
    it("calls next if user has the required role", () => {
      const { req, res, next } = mockExpress("admin");
      const middleware = authorize("admin");

      middleware(req, res, next);
      expect(next).toHaveBeenCalled();
    });

    it("returns 403 if user does not have the required role", () => {
      const { req, res, next } = mockExpress("user");
      const middleware = authorize("admin");

      middleware(req, res, next);
      expect(res.status).toHaveBeenCalledWith(403);
      expect(res.json).toHaveBeenCalledWith({ error: "Access denied." });
      expect(next).not.toHaveBeenCalled();
    });

    it("returns 403 if user role is undefined", () => {
      const { req, res, next } = mockExpress(undefined);
      const middleware = authorize("admin");

      middleware(req, res, next);
      expect(res.status).toHaveBeenCalledWith(403);
      expect(res.json).toHaveBeenCalledWith({ error: "Access denied." });
      expect(next).not.toHaveBeenCalled();
    });
  });
  ```

* Testing should cover horizontal and vertical privilege escalation attempts to ensure unauthorized users cannot escalate their access.
* Automated testing helps maintain consistent security validation and prevents accidental changes from introducing access control flaws.
* Additionally, integration tests should simulate real-world interactions to verify end-to-end authorization workflows across different application components.

## Review the access control logic of chosen technologies and implement necessary custom logic

* Understand how the authorization logic works in the technologies being used to ensure it aligns with security best practices.
* Evaluate the capabilities and limitations of the chosen technologies instead of depending on default configurations.
* Implement custom authorization logic where necessary to ensure security policies are enforced according to the application's requirements.
* Review and update access control settings as new security threats emerge to maintain strong protection against unauthorized access.
  * Regularly check for vulnerabilities in third-party components and apply updates or patches to mitigate security risks.

## Proper error handling and logging

* Handle access control failures carefully to ensure that all errors are managed properly, even those that seem unlikely.
* Avoid exposing sensitive information when an access failure occurs. Instead, return a generic message indicating that the operation was unsuccessful.
  * For example, if a user attempts to access a premium feature without a subscription, the system should display a clear message explaining that a subscription is required instead of crashing or exposing internal system details.
* Adjust logging levels to align with application needs and security requirements, ensuring that sensitive data is not logged in production environments.
* Its recommended to store logs in a centralized location to facilitate monitoring, security audits, and real-time threat detection.
* Proper error handling ensures that security violations are logged while preventing attackers from gaining insights into system vulnerabilities.
