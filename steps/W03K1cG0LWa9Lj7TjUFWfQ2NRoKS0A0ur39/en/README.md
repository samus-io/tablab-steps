# Broken Access Control

## What is Access Control?

* It refers to the process of determining whether the users are allowed to perform an action they are intended to within an application.
* It involves defining and enforcing rules that govern who can access certain resources and what operations they can perform on those resources.
* For example, consider a blogging platform where one can define user roles like admin (allowed for all actions) or readers (allowed with reading only).

## Introduction about Broken Access Control

* Broken Access Control refers to security vulnerabilities that allow unthorized users to access restricted resources or perform priviliged actions within an application.
* It occurs when access control mechanisms, such as authentication, authorization, or session management, are improperly implemented, configured, or enforced.
* It is ranked as one of the top security vulnerabilities in web applications by the OWASP Top 10 list.

## Real world examples of Broken Access Control

### Scenario 1: Platform Data Leak

* A platform inadvertently allows users to access data from other users by manipulating URL parameters. Users could access private photos, personal messages, or profile details that are not intended to be publicly accessible.
* Let's say User A can access User B's Account Info using the following URL:

  ```bash
    https://example.com/accountInfo?accountNo=<B's Account Number> 
  ```

* If any user is able to access other user's info just by adding the parameter, then it is a flaw.

### Scenario 2: Administrative Access to non-admin

* Let's consider the following two URLs:

```bash
    https://example.com/getInfo
    https://example.com/admin_getappInfo
```

* If Non-Admin Users are able to access both the URLs, then it is a flaw in the system. Because the admin related URLs should be only accessible to Admins.

## Impact of Broken Access Control

* **Unauthorized Access to Restricted Resources**:
  * Attackers can access sensitive functionalities or data intended for specific users, roles, or capabilities.
  * This can lead to unauthorized viewing, modification, or deletion of critical information.

* **Increased Risk of Data Breaches**:
  * Bypassing access control checks allows attackers to exploit vulnerabilities and exfiltrate sensitive data.
  * Data breaches can result in financial losses, legal liabilities, and damage to brand reputation.

* **Privacy Violations and Data Manipulation**:
  * Insecure direct object references enable attackers to view or edit other user's accounts or data.
  * This compromises user privacy and integrity of data, leading to loss of trust and credibility.

* **Security Risks in API Access Controls**:
  * Missing access controls in API endpoints (POST, PUT, DELETE) enable attackers to perform unauthorized actions.
  * This can result in data manipulation, service disruptions, and compromise of system integrity.

* **Elevation of Privileges**:
  * Elevation of privilege allows attackers to escalate their privileges and perform actions beyond their authorized scope.
  * This can lead to unauthorized access to sensitive functionalities or administrative capabilities.

* **Tampering with Access Tokens and Metadata**:
  * Manipulating access tokens or metadata allows attackers to bypass access controls and elevate their privileges.
  * This undermines the integrity and security of authentication mechanisms, leading to unauthorized access.

* **Force Browsing and Unauthenticated Access**:
  * Force browsing allows attackers to access authenticated or privileged pages without proper authentication.
  * This exposes sensitive functionalities or data to unauthorized users, increasing the risk of security breaches.
