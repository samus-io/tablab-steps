# Best practices to prevent CORS vulnerabilities

* `CORS (Cross-Origin Resource Sharing)` is a browser-enforced security feature that controls how web applications interact with resources from different origins.
* It allows safe cross-origin communication while protecting users and servers from unauthorized or malicious access.
* Misconfigured CORS policies can expose sensitive data, open doors to cross-site attacks, and undermine the integrity of authentication and authorization mechanisms.
* Therefore, it is important to configure CORS only when it is necessary for the operation of the web application.
* Properly securing CORS is critical in preventing issues such as data leakage, unauthorized access, or privilege escalation.
* Note that implementing the CORS policy correctly is not a replacement for server-side protection. Even if it is set correctly, the server must implement other security protections, such as authentication and preventing the leakage of sensitive data.

## Avoid using wildcards

* Using a wildcard (`*`) in the `Access-Control-Allow-Origin` header allows any origin to access the resource, which eliminate origin-based access control, allowing any website to interact with protected APIs or sensitive data.
* Using wildcards becomes especially dangerous if the server also allows credentials, which is disallowed by the CORS specification and ignored by most browsers but can still signal poor configuration.
* Always specify a known and trusted origin instead of using a wildcard.

## Use specific `Access-Control-Allow-Origin` values

* Only explicitly trusted domains should be allowed to access cross-origin resources. Avoid overly broad access that includes multiple unrelated or third-party origins.
* Maintain a fixed allowlist of origins and check the request's origin against this list before including `Access-Control-Allow-Origin` header in the response.
* Dynamic validation must always include strict checks to ensure only intended origins are allowed.

### Avoid using null as a value

* Never use the `Access-Control-Allow-Origin` header with `null` value. This can unintentionally allow access from untrusted sources and creates security risks similar to using a wildcard (`*`).

## Only send credentials when necessary

* Cross-origin requests that include credentials such as cookies or HTTP authentication should be handled with extra care.
* Only include the header `Access-Control-Allow-Credentials: true` when credentials are required for authentication.
* If credentials are not needed, the header should be omitted or explicitly set to `false`.
* Using credentials unnecessarily increases the impact of any misconfiguration or origin validation failure.

## Origin validation

### Validate Origin header on the server side

* Never trust the `Origin` header blindly, as it can be spoofed in non-browser environments or misused if improperly handled.
* All origin validation must happen on the server side to ensure consistency and security across environments.

### Avoid reflecting the Origin header

* Some insecure implementations dynamically echo the `Origin` header back in the `Access-Control-Allow-Origin` response, regardless of the request's source.
* If an attacker sends a request from a malicious origin, the server will unknowingly authorize it by reflecting the origin, defeating the purpose of CORS.
* Before sending the `Access-Control-Allow-Origin` header, verify that the origin is known and trusted before including it in the response.

## Restrict allowed HTTP methods

* Only allow the HTTP methods that are necessary for the web application. Avoid exposing unsafe or unused methods like `PUT`, `DELETE`, or `PATCH` unless explicitly required.
* Unnecessary exposure of HTTP methods increases the attack surface and could allow malicious users to perform unintended actions.

## Limit allowed headers

* Just like methods, custom request headers should be limited to only what is essential.
* The `Access-Control-Allow-Headers` response should list only the headers the web application requires.
* Avoid reflecting all headers from the request or using `*`, which can unintentionally allow sensitive or unnecessary information to be sent.
