# General best practices against XSS

* Input validation: only the characters needed to represent the input data should be accepted.
* Encode data on output: every time some user-supplied input is used on the web application output, it should be encoded. This might require applying combinations of HTML, URL, JavaScript, and CSS encoding.
* Implement cross-site scripting filters as a middleware (anti-XSS library).
* Use appropriate response headers: to prevent XSS in HTTP responses that aren't intended to contain any HTML or JavaScript, you can use the `Content-Type` and `X-Content-Type-Options` headers to ensure that browsers interpret the responses in the way you intend.
* Use the `Content Security Policy (CSP)` header.
