# DevSecOps security controls

* The fundamental idea of DevSecOps is to integrate security controls as early as possible in the software development lifecycle, rather than addressing them late in the process or merely at the end.
* Below is a generic outline of the security practices that can be applied in each stage of the DevOps workflow:

![DevSecOps Lifecycle: Security Controls][1]

  > :older_man: The `Shift Left` approach focuses on finding and mitigating defects early in the software delivery process to enhance quality by advancing tasks to the earliest possible stage in the lifecycle.

## Secure Code Training

* Educates developers on best practices and potential vulnerabilities in software development with the aim of minimizing risks from the coding phase itself.
* Tailored to specific programming languages and frameworks used within the organization, encouraging more effective use and deeper comprehension.
* Involves regular updates to stay ahead of emerging security threats.

## Secure Architecture Design

* Focuses on building security into the software architecture from the outset, ensuring that organizations are equipped with the IT infrastructure necessary to appropriately prevent, detect, and handle modern attacks.
* Assists in deciding when and which technologies to implement, providing security decision-makers with the flexibility to introduce new capabilities as the threat landscape changes.
* Facilitates organizations comply with regulatory requirements and industry standards, which is particularly important in sectors like healthcare, finance, and government, where data protection regulations are stringent.
* Minimizes expenses related to security tools by ensuring they are implemented optimally and according to genuine requirements.

## Security by Design

* Incorporates security requirements early in the requirements gathering phase, ensuring that security is an integral part of the application design process, not an afterthought.
* Minimizes security issues through proactive design choices, decreasing the likelihood of vulnerabilities susceptible to cyber threats.
* Prioritizes minimal privilege access in system functionalities and many other security best practices.

## Threat Modeling

* Helps in understanding the attack surface and potential attack vectors, enabling the identification of potential threats and vulnerabilities even before coding starts.
* Cultivates a deeper understanding of software and hardware systems, especially from a risk perspective.
* Detects and eradicates bottlenecks, single failure points, and inefficient controls or policies.
* Facilitates more effective threat prioritization, guiding all actions from purchase decisions to mitigation plans.
* Cuts expenses by resolving security issues during the design stage, as it is considerably more cost-effective than addressing them post-deployment.

## Application Data Segregation

* Reduces the risk of unauthorized access to sensitive data and limits potential damage in the event of a security breach.
* Assists in ensuring adherence to regulations by isolating and protecting data according to legal standards.
* Encourages the categorization and storage of data in distinct secure zones, preventing other runtime environments from using the same data as production, or mandating data anonymization when live data use is required.
* Allows tailored storage and backup strategies that align with the importance and stability of the data, ensuring that critical data is backed up more frequently and reliably.

## Git Security

* Helps to prevent unauthorized access to source code and maintains code integrity.
* Includes measures like commit signing to verify author identity.
* Utilizes encryption for data in transit and at rest within the repository.
* Implements hooks to automatically check for security issues in code before merging.

## IDE Security Plugins

* Integrates security analysis directly into the IDE to catch vulnerabilities early.
* Includes linting tools that promote secure coding practices.
* Supports developers by offering real-time feedback on security concerns and reducing their workload by automating routine security checks.

## Repository Scanning

* Provides a broader overview of security posture and bad practices related to code repositories.
* Focuses on scannig the entire repository, looking at both the code and the non-code components, like configuration files.
* Outputs are related to files with potentially insecure configurations, known vulnerabilities in outdated libraries, and exposed secrets like passwords or API keys accidentally pushed.

## Secure Coding Standards

* Establishes distinct sets of rules and guidelines that an organization uses to minimize security vulnerabilities and errors in development. These standards differ across organizations due to distinct security requirements, like PCI compliance for payment-handling applications.
* Ensures consistency and security across all development projects.
* Serves as a benchmark for new and existing employees to follow.

## Software Composition Analysis (SCA)

* Allows developers to adopt open source packages without exposing organizations to unnecessary vulnerabilities or legal and compliance risks.
* Helps in enforcing security policies by blocking the use of components with unacceptable risks or vulnerabilities.
* Provides remediation suggestions like patches or updates for vulnerable components, aiding organizations in quickly and efficiently addressing security vulnerabilities before exploitation.

## Static Application Security Testing (SAST)

* Analyzes source code to identify potential security vulnerabilities and other security flaws that are exploitable by attackers.
* Operates without needing a running application, allowing early detection.
* Enables developers to fix issues at the source level, reducing the cost and effort of later remediation.

## Secrets Management

* Manages and protects sensitive data such as passwords, tokens, and API keys through secure storage mechanisms, ensuring they are not hardcoded into source code.
* Integrates with other tools to automate the provisioning and rotation of secrets.
* Provides centralized control over access to secrets across cloud and on-premises environments.
* Reduces the risk of data breaches by isolating secrets from other components.

## Dynamic Application Security Testing (DAST)

* Tests running applications to find vulnerabilities that appear during operation, mimicking the behavior of an attacker by sending various inputs and examining the application's responses.
* Checks the entire application stack, including third-party components and backend services, ensuring thorough security coverage.
* Complements SAST by identifying runtime issues that static analysis might not detect.
* Provides actionable insights that can be used to fine-tune WAF rules and other defenses.

## Infrastructure Security

* Involves securing the underlying hardware, networks and software that support applications.
* Encompasses both physical and virtual security measures.
* Protects critical infrastructure components from attacks, ensuring the integrity and availability of services.

## Application Hardening

* Refers to techniques used to reduce the attack surface of applications, such as code obfuscation, which converts browser JavaScript code into a complex and obscure form to prevent reverse engineering and protect intellectual property.
* Employs strict configuration management to eliminate default settings and remove unnecessary features and services.
* Enforces HTTPS to secure communication between clients and servers, and across all API calls and external resources, ensuring data protection in transit.
* Adds security headers to HTTP responses enhancing protection against common attacks, including Referrer-Policy, Content Security Policy (CSP), and HTTP Strict Transport Security (HSTS).

## Penetration Testing

* Involves ethical hackers attempting to breach application and system defenses.
* Provides practical insights into the effectiveness of existing security measures.
* Delivers detailed reports that guide remediation efforts and strengthen security.

## Software Bill of Materials (SBOM)

* Provides a detailed inventory of open-source and third-party packages and libraries included in an application, encompassing their licensing and version details, source, and any identified vulnerabilities.
* Helps organizations to better understand the complexity of their software applications, enhancing their ability to identify and tackle newly discovered vulnerabilities, and also speeding up incident response.
* Simplifies the process of preparing for audits by providing detailed documentation of software components and their licenses.

## Content Delivery Network (CDN)

* Mitigates Distributed Denial of Service (DDoS) attacks and other web threats.
* Enables advanced access control policies that restrict access to content based on user's compliance.
* Helps identify and mitigate malicious bots that can scrape content, conduct automated attacks, or engage in fraudulent activities.

## Endpoint Hardening

* Ensures that either host or containers are protected from vulnerabilities and attacks.
* Enforces the principle of least privilege by limiting user, service account or process access to only necessary resources.
* Implements Endpoint Detection and Response (EDR) systems on host machines for sustained threat management.
* Mandates logical partitions and isolation of pods and resources in kubernetes environments using namespaces or other segmentation strategies.

## Web Application Firewall (WAF)

* Blocks malicious requests and protects against common web application attacks by filtering and monitoring HTTP traffic between a web application and the Internet.
* Aids in protecting data privacy and preventing data leaks by monitoring outbound traffic to stop sensitive information from leaving the application.
* Provides detailed logging features that assist in auditing, forensics, and refining security policies over time, serving as a basis for real-time alerts that notify administrators of potential security events.

## Attack Surface Map

* Provides a visual representation of all the potential points where an unauthorized user can try to enter data to or extract data from an environment.
* Helps in understanding and mitigating risks associated with exposed services and functions.
* Useful for security assessments and planning defense strategies, guiding the allocation of resources to protect critical assets more effectively.

## Bug Bounty

* Engages a wide range of security researchers and ethical hackers with varying skills and experiences to discover and disclose vulnerabilities, leveraging the collective expertise of the global security community.
* Facilitates a cost-effective method to security testing since organizations only pay for valid and significant findings.
* Demonstrates a commitment to security, building transparency and trust with customers and stakeholders by showing a proactive approach to securing applications.

## Identity and Access Management (IAM)

* Manages digital identities and controls user access to resources within an organization, preventing unauthorized access and improving visibility into the organizational access control landscape.
* Includes authentication, authorization, roles, and privileges management.
* Provides comprehensive audit trails for compliance and forensic analysis.

## Centralized Logging

* Provides a comprehensive view of the entire application environment, capturing logs from servers, applications, databases, and network devices.
* Enables correlation of events across different components to detect complex attack patterns and potential security incidents.
* Accelerates the investigation of security incidents by providing a single source of truth.
* Facilitates real-time monitoring and alerting on security events, allowing for immediate detection of potential threats.

## Continuous Monitoring

* Provides a proactive approach to security, enabling instant investigation and response to security incidents, and minimizing the impact of potential threats.
* Helps to adjust security measures based on real-time threat intelligence and evolving risks.
* Offers granular insights into system performance, user activities, and security events, aiding in better decision-making.

## Intrusion Prevention

* Prevents attacks by actively monitoring network traffic through signature-based, anomaly-based, and policy-based detection methods, and by blocking or rerouting suspicious traffic.
* Applies pre-configured rules and policies to automatically respond to identified threats without human intervention.
* Works in conjunction with other security tools, such as firewalls, web application firewalls, and endpoint protection systems, to provide a multi-layered defense strategy.
* Integrates with Security Information and Event Management (SIEM) systems to offer a comprehensive approach to threat detection and response.

## Threat Intelligence

* Involves gathering, analyzing, and utilizing information about current and emerging threats to enhance an organization's security posture.
* Delivers actionable insights that enable organizations to anticipate, prepare for, and react effectively to cyber threats.
* Promotes the integration of knowledge into security practices, leading to better-informed decision-making and improved responses to incidents.

[1]: /static/images/learning/devsecops-lifecycle-security-controls.png
