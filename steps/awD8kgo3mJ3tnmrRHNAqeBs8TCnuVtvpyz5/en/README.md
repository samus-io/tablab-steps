# How to generate the CSP

* The CSP also has a violation reporting mechanism that allows developers to receive reports of policy violations and take action to fix them. To use this mechanism, you must use the `report-uri` directive, where the value specifies the location where the reports are sent. These reports will be sent with a POST request to the specified path and in a JSON object.
* An example of using this directive would be as follows:

  ```
  default 'none'; report-uri https://domain.tbl/csp-reports
  ```

* The JSON object received by the endpoint contains the following fields:

  ```json
  {
    "csp-report": {
      "document-uri": "http://domain.tbl/signup.html",
      "referrer": "http://example.tbl/haxor.html",
      "blocked-uri": "http://example.tbl/injected.png",
      "violated-directive": "img-src https://example.tbl",
      "original-policy": "default-src 'self'; img-src 'self' https://example.tbl; report-uri https://domain.tbl/csp-reports",
    }
  }
  ```

* If the CSP blocks a resource from being loaded by the web application, it displays a message through the developer console, as shown in the following image:

![CSP Console Error][4]

* In this case, it warns that the JavaScript code of `https://tablab.io/script.js` cannot load its content because the Content Security Policy has the `default-src 'none'` directive.
* It also indicates that it is not possible to use inline style or inline JavaScript, in which case the browser recommends that we add the `'unsafe-inline'` directive to the `script-src` and `style-src` or use the `'unsafe-hashes'` directive with the SHA-256 hash of the code in question.

## Generating the CSP using the Laboratory extension

* Setting the CSP manually in a web application can become a very tedious and difficult job, for this you can use the browser extension [Laboratoy (Content-Security Policy/CSP Toolkit)][1], which automatically generates the CSP of a web application.
* The Laboratoy extension basically stores all the resources loaded by the page and applies the appropriate policies to make it work properly.
* Once the extension has been downloaded, to use it, simply enable the `Record this site` option and go through the entire web application, using all its functionalities, so that the extension generates the corresponding CSP.
* Note that once this option is selected, the current page must be reloaded to load its resources.

![Laboratory Extension][2]

* In the `Configuration` section you have to select the `'self' if same origin, otherwise origin` option for all directives, this way only the origin will be added in the CSP instead of the whole route. This option is chosen to avoid having many changes in the CSP each time the web application is modified.

![Laboratory Extension Configuration][3]

* Once the CSP has been generated, the `Enforce CSP policy` option must be enabled to check that it has been generated correctly, this way the generated CSP will be applied to check for errors. Next, the entire web application is visited to detect any resources that are not loaded in the web application.
* Finally, after verifying that the CSP has been generated correctly, the CSP value is copied with the `Copy` button.

[1]: https://chrome.google.com/webstore/detail/laboratory/mjcamldajgnpgjcpacomkgfhccnibldg
[2]: /static/images/learning/laboratory-image.png
[3]: /static/images/learning/laboratory-record-site.png
[4]: /static/images/learning/csp-console-error.png
