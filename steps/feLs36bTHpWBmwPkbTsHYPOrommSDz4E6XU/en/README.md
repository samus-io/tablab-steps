# Traditional 3-tier software & secure architectures integration

* Below is a graphical representation of how to integrate the traditional 3-tier software architecture (presentation, application and data tiers) with the traditional 3-tier secure architecture (demilitarized, trusted and private tiers).

![Three-tier software & secure architecture integration][1]

* Notice that web servers will not directly touch the database servers.
  * The business layers should be offloaded from the web servers to dedicated business data processing servers and this is where the actual data processing occurs, including adding information to the database, retrieving and manipulating data, and executing scheduled tasks and jobs.
  * These business backend layers should also take responsibility for implementing most data security measures, ensuring data integrity.
  * Web servers will contact the business data processing servers through a less benign protocol, such as HTTP or HTTPS, and these applications will be coded to make SQL calls to the internal database servers.
  * These backend servers at the trusted tier will never be exposed directly to the Internet.
* This 3-tier approach was observed in traditional on-premises infrastructures, and it can still be considered nowadays for simple web applications or unified development of on-premises and cloud applications.

## Integration process

### Presentation tier is placed in the demilitarized tier

* The presentation tier, containing only application display logic and other display services support, should be placed in the demilitarized tier.

### Application tier is split between the demilitarized and trusted tiers

* Components of the application tier needed to fulfill user interface requests should be placed in the demilitarized tier.
* Application servers containing all business logic should be placed in the trusted tier, making them accessible through designated communications from the demilitarized tier.

### Data tier is placed in the private tier

* The private tier should contain the database servers, which ideally will only be queried by servers at the trusted tier with limited specific access allowed.

### Challenges

* If not properly designed, it's easy to end up creating a middle tier that merely performs CRUD operations on the database, which adds extra latency without contributing any valuable work.
* When breaking down an application into distinct layers or services, there's a potential risk that inter-service communication might lead to unacceptable latency or result in network congestion.

### Best practices

* Use autoscaling to manage workload changes.
* Consider asynchronous messaging to decouple tiers.
* Install a `Web Application Firewall (WAF)` to analyze incoming Internet traffic.
* Restrict access to the data tier by permitting requests only from the trusted tier.

## Pros & cons

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
  * Consider adding a `Read-Only Domain Controller (RODC)` in the trusted tier to manage external user authentications if necessary.
* Users should never directly touch content serving web servers.
  * All incoming Internet requests should be reverse proxied to various web services.
  * These reverse HTTP proxies should be kept on their own subnets, separate from the subnets of other web servers.
* Resources should, whenever possible, be confined to a single network segment to avoid having resources accessible **on service ports** across multiple network interfaces.

[1]: /static/images/three-tier-software-and-secure-architecture-integration.png
