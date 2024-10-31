# Advanced aspects of the CSP header

## Other directives and values

* In addition to the directives and values explained above, there are two other directives that are important for web application frames. There are other values as well, but they are rarely used due to their nature.

> :older_man: Frames are HTML tags like `iframe` or `frame` that add a web page to a window within the same web application.

### The `frame-src` directive

* The `frame-src` directive defines the source from which frames should be loaded. In this example, it is allowed to add frames to the web page that load the same web application or the origin `https://domain.tbl`:

  ```
  frame-src 'self' https://domain.tbl
  ```

### The `frame-ancestors` directive

* This directive allows you to specify the ancestors from which web application frames may be created. Its function is similar to the `X-Frame-Options` header, but with more options, making the `X-Frame-Options` header obsolete, although it is recommended to continue using it for browsers that do not support this directive.
* This directive is especially useful to prevent clickjacking attacks, since it allows to restrict the origins that can use the web application in an `iframe`.
* This example allows the origin `https://example.tbl` to include `frame` tags that add the web application:

  ```
  frame-ancestors 'self' https://example.tbl
  ```

### The `unsafe-hashes` value

* The `unsafe-hashes` value works similarly to the `unsafe-inline` value, but instead of allowing any inline code to be added, only the content specified in the CSP is allowed. To determine what code can be added, first create the `SHA-256` hash of the code in question, then add `sha256-` in conjunction with the hash.
* For example, if you want to add the following attribute to an HTML tag `style='color:red'`, first create the hash of the code and then add it.
* In the case of using `'unsafe-hashes'`, if you want to add the following attribute to an HTML tag `onClick="submit();"` to avoid using `'unsafe-inline'`, you must specify the following content in the CSP

  ```
  Content-Security-Policy: script-src 'unsafe-hashes' 'sha256-o3A3EpEj/sJu6V6W8bXUlCd9vaQ4N6MXlyeKjrePpZ4='
  ```

* When a hash is added, it is preceded by the string `sha-256` and then the hash `o3A3EpEj/sJu6V6W8bXUlCd9vaQ4N6MXlyeKjrePpZ4=` is added, which references the `submit();` code.
* This allows the `submit();` function to be performed on any HTML attribute.
* To generate this hash, run the following command on a Linux or Mac distribution

  ```bash
  echo -n 'submit();' | openssl sha256 -binary | openssl base64
  ```

* It is important to note that if you add a space or a line break, the hash will change and you will not be able to add the attribute.

### The `data:` value

* The `data:` value allows you to add resources that are encoded and embedded in the web application. A very common example is when adding a Base64 image:

  ```html
  <img src="data:image/png;base64,<base64>" alt="Base64 Image">
  ```

In this example, in order for the CSP to allow the image to load in the user's browser the `data:` value would have to be added as follows:

  ```
  Content-Security-Policy: img-src data:
  ```
