# Traditional 3-Tier Software & Secure Architectures Integration

* Below is a graphical representation of how to integrate the traditional 3-tier software architecture (Presentation, Application and Data tiers) with the traditional 3-tier secure architecture (Demilitarized, Trusted and Private tiers).

![Three-tier software & secure architecture integration][1]

* Notice that web servers will not directly touch the database servers.
  * The business layers should be offloaded from the web servers to dedicated business data processing servers and this is where the actual data processing occurs, including adding information to the database, retrieving and manipulating data, and executing scheduled tasks and jobs.
  * These business backend layers should also take responsibility for implementing most data security measures, ensuring data integrity.
  * Web servers will contact the business data processing servers through a less benign protocol, such as HTTP or HTTPS, and these applications will be coded to make SQL calls to the internal database servers.
  * These backend servers at the Trusted Tier will never be exposed directly to the Internet.
* This 3-tier approach is seen in traditional on-premises infrastructures, and it can still be considered nowadays for simple web applications or unified development of on-premises and cloud applications.

## Integration process

### Presentation Tier is placed in the Demilitarized Tier

* The Presentation Tier, containing only application display logic and other display services support, should be placed in the Demilitarized Tier.

### Application Tier is split between the Demilitarized and Trusted Tiers

* Components of the Application Tier needed to fulfill user interface requests should be placed in the Demilitarized Tier.
* Application servers containing all business logic should be placed in the Trusted Tier, making them accessible through designated communications from the Demilitarized Tier.

### Data Tier is placed in the Private Tier

* The Private Tier should contain the database servers, which ideally will only be queried by servers at the Trusted Tier with limited specific access allowed.

### Challenges

* If not properly designed, it's easy to end up creating a middle tier that merely performs CRUD operations on the database, which adds extra latency without contributing any valuable work.
* When breaking down an application into distinct layers or services, there's a potential risk that inter-service communication might lead to unacceptable latency or result in network congestion.

### Best practices

* Use autoscaling to manage workload changes.
* Consider asynchronous messaging to decouple tiers.
* Install a Web Application Firewall (WAF) to analyze incoming Internet traffic.
* Restrict access to the Data Tier by permitting requests only from the Trusted Tier.

## Pros & Cons

### Benefits

* Less learning curve for developers.
* Open to heterogeneous environment (Windows/Linux).
* Portability between cloud and on-premises, and between cloud platforms.
* The shielding of business backend layers from direct Internet exposure can lessen the frequency of technology stack updates, allowing longer intervals to address identified vulnerabilities.

### Drawbacks

* The update frequency is low.
* It can increase network security management in a large system.
* Monolithic design restricts the separate deployment of individual features.

## Additional security considerations

* Public-facing servers should never be granted direct access to internal networks or resources.
  * Consider adding a Read-Only Domain Controller (RODC) in the Trusted Tier to manage external user authentications if necessary.
* Users should never directly touch content serving web servers.
  * All incoming Internet requests should be reverse proxied to various web services.
  * These reverse HTTP proxies should be kept on their own subnets, separate from the subnets of other web servers.
* Resources should, whenever possible, be confined to a single network segment to avoid having resources accessible **on service ports** across multiple network interfaces.

[1]: /static/images/learning/three-tier-software-and-secure-architecture-integration.png
