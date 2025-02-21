# What is Broken Access Control (BAC)?

## What is access control?

* Access control is a fundamental security mechanism that determines which users can perform specific actions within an application or system. It ensures that only authorized individuals can access sensitive data or perform operations, thereby protecting resources from misuse and unauthorized access.
* It involves defining and enforcing rules that decides who can access certain resources and what operations they can perform on those resources.

## What means broken access control?

* Broken access control refers to vulnerabilities in an application that allow unauthorized users to gain access to resources or perform actions that should be restricted.
* This flaw arises when the mechanisms designed to enforce user permissions are improperly implemented, misconfigured, or inconsistently applied.
* As a result, users might be able to bypass security measures and access sensitive data or functions.
* Broken access control is recognized as a significant security risk and is ranked as one of the top security vulnerabilities in web applications by the OWASP Top 10 list.

## Examples of broken access control

### Administrative access to non-admin users

* A common example of broken access control involves administrative functionalities that are accessible to non-admin users. For instance, consider the following URL:

  ```url
  https://example.tbl/admin/getUsers
  ```

* If a user without administrative privileges is able to access to the URL, it indicates a flaw in the system's access control.
* Administrative endpoints, should be exclusively accessible to administrators. When such endpoints are not properly secured, unauthorized users might access sensitive administrative functions or information.

### Leakage of Personally Identifiable Information (PII)

* Consider an online shopping platform where customers register to make purchases. During registration, the platform collects various details from each customer, such as full name, address, phone number and payment information.
* Each of these pieces of information qualifies as PII because they can be used to uniquely identify or locate a specific individual. The combination of these data creates a comprehensive profile that is sensitive in nature. If this information is exposed or misused, it can lead to privacy breaches, identity theft, or financial fraud.
* In the following URL, the web application uses the `id` parameter to determine which user's account information should be retrieved and displayed:

  ```url
    https://example.tbl/accountInfo?id=<userId>
  ```

* The core issue here is that the application is relying solely on the URL parameter to fetch the data without confirming that the requesting user is authorized to view that particular account.

## What could be achieved with broken access control

* When access control measures fail, attackers may obtain **unauthorized access to restricted resources** (data or functionalities) that should be available only to authorized users. This means that sensitive functionalities or critical information might be exposed to individuals who should not have the permission to view or modify them.
* **Privilege escalation** allows attackers to elevate their access rights, enabling them to modify settings, delete data, or create new high-privileged accounts.
* In some cases, attackers might use broken access control to perform actions that disrupt services (e.g., by deleting critical resources), affecting the **data integrity and availability** of the application.
* **Compliance and legal risks** emerge when broken access control leads to regulatory violations, such as GDPR or HIPAA breaches, resulting in fines and legal consequences.
* Once attackers exploit broken access control, they can leverage it as a stepping stone for more sophisticated attacks, expanding the application's **attack surface** and increasing the likelihood of discovering additional vulnerabilities.
