# Types of broken access control

* The following image represents a hierarchy of privileges within a system, visualized as a triangle. Each level in the hierarchy corresponds to different levels of access rights, with users positioned according to their privileges.
* The **highest privilege** is positioned at the top of the triangle, this level signifies the most extensive access rights within the system, typically held by administrators. Individuals at this level have full control over the application and its resources.
* The **lowest privilege** found at the base of the triangle represents the most restricted access rights, such as guests or standard users. These users can perform only basic actions permitted by the system.
* **Vertical access control** is represented by the upward arrow, illustrating an attacker or low-privileged user attempting to bypass access controls to gain a higher privilege level. For example, a guest user exploiting vulnerabilities to perform actions reserved for administrators demonstrates a failure of vertical access control.
* **Horizontal access control** is represented by the arrow pointing to the right, highlights scenarios where an attacker at one privilege level attempts to access resources or data belonging to another user at the same privilege level. For example, a standard user attempting to view or modify the private data of another user.

![Access Control Hierarchy][1]

## Vertical privilege escalation

* Vertical access control restricts access to specific resources or functionalities based on the user's privilege level. It ensures that users can only perform actions or access information relevant to their role or authorization level.
* Vertical privilege escalation occurs when a lower-privileged user gains unauthorized access to higher-privileged resources.
* Considering an e-commerce platform, customers can view and manage their own orders, while administrators can access all customer orders, modify product listings, and handle financial reports.
* An example of privilege escalation would occur if a regular customer manipulates the URL or API request to access an admin-only feature, such as viewing all orders or editing product details.
* For instance, a regular user accessing the admin dashboard by navigating to:

  ```
  https://example.tbl/admin/orders
  ```

* Or using an API endpoint like:

  ```
  GET /api/admin/orders
  ```

* If proper access control isn't enforced, the user could gain unauthorized access to sensitive business data or even modify products.

## Horizontal privilege escalation

* Horizontal access control ensures that users with the same privilege level can only access their own resources or data.
* It prevents one user from viewing or manipulating resources belonging to another user at the same privilege level.
* Horizontal privilege escalation occurs when a user accesses another user's resources without proper authorization.
* Following the same e-commerce example, a privilege escalation would occur if a user manipulates the URL or API requests to access other user's data, such as obtaining its private information or making actions on its behalf.
* For instance, a regular user accessing to another user's order by navigating to:

  ```
  https://example.tbl/getOrder?id=1234
  ```

* Or using an API endpoint like:

  ```
  GET /api/order/1234
  ```

* If proper access control isn't enforced, a user could access to sensitive user's data.

## Context-dependent access control

* Context-dependent access control dynamically adjusts access permissions based on the user's attributes, the application state, or environmental conditions.
* It ensures that permissions change based on contextual factors, offering a granular approach to access control.
* For example, in an e-commerce after payment, the web application locks the shopping cart, and any attempt to modify its contents (e.g., changing item quantities or adding items) is restricted. The server verifies that the cart's status is marked as `Paid` before allowing any actions.
* A breach on access control will occur if a user manipulates a client-side request to bypass the restriction and attempts to change the shopping cart contents even after payment.
* This could allow the user to modify orders by adding more content to their order than they have paid for.

[1]: /static/images/Access_control_types.png
