# Traditional 3-Tier Secure Architecture

* The 3-tier secure architecture is an architectural pattern that defines a model composed of three tiers referred as `Demilitarized Tier`, `Trusted Tier` and `Private Tier`, in which for each of these security tiers different levels of security, access, and resource update policies are established.

![Three-tier secure architecture][1]

* Tiers are separated by firewalls and the traffic between is inspected by IDS/IPS systems.
  * Each tier has its own network segments.
* In a closed tier architecture, all communications originating from lower tiers can reach an asset belonging to any higher tier, but not the other way around; communications originating from a specific tier can only reach an asset belonging to the tier immediately below.
* The 3-tier architecture is very common in traditional on-premises infrastructures.

## Demilitarized Tier

* The Demilitarized Tier is where all public access servers are hosted and services are offered to external users.
* It has very strict security measures and policies, as daily or weekly update procedures.
* Traditionally, a Demilitarized Tier, in on-premise infrastructures, it usually contains one or multiple DMZ networks.
  > :older_man: A DMZ network, also known as a perimeter network, is essentially a physical or logical network that contains and presents an organization's external-facing services to a larger and typically untrusted network, such as the Internet.

## Trusted Tier

* The Trusted Tier, sometimes also called logic or transaction tier, includes those services that published servers use to deliver specific services to external users.
* It actually contains the actual business processing logic as well as links to internal systems for additional processing capabilities.
* Most security measures related to input data processing are implemented at this tier.
* Traditionally, a Trusted Tier, in on-premise infrastructures, contains one or multiple transaction networks.
  > :older_man: A transaction network, also called middle or gray network, is just a physical or logical network that sits between DMZ networks and deeper internal networks.

## Private Tier

* The Private Tier consists of the core data on which the business depends on.
* This is where the most critical and sensitive data belonging to an organization should generally be located.
  * Not only in terms of database servers, but also other sensitive services such as Active Directory Domain Services (AD DS) or Network-Attached Storage (NAS).
* Traditionally, in on-premise infrastructures, it contains multiple internal networks.
  > :older_man: An internal network, often just called a LAN, is a private, proprietary network accessible only to employees of a specific corporation, where most internal business services are offered.

## Additional security considerations

* When transitioning to a lower tier, the communication protocol should be different from the one used to communicate from the tier above to the current tier.
* It's advisable to employ multiple security providers and solutions to analyze traffic between tiers.
* Security rules should be applied as close to the origin as possible.

[1]: /static/images/three-tier-secure-architecture.png
