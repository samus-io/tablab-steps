# CSP recommendations

* It is recommended that you always use the `default-src` directive to set a predefined value for all directives and modify the other directives according to the needs of the web application.
* For web applications that do not require a user interface (such as APIs), use the CSP `default-src: 'none'`.

## Avoid using unsafe-inline

* It is recommended not to use the `'unsafe-inline'` and `'unsafe-eval'` values as they are considered insecure. This is because the `eval()` function and inline code added in HTML tags are used to create cross-site scripting (XSS) vulnerabilities.
* In particular, the `'unsafe-inline'` value negates many of the security benefits of CSP, so it is always advisable to avoid it. However, sometimes the design of the web application makes it imperative to use this value.
* To avoid using the `'unsafe-inline'` value, you should avoid using HTML events such as `onclick`, `onload`, `onerror`, etc.
* In this example, the `onclick` attribute is used to generate an alert when the button is pressed:

  ```html
  <!DOCTYPE html>
  <html>
  <head>
  </head>
  <body>
      <h1>Example CSP with unsafe-inline</h1>
      <button onclick="alert('Hello, World!')">Haz click</button>
  </body>
  </html>
  ```

* The above code would have the following CSP:

  ```
  Content-Security-Policy: default-src 'none'; script-src 'unsafe-inline'
  ```

* To convert this code to code that does not use event attributes, you must handle the event using the `addEventListener` JavaScript function:

  ```html
  <!DOCTYPE html>
  <html>
  <head>
  </head>
  <body>
      <h1>Example CSP without unsafe-inline</h1>
      <button id="myButton">Click here</button>
      <script>
          // Add click event safely without inline JavaScript
          document.getElementById("myButton").addEventListener("click", function() {
              alert('Hello, World!');
          });
      </script>
  </body>
  </html>
  ```

* In this case, by modifying the code by removing the `onclick` event, the CSP would only require that JavaScript code from the same Web application could be executed:

  ```
  Content-Security-Policy: default-src 'none'; script-src 'self'
  ```

* As a last resort, if it is absolutely necessary to use `unsafe-inline`, it is much more advisable to use the `unsafe-hashes` value.
