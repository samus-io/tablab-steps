# CSP header policies and values

* The CSP has several directives that can be used to specify the rules for loading resources on a web page. The directives allow access to all types of resources by default unless otherwise specified, so it is useful to use the `default-src` directive. Some of the most common directives are shown below:

|Directive|Description|
|:--:|:--:|
|default-src|Allows all resource types to be loaded from the specified sources, unless otherwise specified in other directives.|
|script-src|This directive determines which JavaScript resources are loaded in the browser.|
|img-src|Specifies which image sources are valid.|
|style-src|Defines which CSS elements and stylesheets the browser can load.|
|font-src|It defines which fonts (such as WOFF or TTF files) the web application can use.|
|connect-src|It determines which origins can make requests with `XMLHttpRequest (AJAX)`, `WebSocket`, `fetch()`, `<a ping>` and `EventSource`. If the origin to which the request is made is not defined, the browser will emulate that the response was an HTTP 400 code.|
|form-action|Indicates which origins can be used in the `action` attribute of HTML forms (`<form>`).|

## Values of the directives

* The CSP defines one or more values for each directive to define the origins associated with each directive.

|Value|Description|
|:--:|:--:|
|`*`|The `*` value allows loading content from any origin, such as `https://domain.tbl` or from the web application itself.|
|`'none'`|On the other hand, the value `'none'` prevents loading content from any origin.|
|`'self'`|It allows loading resources only from the same web application, for example, you would not be able to load a resource from the origin `https://domain.tbl`.|
|`https://domain.tbl`|In this case we have as value a URL, this means that the resources can only be loaded if they come from that URL.|
|`'unsafe-inline'`|The `'unsafe-inline'` value allows executing inline JavaScript or CSS code. An example of inline code could be `<form onsubmit="alert(1)">`. This value can only be used by the `script-src` and `style-src` directives.|
|`'unsafe-eval'`|Finally, this value allows the `eval()` function to be executed in the JavaScript code. It should be noted that this value is unique to the `script-src` directive.|

* :warning: Please note that the values `self`, `none`, `unsafe-inline` and `unsafe-eval` must be enclosed in single quotes for the CSP to work correctly.
