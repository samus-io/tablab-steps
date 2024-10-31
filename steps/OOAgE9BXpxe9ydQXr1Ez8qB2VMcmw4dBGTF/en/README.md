# Traditional 3-Tier Software Architecture

* The 3-tier software architecture is a client-server software architecture pattern in which the user interface (`Presentation Tier`), bussines logic (`Application Tier`), computer data storage and data access (`Data Tier`) are developed and maintained as independent modules, most often on separate platforms.

![Three-tier software architecture][1]

* Besides the common benefits of modular software with well-defined interfaces, the 3-tier architecture is designed to permit the independent upgrading or replacement of any of its three tiers in response to changes in requirements or technology.
* Each tier runs on its own infrastructure and can exist without the tier above it, but requires the tier below it to function.
* All communication goes through the Application Tier. The Presentation Tier and the Data Tier cannot communicate directly with one another.

## Tier vs Layer

* While the concepts of _layer_ and _tier_ are often used interchangeably, there is indeed an important difference.
* A _layer_ refers to a functional division of the software, a logical structuring mechanism for the conceptual elements that make up a software application.
* A _tier_ instead, refers to a division of the software that runs on infrastructure separate from the other divisions, a physical or virtual structuring mechanism for the hardware elements that make up the system infrastructure.
* The Contacts App on a phone, for example, it's a 3-layer application, but a single-tier application, because all three layers run on the phone itself.

## Presentation Tier

* The Presentation Tier is the User Interface (UI) of the software, where the end user interacts with the application.
* Its main purpose is to display information to and collect information from the user.
* This top-level tier can run on a web browser, like a React App, or as desktop application, for example.

## Application Tier

* The Application Tier, also known as the logic, business or middle tier, is the heart of the application.
* In this tier, information collected in the Presentation Tier is processed against a specific set of business rules.
* This tier is mainly responsible for the input validation checks and security rules.
* This can be a web server hosting the application and its components, and a REST API processing the requests.

## Data Tier

* The Data Tier, sometimes called database tier or data access tier, is where the information processed by the application is stored and managed.
* It includes the data persistence mechanisms (database servers, file shares, etc) and the data access layer that encapsulates the persistence mechanisms and exposes the data.
* The data access layer should provide an API to the Application Tier that exposes methods of managing the stored data without exposing or creating dependencies on the data storage mechanisms.
* This can be a relational database management system such as PostgreSQL, MySQL, MariaDB, Oracle, DB2, Informix or Microsoft SQL Server, or in a NoSQL Database server such as Cassandra, CouchDB or MongoDB or even any cloud storage such as Amazon S3 or Google Cloud Storage.
* Avoiding dependencies on the storage mechanisms allows for updates or changes without the Application Tier clients being affected by or even aware of the change.

## Pros & Cons

### Benefits

* **Improved scalability**: each tier can be scaled independently based on requirements. Additionally, each tier operates on its own dedicated server hardware or virtual server, allowing the services of each tier to be customized and optimized without affecting the other tiers.
* **Improved reliability**: a failure in one tier is less likely to affect the availability or performance of the other tiers.
* **Improved security**: since the presentation tier and data tier do not communicate directly, a well-structured application tier can act as an internal firewall, protecting against SQL injections and other types of malicious exploits.
* **Faster development**: since each tier can be developed concurrently by separate teams, an organization can accelerate the application's time to market. Additionally, programmers can utilize the most current and effective languages and tools specific to each tier.

### Drawbacks

* The 3-tier architecture is outdated and is is also frequently called a monolithic architecture. It was developed prior to the widespread adoption of public cloud and mobile applications, and has struggled to adapt effectively to cloud environments.
* As an application grows in size and complexity, it can become challenging to implement frequent updates.
* Additionally, maintaining at least three separate layers of hardware and software can lead to inefficiencies for a business.

[1]: /static/images/learning/three-tier-software-architecture.png
