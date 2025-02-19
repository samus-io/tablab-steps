# What is Same-Origin Policy (SOP)?

* The `Same-Origin Policy (SOP)` is a fundamental security feature in web browsers designed to prevent malicious websites from accessing or modifying content belonging to a different *origin*. It technically prevents JavaScript running on one origin from:
  * Interacting with *documents* from another origin, meaning it cannot directly manipulate or read the `Document Object Model (DOM)` of another page, including embedded iframes.
  * Reading responses of cross-origin requests, unless explicitly permitted by security mechanisms like `Cross-Origin Resource Sharing (CORS)`.

  ![Same-origin policy overview][1]

* Without the enforcement of the `Same-Origin Policy (SOP)`, visiting malicious websites could allow them to interact with or extract data from other loaded websites, which could result in reading personal emails, retrieving private messages, or performing other actions, particularly when the user is authenticated. By restricting interactions between different origins, browsers ensure the confidentiality and integrity of user data.

## What constitutes an *origin* in relation to SOP?

* An origin is determined by the combination of:
  * Protocol, also referred to as scheme (e.g., `http://`, `https://`).
  * Host, also referred to as domain (e.g., `example.tbl`, `sub.example.tbl`).
  * Port number (e.g., `443` for `HTTPS`, `80` for `HTTP`).
* Two URLs belong to the same origin only if all three components match exactly:

  | URL 1 | URL 2 | Same origin? | Reason |
  |----------|----------|-------------|--------|
  | `https://example.tbl` | `https://example.tbl` | ✅ Yes | All components match |
  | `https://example.tbl` | `http://example.tbl` | ❌ No | Protocol differs (`https` vs `http`) |
  | `https://example.tbl` | `https://sub.example.tbl` | ❌ No | Host differs (`example.tbl` vs `sub.example.tbl`) |
  | `https://example.tbl:443` | `https://example.tbl:8443` | ❌ No | Port differs (`443` vs `8443`) |
  | `https://example.tbl/profile/account` | `https://example.tbl/payment?id=123` | ✅ Yes | Query parameters do not affect the origin |

## Exceptions to SOP restrictions

* Certain resource types, such as images, stylesheets (CSS), scripts (JavaScript files), and media files (videos/audio), are not restricted by the `Same-Origin Policy (SOP)`. These resources are freely loaded by the browser from external origins without SOP enforcement, except for fonts, being a notable distinction.
  * Without this exceptions, displaying images or including JavaScript code from external origins would not be possible.
  * As example, `websiteA.tbl` can include a JavaScript file hosted on `websiteB.tbl`, and the JavaScript code from `websiteB.tbl` will run as expected within `websiteA.tbl`'s execution environment.

## What SOP actually restricts

* DOM access: JavaScript from one origin cannot access or manipulate the `Document Object Model (DOM)` of a page loaded from a different origin. This prevents attacks where one website attempts to steal or modify content from another loaded in the same browser session (e.g., in an iframe).
* Reading HTTP responses: although JavaScript can send cross-origin HTTP requests (e.g., via `fetch` or `XMLHttpRequest`), it cannot read the response unless the target server explicitly allows it via `Cross-Origin Resource Sharing (CORS)` headers.
  * Despite this restriction, the **browser still processes these cross-origin responses**, including managing `Set-Cookie` headers. This means that cookies may still be stored and authentication mechanisms may still function, even though JavaScript running in a different origin cannot access the response body.

## When SOP is applied

* Origin checks are applied by the browser in every case of potential interaction between elements from different origins. However, SOP does not entirely block cross-origin interactions, as cross-origin links can be included, forms can be submitted across origins, and embedding cross-origin resources is generally allowed.

[1]: /static/images/same-origin-policy-overview.png
