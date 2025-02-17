# Vertical privilege escalation

* Vertical privilege escalation occurs when a user exploits a vulnerability to gain unauthorized access to higher levels of privileges or resources, surpassing their designated authorization level.
* In this type of escalation, an attacker attempts to elevate the permissions of an account they control or have compromised, allowing them to perform actions reserved for higher-privileged roles, such as administrators.
* Some vulnerabilities that can lead to vertical privilege escalation can be missing access controls, parameter-based access controls or broken access control by URL mismatching.

## Missing access control

* Missing access control is the most basic type of broken access control. In this scenario, the web application fails to enforce access controls, allowing users to perform actions or access resources beyond their authorized level.
* For example, a regular user may exploit this vulnerability to gain administrative privileges and access sensitive functionalities or data intended only for administrators.
* In a web application lacking proper access control, the following endpoint for deleting user accounts is vulnerable because it fails to verify whether the requester possesses the necessary administrative privileges before performing the action:

  ```javascript
  // Route for deleting user accounts
  app.delete('/users/:id', (req, res) => {
      const userId = req.params.id;
      // Delete user account from the database without access control check
      User.findByIdAndDelete(userId, (err, deletedUser) => {
          if (err) {
              return res.status(500).send('Internal Server Error');
          }
          res.send('User account deleted successfully');
      });
  });
  ```

* In the previous example, any user (including those not authenticated) can delete the users just by requesting to `/users/<id>` with `DELETE` method.

## Parameter-based access control

* These vulnerabilities occur when access permissions are determined using user-supplied parameters or inputs without properly validating their authenticity or origin. This flawed approach enables attackers to manipulate parameters and bypass access controls.
* In such cases, attackers can manipulate these parameters to bypass access controls and gain unauthorized access. For instance, an attacker may tamper with URL parameters to escalate their privileges and access restricted resources.
* Consider a web application where administrators can view all user information through an endpoint like `/admin/users`. The application uses a query parameter, such as `isAdmin`, to determine whether the requester has administrative privileges. If the server logic simply checks the presence of this parameter without verifying the user's role or authentication status, attackers can exploit it by tampering with the parameter to gain unauthorized access:

  ```javascript
  // Route for accessing user profile
  app.get('/admin/users', (req, res) => {
      const isAdmin = req.query.isAdmin;

      if (isAdmin) {
          User.findMany({}, (err, users) => {
              if (err) {
                  return res.status(500).send('Internal Server Error');
              }
              res.json(users);
          });
      }
      else {
          res.status(403).send('Access Denied');
      }
  });
  ```

* In this example, an attacker could manipulate the URL by modifying the `isAdmin` parameter:

  ```url
  https://example.tbl/admin/users?isAdmin=true
  ```

## Vertical privilege escalation for authenticated and unauthenticated users

* Even in the simplest access control models where there are only user and administrator roles, there is also an implicit third role, unauthenticated users, which is often overlooked in access control implementation. If an unauthenticated user manages to perform actions as an authenticated user or administrator, it is also considered vertical privilege escalation.
* Some web applications fail to apply proper access control to administrator functions, making them accessible to both authenticated and unauthenticated users. This allows privilege escalation where an attacker can directly access admin functionalities without having an authorized session.
* In other cases, access control only verifies whether a user is authenticated, but does not check their assigned role. This allows users to escalate privileges by exploiting flaws in role validation, granting them unintended administrative access.
