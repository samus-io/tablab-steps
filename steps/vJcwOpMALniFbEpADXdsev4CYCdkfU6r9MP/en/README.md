# Types of access control

* There are multiple types of access control, but the most commonly used in web applications are:
  * Role-Based Access Control (RBAC).
  * Attribute-Based Access Control (ABAC).
  * Relationship-Based Access Control (ReBAC).
* These models define how users, roles, attributes, and relationships interact to enforce security policies and restrict access to sensitive resources.

## Role-Based Access Control (RBAC)

* RBAC is a widely-used access control model where access permissions are assigned to roles, and users are assigned to roles based on their responsibilities.
* Users do not receive individual permissions directly; instead, they inherit permissions from the role they are assigned to.
* Roles define sets of permissions, and users inherit these roles, which determine the actions they are allowed to perform.

### How RBAC works

* Roles are defined to represent a set of permissions.
* Users are assigned one or more roles based on their needs.
* Defining permissions links actions to roles, determining which tasks users in each role can perform, such as viewing, editing, or deleting records.
* When a user requests access to a resource, the system evaluates their assigned role and verifies whether it has the required permissions. If access is permitted, the user is granted access; otherwise, it is denied.

#### Example of RBAC

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

##### How access decisions are made

* When a bank teller attempts to approve a large transaction, the system denies the request because the `Teller` role does not include the necessary permissions for that action.
* If a customer tries to access another customer's account information, the system also denies the request because the `Customer` role is restricted to accessing only their own account.
* In contrast, if a manager logs in, they are able to approve the transaction because their `Manager` role has the required permissions for such actions.

### Advantages of RBAC

* RBAC is simple and easy to implement.
* It provides clear definitions of roles and responsibilities, ensuring users understand their access limits.
* Permissions are managed efficiently at scale by assigning users to predefined roles.
* It is well-suited for hierarchical organizations where access levels align with job positions.
* Administrative workload is reduced by centralizing permission management through roles rather than individual assignments.
* Ensures data and information are handled according to confidentiality standards.
* Provides an easy way to demonstrate compliance with access control policies since roles and permissions are clearly documented.

### Disadvantages of RBAC

* RBAC offers limited granularity and flexibility, which may not meet the needs of more dynamic systems.
* Role explosion can occur in large systems, where too many roles are created to accommodate specific requirements.
* It is challenging to manage dynamic access control needs, such as granting temporary or situational permissions.
* Users may inadvertently receive more permissions than necessary, increasing security risks.
* Assigning roles in large or rapidly growing organizations can be complex and time-consuming.
* Ongoing maintenance is required to keep roles updated and aligned with organizational changes and evolving responsibilities.
* Collaboration between multiple teams may be necessary for effective implementation, which can increase coordination efforts and workload.

## Attribute-Based Access Control (ABAC)

* ABAC is an access control model that makes decisions based on attributes of users, resources, and environmental conditions.
* When a user requests access to a resource, the system evaluates attributes such as user role, department, or clearance level, along with resource attributes like sensitivity level or owner.
  * Environmental conditions such as time, location or device type can also be considered in the evaluation.
* Access is granted only if the attributes of the user match the attributes required by the resource.
* ABAC allows for more fine-grained and dynamic access control by considering multiple factors beyond just roles or predefined rules.

### How ABAC works

* Attributes are characteristics or types of users, resources or the environment.
* Access control policies are created using combinations of attributes to determine permissions.
* When a user requests access to a resource, the system evaluates the access control policies based on the attributes of the user, resource, and environment. If the user's attributes match the policy criteria, access is granted; otherwise, access is denied.

#### Example of ABAC

* The following image represents the implementation of ABAC in an enterprise to manage access based on the attributes `Users`, `Department`, `Document Type` and `Access Time`. The combination of these attributes define the access to resources and functionalities:

    ![ABAC][2]

  * User attributes such as role (e.g., `Employee` or `Manager`) determine access levels and responsibilities.
  * Department attributes, such as `Finance` or `Human Resources`, help restrict access to documents based on organizational roles.
  * Resource attributes like document sensitivity, classified as `Confidential` or `Public`, ensure that only authorized users can access protected information.
  * Time-based attributes, such as `During Business Hours` or `After Hours`, regulate when a resource can be accessed.
* Access decisions are dynamically determined by evaluating the attributes specified in the access control policies against the attributes of the user, resource, and environmental context in real time.
* ABAC provides granular access control by allowing policies to consider multiple attributes and conditions simultaneously.

##### How access decisions are made

* Based on the previous image, here are some example policies that could be implemented using ABAC:
  * Only users with the `Manager` attribute in the `Finance` department are allowed to create and modify invoices.
  * Employees in the `HR` department can access employee records, but only during business hours.
  * Documents classified as `Confidential` can only be accessed by `Managers`, while documents marked as Public can be accessed by all employees.
  * Users with the `Employee` attribute can view payroll details, but only `Managers` in the Finance department can approve payroll changes.
* These policies ensure fine-grained access control by evaluating multiple attributes simultaneously, such as user role, department, document sensitivity and access time.

### Advantages of ABAC

* ABAC provides granular and dynamic access control, allowing fine-tuned decisions based on multiple attributes.
* Policies are flexible and can be customized based on user roles, resource sensitivity, and environmental conditions.
* The model can adapt to changing environments, ensuring access rules remain effective as organizational needs evolve.
* ABAC supports the principle of least privilege, ensuring users have access only to the resources necessary for their tasks.
* Policies can incorporate contextual factors such as location, time, and device type, enhancing security.
* The system enables centralized policy enforcement, making it easier to manage access across different resources and applications.

### Disadvantages of ABAC

* Implementing ABAC is complex, requiring a detailed definition of attributes and policies.
* Managing a large number of attributes across users, resources, and environments can be challenging.
* The risk of attribute sprawl increases as more attributes are introduced, leading to inconsistencies in policy enforcement.
* The system introduces performance overhead due to real-time evaluation of multiple attributes for each access request.
* Policies require continuous updates to remain aligned with evolving business and security requirements.
* Organizations may need specialized tools or frameworks to efficiently implement and maintain ABAC policies.

## Relationship-Based Access Control (ReBAC)

* ReBAC is an access control model that considers relationships between entities (such as users, resources, and roles) when making access decisions. Unlike traditional access control models like Role-Based Access Control (RBAC), which primarily focus on roles and permissions, ReBAC evaluates the connections and associations between entities within an organization.
* Access control policies in ReBAC define rules based on how users and resources are related, rather than just assigning static roles.
* Policies specify conditions for granting or denying access by analyzing relationships between users, resources, and other entities.
* This model is particularly useful in collaborative environments, where access needs to be dynamically adjusted based on interactions between different users and shared resources.
* ReBAC enables fine-grained access control by considering real-time relationships, making it effective for systems that require dynamic access management.

### How ReBAC works

* ReBAC determines access permissions based on relationships that are defined between users and resources, indicating associations such as ownership, creation, or specific interactions.
* Permissions are assigned based on these relationships, specifying what actions users can perform on resources they have a relationship with.
  * Relationships can be direct (e.g., an employee managing a project) or indirect (e.g., an employee belonging to a team that owns the project).
  * For example, a policy might specify that only a document owner and their direct collaborators can edit a file, while others can only view it.
* When a user requests access to a resource, the system evaluates the existing relationships between the user and the resource to determine whether access should be granted.
  * If a user is not explicitly related to the resource in the required way, the system denies access.
* ReBAC enables dynamic access control, adjusting permissions as relationships change, making it ideal for social networks, collaboration platforms, and enterprise resource management systems.
* Unlike traditional models, ReBAC ensures that access evolves with user interactions, reducing the need for manual permission management.
* Normally in ReBAC systems, groups are established to group different users or resources together to make it easier to manage permissions.

#### Example of ReBAC

* The following image represents the implementation of ReBAC in a medical system to manage access based on the user relationships:

![ReBAC][3]

* In this medical system, access to resources may be controlled based on relationships such as:
  * The creator or owner of a resource has permission to edit or delete it.
    * `Sam` and `Bob` are owners of their respective `Member Profiles`, giving them full control over their own `Medical Plans` and `Medical Records`.
  * Users belonging to a specific group have access to the resources that belongs to that group.
    * Bob has an `Admin` role, likely granting him additional permissions to manage group resources.
  * Access permissions are inherited from higher-level entities such as organizational units or parent resources.
    * If a user has access to a `Member Profile`, they also inherit access to its associated medical resources, such as `Medical Plan` and `Medical Record`.

### Advantages of ReBAC

* Provides fine-grained access control by defining permissions based on relationships between users, resources, and groups.
* Access control policies are intuitive, reflecting real-world relationships such as ownership, caregiving roles, or team membership.
* The model supports complex access scenarios, including multi-tenancy environments, where multiple organizations or user groups share the same system.
* Cross-organizational access can be securely managed, allowing controlled collaboration between different entities.
* Security is enhanced by restricting access based on specific relationships, using the deny by default method, ensuring that only authorized users can interact with certain resources.
* Permissions are dynamically adjusted as relationships change, reducing the need for manual role assignments and making the system more flexible.

### Disadvantages of ReBAC

* Managing relationships and permissions requires careful planning to prevent unintended access issues.
* The complexity increases as the number of relationships grows, making large-scale implementations more challenging.
* Systems with highly dynamic data may face difficulties in maintaining accurate and up-to-date relationships for access control.
* Performance overhead can arise when evaluating relationship-based access decisions, especially in systems with millions of interconnected users and resources.
* Implementing ReBAC requires specialized infrastructure, such as graph databases or relationship management tools, to efficiently handle access queries.

## Why is Attribute and Relationship Based Access Control preferable over RBAC?

* Each access model has its own strengths and weaknesses, and the preference for one over the others depends on the specific requirements and context of the system. However, ABAC and ReBAC offer some advantages over RBAC in certain scenarios.

### Flexibility and granularity

* RBAC typically relies on predefined roles that determine access permissions. While this approach works well for simple systems with clearly defined roles, it can be rigid and less adaptable to complex scenarios where users have diverse roles or require fine-grained access control.
* ABAC and ReBAC offer greater flexibility by allowing access decisions to be based on dynamic attributes or relationships between users, resources, and environmental factors. This flexibility enables more granular access control policies that can adapt to changing conditions and accommodate a wider range of access scenarios.

### Dynamic authorization policies

* RBAC requires static assignment of roles to users, which may not be suitable for environments where access requirements vary dynamically based on factors such as time of day, location, or user attributes.
* ABAC and ReBAC support dynamic authorization policies that evaluate attributes and relationships in real-time to make access decisions. This dynamic nature allows for more adaptive and context-aware access control, enhancing security and usability.

### Resource-centric access control

* RBAC focuses primarily on user roles and permissions, with less emphasis on the characteristics of the resources being accessed. While this approach simplifies access management, it may lead to situations where users have inappropriate access to sensitive resources.
* ABAC and ReBAC take a more resource-centric approach by considering attributes and relationships associated with both users and resources when making access decisions. This ensures that access is granted or denied based on the specific attributes and context of the resources, leading to more precise and context-aware control.

### Scalability and maintenance

* RBAC can become complex and difficult to manage as the number of roles and permissions grows, especially in large-scale systems with diverse user populations and access requirements.
* ABAC and ReBAC offer scalability advantages by allowing access control policies to be defined based on flexible attribute and relationship criteria. This simplifies policy management and maintenance, as policies can be more easily adapted and extended to accommodate changes in the system or business requirements.

### Speed

* In RBAC, having too many roles can lead to **role explosion**, where there are more roles defined than can be efficiently managed. When users send their credentials and roles, such as through HTTP headers, there's a risk of exceeding size limits, causing performance issues. One workaround is to only send the user ID and retrieve roles separately, but this adds latency to each request.
* In ABAC and ReBAC, there's no **role explosion** issue because access decisions are based on attributes and relationships rather than predefined roles. This means there's less data to send with each request, resulting in better performance overall.

### Multi-tenancy and cross-organizational requests

* In RBAC, handling multi-tenancy and cross-organizational requests can be challenging. Configuring rule sets for each customer or pre-provisioning identities for cross-organizational requests is cumbersome and can lead to security risks.
* In contrast, ABAC implementations offer better support for multi-tenancy and cross-organizational requests. By consistently defining attributes, access control decisions can be executed and administered across different infrastructures while maintaining security. This makes ABAC more suitable for handling such scenarios efficiently and securely.

### Management and robustness

* RBAC setup may seem simpler initially, but as the system grows in size and complexity, managing roles becomes challenging. Testing and auditing also become more difficult as the number of roles increases.
* In contrast, ABAC and ReBAC are more expressive and easier to manage. They use attributes and Boolean logic to reflect real-world concerns better, making them simpler to update when access control needs change. Additionally, they encourage separating policy management from enforcement and identity provisioning, leading to easier management overall.

### Fine-grained and detailed boolean logic

* RBAC's simplistic approach allows access decisions to be based solely on the presence or absence of roles, which limits the granularity of control and makes it challenging to support object-level or horizontal access control decisions and those that require multiple factors.
* In contrast, ABAC expands the range of characteristics considered for access decisions. It includes dynamic attributes like time of day and device type, allowing for more precise control. For example, ABAC can deny access to sensitive resources outside of business hours. Thus, ABAC is more effective in enforcing the principle of least privilege.
* ReBAC enables fine-grained permissions by supporting direct relationships between users and objects. Some systems use algebraic operators like AND and NOT for complex policies. For instance, ReBAC can grant access based on specific relationships, such as granting access only if a user has a certain relationship with an object.

[1]: /static/images/rbac.png
[2]: /static/images/abac.png
[3]: /static/images/rebac.png
