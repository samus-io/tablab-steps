# Input validation overview

* `Input validation` is the practice of verifying that untrusted input aligns with predefined criteria before it's processed or stored.
* It involves examining and validating untrusted input to ensure adherence to specified requirements and constraints.
* Essentially, input validation acts as a gatekeeper, screening out invalid or malicious data to safeguard the application's integrity and prevent potential harm.

![Insecure input validation overview][1]

## What is considered untrusted input?

* `Untrusted input` is any data provided by an external source, referring to any data not produced or controlled by the application, such as:
  * User-supplied data.
  * External API responses.
  * Files content.

  > :older_man: Validating every variable of an application is a time-consuming task from both development and performance standpoints. A useful guideline is to only validate data from all external sources of the application.

## What can be achieved with input validation

* **Data sanitization and standardization** by enforcing specific rules and formats, such as trimming whitespace, converting data to a consistent case, or removing forbidden characters, making sure the data entering the system is clean and uniform.
  * This promotes data integrity and simplifies downstream processing and analysis.
* **Enhanced data quality and accuracy** by verifying the integrity and correctness of user-supplied data, reducing the likelihood of errors, inconsistencies, and inaccuracies in the system's datasets.
  * This promotes trust in the reliability of the application's output and facilitates informed decision-making based on accurate and trustworthy data.
* **Compliance with regulatory requirements** like `GDPR`, `HIPAA`, or `PCI DSS` by adhering to mandated validation practices, safeguarding sensitive information, user privacy, and avoiding penalties due to breaches or non-compliance.
* **Prevention of injection attacks** like SQL injection and cross-site scripting (XSS) by validating input against patterns and blocking harmful characters or commands, safeguarding data, and maintaining system confidentiality and integrity.
* **Reduce the impact of Denial-of-Service (DoS) attacks** by limiting input size and complexity. Setting reasonable constraints, like maximum input length or request limits per user, prevents malicious actors from flooding the system with excessive or malformed data.
* **Protection against business logic flaws** by enforcing validation rules aligned with the application's business logic, preventing users from submitting invalid, incorrect or unexpected data inputs that could disrupt critical processes or lead to errors.
  * This ensures the application operates as intended, delivering consistent results aligned with business objectives.

## Input validation strategies

* Input validation strategies are categorized into syntactic and semantic validation.

### Syntactic validation

* Focuses on the superficial characteristics of data, ensuring it meets the predefined structure and format expectations. This type of validation checks for correctness in terms of syntax without regard to the meaning of the data.
  * It's like a grammar check for your data, verifying if it aligns with the syntax rules.
* Acts as the first line of defense, swiftly rejecting malformed or improperly formatted data before it infiltrates deeper layers of the application.

#### Use cases

* **Data types**: ensuring that numeric fields contain numbers, text fields contain alphabets, and email addresses adhere to the standard format (e.g., `user@example.tbl`) or a date is in a specific format (e.g.,`DD-MM-YYYY`).
* **Length limits**: checking if input lengths fall within acceptable boundaries to prevent buffer overflows or truncation issues.
* **Format constraints**: validating data against predetermined patterns, such as credit card numbers, phone numbers, or postal codes.

### Semantic validation

* Dives deeper than syntactic validation examining the meaning and context of the data beyond its surface appearance.
  * It's about ensuring that the data makes sense and aligns with the application's expectations.
* Acts as a judge interpreting the facts of a case, assessing the data to ensure it not only appears correct but also fits well within the overall context of the application's purpose.

#### Use cases

* **Range checks**: verifying if numeric inputs fall within permissible ranges, such as ensuring a user's age is between 18 and 100.
* **Business rules**: enforcing specific business logic constraints, like validating product quantities against available stock, checking if a booking falls within operating hours or verifying that an email domain is among those expected, exists, and can receive emails.
* **Cross-field validation**: examining relationships between multiple fields, such as verifying that a start date precedes an end date or ensuring consistency between related fields.

## Input validation challenges

* The following are some of the more challenging scenarios when applying input validation techniques.

### Validating rich user-generated content

* Rich user content spans a wide range of data types and formats, including text, images, videos, documents, and more. Ensuring the integrity and security of this rich user-generated content becomes essential, but complicated.
* Traditional validation techniques designed for simpler data structures may struggle to adequately handle the intricacies of rich content validation.
* Developers must deal with parsing, sanitizing, and validating diverse content formats to prevent vulnerabilities such as Cross-Site Scripting (XSS), injection attacks, and data corruption.

### Client-side vs server-side validation

* The eternal debate between client-side and server-side validation revolves around the trade-offs between user experience and security.

#### Client-side validation

* Client-side validation, executed within the user's browser, offers instantaneous feedback and a responsive interface, enhancing the user experience and interactivity by preemptively catching errors before submitting data to the server.
* However, it is susceptible to bypassing and manipulation by malicious actors, making it insufficient as the sole line of defense against attacks.

#### Server-side validation

* Server-side validation, on the other hand, emerges as the bulwark of defense against malicious attacks and data integrity breaches, prioritizing security and reliability.
* It acts as the final arbiter, rigorously scrutinizing incoming data to enforce business rules, sanitize inputs, and mitigate security risks.
* Unlike client-side validation, which can be circumvented or disabled, server-side validation operates beyond the user's control, ensuring the integrity and trustworthiness of the application's data.

  > :older_man: By combining client-side validation for usability enhancements with server-side validation for security enforcement, developers need to find a delicate balance between user experience and application integrity and security, delivering a seamless yet fortified user interaction paradigm.

[1]: /static/images/insecure-input-validation-overview.png
