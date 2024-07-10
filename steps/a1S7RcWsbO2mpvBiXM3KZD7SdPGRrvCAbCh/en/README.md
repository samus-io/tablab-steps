# Introduction of LDAP Injection

* LDAP Injection is a security vulnerability that occurs when untrusted input is inserted into an LDAP statement, allowing an attacker to alter the intended query.
* This type of injection exploits weaknesses in the construction of LDAP statements to execute arbitrary queries or commands, potentially leading to unauthorized access, data manipulation, or disclosure.

## What Can Be Achieved with LDAP Injection?

* **Unauthorized Access**: Bypass authentication mechanisms to gain access to restricted areas of an application.
* **Data Manipulation**: Modify, add, or delete entries in the LDAP directory.
* **Data Disclosure**: Retrieve sensitive information that should not be accessible.
* **Denial of Service**: Disrupt the normal operation of the LDAP server.

## How LDAP Injection Works

* LDAP injection exploits vulnerabilities in applications that construct LDAP queries using untrusted user input without proper validation or sanitization.
* When an application inserts user input directly into an LDAP query, an attacker can manipulate this input to alter the query's logic, achieving unintended outcomes.

## Use Case of LDAP Injection to Bypass Login

* Consider a login system that authenticates users by verifying their username and password against an LDAP directory.
* The application constructs an LDAP query based on user input as follows:

```bash
(&(USER={username})(PASSWORD={password}))
```

* If an attacker inputs the following payload for the username:

```bash
brad)(&))
```

* And any password, the resulting LDAP query would look like this:

```bash
(&(USER=brad)(&))(PASSWORD=pwd))
```

* This malformed query effectively bypasses the password check because the (&) condition always evaluates to true, granting unauthorized access to the attacker.

## Example of LDAP Injection

* Below is a conceptual diagram illustrating how LDAP injection can alter the expected flow of an application.
 
![ldap injection](https://github.com/samus-io/tablab-steps/assets/44079067/bdc4f4b7-4ad9-4672-afd3-59080c54b254)

* **Expected Flow**:

    ```bash
    User Input: 
    Username: brad123
    Password: pwd

    LDAP Query: 
    (&(USER=brad123)(PASSWORD=pwd))
    ```

  * The application sends a valid query to the LDAP server, which verifies the credentials.

* **Injected Flow**:

    ```bash
    User Input: 
    Username: brad)(&))
    Password: pwd

    LDAP Query: 
    (&(USER=brad)(&))(PASSWORD=pwd))
    ```

  * The application constructs an invalid query that bypasses the password check due to the injected (&) condition.

## Additional Examples

* **Extracting Data**: An attacker could input a payload to retrieve all users' details.

    ```bash
    User Input: 
    Username: *)
    Password: *

    LDAP Query: 
    (&(USER=*)(PASSWORD=*))
    ```

* **Deleting an Entry**: If the application allows modification operations, an attacker might delete an entry.

    ```bash
    User Input: 
    Username: admin)(objectClass=*)
    Password: *

    LDAP Query: 
    (&(USER=admin)(objectClass=*))(PASSWORD=*)
    ```

## Preventing LDAP Injection

* **Input Validation**: Rigorously validate and sanitize all user inputs.
* **Parameterized Queries**: Use LDAP libraries that support parameterized queries to ensure that user inputs are not interpreted as LDAP code.
* **Allow-Lists**: Implement allow-lists to restrict acceptable inputs to known, safe values.
* **Escaping**: Properly escape special characters in user inputs to prevent them from being interpreted as LDAP operators.

## References

* <https://www.techtarget.com/searchsoftwarequality/definition/LDAP-injection>
