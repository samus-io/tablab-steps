# Referer header overview

* The `Referer` response header is automatically included by the browser in HTTP requests and shows the URL of the page that initiated the request.
* To better understand this header, consider the following example:
  * The web application `https://domain.tbl` has a link that points to the URL `https://example.tbl`.
  * When a user requests this link, the request includes the `Referer` header with the value `https://domain.tbl`.
* This behavior can unintentionally expose sensitive information when the referring URL contains data such as tokens or session identifiers.
* A critical case could happen if a request originates from a URL like `https://domain.tbl/resetPassword/<token>`, which includes a password reset token.
* In such cases, the Referer header would expose the full URL, including the token, to the destination site `https://example.tbl`.
* If the external site is controlled by an attacker, the token could be stored in logs and misused to perform account takeover.
* To limit this kind of information leakage, the `Referrer-Policy` response header can be used to control what information is sent in the `Referer` header.
* Implementing a strict `Referrer-Policy` helps protect sensitive data by reducing or blocking the Referer value entirely in cross-origin requests
