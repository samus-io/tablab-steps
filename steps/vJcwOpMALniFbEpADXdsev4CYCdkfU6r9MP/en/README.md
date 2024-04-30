# Types Of Access Control

* Access Control is mainly divided into 3 types: Role-Based Access Control, Attribute-Based Access Control, and Relationship-Based Access Control.

## Role-Based Access Control (RBAC)

* RBAC is a widely-used access control model where access permissions are assigned to roles, and users are assigned to roles based on their responsibilities within an organization.
* Roles define sets of permissions that users with that role are allowed to perform.

### Working of RBAC

* **Defining roles:** Roles are predefined categories that represent a set of permissions.
* **Assigning roles:** Users are assigned one or more roles based on their job or position.
* **Defining permissions:** Permissions are associated with each role, specifying what actions users assigned to that role can perform.
* **Access decision:** When a user tries to access a resource, the system checks if the user's role has the necessary permissions for that resource. If so, access is granted; otherwise, access is denied.

#### Example of RBAC

* In a banking system, roles could include Customer, Teller, Manager, and Administrator. Each role is associated with specific permissions:

    ![RBAC][1]

  * The `Customer` role might have permissions to view account balances and transaction history.
  * The `Teller` role might have permissions to deposit and withdraw funds.
  * The `Manager` role might have permissions to approve large transactions and generate reports.
  * The `Administrator` role might have permissions to manage user accounts and system configurations.
* Users are assigned one or more roles based on their job responsibilities. For example, a bank teller might be assigned the **Teller** role, while a bank manager might be assigned both the **Manage** and **Teller** roles.

### Pros of RBAC

* Simple and easy to implement.
* Provides clear roles and responsibilities.
* Helps in managing permissions at scale.
* Well-suited for hierarchical organizations.
* Reduces administrative workload by assigning users to predefined roles with set permissions.
* Ensures data and information are handled according to confidentiality standards.
* Provides an easy way to demonstrate compliance with access control policies.

### Cons of RBAC

* Limited granularity and flexibility.
* May lead to role explosion in large systems.
* Difficult to handle dynamic access control requirements.
* Users may end up with more permissions than necessary.
* Challenges in assigning roles in large or growing organizations.
* Requires ongoing maintenance to keep roles updated and aligned with organizational needs.
* Collaboration between teams may be necessary for proper implementation, impacting workload distribution.

## Attribute-Based Access Control (ABAC)

* ABAC is an access control model that evaluates access decisions based on attributes associated with users, resources, and environmental conditions.
* Users are granted access only to resources that possess corresponding attributes. When a user requests access to a resource, the system evaluates their attributes along with attributes associated with the resource and environmental context.

### Working of ABAC

* **Defining attributes:** Attributes are characteristics of users, resources, and the environment.
* **Assigning attributes:** Users, resources, and environmental factors are assigned attributes based on their properties.
* **Defining policies:** Access control policies are defined based on combinations of attributes. For example, a policy could specify that only users with the attribute **Role: Employee** and **Department: Finance** can access course materials.
* **Access decision:** When a user requests access to a resource, the system evaluates the access control policies based on the attributes of the user, resource, and environment. If the user's attributes match the policy criteria, access is granted; otherwise, access is denied.

#### Example of ABAC

* In an enterprise system, access to sensitive documents may be controlled based on attributes such as:

    ![ABAC][2]

  * User role (e.g., `Employee` or `Manager`)
  * Department (e.g., `Finance` or `Human Resources`)
  * Sensitivity level of the document (e.g., `Confidential` or `Public`)
  * Time of access (e.g.,` During Business Hours` or `After Hours`)
* Access decisions are dynamically determined by evaluating the attributes specified in the access control policies against the attributes of the user, resource, and environmental context in real time.
* ABAC provides granular access control by allowing policies to consider multiple attributes and conditions simultaneously.

### Pros of ABAC

* Offers granular and dynamic access control.
* Allows for flexible policies based on attributes.
* Can adapt to changing environments and requirements.
* Supports the principle of least privilege.

### Cons of ABAC

* Complex to implement and manage.
* Requires defining and managing a large number of attributes.
* Potential for attribute sprawl and inconsistency.
* Performance overhead due to attribute evaluation.

## Relationship-Based Access Control (ReBAC)

* ReBAC is an access control model that considers relationships between entities (such as users, resources, and roles) when making access decisions. Unlike traditional access control models like Role-Based Access Control (RBAC), which primarily focus on roles and permissions, ReBAC takes into account the connections and associations between entities within an organization.
* Access control policies in ReBAC define rules based on relationships between entities. These policies specify conditions under which access is granted or denied based on the connections between users, resources, and other entities.

### Working of ReBAC

* **Establishing relationships:** Relationships are defined between users and resources, indicating associations such as ownership, creation, or specific interactions. For example, a user might have a relationship of **Owner** with a document they created.
* **Defining permissions:** Permissions are assigned based on these relationships, specifying what actions users can perform on resources they have a relationship with. For instance, a user with an **Owner** relationship with a document might have permission to edit or delete it.
* **Access decision:** When a user tries to perform an action on a resource, the system checks if there is a relationship between the user and the resource that grants the necessary permission. If so, access is granted; otherwise, access is denied.

#### Example of ReBAC

* In a content management system, access to documents may be controlled based on relationships such as:

    ![REBAC][3]

  * **Ownership:** Only the creator or owner of a document has permission to edit or delete it.
  * **Group membership:** Users belonging to a specific group have access to documents shared within that group.
  * **Inheritance:** Access permissions are inherited from higher-level entities such as organizational units or parent resources.
* ReBAC allows for dynamic access control decisions based on real-time evaluation of relationships between entities. Access decisions may change dynamically as relationships evolve or as users interact with different resources.

### Pros of ReBAC

* Provides fine-grained control based on relationships between users and resources.
* Allows for intuitive access control policies based on ownership and other relationships.
* Supports complex access scenarios, such as multi-tenancy and cross-organizational access.
* Enhances security by restricting access to specific relationships.

### Cons of ReBAC

* Requires careful management of relationships and permissions.
* Complexity increases with the number of relationships.
* May be challenging to implement in systems with highly dynamic data.
* Performance overhead in evaluating relationship-based access decisions.

## Why is Attribute and Relationship Based Access Control preferable over RBAC?

* Each Access model has its own strengths and weaknesses, and the preference for one over the others depends on the specific requirements and context of the system. However, ABAC and ReBAC offer some advantages over RBAC in certain scenarios:

### Flexibility and Granularity

* RBAC typically relies on predefined roles that determine access permissions. While this approach works well for simple systems with clearly defined roles, it can be rigid and less adaptable to complex scenarios where users have diverse roles or require fine-grained access control.
* ABAC and ReBAC offer greater flexibility by allowing access decisions to be based on dynamic attributes or relationships between users, resources, and environmental factors. This flexibility enables more granular access control policies that can adapt to changing conditions and accommodate a wider range of access scenarios.

### Dynamic Authorization policies

* RBAC requires static assignment of roles to users, which may not be suitable for environments where access requirements vary dynamically based on factors such as time of day, location, or user attributes.
* ABAC and ReBAC support dynamic authorization policies that evaluate attributes and relationships in real-time to make access decisions. This dynamic nature allows for more adaptive and context-aware access control, enhancing security and usability.

### Resource-Centric Access Control

* RBAC focuses primarily on user roles and permissions, with less emphasis on the characteristics of the resources being accessed. While this approach simplifies access management, it may lead to situations where users have inappropriate access to sensitive resources.
* ABAC and ReBAC take a more resource-centric approach by considering attributes and relationships associated with both users and resources when making access decisions. This ensures that access is granted or denied based on the specific attributes and context of the resources, leading to more precise and context-aware control.

### Scalability and Maintenance

* RBAC can become complex and difficult to manage as the number of roles and permissions grows, especially in large-scale systems with diverse user populations and access requirements.
* ABAC and ReBAC offer scalability advantages by allowing access control policies to be defined based on flexible attribute and relationship criteria. This simplifies policy management and maintenance, as policies can be more easily adapted and extended to accommodate changes in the system or business requirements.

### Speed

* In RBAC, having too many roles can lead to **role explosion**, where there are more roles defined than can be efficiently managed. When users send their credentials and roles, such as through HTTP headers, there's a risk of exceeding size limits, causing performance issues. One workaround is to only send the user ID and retrieve roles separately, but this adds latency to each request.
* In ABAC and ReBAC, there's no **role explosion** issue because access decisions are based on attributes and relationships rather than predefined roles. This means there's less data to send with each request, resulting in better performance overall.  

### Multi-Tenancy and Cross-Organizational requests

* In RBAC, handling multi-tenancy and cross-organizational requests can be challenging. Configuring rule sets for each customer or pre-provisioning identities for cross-organizational requests is cumbersome and can lead to security risks.
* In contrast, ABAC implementations offer better support for multi-tenancy and cross-organizational requests. By consistently defining attributes, access control decisions can be executed and administered across different infrastructures while maintaining security. This makes ABAC more suitable for handling such scenarios efficiently and securely.

### Management and Robustness

* RBAC setup may seem simpler initially, but as the system grows in size and complexity, managing roles becomes challenging. Testing and auditing also become more difficult as the number of roles increases.
* In contrast, ABAC and ReBAC are more expressive and easier to manage. They use attributes and Boolean logic to reflect real-world concerns better, making them simpler to update when access control needs change. Additionally, they encourage separating policy management from enforcement and identity provisioning, leading to easier management overall.

### Fine-grained and detailed Boolean logic

* RBAC's simplistic approach allows access decisions to be based solely on the presence or absence of roles, which limits the granularity of control and makes it challenging to support object-level or horizontal access control decisions and those that require multiple factors.
* In contrast, ABAC expands the range of characteristics considered for access decisions. It includes dynamic attributes like time of day and device type, allowing for more precise control. For example, ABAC can deny access to sensitive resources outside of business hours. Thus, ABAC is more effective in enforcing the principle of least privilege.
* ReBAC enables fine-grained permissions by supporting direct relationships between users and objects. Some systems use algebraic operators like AND and NOT for complex policies. For instance, ReBAC can grant access based on specific relationships, such as granting access only if a user has a certain relationship with an object.

[1]: /static/images/rbac.png
[2]: /static/images/abac.png
[3]: /static/images/rebac_group_membership.png
