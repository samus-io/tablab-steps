# What is Cross-Origin Resource Sharing (CORS)?

* The `Same-Origin Policy (SOP)` is a web security feature that restricts how content from one origin can interact with content from another origin.
* While SOP is necessary and an important element of web security, it is also very restrictive when two different origins need to communicate with each other.
* `Cross-Origin Resource Sharing (CORS)` is a mechanism to bypass SOP restrictions and enable secure data sharing between different origins.
* CORS works by using special HTTP headers that let a server indicate which origins are allowed to access its resources.
* A common example of CORS is in an API hosted in a different origin than the web application, where it returns information necessary for the correct functioning of the application, and the API responses need to be accessed by JavaScript.
* Then, by using these headers, it is possible to allow access to the response bypassing the `SOP`.

## Cross-Origin Resource Sharing (CORS) headers

### Server-side headers

* Servers use specific HTTP response headers to control how their resources can be accessed by other origins.
* These headers are part of the CORS mechanism and are often involved in preflight requests, which are checks made by the browser before the actual request.

|Header|Description|Example|
|:--:|:--:|:--:|
|`Access-Control-Allow-Origin`|It is used by the web application to determine which origins can access its response and interact with it.|Access-Control-Allow-Origin: `https://domain.tbl`|
|`Access-Control-Allow-Credentials`|Indicates whether the request can include the requesting user's credentials (cookies). If this header is omitted, the default value is `false`.|Access-Control-Allow-Credentials: true|
|`Access-Control-Allow-Methods`|Lists the HTTP methods allowed for cross-origin requests.|Access-Control-Allow-Methods: POST, GET, OPTIONS, DELETE|
|`Access-Control-Allow-Headers`|Determines which non-standard HTTP headers are accepted by the web application when a request is made from another origin.|Access-Control-Allow-Headers: Front-End-Https|
|`Access-Control-Max-Age`|Specifies how long in seconds the value of the `Access-Control-Allow-Methods` and `Access-Control-Allow-Headers` headers can be cached in the browser cache.|Access-Control-Max-Age: 3600|
|`Access-Control-Expose-Headers`|This header allows you to specify which response headers can be accessed from another origin. By default, only the `Cache-Control`, `Content-Language`, `Content-Length`, `Content-Type`, `Expires`, `Last-Modified` and `Pragma` headers can be accessed. This allows the headers specified in `Access-Control-Expose-Headers` to be accessed by JavaScript in requests to a different origin.|Access-Control-Expose-Headers: Content-Encoding|

### Client-side headers

* The following `HTTP` headers are sent by the client (the user) to send information about the request being made.
* These headers are usually part of a preflight request, which is sent using the `OPTIONS` method before the actual request.

|Header|Description|Example|
|:--:|:--:|:--:|
|`Origin`|Determines from which origin the request has been made.|Origin: `https://domain.tbl`|
|`Access-Control-Request-Method`|This header is sent in requests with the `OPTIONS` method to specify which method is used in the request.|Access-Control-Request-Method: POST|
|`Access-Control-Request-Header`|Sent during a preflight request to list the custom headers the actual request will include.|Access-Control-Request-Headers: Front-End-Https|
