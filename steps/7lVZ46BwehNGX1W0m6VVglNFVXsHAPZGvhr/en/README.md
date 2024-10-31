# Referrer-Policy header basics

* To understand what the `Referrer-Policy` header is, you need to know what the `Referer` header is, because the `Referrer-Policy` header is responsible for setting the policy for that header.
* The `Referer` header is sent with HTTP requests and its value is the URL from which the request originated. To better understand this header, consider the following example:
  * The web application `https://domain.tbl` has a link pointing to the URL `https://example.tbl`.
  * When a user requests this link, the value of the `Referer` header is `https://domain.tbl`.
  * While this may not appear to have any security implications, it is possible that the `https://domain.tbl` web application could originate the request from the URL `https://domain.tbl/users/<user>`, where `<user>` is the user's name. This would send the user's name to the `https://example.tbl` page, causing an information leak.
* Although this example is not very serious from a security point of view, it is important to know what information is sent to other pages, because it could have a high impact in some cases.
* The `Referrer-Policy` header is used to control what information is sent to other pages with the `Referer` header. It is important to define this header well to avoid information leakage by sending routes or web application parameters.
* This header is made up of directives that are interpreted by the browser and the appropriate information is appended according to its directive. An example of the `Referrer-Policy` could be the following

  ```
  Referrer Policy: no-referrer
  ```
