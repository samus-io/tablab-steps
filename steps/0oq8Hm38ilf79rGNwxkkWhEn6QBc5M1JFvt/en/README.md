# What is Cross-Origin Resource Sharing (CORS)?

* `Cross-Origin Resource Sharing (CORS)` is a mechanism to bypass the `Same-Origin Policy (SOP)` restrictions and enable secure data sharing between different origins.

	> :older_man: The `Same-Origin Policy (SOP)` is a fundamental security feature in web browsers designed to prevent malicious websites from accessing or modifying content belonging to a different origin. Although SOP plays a crucial role in web security, it can be very restrictive when different origins need to interact.

* CORS is an HTTP-header based mechanism that enables servers to declare which external origins may access their resources.
	* Browsers implementing CORS usually also dispatch a "preflight" request to the relevant server, confirming whether it allows the forthcoming cross-origin request. This request transmits headers specifying the HTTP method and other headers to be used later in the actual intended request.
	
	> :older_man: A preflight request is an HTTP OPTIONS request that a browser automatically sends before making a cross-origin request in certain conditions. It is part of the CORS mechanism and is used to determine whether the actual request is allowed by the target server.

* In web development, CORS is commonly applied when an API resides on a different origin than the web UI application, supplying crucial data for its functionality. This setup requires JavaScript to access API responses, and proper CORS headers enable the browser to grant that access, bypassing the SOP.

## Defined CORS headers

* CORS defines a series of headers that regulate cross-origin requests, ensuring that resources can be shared securely between different origins while maintaining security constraints.

### HTTP response headers

* Servers use specific HTTP response headers to indicate how their resources can be accessed by other origins. These headers are part of the CORS mechanism and are often involved in preflight requests.

	|Header|Description|Example|
	|:--:|:--:|:--:|
	|`Access-Control-Allow-Origin`|Specifies which origins are permitted to access the server's resources. If set to `*`, any origin is allowed, while a specific domain restricts access to that domain.|`Access-Control-Allow-Origin: https://domain.tbl`|
	|`Access-Control-Allow-Credentials`|Indicates whether the final request can include user credentials (such as cookies, HTTP authentication, or client-side SSL certificates). If omitted, the default value is `false`, meaning credentials are not allowed.|`Access-Control-Allow-Credentials: true`|
	|`Access-Control-Allow-Methods`|Defines the HTTP methods allowed for cross-origin requests. If not specified, only `GET` and `HEAD` methods are allowed by default.|`Access-Control-Allow-Methods: POST, GET, OPTIONS, DELETE`|
	|`Access-Control-Allow-Headers`|Lists the additional HTTP headers that can be sent in a request from another origin. This is useful for allowing non-standard headers required by the client.|`Access-Control-Allow-Headers: Front-End-Https`|
	|`Access-Control-Max-Age`|Sets the duration (in seconds) for which the results of a preflight request can be cached by the browser, reducing unnecessary repeated requests.|`Access-Control-Max-Age: 3600`|
	|`Access-Control-Expose-Headers`|Specifies which response headers can be made accessible to the client from a different origin. By default, only a limited set of headers are exposed, but additional headers can be included using this directive, adding them to the allowlist that JavaScript in browsers is permitted to access.|`Access-Control-Expose-Headers: Content-Encoding`|

### HTTP request headers

* These HTTP headers are utilized by clients when making HTTP requests for cross-origin sharing. They are automatically set by the browser during server interactions, meaning developers don't need to specify them programmatically.

	|Header|Description|Example|
	|:--:|:--:|:--:|
	|`Origin`|Determines from which origin the request has been made. This allows the server to determine whether it should permit access based on cross-origin rules.|`Origin: https://domain.tbl`|
	|`Access-Control-Request-Method`|Used in preflight requests  to inform the server of the HTTP method the actual request intends to use.|`Access-Control-Request-Method: POST`|
	|`Access-Control-Request-Header`|Sent during a preflight request to notify the server of any custom headers that the actual request will include. This ensures the server is aware of all headers before permitting the request.|`Access-Control-Request-Headers: Front-End-Https`|
