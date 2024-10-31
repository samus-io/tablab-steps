# X-Frame-Options header basics

* The `X-Frame-Options` response header is used to prevent other origins from creating an `iframe` of the web application.
* For example, if the web application `https://domain.tbl` creates an `iframe` of the page `https://example.tbl`, if it has the `X-Frame-Options` header configured, it would not be able to create the `iframe` because the user's browser would block it.
* This may not seem very important for security, but it is very useful to protect the application from vulnerabilities like `Clickjacking` or `Cross-Site Scripting (XSS)`.
* This header contains some directives that are interpreted by the browser, which is responsible for taking action on the directive sent with the header.
* An example of this header would be the following:

  ```
  X-Frame-Options: DENY
  ```
  
* Although this functionality is best implemented from within the `Content Security Policy`, it is considered good practice to use it as older browsers do not support the `Content Security Policy` header.

## Directives

* The `X-Frame-Options` header has only two directives:
  * The `DENY` directive, which prohibits creating a frame on any page.
  * The `SAMEORIGIN` directive, which only allows a frame to be created for the same origin.
* There is another directive called `ALLOW-FROM` which allows a frame to be created from the pages you specify, but this directive is considered deprecated. To specify which pages are allowed to create a frame, it is better to use the `frame-ancestors` directive of the `Content Security Policy`.

## Recommendations

* It is recommended that if the web application does not use the HTML `frame` tags, then the `DENY` directive is used, and if a `frame` created by the same web application is used, then the `SAMEORIGIN` directive must be used.
* If the web application requires a different origin to create a `frame`, then the `Content-Security Policy` must be used to specify the allowed origins.
* In the event that a web application has both the `X-Frame-Options` header and the `Content Security Policy` with the `frame-ancestors` directive, the `Content Security Policy` header will always take precedence, even if the `X-Frame-Options` header is more restrictive.
