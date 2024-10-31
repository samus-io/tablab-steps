# Systems Testing

* `Systems Testing` exists as a layer in which to evaluate the entire system as a whole.
* It provides confidence that the system meets the specified requirements and is ready for deployment.
* It aims to detect issues in both the inter-assemblages of units, and the system on which they run, also enabling non-functional tests.
  > Non-functional testing evaluates software beyond features, like performance, security and usability, which makes the Systems Testing phase an ideal stage to test some of these non-functional aspects.
* This testing phase takes place after `Unit` and `Integration` and before `User Acceptance`.

## Approach

### Destructive Testing

* Assesses the performance and stability of a software application under extreme conditions or by applying inputs that may lead to system crashes or data loss.

### Non-destructive Testing

* Aims to verify the functionality and quality of a software application without causing any harm to the system or data.

### Fault Injection

* Deliberately introduces faults or errors into the system.
* Helps improve an app's fault tolerance and recovery mechanisms.

## Non-Functional Tests

### Performance

#### Load Tests

* Apply varying amounts of load into the system and watch its behavior.
* Evaluate under different concurrent user and system activity scenarios, giving insight into the system's readiness for real-world usage.

#### Stress Tests

* Apply an extreme load beyond the systems expected limits to determine the breaking point and handle possible crashing behaviors.

#### Scalability Tests

* Assess the software's ability to scale and handle ever-increasing loads or users.
* Aims to ensure healthy growth and to preemptively mitigate performance degradation.

### Security

#### Non-Repudiation Tests

* Focus on establishing user-action accountability and preventing users from disavowing their interactions or transactions with the system.
* Specially useful in applications where the traceability/verification of user actions is critical, such as legal or financial systems.

#### Data Integrity Tests

* Verifiy that the stored or transmitted data remains uncompromised and secure; ensuring the data's integrity is preserved against unauthorized queries, corruption, or tampering.
* For systems that handle sensitive data, legal and regulatory requirements, testing might help adhere to these standards.

#### Authentication Tests

* Scrutinize the system's access control, including user authentication, session management, and permissions.

### Recovery and Resilience

#### Data Migration Tests

* Evaluate the system's competence in migrating data from one source to another without loss or corruption issues.

#### Failback Tests

* Work on the system's behavior after a failover event.
* Focus on the system's ability to transition back to the primary, healthier state.
* Aim to minimize downtime and data loss in real-world scenarios.

### Usability

#### Compatibility Tests

* Assess how well the software performs across various platforms and configurations.
* Help enhance usability and operability, ensuring the software works consistently across the targeted environments.

#### Accessibility Tests

* Focus on making the software usable for people with visual impairements or disabilities.
* Evaluate compatiblity with assistive technologies, such as screen readers, voice recognition software, keyboard navigation, alternative text, form field accessibility, etc.
