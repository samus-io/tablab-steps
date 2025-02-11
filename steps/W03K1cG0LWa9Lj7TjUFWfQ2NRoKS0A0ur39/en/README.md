# What is Broken Access Control (BAC)?

## What is access control?

* Access control is a fundamental security mechanism that determines which users can perform specific actions within an application or system. It ensures that only authorized individuals can access sensitive data or perform operations, thereby protecting resources from misuse and unauthorized access.
* It involves defining and enforcing rules that decides who can access certain resources and what operations they can perform on those resources.

## What is broken access control?

* Broken access control refers to vulnerabilities in an application that allow unauthorized users to gain access to resources or perform actions that should be restricted.
* This flaw arises when the mechanisms designed to enforce user permissions are improperly implemented, misconfigured, or inconsistently applied.
* As a result, users might be able to bypass security measures and access sensitive data or functions.
* Broken access control is recognized as a significant security risk and is ranked as one of the top security vulnerabilities in web applications by the OWASP Top 10 list.

## Examples of broken access control

### Administrative access to non-admin users

* A common example of broken access control involves administrative functionalities that are accessible to non-admin users. For instance, consider the following URL:

  ```bash
  https://example.tbl/admin/getUsers
  ```

* If a user without administrative privileges is able to access to the URL, it indicates a flaw in the system's access control.
* Administrative endpoints, should be exclusively accessible to administrators. When such endpoints are not properly secured, unauthorized users might access sensitive administrative functions or information.

### Leakage of Personally Identifiable Information (PII)

* Consider an online shopping platform where customers register to make purchases. During registration, the platform collects various details from each customer, such as full name, address, phone number and payment information.
* Each of these pieces of information qualifies as PII because they can be used to uniquely identify or locate a specific individual. The combination of these data creates a comprehensive profile that is sensitive in nature. If this information is exposed or misused, it can lead to privacy breaches, identity theft, or financial fraud.
* In the following URL, the web application uses the `id` parameter to determine which user's account information should be retrieved and displayed:

  ```
    https://example.tbl/accountInfo?id=<userId>
  ```

* The core issue here is that the application is relying solely on the URL parameter to fetch the data without confirming that the requesting user is authorized to view that particular account.

## What could be achieved with broken access control

### Unauthorized access to restricted resources

* When access control measures fail, attackers can access to restricted resources (data or functionalities) that should be available only to authorized users. This means that sensitive functionalities or critical information might be exposed to individuals who should not have the permission to view or modify them.

### Privilege escalation

* An attacker with limited access might exploit vulnerabilities to perform actions reserved for administrators or other higher-privileged users.
* With elevated privileges, attackers can change user settings, modify or delete data, or even create new user accounts with full permissions.

### Data integrity and availability issues

* Unauthorized modifications can lead to corrupted data or altered business processes, undermining the integrity of the system.
* In some cases, attackers might use broken access control to perform actions that disrupt services (e.g., by deleting critical resources), affecting the availability of the application.

### Compliance and legal risks

* Breaches resulting from broken access control can lead to non-compliance with data protection regulations (like GDPR or HIPAA), potentially resulting in fines and legal liabilities.

### Potential for further exploitation

* Once attackers exploit a broken access control, they can use it as a stepping stone to more sophisticated attacks, as the application's exposure surface has increased, giving attackers more opportunities to find more vulnerabilities.
