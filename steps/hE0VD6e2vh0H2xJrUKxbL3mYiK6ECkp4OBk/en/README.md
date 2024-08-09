# HTTP response codes

* HTTP response codes are the three digit status codes issued by a server in response to a client's request made to the server.
* These codes indicate whether a specific HTTP request has been successfully completed.
* They are categorized into five classes based on their first digit and the other two digits indicate the specific response.

## Importance of using HTTP response codes

* **Communication clarity**: HTTP response codes provide a clear and standardized way for servers to communicate the result of a client's request, ensuring both client and server understand the outcome.

* **Troubleshooting**: these codes help in diagnosing issues by indicating whether problems are originated from the client, server, or network.

* **Security**: response codes can help in identifying and mitigating potential security issues by signaling unauthorized access attempts or server errors.

* **Automation**: automated systems and applications rely on HTTP response codes to determine next steps in processes, such as retries or logging errors.

* **SEO**: search engines use response codes to index pages correctly, where codes like `200` and `301` play a significant role in search engine optimization.

## Categories of HTTP response codes

* HTTP response codes (or HTTP status codes) are grouped into five distinct categories, each serving a unique function.

### 1xx – Informational codes

* These codes indicate that the request has been received and is being processed. They indicate the progress of the request and send the information in the form of headers.

#### 100 Continue

* This temporary response signals that the client should proceed with the request or disregard the response if the request is already complete.

* For example, a client is sending a large file upload to the server. It first sends the initial headers to check if the server is willing to accept the request:

```http
POST /upload HTTP/1.1
Host: domain.tbl
Content-Length: 348789
Expect: 100-continue
```

* If the server is ready to accept the data, it responds with:

```http
HTTP/1.1 100 continue
```

* The server's `100 Continue` response informs the client that it should proceed with sending the body of the request. This ensures that the client doesn't send large amounts of data if the server is going to reject the request based on the headers alone.
  
#### 101 Switching Protocols

* Issued in response to an upgrade request header from the client, this code indicates the new protocol the server is transitioning to.
* For example, a client requests to switch from HTTP to the WebSocket protocol:

```http
GET /chat HTTP/1.1
Host: domain.tbl
Upgrade: websocket
Connection: Upgrade
```

* The server agrees and responds with:

```http
HTTP/1.1 101 switching protocols
Upgrade: websocket
Connection: Upgrade
```

* The server's `101 Switching Protocols` response indicates that it is switching to the protocol specified in the upgrade header sent by the client. In this case, switching to the WebSocket protocol allows for real-time, full-duplex communication.
  
#### 102 Processing (WebDAV)

* This status code signifies that the server has received and is handling the request, but has not yet provided a response.
* For example, a client makes a WebDAV (Web distributed authoring and versioning) request to copy a large collection of resources:

```http
COPY /collection/ HTTP/1.1
Host: domain.tbl
Destination: /newCollection
```

* The server, acknowledging the time required for the operation, responds with:

```Text
HTTP/1.1 102 processing
```

* The `102 Processing` response informs the client that the request is being processed, but no final response is available yet. This is particularly useful for lengthy operations to prevent the client from timing out.
* WebDav is a collection of HTTP extensions that allows to perform operations directly on web server from client. This ensures that the plaform is not only readable but also can be collaboratively operated from multiple clients.

#### 103 Early Hints

* Mainly used with the link header, this code allows the user agent to begin preloading resources or establish connections to an origin from which the page will require resources while the server is preparing a full response.
* For example, a client requests a webpage that includes several large resources.

```http
GET /index.html HTTP/1.1
Host: domain.tbl
```

* The server, preparing to send the full response, first sends:

```http
HTTP/1.1 103 early hints
Link: </style.css>; rel=preload; as=style
Link: </script.js>; rel=preload; as=script
```

* The `103 Early Hints` response allows the client to start preloading resources (like CSS and JavaScript files) while the server prepares the final response. This improves page load times and enhances the user experience by utilizing the time before the final response is ready.

### 2xx – Successful codes

* These codes signify that the request has been successfully received, understood, and accepted.

#### 200 OK

* It indicates that the request was successful. The meaning of success depends on the HTTP method used:
  * **GET**: the requested resource has been retrieved and is included in the response body.
  * **HEAD**: the response includes headers without a message body.
  * **PUT or POST**: the response contains a representation of the result of the action.
  * **TRACE**: the response body contains the request message as received by the server.
* For example, a client requests a webpage using a `GET` method:

```http
GET /index.html HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1234
```

### 201 Created

* It indicates that the request was successful, and a new resource was created as a result. This is typically used in response to `POST` or some `PUT` requests.
* For example, a client submits a new user registration via `POST` in JSON format:

```http
POST /users HTTP/1.1
Content-Type: application/json

{
  "username": "newUser",
  "password": "password123"
}
```

* The server responds with:

```http
HTTP/1.1 201 Created
Location: /users/newUser
```

### 202 Accepted

* It indicates that the request has been received but not yet processed. It is typically used for actions that take time or are handled by another server or process.
* For example, a client submits a request to process a large dataset:

```http
POST /processData HTTP/1.1
Content-Type: application/json

{
  "dataId": "12345"
}
```

* The server responds with:

```http
HTTP/1.1 202 Accepted
```

### 203 Non-Authoritative Information

* It indicates that the request was successful, but the returned metadata is from a copy, not the original server. This is used for mirrors or backups.
* For example, a client requests a resource from a mirror server:

```http
GET /mirroredResource HTTP/1.1
```

* The mirror server responds with:

```http
HTTP/1.1 203 Non-Authoritative Information
Content-Type: text/html
Content-Length: 1234
```

### 204 No Content

* It indicates that the request was successful, but there is no content to return. The headers may still be useful for updating cached information.
* For example, a client deletes a user account:

```http
DELETE /users/123 HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 204 No Content
```

### 205 Reset Content

* It indicates that the server successfully processed the request, and the user agent should reset the document view that sent the request.
* For example, a client submits a form and needs to clear it afterwards:

```http
POST /submitForm HTTP/1.1
Content-Type: application/x-www-form-urlencoded

name=John&email=john@domain.tbl
```

* The server responds with:

```http
HTTP/1.1 205 Reset Content
```

### 206 Partial Content

* It indicates that the server is delivering only part of the resource due to a `Range` header sent by the client.
* For example, a client requests a portion of a large file:

```http
GET /largeFile.zip HTTP/1.1
Range: bytes=0-999
```

* The server responds with:

```http
HTTP/1.1 206 Partial Content
Content-Range: bytes 0-999/12345
Content-Length: 1000
```

### 3xx – Redirection codes

* These codes inform the client that further action is needed to complete the request, typically involving redirection.

#### 300 Multiple Choices

* It indicates that the request has more than one possible response. The user agent or user should choose one. HTML links to the options are recommended to help the user pick.
* For example, a client requests a file from a server, and the server responds with different versions of the file, such as `version1.pdf` and `version2.pdf`.

  ```http
  GET /files HTTP/1.1
  Host: domain.tbl
  ```

* The response might include links to these versions for the client to select:

```http
  HTTP/1.1 300 Multiple Choices
  Content-Type: text/html
  Content-Length: 123

  <html>
  <body>
    <p>Please choose a version:</p>
    <ul>
      <li><a href="/files/version1.pdf">Version 1</a></li>
      <li><a href="/files/version2.pdf">Version 2</a></li>
    </ul>
  </body>
  </html>
```

#### 301 Moved Permanently

* It indicates that the requested resource's URL has permanently changed. The new URL is provided in the response.

* For example, a user requests `http://domain.tbl/oldPage`:

```http
GET /oldPage HTTP/1.1
Host: domain.tbl
```

* The server responds with a new URL for the requested content:  

```http
HTTP/1.1 301 Moved Permanently
Location: http://domain.tbl/newPage
Content-Length: 0
```

#### 302 Found

* It indicates that the requested resource's URI has temporarily changed. The same URI should be used for future requests.
* For example, a user requests `http://domain.tbl/temporary`:

```http
GET /temporary HTTP/1.1
Host: domain.tbl
```

* The server temporarily redirects them to `http://domain.tbl/temporaryLocation`. The client should continue using the original URI for future requests:

```http
HTTP/1.1 302 Found
Location: http://domain.tbl/temporaryLocation
Content-Length: 0
```

#### 303 See Other

* It indicates that the client should retrieve the requested resource from a different URI using a `GET` request.

* For example, after submitting a form to `http://domain.tbl/submitForm`:

  ```http
  POST /submitForm HTTP/1.1
  Host: domain.tbl
  Content-Type: application/x-www-form-urlencoded
  ```

* The server responds with a URL to view the result at `http://domain.tbl/result`:

  ```http
  HTTP/1.1 303 See Other
  Location: http://domain.tbl/result
  Content-Length: 0
  ```

#### 304 Not Modified

* It indicates that the response has not been modified since the last request. The client should continue using the cached version.

* A client requests `http://domain.tbl/image.png` with a `If-Modified-Since` header:

  ```http
  GET /image.png HTTP/1.1
  Host: domain.tbl
  If-Modified-Since: Wed, 21 Aug 2024 07:00:00 GMT
  ```

* The server responds with `304 Not Modified` because the image has not changed:

  ```http
  HTTP/1.1 304 Not Modified
  Content-Length: 0
  ```

* The server sends `200` along with new body if the content is modified after `If-Modified-Since` else it sends `304` with no body but with `Last-Modified` response header indicating when it was lastly modified.  

#### 307 Temporary Redirect

* It indicates that the client should access the requested resource at another URI using the same HTTP method as in the previous request.

* A client performs a `POST` request to `http://domain.tbl/data`:

  ```http
  POST /data HTTP/1.1
  Host: domain.tbl
  Content-Type: application/x-www-form-urlencoded
  ```

* And is redirected to `http://domain.tbl/newData` with another `POST` request:

  ```http
  HTTP/1.1 307 Temporary Redirect
  Location: http://domain.tbl/newData
  Content-Length: 0
  ```

#### 308 Permanent Redirect

* It indicates that the resource is permanently located at a different URI, specified in the `Location` header. The client must use the same HTTP method for the new request.

* A client sends a `POST` request to `http://domain.tbl/submit`:

  ```http
  POST /submit HTTP/1.1
  Host: domain.tbl
  Content-Type: application/x-www-form-urlencoded
  ```

* And is redirected to `http://domain.tbl/newSubmit`, where the client should also use `POST`:

  ```http
  HTTP/1.1 308 Permanent Redirect
  Location: http://domain.tbl/newSubmit
  Content-Length: 0
  ```

* `307` is similar to `302` and `308` is similar to `301` but `307` and `308` also preserve the original request method.

### 4xx – Client error codes

* These codes denote issues with the request made by the client (browser), such as bad syntax or unauthorized access.

#### 400 Bad Request

* Indicates that the server cannot or will not process the request due to client-side errors. Examples include malformed request syntax or invalid request message framing.
* For example, a client sends an HTTP request with an invalid JSON body:

```http
POST /api/data HTTP/1.1
Content-Type: application/json

{
  "name": "John Doe",
  "age": "twenty-five"
}
```

* The server responds with:

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": "Invalid data format for 'age'."
}
```

#### 401 Unauthorized

* Indicates that authentication is required to access the requested resource. It signifies that the client must authenticate to obtain a response.
* For example, a client tries to access a protected API endpoint without proper authentication:

```http
GET /api/protectedData HTTP/1.1
Authorization: Bearer
```

* The server responds with:

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error": "Authentication required."
}
```

#### 403 Forbidden

* Indicates that the client does not have permission to access the requested resource. The client’s identity is known, but access is denied.
* For example, a user attempts to access an admin dashboard without the required permissions:

```http
GET /admin/dashboard HTTP/1.1
Authorization: Bearer <valid-token>
```

* The server responds with:

```http
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "error": "Access denied."
}
```

* The `Authorization` header is used to send any kind of credentials to the server with different standard methods like `Bearer`.

#### 404 Not Found

* Indicates that the server cannot find the requested resource. This can mean the URL is not recognized or the resource does not exist.
* For example, a client requests a non-existent resource:

```http
GET /api/nonexistentResource HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": "Resource not found."
}
```

#### 405 Method Not Allowed

* Indicates that the request method is known but not supported by the target resource. Commonly used when the method is not allowed for the requested resource.
* For example, a client tries to `DELETE` a resource that only supports `GET` requests:

```http
DELETE /api/resource HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 405 Method Not Allowed
Content-Type: application/json

{
  "error": "DELETE method is not allowed for this resource."
}
```

#### 406 Not Acceptable

* Indicates that the server cannot generate content that matches the criteria given by the client. Used when content negotiation fails.
* For example, a client requests a resource with an unsupported media type:

```http
GET /api/data HTTP/1.1
Accept: application/xml
```

* The server responds with:

```http
HTTP/1.1 406 Not Acceptable
Content-Type: application/json

{
  "error": "Requested media type not acceptable."
}
```

#### 407 Proxy Authentication Required

* Similar to `401 Unauthorized`, but authentication is needed by a proxy server. The client must authenticate with the proxy.
* For example, a client requests a resource through a proxy without proper proxy authentication:

```http
GET /api/data HTTP/1.1
Proxy-Authorization: Basic <credentials>
```

* The server responds with:

```http
HTTP/1.1 407 Proxy Authentication Required
Content-Type: application/json

{
  "error": "Proxy authentication required."
}
```

* `Proxy-Authorization` is similar to `Authorization` but only for proxy authentication.

#### 408 Request Timeout

* Indicates that the server timed out waiting for the request. Often used when a connection remains idle.
* For example, a client does not send the full request within the server's timeout period:

```http
GET /api/data HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 408 Request Timeout
Content-Type: application/json

{
  "error": "Request timeout."
}
```

#### 409 Conflict

* Indicates that the request conflicts with the current state of the server. Often used for scenarios where there is a conflict in resource state.
* For example, a client attempts to create a resource that already exists:

```http
POST /api/users HTTP/1.1
Content-Type: application/json

{
  "username": "john_doe"
}
```

* The server responds with:

```http
HTTP/1.1 409 Conflict
Content-Type: application/json

{
  "error": "Username already exists."
}
```

#### 410 Gone

* Indicates that the requested resource is no longer available and will not be available again. Clients should remove their references to the resource.
* For example, a client requests a deleted product:

```http
GET /api/products/123 HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 410 Gone
Content-Type: application/json

{
  "error": "Product has been permanently removed."
}
```

#### 411 Length Required

* Indicates that the server requires the `Content-Length` header in the request. This header is necessary for processing the request.
* For example, a client sends a `POST` request without a `Content-Length` header:

```http
POST /api/data HTTP/1.1
Content-Type: application/json
```

* The server responds with:

```http
HTTP/1.1 411 Length Required
Content-Type: application/json

{
  "error": "Content-Length header required."
}
```

#### 412 Precondition Failed

* Indicates that a precondition specified in the request headers is not met. Used when conditional headers are not satisfied.
* For example, a client’s request includes a condition that fails:

```http
PUT /api/resource HTTP/1.1
If-Match: "etag123"
```

* The server responds with:

```http
HTTP/1.1 412 Precondition Failed
Content-Type: application/json

{
  "error": "Precondition failed."
}
```

* This code is sent to the client with conditional requests on methods other than `GET` or `HEAD` when the condition defined by the `If-Unmodified-Since` or `If-Match` headers is not fulfilled. Meaning that the request (usually an upload or a modification of a resource) cannot be made because the document has been edited in-between and a `412 Precondition Failed` error is thrown.

#### 413 Content Too Large

* Indicates that the request payload is larger than the server can process. The server may close the connection or return a `Retry-After` header.
* For example, a client sends a large file that exceeds server limits with `<input type="file">` HTML element:

```http
POST /api/upload HTTP/1.1
Content-Type:  multipart/form-data; boundary=----Boundary
Content-Length: 5000000

------Boundary
Content-Disposition: form-data; name="file"; filename="image.jpg"
Content-Type: image/jpeg

(large binary data)
------Boundary--
```

* The server responds with:

```http
HTTP/1.1 413 Content Too Large
Content-Type: application/json

{
  "error": "Content too large."
}
```

#### 414 URI Too Long

* Indicates that the URI requested by the client is too long for the server to process. Often used with `GET` requests that include long query strings.
* For example, a client sends a `GET` request with an excessively long URI:

```http
GET /api/search?query=<very-long-query> HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 414 URI Too Long
Content-Type: application/json

{
  "error": "URI too long."
}
```

#### 415 Unsupported Media Type

* Indicates that the media format of the request data is not supported by the server. Used when the server cannot process the media type of the request.
* For example, a client sends a request with an unsupported media type:

```http
POST /api/data HTTP/1.1
Content-Type: application/unknown

<data>
```

* The server responds with:

```http
HTTP/1.1 415 Unsupported Media Type
Content-Type: application/json

{
  "error": "Unsupported media type."
}
```

#### 416 Range Not Satisfiable

* Indicates that the range specified in the `Range` header cannot be fulfilled. Used when the requested range is outside the bounds of the resource.
* For example, a client requests a byte range outside the file size:

```http
GET /api/file HTTP/1.1
Range: bytes=1000-2000
```

* The server responds with:

```http
HTTP/1.1 416 Range Not Satisfiable
Content-Type: application/json

{
  "error": "Requested range not satisfiable."
}
```

#### 417 Expectation Failed

* Indicates that the server cannot meet the expectations specified in the `Expect` header. Used when the server cannot fulfill the `Expect` request header field.
* For example, a client includes an `Expect` header that the server cannot handle:

```http
POST /api/upload HTTP/1.1
Expect: 100-continue
Content-Type: application/json
Content-Length: 1000

<large payload>
```

* The server responds with:

```http
HTTP/1.1 417 Expectation Failed
Content-Type: application/json

{
  "error": "Expectation failed."
}
```

#### 421 Misdirected Request

* Indicates that the request was directed at a server that cannot produce a response. Often used when the server is not configured for the requested URI scheme and authority.
* For example, a request is sent to a server not configured to handle the URI:

```http
GET /api/resource HTTP/1.1
Host: attacker.tbl
```

* The server responds with:

```http
HTTP/1.1 421 Misdirected Request
Content-Type: application/json

{
  "error": "Request misdirected."
}
```

#### 422 Unprocessable Content (WebDAV)

* Indicates that the request was well-formed but contains semantic errors that prevent processing. Used in WebDAV for semantic issues with the request.
* For example, a client submits a resource with invalid data:

```http
POST /api/resource HTTP/1.1
Content-Type: application/json

{
  "name": ""
}
```

* The server responds with:

```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "error": "Name cannot be empty."
}
```

#### 423 Locked (WebDAV)

* Indicates that the resource being accessed is locked. Used in WebDAV when a resource is locked by another process or user.
* For example, a client tries to modify a locked resource:

```http
PUT /api/resource HTTP/1.1
Content-Type: application/json

{
  "name": "New Name"
}
```

* The server responds with:

```http
HTTP/1.1 423 Locked
Content-Type: application/json

{
  "error": "Resource is locked."
}
```

#### 424 Failed Dependency (WebDAV)

* Indicates that a request failed due to the failure of a previous request. Used in WebDAV when a dependent request fails.
* For example, a client tries to update a resource that depends on another failed update:

```http
POST /api/resource HTTP/1.1
Content-Type: application/json

{
  "dependency": "failed"
}
```

* The server responds with:

```http
HTTP/1.1 424 Failed Dependency
Content-Type: application/json

{
  "error": "Previous request failed."
}
```

#### 426 Upgrade Required

* Indicates that the server refuses to process the request using the current protocol. The client must upgrade to a different protocol.
* For example, a client requests an HTTPS resource over HTTP:

```http
GET /api/data HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 426 Upgrade Required
Content-Type: application/json

{
  "error": "Upgrade to HTTPS required."
}
```

#### 428 Precondition Required

* Indicates that the server requires the request to be conditional. Used to prevent lost update problems in resource updates.
* For example, a client tries to modify a resource without conditional headers like `If-match`:

```http
PUT /api/resource HTTP/1.1
Content-Type: application/json

{
  "name": "Updated Name"
}
```

* The server responds with:

```http
HTTP/1.1 428 Precondition Required
Content-Type: application/json

{
  "error": "Request must be conditional."
}
```

#### 429 Too Many Requests

* Indicates that the client has sent too many requests in a given time period. Used for rate limiting.
* For example, a client exceeds the rate limit for API requests:

```http
GET /api/data HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json

{
  "error": "Too many requests. Please try again later."
}
```

#### 431 Request Header Fields Too Large

* Indicates that the server is unwilling to process the request due to its header fields being too large. The request may need to be resubmitted with smaller headers.
* For example, a client sends a request with excessively large headers:

```http
GET /api/data HTTP/1.1
X-Custom-Header: <very-large-value>
```

* The server responds with:

```http
HTTP/1.1 431 Request Header Fields Too Large
Content-Type: application/json

{
  "error": "Request header fields too large."
}
```

#### 451 Unavailable For Legal Reasons

* Indicates that the requested resource cannot be provided due to legal reasons. This may include content censored by a government.
* For example, a client requests a page blocked due to legal restrictions:

```http
GET /api/legal-blocked HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 451 Unavailable For Legal Reasons
Content-Type: application/json

{
  "error": "Resource unavailable due to legal reasons."
}
```

### 5xx – Server error codes

* These codes indicate problems on the server side that prevent it from providing a valid response.

#### 500 Internal Server Error

* Indicates that the server encountered an unexpected condition that prevented it from fulfilling the request. A general error message for server-side issues.
* For example, a server encounters an unhandled exception:

```http
GET /api/data HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "error": "Internal server error."
}
```

* This is the most commonly used response code even if there are multiple codes available for different type of errors in server.

#### 501 Not Implemented

* Indicates that the server does not support the functionality required to fulfill the request. The request method is not supported.
* For example, a client uses an unsupported HTTP method:

```http
PATCH /api/resource HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 501 Not Implemented
Content-Type: application/json

{
  "error": "Method not implemented."
}
```

#### 502 Bad Gateway

* Indicates that the server, while acting as a gateway or proxy, received an invalid response from an upstream server. Used when the server cannot get a valid response.
* For example, a proxy server receives a bad response from an upstream server:

```http
GET /api/data HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 502 Bad Gateway
Content-Type: application/json

{
  "error": "Bad gateway response."
}
```

#### 503 Service Unavailable

* Indicates that the server is currently unable to handle the request due to temporary overloading or maintenance. Used for temporary conditions.
* For example, a server is down for maintenance:

```http
GET /api/data HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 503 Service Unavailable
Content-Type: application/json

{
  "error": "Service unavailable. Please try again later."
}
```

#### 504 Gateway Timeout

* Indicates that the server, while acting as a gateway or proxy, did not receive a timely response from an upstream server. Used when a response is delayed.
* For example, a proxy server times out waiting for a response:

```http
GET /api/data HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 504 Gateway Timeout
Content-Type: application/json

{
  "error": "Gateway timeout."
}
```

#### 505 HTTP Version Not Supported

* Indicates that the server does not support the HTTP protocol version used in the request. Used when an unsupported HTTP version is requested.
* For example, a client requests a resource using an outdated HTTP version 1.0:

```http
GET /api/data HTTP/1.0
```

* The server responds with:

```http
HTTP/1.1 505 HTTP Version Not Supported
Content-Type: application/json

{
  "error": "HTTP version not supported."
}
```

#### 506 Variant Also Negotiates

* Indicates an internal server error where the resource is configured to negotiate content itself, leading to an infinite negotiation loop. Used when content negotiation fails internally.
* For example, a resource incorrectly handles content negotiation:

```http
GET /api/data HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 506 Variant Also Negotiates
Content-Type: application/json

{
  "error": "Variant also negotiates."
}
```

#### 507 Insufficient Storage (WebDAV)

* Indicates that the server cannot store the representation needed to complete the request. Used in WebDAV for storage issues.
* For example, a client’s request exceeds available storage:

```http
POST /api/upload HTTP/1.1
Content-Type: application/octet-stream

<large payload>
```

* The server responds with:

```http
HTTP/1.1 507 Insufficient Storage
Content-Type: application/json

{
  "error": "Insufficient storage."
}
```

#### 508 Loop Detected (WebDAV)

* Indicates that the server detected an infinite loop while processing a request. Used in WebDAV when a request causes a loop.

* For example, a recursive request results in a loop:

```http
PROPFIND /api/resource HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 508 Loop Detected
Content-Type: application/json

{
  "error": "Loop detected."
}
```

* `PROPFIND` is a method used to fetch the properties stored in the form of XML from the server.

#### 510 Not Extended

* Indicates that further extensions to the request are required for the server to fulfill it. Used when additional information or extensions are needed.
* For example, a request requires additional parameters or headers:

```http
GET /api/resource HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 510 Not Extended
Content-Type: application/json

{
  "error": "Further extensions required."
}
```

#### 511 Network Authentication Required

* Indicates that the client needs to authenticate to gain network access. Used for network-level authentication.
* For example, a client needs to authenticate to access a network resource:

```http
GET /api/resource HTTP/1.1
```

* The server responds with:

```http
HTTP/1.1 511 Network Authentication Required
Content-Type: application/json

{
  "error": "Network authentication required."
}
```
