# Relationship-Based Access Control (ReBAC)

* ReBAC is an access control model that considers relationships between entities (such as users, resources, and roles) when making access decisions. Unlike traditional access control models like Role-Based Access Control (RBAC), which primarily focus on roles and permissions, ReBAC evaluates the connections and associations between entities within an organization.
* Access control policies in ReBAC define rules based on how users and resources are related, rather than just assigning static roles.
* Policies specify conditions for granting or denying access by analyzing relationships between users, resources, and other entities.
* This model is particularly useful in collaborative environments, where access needs to be dynamically adjusted based on interactions between different users and shared resources.
* ReBAC enables fine-grained access control by considering real-time relationships, making it effective for systems that require dynamic access management.

## How ReBAC works

* ReBAC determines access permissions based on relationships that are defined between users and resources, indicating associations such as ownership, creation, or specific interactions.
* Permissions are assigned based on these relationships, specifying what actions users can perform on resources they have a relationship with.
  * Relationships can be direct (e.g., an employee managing a project) or indirect (e.g., an employee belonging to a team that owns the project).
  * For example, a policy might specify that only a document owner and their direct collaborators can edit a file, while others can only view it.
* When a user requests access to a resource, the system evaluates the existing relationships between the user and the resource to determine whether access should be granted.
  * If a user is not explicitly related to the resource in the required way, the system denies access.
* ReBAC enables dynamic access control, adjusting permissions as relationships change, making it ideal for social networks, collaboration platforms, and enterprise resource management systems.
* Unlike traditional models, ReBAC ensures that access evolves with user interactions, reducing the need for manual permission management.
* Normally in ReBAC systems, groups are established to group different users or resources together to make it easier to manage permissions.

### Example of ReBAC

* The following image represents the implementation of ReBAC in a medical system to manage access based on the user relationships:

![ReBAC][1]

* In this medical system, access to resources may be controlled based on relationships such as:
  * The creator or owner of a resource has permission to edit or delete it.
    * `Sam` and `Bob` are owners of their respective `Member Profiles`, giving them full control over their own `Medical Plans` and `Medical Records`.
  * Users belonging to a specific group have access to the resources that belongs to that group.
    * Bob has an `Admin` role in `Patient Group`, likely granting him full permissions to manage group resources.
  * Access permissions are inherited from higher-level entities such as organizational units or parent resources.
    * If a user has access to a `Member Profile`, they also inherit access to its associated medical resources, such as `Medical Plan` and `Medical Record`.

## Advantages of ReBAC

* Provides fine-grained access control by defining permissions based on relationships between users, resources, and groups.
* Access control policies are intuitive, reflecting real-world relationships such as ownership, caregiving roles, or team membership.
* The model supports complex access scenarios, including multi-tenancy environments, where multiple organizations or user groups share the same system.
* Cross-organizational access can be securely managed, allowing controlled collaboration between different entities.
* Security is enhanced by restricting access based on specific relationships, using the deny by default method, ensuring that only authorized users can interact with certain resources.
* Permissions are dynamically adjusted as relationships change, reducing the need for manual role assignments and making the system more flexible.

## Disadvantages of ReBAC

* Managing relationships and permissions requires careful planning to prevent unintended access issues.
* The complexity increases as the number of relationships grows, making large-scale implementations more challenging.
* Systems with highly dynamic data may face difficulties in maintaining accurate and up-to-date relationships for access control.
* Performance overhead can arise when evaluating relationship-based access decisions, especially in systems with millions of interconnected users and resources.
* Implementing ReBAC requires specialized infrastructure, such as graph databases or relationship management tools, to efficiently handle access queries.

[1]: /static/images/rebac.png