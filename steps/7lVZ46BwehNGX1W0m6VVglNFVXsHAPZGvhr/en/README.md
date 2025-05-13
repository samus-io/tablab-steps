# Referrer-Policy header overview

* Browsers include the `Referer` header when making requests, and without a `Referrer-Policy`, this may reveal entire URLs with potentially sensitive details like user identifiers or tokens.
* The `Referrer-Policy` header provides control over the `Referer` content by allowing the use of directives that define how much URL data is included. These directives serve to minimize the risk of sharing sensitive information with external domains during page navigation or asset loading.

  > :older_man: The header name `Referer` is a misspelling of the word "referrer", whereas the `Referrer-Policy` header uses the correct spelling.

## Directives

* The following table presents the different available directives supported by the `Referrer-Policy` header:

  |Directive|Description|`Referer` header result|
  |:--:|:--:|:--:|
  |`no-referrer`|The `Referer` header is **never sent**, regardless of request context.|No `Referer` header is sent.|
  |`no-referrer-when-downgrade`|The **full URL** is sent in the `Referer` header for **same-origin** and **HTTPS→HTTPS** requests, but **omitted** when navigating from **HTTPS to HTTP**.|Full URL, unless HTTPS→HTTP (then none).|
  |`origin`|Only the **origin** (scheme + host + port) is sent in the `Referer` header, excluding path and query string.|`https://domain.tbl`|
  |`origin-when-cross-origin`|Sends the **full URL** for **same-origin** requests and only the **origin** for **cross-origin** requests.|`https://domain.tbl` (cross-origin), full URL (same-origin)|
  |`same-origin`|Sends the **full URL** only for **same-origin** requests. Nothing is sent for **cross-origin** requests.|No `Referer` header (cross-origin), full URL (same-origin)|
  |`strict-origin`|Sends only the **origin** if the request is **not downgraded** (e.g., HTTPS→HTTPS). Omits the header when **downgrading from HTTPS to HTTP**.|`https://domain.tbl` (if not downgraded)|
  |`strict-origin-when-cross-origin`|Sends the **full URL** for **same-origin** requests. Sends only the **origin** for **cross-origin** requests with same protocol. Omits header when **downgrading**.|`https://domain.tbl` (cross-origin), full URL (same-origin), none if HTTPS→HTTP|
  |`unsafe-url`|Always sends the **full URL**, including path and query string, even across origins. **Not recommended** for security reasons.|`https://domain.tbl/user?name=johndoe`|

## Additional considerations

* Web analytics tools like Google Analytics rely on the `Referer` header to track which pages users visit. The chosen `Referrer-Policy` directive can impact how much information is shared with these services.
  * When using a data analytics service, it is advisable to set the directive to `same-origin`, `origin-when-cross-origin`, or `strict-origin-when-cross-origin` to prevent operational issues.
  * In the absence of analytics or tracking services, stricter directives such as `strict-origin`, `origin`, and `no-referrer` are preferred to improve privacy and limit data exposure.
