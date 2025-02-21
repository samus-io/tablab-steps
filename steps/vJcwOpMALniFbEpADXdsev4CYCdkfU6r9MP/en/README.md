# Role-Based Access Control (RBAC)

* RBAC is a widely-used access control model where access permissions are assigned to roles, and users are assigned to roles based on their responsibilities.
* Users do not receive individual permissions directly; instead, they inherit permissions from the role they are assigned to.
* Roles define sets of permissions, and users inherit these roles, which determine the actions they are allowed to perform.

## How RBAC works

* Roles are defined to represent a set of permissions.
* Users are assigned one or more roles based on their needs.
* Defining permissions links actions to roles, determining which tasks users in each role can perform, such as viewing, editing, or deleting records.
* When a user requests access to a resource, the system evaluates their assigned role and verifies whether it has the required permissions. If access is permitted, the user is granted access; otherwise, it is denied.

### Example of RBAC

* The following image represents the implementation of RBAC in a banking system to manage access based on user responsibilities. Roles include `Administrator`, `Manager`, `Customer` and `Teller` and each role is associated with specific permissions:

    ![RBAC][1]

  * The `Administrator` role has permissions to manage user accounts, configure the system, and oversee security settings.
  * The `Manager` role has permissions to approve large transactions, generate reports, and oversee branch operations.
  * The `Customer` role is designed for end-users, allowing them to view their account balances, check transaction history, and transfer funds.
  * The `Teller` role includes permissions to handle customer deposits, withdrawals, and cash-related operations.
* Users are assigned one or more roles based on their job responsibilities.
* For example, a bank teller would be assigned the `Teller` role, while a bank manager could be assigned both `Manager` and `Teller` roles to allow flexibility in performing tasks.
* Roles can inherit permissions from other roles to streamline access management.
  * For instance, the `Manager` role may inherit all the permissions of the `Teller` role, ensuring managers can perform teller tasks when needed without explicitly assigning the `Teller` role.

#### How access decisions are made

* When a bank teller attempts to approve a large transaction, the system denies the request because the `Teller` role does not include the necessary permissions for that action.
* If a customer tries to access another customer's account information, the system also denies the request because the `Customer` role is restricted to accessing only their own account.
* In contrast, if a manager logs in, they are able to approve the transaction because their `Manager` role has the required permissions for such actions.

## Advantages of RBAC

* RBAC is simple and easy to implement.
* It provides clear definitions of roles and responsibilities, ensuring users understand their access limits.
* Permissions are managed efficiently at scale by assigning users to predefined roles.
* It is well-suited for hierarchical organizations where access levels align with job positions.
* Administrative workload is reduced by centralizing permission management through roles rather than individual assignments.
* Ensures data and information are handled according to confidentiality standards.
* Provides an easy way to demonstrate compliance with access control policies since roles and permissions are clearly documented.

## Disadvantages of RBAC

* RBAC offers limited granularity and flexibility, which may not meet the needs of more dynamic systems.
* Role explosion can occur in large systems, where too many roles are created to accommodate specific requirements.
* It is challenging to manage dynamic access control needs, such as granting temporary or situational permissions.
* Users may inadvertently receive more permissions than necessary, increasing security risks.
* Assigning roles in large or rapidly growing organizations can be complex and time-consuming.
* Ongoing maintenance is required to keep roles updated and aligned with organizational changes and evolving responsibilities.
* Collaboration between multiple teams may be necessary for effective implementation, which can increase coordination efforts and workload.

[1]: /static/images/rbac.png
