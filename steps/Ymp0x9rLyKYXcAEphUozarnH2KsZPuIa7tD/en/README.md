# Introduction of LDAP

* LDAP `(Lightweight Directory Access Protocol)` is an open, vendor-neutral application protocol used for accessing and maintaining distributed directory information services over an IP network.
* It provides a way to manage and query directory information, often used for storing details about users, groups, and resources within an organization.

## LDAP Use Cases

* **Authentication and Authorization**
  * **Authentication**: Verifies the identity of a user or system attempting to access a resource.
  * **Authorization**: Determines what resources the authenticated user or system is allowed to access based on defined permissions.

* **Centralized Directory Services**
  * Provides a single, centralized repository for storing and managing user credentials, organizational hierarchies, and resource information, ensuring consistent data management across the network.

* **Single Sign-On (SSO)**
  * Allows users to authenticate once and gain access to multiple systems and applications without needing to re-authenticate, enhancing both user experience and security.

* **Email Client Configuration**
  * Stores and retrieves contact information, enabling email clients to access a central directory for email addresses and related data.

* **Network Resource Management**
  * Manages networked resources such as printers, servers, and other devices, allowing centralized control and access management.

* **Corporate Directory Services**
  * Maintains employee contact details, organizational charts, and other personnel-related information.

## How LDAP Works

* **Directory Structure (DIT)**
  * The `Directory Information Tree` (DIT) is the hierarchical structure of an LDAP directory, where entries are organized in a tree-like format.
  * The top level is the root, followed by branches representing organizational units, and leaf nodes representing individual entries such as users or devices.  

* **Entries**
  * Each entry in an LDAP directory represents a single unit of information and is composed of a set of attributes.
  * Each entry is identified by a unique Distinguished Name (DN),which is a concatenation of the relative distinguished names (RDNs) of each entry along the path from the root

* **Attributes**
  * Attributes are specific pieces of information associated with an entry.
  * Each attribute has a type and one or more values.

* **Object Classes**
  * Object classes define the schema for entries, specifying the required and optional attributes for each type of entry.
  * Common object classes include `inetOrgPerson` for user entries, `organizationalUnit` for organizational units, and `groupOfNames` for groups.

  ![ldap](https://github.com/samus-io/tablab-steps/assets/44079067/b36e8186-28a8-49d0-952c-f4961b766bab)

## LDAP Directory Structure

* **Root Entry (Directory Information Tree - DIT)**: The topmost entry in the LDAP directory is called the root or the Directory Information Tree (DIT). It is the starting point of the hierarchy.
* **Country (c)**: Just below the root, the directory may have entries for different countries, represented by the attribute "c" (e.g., c=US for the United States).
* **Organization (o)**: Under each country entry, there can be entries for different organizations, represented by the attribute "o" (e.g., o=ExampleCorp).
* **Organizational Units (ou)**: Within an organization, entries can be further divided into organizational units, represented by the attribute "ou" (e.g., ou=Engineering, ou=Sales).
* **Common Name (cn)**: The leaf nodes of the directory structure are individual entries, such as people or devices, represented by the attribute "cn" (e.g., cn=John Doe).
* **Domain Component (dc)**: An alternative naming method is based on domain components, useful for Internet domain names (e.g., dc=example, dc=com).

* Example of an LDAP Directory Structure

```bash
    dc=example, dc=com
    |
    +-- ou=Engineering
    |   +-- cn=John Doe
    |   +-- cn=Jane Smith
    |
    +-- ou=Sales
        +-- cn=Alice Johnson
        +-- cn=Bob Brown
```

* In this example:
  * The root is dc=example, dc=com.
  * There are two organizational units: ou=Engineering and ou=Sales.
  * Under ou=Engineering, there are two entries: cn=John Doe and cn=Jane Smith.
  * Under ou=Sales, there are two entries: cn=Alice Johnson and cn=Bob Brown.

* This hierarchical structure allows LDAP to efficiently organize and manage directory information, making it easy to locate and authenticate users and resources within a network.

## LDAP Workflow operations

* **Bind**
  * Establishes a connection to the LDAP server and authenticates the client, allowing subsequent operations to be performed under the authenticated user's context.

* **Search**
  * Retrieves directory entries that match a given search filter, allowing queries on specific attributes or a set of attributes.

* **Compare**
  * Compares an attribute value with those of a specified entry to determine if they match.

* **Add**
  * Adds a new entry to the directory, allowing the creation of new users, groups, or resources.

* **Delete**
  * Removes an entry from the directory, effectively deleting users, groups, or resources.

* **Modify**
  * Updates attributes of an existing entry, allowing changes to user information, group memberships, or resource details.

* **Modify DN**
  * Changes the Distinguished Name (DN) of an entry, effectively moving it within the directory tree or renaming it.

* **Unbind**
  * Terminates the connection to the LDAP server, closing the session and cleaning up any associated resources.

### References

* OKTA: <https://www.okta.com/identity-101/what-is-ldap/>
* JumpCloud: <https://jumpcloud.com/blog/what-is-ldap>
* IBM: <https://www.ibm.com/support/pages/master-document-ldap-configurations-flow-chart>
