# General best practices against LDAP Injections

* LDAP injection is a critical security vulnerability that can be mitigated through a series of best practices.
* These measures ensure that LDAP queries are secure, preventing unauthorized access and data manipulation.

## Input Validation

* Input validation is the first line of defense against LDAP injection.
* Techniques such as syntax validation and whitelists should be used to ensure that inputs conform to expected formats and values.
* Example:
  * Creating a whitelist of allowed users can prevent unauthorized access.
  * For instance, only allowing users with specific usernames like "`admin`", "`user1`", "`user2`" ensures that unexpected or malicious usernames are not processed by the LDAP server.

## Escape special characters

* Special characters in LDAP queries must be escaped to prevent them from being interpreted as LDAP commands.
  * **Escape Characters**: Convert special characters to their hexadecimal equivalents.
  * For example, the backslash `\` should be escaped as `\5c`.
  * **First character to escape**: Always start escaping with the backslash ().
    * Escaping Distinguished Names (DN)
    * In distinguished names, the following characters must be escaped: `\ # + < > , ; " =` and any leading or trailing spaces.

* **Escaping search filters**
* In search filters, the following characters must be escaped: `\ * ( ) NUL` (where NUL is the null byte `\x00`).

## Where to use each escape model

* **Escape DN**: Use this when performing operations like add, modify DN, and delete.
* **Escape Filter**: Use this when performing search, bind, and compare operations, or when creating filters.

## Use a library to create filters

* To avoid constructing filters by concatenating strings, utilize libraries that provide methods for safely creating LDAP filters.
* This ensures that inputs are properly sanitized and encoded.

## Bind Authentication

* When using bind authentication for logging in users, disable anonymous and unauthenticated bind options on the LDAP server.
* This prevents unauthorized access by ensuring that all binds are authenticated.

## Use frameworks that prevent LDAP injection

* Leverage frameworks and libraries that include built-in protections against LDAP injection.
* These tools help to automate many of the security best practices, reducing the risk of human error.

## Additional Defenses

* **Restrict User Requests**:
  * **Set the Base DN and Scope**: Define a base DN and scope to limit the part of the directory tree that can be searched or modified.
  * **Example**: For an organization, set the base DN to "`dc=example,dc=com`" and scope to "`subtree`" to ensure that searches are confined to the relevant portion of the directory.

  * **Entry Limit**: Set limits on the number of entries that can be returned by a query to prevent denial of service attacks.
    * **Example**: Limit search results to a maximum of 1000 entries to prevent excessive data retrieval.

  * **Timeouts**: Implement timeouts on LDAP queries to avoid long-running operations that can degrade performance or be exploited.
    * **Example**: Implement a 30-second timeout on LDAP queries to prevent prolonged execution times.

* **Least Privilege**:

  * Assign the minimal necessary privileges to the LDAP binding account.
  * This principle limits the potential damage in case of an account compromise, ensuring that the binding account can only perform specific, necessary actions.
    * **Example**: Configure the LDAP binding account to only have read access to user attributes necessary for authentication, rather than write access.
