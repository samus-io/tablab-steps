# Referrer-Policy header basics

* The `Referrer-Policy` response header helps control what gets shared in the Referer header when a browser makes a request.
* Without restrictions, the `Referer` header can include full URLs that may contain sensitive information like tokens or user identifiers
* This header allows websites to define rules that limit or remove parts of the referring URL before it is sent.
* Different values, known as directives, can be set to adjust how much information is included in the `Referer` header.
* These directives help reduce the risk of leaking sensitive data to external domains during navigation or resource loading.

## Directives

* The following table defines the different directives of the `Referrer-Policy` header:
  |Directive|Description|Referer header result|
  |:--:|:--:|:--:|
  |`no-referrer`|Completely removes the `Referer` header from all requests, preventing any referrer data from being shared.|No `Referer` header is sent.|
  |`no-referrer-when-downgrade`|Sends the full URL in the Referer header for HTTPS to HTTPS requests, but omits it when navigating from HTTPS to HTTP. This is the default behavior in many browsers but is not recommended for secure setups.|`https://domain.tbl/user?name=User`|
  |`origin`|The `Referer` header contains only the origin from which the request originated.|`https://domain.tbl/user/`|
  |`origin-when-cross-origin`|Sends the full URL for same-origin requests and only the origin for cross-origin requests.|`https://domain.tbl`|
  |`same-origin`|Sends the full URL in the Referer header only for same-origin requests. Nothing is sent for cross-origin requests.|No `Referer` header is sent.|
  |`strict-origin`|Sends only the origin in the `Referer` header if the security protocol is the same (`HTTP` to `HTTP` or `HTTPS` to `HTTPS`), otherwise the header is not sent.|`https://domain.tbl`|
  |`strict-origin-when-cross-origin`|Sends the full URL for same-origin requests. For cross-origin requests, sends only the origin if the protocol is the same. No header is sent if downgrading from HTTPS to HTTP.|`https://domain.tbl`|
  |`unsafe-url`|Always sends the full URL in the Referer header, including path and query parameters. This directive is not recommended due to the risk of exposing sensitive data.|`https://domain.tbl/user?name=johndoe`|

## Referrer-Policy header recommendations

* Web analytics tools like Google Analytics rely on the `Referer` header to track which pages users visit. The chosen `Referrer-Policy` directive can impact how much information is shared with these services.
* If a data analytics service is being used, it is recommended to use the `same-origin`, `origin-when-cross-origin` or `strict-origin-when-cross-origin` directives to avoid errors in its operation.
* If no analytics or tracking services are in use, more restrictive directives are preferred to enhance privacy and reduce data exposure like `strict-origin`, `origin` and `no-referrer`.
