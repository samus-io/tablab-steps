# Attribute-Based Access Control (ABAC)

* ABAC is an access control model that makes decisions based on attributes of users, resources, and environmental conditions.
* When a user requests access to a resource, the system evaluates attributes such as user role, department, or clearance level, along with resource attributes like sensitivity level or owner.
  * Environmental conditions such as time, location or device type can also be considered in the evaluation.
* Access is granted only if the attributes of the user match the attributes required by the resource.
* ABAC allows for more fine-grained and dynamic access control by considering multiple factors beyond just roles or predefined rules.

## How ABAC works

* Attributes are characteristics or types of users, resources or the environment.
* Access control policies are created using combinations of attributes to determine permissions.
* When a user requests access to a resource, the system evaluates the access control policies based on the attributes of the user, resource, and environment. If the user's attributes match the policy criteria, access is granted; otherwise, access is denied.

### Example of ABAC

* The following image represents the implementation of ABAC in an enterprise to manage access based on the attributes `Users`, `Department`, `Document Type` and `Access Time`. The combination of these attributes define the access to resources and functionalities:

    ![ABAC][1]

  * User attributes such as role (e.g., `Employee` or `Manager`) determine access levels and responsibilities.
  * Department attributes, such as `Finance` or `Human Resources`, help restrict access to documents based on organizational roles.
  * Resource attributes like document sensitivity, classified as `Confidential` or `Public`, ensure that only authorized users can access protected information.
  * Time-based attributes, such as `During Business Hours` or `After Hours`, regulate when a resource can be accessed.
* Access decisions are dynamically determined by evaluating the attributes specified in the access control policies against the attributes of the user, resource, and environmental context in real time.
* ABAC provides granular access control by allowing policies to consider multiple attributes and conditions simultaneously.

#### How access decisions are made

* Based on the previous image, here are some example policies that could be implemented using ABAC:
  * Only users with the `Manager` attribute in the `Finance` department are allowed to create and modify invoices.
  * Employees in the `HR` department can access employee records, but only during business hours.
  * Documents classified as `Confidential` can only be accessed by `Managers`, while documents marked as Public can be accessed by all employees.
  * Users with the `Employee` attribute can view payroll details, but only `Managers` in the Finance department can approve payroll changes.
* These policies ensure fine-grained access control by evaluating multiple attributes simultaneously, such as user role, department, document sensitivity and access time.

## Advantages of ABAC

* ABAC provides granular and dynamic access control, allowing fine-tuned decisions based on multiple attributes.
* Policies are flexible and can be customized based on user roles, resource sensitivity, and environmental conditions.
* The model can adapt to changing environments, ensuring access rules remain effective as organizational needs evolve.
* ABAC supports the principle of least privilege, ensuring users have access only to the resources necessary for their tasks.
* Policies can incorporate contextual factors such as location, time, and device type, enhancing security.
* The system enables centralized policy enforcement, making it easier to manage access across different resources and applications.

## Disadvantages of ABAC

* Implementing ABAC is complex, requiring a detailed definition of attributes and policies.
* Managing a large number of attributes across users, resources, and environments can be challenging.
* The risk of attribute sprawl increases as more attributes are introduced, leading to inconsistencies in policy enforcement.
* The system introduces performance overhead due to real-time evaluation of multiple attributes for each access request.
* Policies require continuous updates to remain aligned with evolving business and security requirements.
* Organizations may need specialized tools or frameworks to efficiently implement and maintain ABAC policies.

[1]: /static/images/abac.png