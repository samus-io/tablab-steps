# Preventing LDAP Injection in Node.js

* LDAP injection is a serious security threat that can compromise the integrity and confidentiality of an application.
* Several strategies can be implemented in Node.js to prevent LDAP injection, ensuring secure and reliable operations.

## Escape special characters

* Escaping special characters is crucial to prevent them from being interpreted as LDAP commands.
* This involves converting special characters to their hexadecimal equivalents.
* **Example** for `implementing Escape special characters`:

    ```javascript
    function escapeSpecialCharacters(input) {
        return input.replace(/\\/g, '\\5c')
                    .replace(/\*/g, '\\2a')
                    .replace(/\(/g, '\\28')
                    .replace(/\)/g, '\\29')
                    .replace(/\x00/g, '\\00');
    }

    // Usage
    const userInput = 'John*Doe';
    const escapedInput = escapeSpecialCharacters(userInput);
    console.log(escapedInput); // Output: John\2aDoe
    ```

### Escaping Distinguished Names (DNs)

* For `Distinguished Names`, additional characters need to be escaped: `\ # + < > , ; " =` and leading or trailing spaces.
* Distinguished Names (DNs) are used to uniquely identify entries in the LDAP directory.
* Properly escaping special characters in DNs prevents them from being misinterpreted as LDAP commands or causing unintended behavior.
* **Example** for `implementing Escape Distinguished Names (DNs)`:

    ```javascript
    function escapeDN(input) {
        // Escape leading and trailing spaces
        let escaped = input.replace(/^ /, '\\20').replace(/ $/, '\\20');
        // Escape other special characters
        escaped = escaped.replace(/\\/g, '\\5c')
                        .replace(/#/g, '\\23')
                        .replace(/\+/g, '\\2b')
                        .replace(/</g, '\\3c')
                        .replace(/>/g, '\\3e')
                        .replace(/,/g, '\\2c')
                        .replace(/;/g, '\\3b')
                        .replace(/"/g, '\\22')
                        .replace(/=/g, '\\3d');
        return escaped;
    }

    // Usage
    const dnInput = ' John Doe ';
    const escapedDN = escapeDN(dnInput);
    console.log(escapedDN); // Output: \20John\20Doe\20
    ```

## Use a library to create filters

* Using a library to create LDAP filters ensures that inputs are properly sanitized and encoded, reducing the risk of injection attacks.
* Libraries like ldap-filters provide methods to safely construct LDAP filters.
* **Example** using `ldap-filters`:
  * First, install the `ldap-filters` library:

    ```bash
    npm install ldap-filters
    ```

  * Then, use it to create secure filters:

    ```javascript
    const ldapFilters = require('ldap-filters');

    // Create a filter for user login
    const username = 'johndoe';
    const password = 'password123';
    const filter = ldapFilters.and(
        ldapFilters.equals('uid', username),
        ldapFilters.equals('userPassword', password)
    );

    console.log(filter.toString()); // Output: (&(uid=johndoe)(userPassword=password123))
    ```

## Use frameworks that prevent LDAP Injection

* Frameworks and libraries that abstract LDAP operations often include built-in protections against LDAP injection.
* Using these tools can automate many security best practices, reducing the risk of manual errors.
* **Example** using `Passport-LDAPauth`:
  * The passport-ldapauth middleware for Node.js provides LDAP authentication with built-in protections against injection attacks.
  * First, install the passport-ldapauth library:

    ```bash
    npm install passport passport-ldapauth
    ```

  * Then, configure it in the application:

    ```javascript
    const passport = require('passport');
    const LdapStrategy = require('passport-ldapauth');

    const OPTS = {
        server: {
            url: 'ldap://ldap.example.com:389',
            bindDN: 'cn=admin,dc=example,dc=com',
            bindCredentials: 'adminpassword',
            searchBase: 'dc=example,dc=com',
            searchFilter: '(uid={{username}})'
        }
    };

    passport.use(new LdapStrategy(OPTS));

    app.post('/login', passport.authenticate('ldapauth', { session: false }), (req, res) => {
        res.send('Logged in successfully');
    });
    ```

## Additional Defenses

* Implementing additional defenses further strengthens security by limiting the scope and impact of potential attacks.

### Restricting User Requests

* Restricting user requests involves setting limits on the scope and amount of data that can be retrieved or modified through LDAP operations.
* This can include defining a base DN, setting a scope for searches, and imposing entry limits and timeouts.
* Let us first understand these concepts.

#### Set the Base DN and Scope

* Define a base DN and scope to limit the searchable directory tree.
* **Example** for `Setting the Base DN and Scope`:

    ```javascript
    const OPTS = {
        server: {
            url: 'ldap://ldap.example.com:389',
            bindDN: 'cn=admin,dc=example,dc=com',
            bindCredentials: 'adminpassword',
            searchBase: 'ou=users,dc=example,dc=com', // Base DN
            searchFilter: '(uid={{username}})',
            scope: 'sub' // Subtree scope
        }
    };
    ```

#### Entry Limit and Timeouts

* Set limits on the number of entries returned and implement timeouts to prevent long-running queries.
* **Example** for `implementing Entry Limit and Timeouts`:

    ```javascript
    const ldap = require('ldapjs');

    const client = ldap.createClient({
        url: 'ldap://ldap.example.com:389',
        connectTimeout: 30000 // 30 seconds
    });

    const opts = {
        filter: '(uid=johndoe)',
        scope: 'sub',
        sizeLimit: 1000 // Max 1000 entries
    };

    client.search('ou=users,dc=example,dc=com', opts, (err, res) => {
        if (err) {
            console.error('Error in search operation:', err);
            return;
        }

        res.on('searchEntry', entry => {
            console.log('Entry:', entry.object);
        });

        res.on('end', result => {
            console.log('Search completed with status:', result.status);
        });
    });
    ```

* After combining the above steps, we can setup the basic implementation of Restricting user requests.
* **Example** for `implementing Restricting User Requests`: Setting Base DN, Scope, Entry Limits, and Timeouts.

    ```javascript
    const ldap = require('ldapjs');

    // Create LDAP client with a connection timeout
    const client = ldap.createClient({
        url: 'ldap://ldap.example.com:389',
        connectTimeout: 30000, // 30 seconds timeout
    });

    // Search options to restrict user requests
    const searchOptions = {
        filter: '(uid=johndoe)', // Filter to search for a specific user
        scope: 'sub', // Subtree scope
        sizeLimit: 1000, // Limit to 1000 entries
        timeLimit: 10 // Limit search operation to 10 seconds
    };

    // Perform search operation
    client.search('ou=users,dc=example,dc=com', searchOptions, (err, res) => {
        if (err) {
            console.error('Error in search operation:', err);
            return;
        }

        res.on('searchEntry', entry => {
            console.log('Entry:', entry.object);
        });

        res.on('end', result => {
            console.log('Search completed with status:', result.status);
        });
    });
    ```

* In this example, the `searchOptions` object specifies:
  * **filter**: The filter to apply, limiting the search to users with a specific UID.
  * **scope**: The scope of the search, set to 'sub' for subtree searches.
  * **sizeLimit**: The maximum number of entries to return.
  * **timeLimit**: The maximum time to allow the search operation to run.

### Least Privilege

* The principle of least privilege involves granting only the minimum set of permissions necessary for the LDAP binding account to perform required operations.
* This reduces the risk associated with compromised credentials or misconfigured access controls.
* **Example** for `implementing Least Privilege`: Configuring LDAP Client with Least Privilege
  * LDAP Server Configuration: Ensure the LDAP binding account has limited permissions on the LDAP server.
  * This configuration is usually done on the LDAP server itself, outside of the Node.js application.
  * Using a Limited Privilege Binding Account: Configure the Node.js LDAP client to use an account with restricted permissions.

    ```javascript
    const ldap = require('ldapjs');

    // Create LDAP client
    const client = ldap.createClient({
        url: 'ldap://ldap.example.com:389'
    });

    // Bind to the server with a limited privilege account
    client.bind('cn=readonly,dc=example,dc=com', 'readonlypassword', err => {
        if (err) {
            console.error('Error in binding:', err);
            return;
        }

        // Perform a search operation with limited privileges
        const searchOptions = {
            filter: '(uid=johndoe)',
            scope: 'sub',
            attributes: ['uid', 'cn', 'mail'] // Only retrieve necessary attributes
        };

        client.search('ou=users,dc=example,dc=com', searchOptions, (err, res) => {
            if (err) {
                console.error('Error in search operation:', err);
                return;
            }

            res.on('searchEntry', entry => {
                console.log('Entry:', entry.object);
            });

            res.on('end', result => {
                console.log('Search completed with status:', result.status);
                client.unbind();
            });
        });
    }); 
    ```

* In this example, the LDAP client binds to the server using a read-only account (`cn=readonly,dc=example,dc=com`).
* This account should be configured on the LDAP server to have minimal permissions, only allowing it to perform necessary operations like searching for user information.
