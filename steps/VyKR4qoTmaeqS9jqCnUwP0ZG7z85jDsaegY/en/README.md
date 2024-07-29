# Types Of Access Controls

* The next image represents the hierarchy of privileges within a system.
* The **Highest Privilege** at the top signifies the level with the most access, such as an administrator.
* The **Lowest Privilege** at the bottom represents the base level of access, such as a guest or a standard user.
* **Vertical Access Control** is indicated by an upward arrow, depicting the effort of an attacker or a user to access higher-privileged resources.
* **Horizontal Access Control** is shown by a rightward arrow, illustrating an attacker trying to access resources of another user at the same privilege level.
* The icons represent different users at various privilege levels, with their position on the triangle indicating their access rights.

![Access Control Hierarchy][1]

## Vertical Access Control

* Vertical Access Control restricts access to data or resources to specific type of user.
* It ensures that users can only access information relevant to their level of authorization.
* If a user with lower privileges gains access to rights or resources intended for higher privileged users, it would be considered a breach of access control.
* For example: In a school, teachers have access to student records for their own classes (e.g., attendance, grades). However, the principal has access to all student records in the school. This is an example of vertical access control, where access to student records is based on the role or clearance level of the user. If a teacher tries to access records outside their class without proper authorization, it would be a breach of Vertical Access Control.

## Horizontal Access Control

* Horizontal Access Control enables different users to access similar resource types.
* It ensures that users can only access functionalities or resources that are relevant to their role, regardless of their individual clearance level.
* For example: In a company's file-sharing system, employees are divided into different departments, such as Marketing, Finance, and Human Resources. Horizontal Access Control ensures that employees in the Marketing department can only access files and documents related to marketing activities, while employees in Finance can access financial data and reports. If a marketing employee tries to access financial documents without proper authorization, it would be a breach of Horizontal Access Control.

## Context-dependent Access Control

* Context-dependent Access Control resticts access to functionality and resources based on the state of the application or the user's interaction with it.
* Context-dependent Access Control refers to the practice of dynamically adjusting access permissions based on contextual factors such as user attributes, environmental conditions, or situational variables.
* For example: In a task management web application, the delete operation exemplifies access control enforcement, where users can only delete tasks they have created or possess appropriate permissions. Upon clicking the `Delete` button next to a task, a `DELETE` request is sent to the server, which verifies the user's authorization to perform the action. If validated, the server proceeds with the deletion, prompting the user for confirmation before removing the task from the database. Error handling mechanisms ensure appropriate feedback is provided in case of access violations or other errors, maintaining the application's data integrity and security.

[1]: /static/images/Access_control_types.png
