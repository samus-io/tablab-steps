# Cookie flag HttpOnly

* The `HttpOnly` attribute prevents the user's browser from allowing JavaScript to access the value of Cookies using, for example, the `document.cookie` property. However, JavaScript requests (such as `fetch` or `XMLHttpRequest` calls) will still include Cookies.
* This approach mitigates the impact of client-side attacks (such as `XSS` vulnerabilities) that allow Cookies to be stolen by an attacker, because it prevents the Cookies value from being accessed directly.

> :older_man: The XSS vulnerability allows an attacker to add JavaScript code to a user's browser, allowing them to steal Cookies or make requests impersonating the user's identity.

* Be aware that in the case of having to access the Cookie via JavaScript, it will not be possible to add this attribute. In this case, it is necessary to make sure that this Cookie is not used in the backend.
* To set the `HttpOnly` attribute, just add it in the `Set-Cookie` header:

  ```
  Set-Cookie: <cookie-name>=<cookie-value>; Secure
  ```
