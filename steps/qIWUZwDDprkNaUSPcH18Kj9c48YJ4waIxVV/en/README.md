# Basic concepts of Cookies

* The Cookies (or HTTP Cookies) is a string of characters stored in the user's browser. Their main use is to identify a user and for the server to recognize when two requests come from the same browser.
* This is useful for the browser to maintain state between HTTP requests, as the HTTP protocol is defined as `stateless`, meaning that each request is independent of the others.
* Cookies are mainly used in the following cases:
  * Session handling:
    * They are used to determine whether a user is logged in to the `login` of a web application. This helps the server to identify which user made the HTTP request. They can also be used to save the shopping cart in an `e-commerce` application.
  * Customization:
    * In this case, the use of cookies is to customize the website, such as language, page theme (dark or light), and other user preferences.
  * Tracking:
    * Finally, tracking cookies are used to store and analyze user behavior through the website.

## Types of cookies

### Persistent Cookies

* Persistent cookies have an expiration date set by the server in the cookie attributes. They are primarily used to maintain the user's session, personalize the web application or track users.

### Session Cookies

* Session cookies, unlike persistent cookies, do not have an expiration date. They are stored in memory and deleted when the session ends. Each browser defines the end of the session differently; some determine that the session ends when the browser is closed, while other browsers use other criteria to determine when the session ends.
* They are typically used to store the shopping cart in `e-commerce` or for user tracking.

> :warning: Many browsers have a feature that resets all windows the next time the browser is started. In this case, session cookies will also be reset, acting as if the browser had never been closed. For this reason, these cookies may pose a security risk, as they may be stored indefinitely.

## HTTP Set-Cookie Header

* The `Set-Cookie` response header is responsible for setting cookies in the user's browser, so that on subsequent requests the user can send the `Cookie` header with the cookies set by the server. Each Set-Cookie header can only contain one Cookie, so if the server wants to send multiple cookies, it must send multiple Set-Cookie headers.
* This header, in addition to sending the Cookie, also has attributes that can be defined to define its behavior, such as only being sent on `HTTPS` requests where the connection is encrypted.
* This is the most basic example of the header:

  ```
  Set-Cookie: <cookie-name>=<cookie-value>
  ```

## Cookie Format

* These are some of the most common attributes used in the `Set-Cookie` header:

  |Attribute|Description|
  |:--:|:--:|
  |Domain|The `Domain` attribute specifies the domain (or subdomain) to which the Cookie belongs.|
  |Expires|Sets the date when the Cookie will be removed from the browser. The format of the date is `<day-name>, <day> <month> <year> <hour>:<minute>:<second> GMT`. If the Cookie does not have this attribute, it becomes a session Cookie.|
  |Path|Specifies the web application path in which the Cookie must be sent.|
  |Max-Age|Define the time in seconds after which the cookie will be deleted from the browser. If `Max-Age` and `Expires` exist, `Max-Age` takes precedence.|

## Cookie limitations

* A cookie cannot be larger than 4096 bytes (the size is the sum of the cookie name, the value and its attributes).
* A domain cannot have more than 50 cookies.
* A browser cannot store more than 3000 cookies.
