# Preventing Privilege Escalation

* By incorporating the below principles into your application development process, you can establish robust access controls and reduce the risk of privilege escalation vulnerabilities:

## Enforce Least Privileges

* This principle advocates for granting users the minimum level of access or permissions required to perform their tasks effectively. By limiting privileges, you reduce the potential impact of security breaches and unauthorized access.
* During design phase of any app, define trust boundaries, user types, resources, and operations they can perform. Granting too many permissions is risky, so plan carefully to avoid needing to revoke later.
* An example of this is in a web application, instead of giving all users administrative privileges, create different roles such as **admin**, **editor**, and **user**. Admins have full control, editors can edit content but not manage users, and regular users have limited access to their own profile information. The roles should have their own permissions and should ensure that it is both horizontally and vertically controlled.

## Deny by Default

* Following the **deny by default** principle means that access to resources is denied unless explicitly allowed. This approach helps minimize the attack surface and reduces the risk of unauthorized access.
* Keep in mind to justify permissions granted to users or groups, rather than assuming access is the default and to explicitly configure over relying on default settings of frameworks or libraries, as these may change over time without the developer's knowledge.
* For instance one can configure network firewalls to block all incoming traffic by default and only allow specific ports or IP addresses that are required for legitimate communication.

### Example Deny by Default Access Control in Nodejs + Express

* Let's implement **deny by default** access control in a Node.js application using a simple Express server and a Client-side API call.

#### Server-side implementation (Node.js)

```javascript
  const express = require('express'); // install express
  const session = require('express-session'); // install express-session
  const app = express();

  // Middleware for session authentication
  app.use(session({
      secret: 'secret',
      resave: true,
      saveUninitialized: true
  }));

  // Middleware for access control
  app.use((req, res, next) => {
      // Check if user is authenticated
      if (req.session.authenticated || req.path == '/login') {
          return next(); // Allow access for authenticated users
      }
      // Deny access by default
      return res.status(403).send('Access denied');
  });

  app.get('/login', (req, res) => {
      // Simulate login
      req.session.authenticated = true;
      res.send('Login successful');
  });

  app.get('/logout', (req, res) => {
      // Simulate logout
      req.session.authenticated = false;
      res.send('Logged out');
  });

  app.get('/data', (req, res) => {
      res.json({ message: 'Access granted for authenticated user' });
  });

  app.listen(3000, () => {
      console.log('Server is running...');
  });
```

#### Client-side implementation (API call)

* Firstly, send a `GET` request to the path `/data`. It will deny with `403` response code.
* Secondly, make a request to `/login` and then to `/data`. It will grant access.
* Finally, send a request to `/logout` and then `/data`. It will deny again.
* This setup simulates the deny by default prevention technique.

## Validate permissions on every request before anything else

* Authorization checks should be performed as the first step in request processing to ensure that only authorized users can access resources or perform actions.
* Ensure the access control technology used allows for global configuration across the entire application. Even a single missed access control check can compromise the confidentiality or integrity of a resource.
* An example would be to implement middleware in nodejs app to verify user permissions before executing route handlers. If a user lacks the necessary permissions, return a `403 Forbidden` response without further processing.

## Enforce Authorization checks on static resources

* Static resources such as files, directories, or endpoints should also be protected by access controls to prevent unauthorized access or disclosure of sensitive information.
* For cloud services like GCP or AWS or Azure, use configuration options and tools provided by cloud service vendors to secure static resources. Refer to documentation from providers for specific implementation details.
* Ensure uniform protection across all aspects of the application to maintain security consistency.
* For instance, one can configure web server settings (e.g., Apache, Nginx) to restrict access to directories containing sensitive files, such as configuration files or logs. Use server directives like **Deny from all** or **Require all denied** to enforce access controls.

## Verify that Authorization checks are performed in the right location

* Authorization logic should be implemented consistently across all layers of the application stack, including frontend (UI) and backend (API) components, to prevent bypassing of access controls.
* An example is to perform authorization checks in a single-page application (SPA) on both the client-side and server-side. The client-side checks provide a better user experience by hiding or disabling unauthorized UI elements, while the server-side checks enforce security and prevent unauthorized API access.

## Create Unit and Integration Test cases for Authorization logic

* Testing authorization logic ensures that access controls are correctly enforced and help identify vulnerabilities or misconfigurations early in the development lifecycle.
* For instance one can write unit tests using testing frameworks like Jest or Mocha to validate authorization functions or middleware. Include test cases for different user roles and scenarios to verify proper enforcement of access controls. Additionally, create integration tests to simulate real-world interactions and validate end-to-end authorization workflows.

## Proper Error Handling and Logging

* Deal with access control failures carefully and make sure to handle all errors, even if they seem unlikely.
* Keep the handling of access control failures in one place. Double-check how you handle errors and access control failures to avoid making the software unstable.
* Do not reveal any sensitive information to users when a failure occurs. Instead inform them that the attempted operation was not successful.
* Utilize clear and consistent log formats for easy analysis. Tailor logging levels to match application needs and environment.
* Maintain synchronized clocks and timezones across systems. Integrate application logs into a centralized server.
* For example, if a user tries to access a premium feature without a subscription, the application should display a message explaining the need for a subscription instead of crashing or exposing sensitive data.

## Ensuring protected access to object identifiers

* Keep object identifiers hidden from users whenever possible.
* Use techniques to obfuscate or randomize identifiers to prevent easy guessing.
* Implement access controls to verify permissions for each object or functionality accessed. Ensure that users cannot access unauthorized resources by manipulating object identifiers in URLs or other parameters.
* For instance, in a banking application, instead of exposing account numbers in URLs like `https://example.org/account?acct_id=2024`, use session-specific references to retrieve account details securely.

## Review the Access Control logic of chosen technologies and implement necessary custom logic

* Pick libraries and frameworks carefully, considering their security track record. Understand the authorization logic provided by chosen components.
* Regularly check for vulnerabilities in third-party components. Don't rely solely on one framework or library for access control.
* Understand the capabilities of the technologies you use. Don't depend solely on default configurations.
* Test configurations thoroughly in your specific environment.
* Suppose you're using a popular authentication library for your web application. By default, it allows users to reset their passwords via email without verifying their identity. To ensure secure access control, you customize the configuration to require additional verification steps before allowing password resets, such as answering security questions or entering a temporary code sent to their registered phone number.
