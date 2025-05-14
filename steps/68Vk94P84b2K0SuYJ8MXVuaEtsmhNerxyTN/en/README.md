# Information disclosure via HTTP methods

* HTTP methods provide interaction with web resources, but improper restrictions can lead to unintended information disclosure.
* Disabling or restricting unnecessary methods helps reduce the attack surface of a web application.

## Insecure HTTP methods that may expose sensitive data

* Some HTTP methods are not necessary for most web applications and can expose sensitive data or increase the attack surface if left enabled. Common insecure methods include `TRACE`, `TRACK`, `DEBUG`, `OPTIONS`, `PUT`, and `DELETE`. These should be disabled unless required.
* The `PUT` and `DELETE` methods, for example, allow clients to upload or delete resources on the server. If improperly configured or left unrestricted, they could enable attackers to overwrite or remove server files.

### TRACE method

* The `TRACE` method is primarily used for diagnostic purposes. When a web server receives an HTTP `TRACE` request and supports this method, it echoes back the received HTTP request with all headers. This allows clients to see what data is being sent to the server.
* However, if this method is enabled, it can pose a security risk. For example, an attacker might exploit a vulnerability like `Cross-Site Scripting (XSS)` to run malicious code in a user's browser. That code could silently send a `TRACE` request to a server and read the response. Since the response includes all original headers, the attacker might gain access to sensitive information such as cookies or authentication tokens.
* Here's an example of how the `TRACE` method works using `curl`:

  ```bash
  curl -i -X TRACE http://example.tbl/
  ```

  If the server supports the `TRACE` method, the response might look like this:

  ```http
  HTTP/1.1 200 OK
  Date: Wed, 07 May 2025 12:00:00 GMT
  Content-Type: text/html
  Content-Length: 259

  TRACE / HTTP/1.1
  Host: example.tbl
  Cookie: sessionId=1234; HttpOnly
  User-Agent: curl/7.68.0
  Accept: */*
  ```

### TRACK method

* `TRACK` mirrors the request back in the response similarly to `TRACE`, and if available, may be exploited to disclose headers in the same way as `TRACE`.
* The method is deprecated and generally seen as a security concern.
* A request using the `TRACK` method can be done using `curl`:

  ```bash
  curl -i -X TRACK http://example.tbl/
  ```

  If enabled, the server could respond as follows:

  ```http
  HTTP/1.1 200 OK
  Date: Wed, 07 May 2025 12:00:00 GMT
  Content-Type: text/html
  Content-Length: 259

  TRACK / HTTP/1.1
  Host: example.tbl
  Cookie: sessionId=1234; HttpOnly
  User-Agent: curl/7.68.0
  Accept: */*
  ```

### DEBUG method

* The `DEBUG` method is designed for debugging and is rarely used in production setups. This method poses a high risk and should not be available on public-facing systems.
* If enabled, it might expose internal server details or allow command execution depending on the server configuration.
* Misconfigured environments with the `DEBUG` method enabled can be tested using the example `curl` command provided:

  ```bash
  curl -i -X DEBUG http://example.tbl/
  ```

  If accepted, the server could return internal diagnostic data such as:

  ```http
  HTTP/1.1 200 OK
  Date: Wed, 07 May 2025 12:10:00 GMT
  Content-Type: text/plain
  Content-Length: 512

  --- DEBUG INFO ---
  Request start time: 2025-05-07T12:10:00Z
  Application root: /var/www/html/app
  Loaded modules: auth, db_connector, cache
  Database connection string: Server=db.example.tbl;Database=prod;User Id=...
  Stack trace:
  at Database.Connect()
  at Api.HandleRequest()
  ...
  ```

### OPTIONS method

* The `OPTIONS` method returns information about which HTTP methods are supported by the server for a given resource.
* While it does not directly expose data, it can help attackers map out potential methods to target. In some frameworks or API configurations, it may also return metadata or documentation that was not meant to be exposed.
* Limiting or customizing its response can reduce unintended information disclosure.
* The following `curl` command demonstrates how to retrieve the supported HTTP methods for a given endpoint using the `OPTIONS` method:

  ```bash
  curl -i -X OPTIONS http://example.tbl/api/users
  ```

  When the server allows this method under certain configurations, it might return metadata related to the endpoint:

  ```http
  HTTP/1.1 200 OK
  Date: Wed, 07 May 2025 12:15:00 GMT
  Allow: GET, POST, OPTIONS
  Content-Type: application/json
  Content-Length: 198

  {
    "methods": ["GET", "POST", "OPTIONS"],
    "apiVersion": "v1.2.3",
    "parameters": [
        {
        "name": "id",
        "type": "string",
        "required": true,
        "description": "Unique resource identifier"
        },
        {
        "name": "verbose",
        "type": "boolean",
        "required": false,
        "description": "Include detailed logs in response"
        }
    ]
  }
  ```

## Recommended security approaches

* Identify all supported HTTP methods using security scanning tools.
* Restrict methods to the minimum necessary for application functionality.
* Use web server configuration to enforce method restrictions.
* Apply security headers (e.g., `X-Content-Type-Options`, `X-Frame-Options`) to mitigate the impact of method-based attacks.
* Monitor and log unusual HTTP method usage as part of routine security operations.

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

  * In IIS, HTTP methods can be restricted by configuring the `web.config` file. This helps prevent the use of unsafe or unnecessary methods, reducing the potential attack surface. The following example allows only `GET` and `POST` methods, while explicitly denying all others:

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

  * In Nginx, HTTP methods can be restricted using conditional rules inside the server or location block. The following configuration allows only `GET` and `POST` methods, rejecting all others:

    ```nginx
    server {
      location / {
        if ($request_method !~ ^(GET|POST)$) {
          return 405;
        }

        # Other configuration here
      }
    }
    ```

  @@TagEnd@@
