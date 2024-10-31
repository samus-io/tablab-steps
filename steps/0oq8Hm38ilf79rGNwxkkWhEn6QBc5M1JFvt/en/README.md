# Cross-Origin Resource Sharing (CORS) basics

* While the `Same-Origin Policy (SOP)` is necessary and an important element of Web security, it is also very restrictive when two different origins need to communicate with each other.
* `Cross-Origin Resource Sharing (CORS)` is a mechanism that uses HTTP headers to bypass `SOP` and allow two different sources to interact.
* The most common use of `CORS` is in an API hosted in a different origin than the web application, where it returns information necessary for the correct functioning of the application, and the API responses need to be accessed by JavaScript. Then, by using these headers, it is possible to allow access to the response bypassing the `SOP`.

## Cross-Origin Resource Sharing (CORS) Headers

### Server-side headers

* These HTTP response headers are used by the server that wants to allow other origins to access and interact with the response. These are typically sent in `Preflight` requests.

|Header|Description|Example|
|:--:|:--:|:--:|
|`Access-Control-Allow-Origin`|It is used by the web application to determine which origins can access its response and interact with it.|Access-Control-Allow-Origin: `https://domain.tbl`|
|`Access-Control-Allow-Credentials`|Indicates whether the request can include the requesting user's credentials (cookies). If this header is omitted, the default value is `false`.|Access-Control-Allow-Credentials: true|
|`Access-Control-Allow-Methods`|Determines which methods are accepted by the server when a request is made from a different origin.|Access-Control-Allow-Methods: POST, GET, OPTIONS, DELETE|
|`Access-Control-Allow-Headers`|Determines which non-standard HTTP headers are accepted by the web application when a request is made from another origin.|Access-Control-Allow-Headers: Front-End-Https|
|`Access-Control-Max-Age`|Specifies how long in seconds the value of the `Access-Control-Allow-Methods` and `Access-Control-Allow-Headers` headers can be cached in the browser cache.|Access-Control-Max-Age: 3600|
|`Access-Control-Expose-Headers`|This header allows you to specify which response headers can be accessed from another origin. By default, only the `Cache-Control`, `Content-Language`, `Content-Length`, `Content-Type`, `Expires`, `Last-Modified` and `Pragma` headers can be accessed. This allows the headers specified in `Access-Control-Expose-Headers` to be accessed by JavaScript in requests to a different origin.|Access-Control-Expose-Headers: Content-Encoding|

### Client-side headers

* The following `HTTP` headers are sent by the client (the user) to send information about the request being made. They are usually sent in preflight requests.

|Header|Description|Example|
|:--:|:--:|:--:|
|`Origin`|Determines from which origin the request has been made.|Origin: `https://domain.tbl`|
|`Access-Control-Request-Method`|This header is sent in requests with the `OPTIONS` method to specify which method is used in the request.|Access-Control-Request-Method: POST|
|`Access-Control-Request-Header`|This header is sent in requests with the `OPTIONS` method to specify which non-standard HTTP headers are sent with the request.|Access-Control-Request-Headers: Front-End-Https|
