# Types Of Access Control

* Access Control is mainly divided into 3 types: Role-Based Access Control, Attribute-Based Access Control, and Relationship-Based Access Control.

## Role-Based Access Control (RBAC)

* RBAC is a widely-used access control model where access permissions are assigned to roles, and users are assigned to roles based on their responsibilities within an organization.
* Roles define sets of permissions that users with that role are allowed to perform.
* **Example:** In a banking system, roles could include Customer, Teller, Manager, and Administrator. Each role is associated with specific permissions:

    ![RBAC][1]

  * The `Customer` role might have permissions to view account balances and transaction history.
  * The `Teller` role might have permissions to deposit and withdraw funds.
  * The `Manager` role might have permissions to approve large transactions and generate reports.
  * The `Administrator` role might have permissions to manage user accounts and system configurations.
* Users are assigned one or more roles based on their job responsibilities. For example, a bank teller might be assigned the "Teller" role, while a bank manager might be assigned both the "Manager" and "Teller" roles.

## Attribute-Based Access Control (ABAC)

* ABAC is an access control model that evaluates access decisions based on attributes associated with users, resources, and environmental conditions.
* Users are granted access only to resources that possess corresponding attributes. When a user requests access to a resource, the system evaluates their attributes along with attributes associated with the resource and environmental context.
* **Example:** In an enterprise system, access to sensitive documents may be controlled based on attributes such as:

    ![ABAC][2]

  * User role (e.g., `Employee` or `Manager`)
  * Department (e.g., `Finance` or `Human Resources`)
  * Sensitivity level of the document (e.g., `Confidential` or `Public`)
  * Time of access (e.g.,` During Business Hours` or `After Hours`)
* Access decisions are dynamically determined by evaluating the attributes specified in the access control policies against the attributes of the user, resource, and environmental context in real time.
* ABAC provides granular access control by allowing policies to consider multiple attributes and conditions simultaneously.

## Relationship-Based Access Control (ReBAC)

* ReBAC is an access control model that considers relationships between entities (such as users, resources, and roles) when making access decisions. Unlike traditional access control models like Role-Based Access Control (RBAC), which primarily focus on roles and permissions, ReBAC takes into account the connections and associations between entities within an organization.
* Access control policies in ReBAC define rules based on relationships between entities. These policies specify conditions under which access is granted or denied based on the connections between users, resources, and other entities.
* **Example:** In a content management system, access to documents may be controlled based on relationships such as:

    ![REBAC][3]

  * **Ownership:** Only the creator or owner of a document has permission to edit or delete it.
  * **Group Membership:** Users belonging to a specific group have access to documents shared within that group.
  * **Inheritance:** Access permissions are inherited from higher-level entities such as organizational units or parent resources.
* ReBAC allows for dynamic access control decisions based on real-time evaluation of relationships between entities. Access decisions may change dynamically as relationships evolve or as users interact with different resources.

## Why is Attribute and Relationship Based Access Control preferable over RBAC?

* Each Access model has its own strengths and weaknesses, and the preference for one over the others depends on the specific requirements and context of the system. However, ABAC and ReBAC offer some advantages over RBAC in certain scenarios:

  * **Flexibility and Granularity:**
    * RBAC typically relies on predefined roles that determine access permissions. While this approach works well for simple systems with clearly defined roles, it can be rigid and less adaptable to complex scenarios where users have diverse roles or require fine-grained access control.
    * ABAC and ReBAC offer greater flexibility by allowing access decisions to be based on dynamic attributes or relationships between users, resources, and environmental factors. This flexibility enables more granular access control policies that can adapt to changing conditions and accommodate a wider range of access scenarios.
  * **Dynamic Authorization Policies:**
    * RBAC requires static assignment of roles to users, which may not be suitable for environments where access requirements vary dynamically based on factors such as time of day, location, or user attributes.
    * ABAC and ReBAC support dynamic authorization policies that evaluate attributes and relationships in real-time to make access decisions. This dynamic nature allows for more adaptive and context-aware access control, enhancing security and usability.
  * **Resource-Centric Access Control:**
    * RBAC focuses primarily on user roles and permissions, with less emphasis on the characteristics of the resources being accessed. While this approach simplifies access management, it may lead to situations where users have inappropriate access to sensitive resources.
    * ABAC and ReBAC take a more resource-centric approach by considering attributes and relationships associated with both users and resources when making access decisions. This ensures that access is granted or denied based on the specific attributes and context of the resources, leading to more precise and context-aware control.
  * **Scalability and Maintenance:**
    * RBAC can become complex and difficult to manage as the number of roles and permissions grows, especially in large-scale systems with diverse user populations and access requirements.
    * ABAC and ReBAC offer scalability advantages by allowing access control policies to be defined based on flexible attribute and relationship criteria. This simplifies policy management and maintenance, as policies can be more easily adapted and extended to accommodate changes in the system or business requirements.

[1]: /static/images/rbac.png
[2]: /static/images/abac.png
[3]: /static/images/rebac_group_membership.png
