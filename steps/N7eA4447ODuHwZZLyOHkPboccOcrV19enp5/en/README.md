# Examples of the CSP header

* Once you understand the operation, directives, and values of the CSP, some examples of how to create it will be shown, reviewing the directives and values previously explained.
* The first directive to add when creating a CSP is the `default-src` directive, since it defines which origins can access resources by default, unless otherwise specified in other directives. Typically, the value of this directive will be `'none'`, and then each directive will specify which origins can load each resource.
* The following CSP allows the web application itself and the origin `domain.tbl` to load JavaScript code. It also allows inline code to be added and the `eval()` function to be executed:

  ```
  default-src: 'none'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://domain.tbl
  ```

* An example of code that could be loaded with this CSP would be as follows:

  ```html
  <!DOCTYPE html>
  <html>
    <head>
      <script src=https://domain.tbl/script.js></script>
    </head>
    <body>
      <script>
        alert(eval(2 + 2))
      </script>
      <div onload=alert("Hello!")>Hello!</div>
    </body>
  </html>
  ```

* If CSS code and text fonts were to be added to the above code, the CSP would need to be changed, an example code could be like this:

  ```html
  <!DOCTYPE html>
  <html>
    <head>
      <script src=https://domain.tbl/script.js></script>
      <style>
        @font-face {
          font-family: 'ExternalFont';
          src: url('https://example.tbl/fonts/font.ttf');
        }
        div {
            color: blue;
        }
    </style>
    </head>
    <body>
      <script>
        alert(eval(2 + 2))
      </script>
      <div onload=alert("Hello!")>Hello!</div>
    </body>
  </html>
  ```

* To prevent the code you have added from being blocked by the browser, you must modify the CSP and add the following directives:

  ```
  default-src: 'none'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://domain.tbl; style-src 'self'; font-src https://example.tbl/ 
  ```
