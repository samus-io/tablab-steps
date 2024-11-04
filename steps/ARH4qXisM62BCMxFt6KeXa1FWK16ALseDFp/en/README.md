# CSP header basics

* The Content Security Policy (CSP) header is a security mechanism that allows web application developers to specify the resources (such as scripts, images, styles, and so on) from which a web page can load content. This header is sent as the web application's response header and interpreted by the user's browser.
* The CSP is very useful in preventing malicious code injection attacks, such as Cross-Site Scripting (XSS), by allowing only content from trusted sources to be loaded.
* When a browser receives a CSP, it checks that the content it is loading conforms to the rules specified in the header. If it does not, the browser blocks loading the content not specified in the CSP and displays an error in the developer console, which is very useful to know when it is blocking resources that are trusted and therefore the CSP needs to be modified.
* It is worth mentioning that not all browsers support the CSP, but modern browsers do, and its use is highly recommended in any web application to improve security and prevent vulnerabilities.

![content-security-policy-graphical-representation.png][1]

* In this image, you can see how the CSP has defined that only the resources of the URL `http://example.com` can be added, so when the web application tries to make a request to `http://malicious.com` to load a JavaScript resource, this request is blocked, preventing the execution of malicious JavaScript code in the user's browser.

## Parts of the CSP

* The CSP consists in two parts, the first is called a directive and the second is the value of the directive.
* The directive is a rule that refers to a type of resource, such as images, JavaScript or CSS files, client-side links between web pages, frames, and so on.
* On the other hand, the value is a text string associated with a directive, and it indicates from which sources resources can be loaded into the web application. In this example, there are several directives and each of them has one or more values associated with it:

  ```
  Content Security Policy: default-src 'self'; script-src 'unsafe-inline' 'unsafe-eval' https://example.com; img-src *; style-src 'none'; font-src 'self'; connect-src 'none'.
  ```
  
* By setting a CSP header, you define a list of allowed origins for all resource types used by the web application and restrict the others, thus avoiding client-side vulnerabilities.

[1]: /static/images/content-security-policy-graphical-representation.png
