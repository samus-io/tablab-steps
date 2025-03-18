# Information exposure through sensitive query strings in URL

* This type of information exposure occurs when sensitive data such as usernames, passwords, session identifiers, tokens, database details, credit card numbers or any kind of Personally Identifiable Information (PII) or other potentially sensitive data is passed to parameters in the URL, as shown in the following example:

  ```url
  https://example.tbl/?user=john&auth_token=7s41nx93hdlaks8FtSbWM3NHRICy2sdhd83jksd9
  ```

## What could result from this scenario

* This information is susceptible to be:
  * Saved in the browser's history and browser's cache.
  * Stored in web logs.
  * Stored in any potential intermediaries, like load balancers or caching proxies.
  * Passed through the `Referer` header to other web sites.
  * Exposed in shoulder surfing scenarios.
* Attackers having access to any of these circumstances can obtain valuable information from sensitive query strings that can be used to scale their attack method.
  * Successful exploitation of query string parameter vulnerabilities could lead an attacker to impersonate a legitimate user, obtain proprietary data, know about the internals of the application or simply perform actions not intended by the application developers.

## Preventive measures that can be adopted

* Notice that simply using HTTPS does not resolve this vulnerability.
* All sensitive data should be sent to the server in the HTTP message body or headers.
* Applying some form of encryption to the sensitive data before it's transmitted in the URL could be an alternative in certain contexts. However, it can add unnecessary latency and complexity to the application.
  * Expressing some data in the target URI is inefficient, because it needs to be encoded to be a valid URI.
  * Furthermore, this practice is subject to max-length restrictions on URIs.

### Use of headers

* When passing information through headers, the creation of customized headers that are not defined by the [HTTP specifications][1] should be avoided as much as possible.
  * Instead, whenever possible, use the predefined headers, i.e., use the `Authorization` header to send credential tokens to authenticate users against a server.
* Be aware that Web Application Firewalls (WAFs) can remove response header fields. Some may remove everything that isn't mentioned in the HTTP specifications.

### Use of body

#### HTTP GET

* An `HTTP GET` request shouldn't be sent with a body according to the [HTTP specifications][1]. Consequently:
  * A payload body on a `GET` request might cause some existing implementations to reject the request. As example, Spring Boot throws `HttpMessageNotReadableException` when a body is passed and the `Fetch API` throws also an error in such scenario.
  * Others implementations may just ignore `GET` request bodies when handling the request.
  * Potential intermediaries, like load balancers or caching proxies, may remove `GET` request bodies for performance reasons.
  * Since a `GET` request is cacheable and a cache may use it to satisfy subsequent `GET` requests, this circumstance can create inconsistencies because proxies will not read the request body.

#### HTTP POST

* An `HTTP POST` request shouldn't be used to retrieve data because `POST` requests are widely considered as a method of creating resources. **However, it is often the most common implemented approach**, although:
  * It's semantically incorrect, particularly in REST conventions.
  * Imposes restrictions on caching.
* A typical use of `HTTP POST` for requesting a simple search would be:

  ```http
  POST /search HTTP/1.1
  Host: example.tbl
  Content-Type: application/x-www-form-urlencoded

  q=foo&limit=10&sort=-published
  ```

* Conventionally, the adoption of the `POST` method over `GET` is not solely based on the need to send sensitive information.
* Some requests require sending complex filters, multiple search criteria, or deeply structured data that can exceed URL length limits.
  * Browsers, servers, and proxies impose restrictions on URL length, which can cause `GET` requests to be truncated or rejected.
* Using `POST` allows sending data in the request body, avoiding these limitations and ensuring the full dataset is processed.

#### HTTP QUERY

* `HTTP QUERY` was drafted at the [IETF standard][2] as a means of making a safe, cacheable, idempotent request that contains content.
* According to the specification, the `QUERY` method is used to ask the server to perform a query operation over some set of data scoped to the effective request URI. The body payload of the request defines the query.
* It states that implementations may use a request body of any content type, although the example provided is:

  ```http
  QUERY /contacts HTTP/1.1
  Host: example.org
  Content-Type: example/query
  Accept: text/csv

  select surname, givenname, email limit 10
  ```

  With this corresponding response:

  ```http
  HTTP/1.1 200 OK
  Content-Type: text/csv

  surname, givenname, email
  Smith, John, john.smith@example.org
  Jones, Sally, sally.jones@example.com
  Dubois, Camille, camille.dubois@example.net
  ```

[1]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Resources_and_specifications
[2]: https://www.ietf.org/archive/id/draft-ietf-httpbis-safe-method-w-body-02.html
