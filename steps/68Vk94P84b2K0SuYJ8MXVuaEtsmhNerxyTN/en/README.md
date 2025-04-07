# Information disclosure via HTTP methods

* HTTP methods allow interaction with web resources, but some can unintentionally leak sensitive information if not properly restricted.
* Disabling or restricting unnecessary methods helps reduce the attack surface of a web application

## Insecure HTTP methods that may expose sensitive data

### TRACE

* The `TRACE` method is primarily used for diagnostic purposes. When a web server receives an HTTP `TRACE` request and supports this method, it mirrors back the incoming data, including all HTTP headers.
* If an attacker combines this with another vulnerability, such as `Cross-Site Scripting (XSS)`, it can be used to trick a browser into sending a `TRACE` request and capturing the response
* This behavior may expose cookies, authentication headers, or other sensitive information.

### TRACK

* `TRACK` works similarly to `TRACE` by reflecting the received request in the response.
* Although not commonly enabled, if active, it can be exploited to leak header data in the same way as `TRACE`.
* Its use is outdated and generally considered insecure.

### DEBUG

* The `DEBUG` method is designed for debugging and is rarely used in production setups.
* If enabled, it might expose internal server details or allow command execution depending on the server configuration.
* This method poses a high risk and should not be available on public-facing systems.

### OPTIONS

* The `OPTIONS` method returns information about which HTTP methods are supported by the server for a given resource.
* While it does not directly expose data, it can help attackers map out potential methods to target.
* In some frameworks or API configurations, it may also return metadata or documentation that was not meant to be exposed.
* Limiting or customizing its response can reduce unintended information disclosure.

## Recommended security approaches

### Restrict unnecessary HTTP methods

* Web servers and applications should be configured to allow only the HTTP methods that are strictly required.
* Disabling unused or potentially dangerous methods reduces the risk of information leakage and abuse.

@@TagStart@@apache

* In Apache, the following configuration can be used to allow only `GET` and `POST`, denying all other methods:

```apache
<Location />
    <LimitExcept GET POST>
        Require all denied
    </LimitExcept>
</Location>
```

@@TagEnd@@

@@TagStart@@iis

* In IIS, HTTP methods can be restricted by configuring the `web.config` file. This helps prevent the use of unsafe or unnecessary methods, reducing the potential attack surface.
* The following example allows only `GET` and `POST` methods, while explicitly denying all others:

```xml
<configuration>
    <system.webServer>
        <security>
            <requestFiltering>
                <verbs>
                    <add verb="GET" allowed="true"/>
                    <add verb="POST" allowed="true"/>
                    <add verb="*" allowed="false"/>
                </verbs>
            </requestFiltering>
        </security>
    </system.webServer>
</configuration>
```

@@TagEnd@@

@@TagStart@@nginx

* In Nginx, HTTP methods can be restricted using conditional rules inside the server or location block.
* The following configuration allows only `GET` and `POST` methods, rejecting all others:

```nginx
server {
    location / {
        if ($request_method !~ ^(GET|POST)$) {
            return 405;
        }

        # Other configuration
    }
}
```

@@TagEnd@@
