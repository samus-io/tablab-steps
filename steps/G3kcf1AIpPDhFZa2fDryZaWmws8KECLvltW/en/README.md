# How to view HTTP response headers in Google Chrome

* Response headers are essential elements in the communication between a Web server and a client. These headers are a fundamental part of the response that the server sends to the client after receiving an HTTP request. Their contents provide critical information about the response that allows the client to properly interpret and process the data received.
* These headers provide information about the response itself, such as its status, content type, length, and more. They are included at the top of the HTTP response, before the body of the response.
* Another use for response headers is to enhance the security of the web application on the client side, with headers such as `Content-Security-Policy`, `Referrer-Policy`, or `Strict-Transport-Security`.
* To view the response headers of a web application, access the Developer Console with the `F12` key and select the `Network` section.
* Finally, refresh the page so that the browser console receives all requests. Then select the request for which you want to get the response headers:

![Developer Console Header Response][1]

[1]: /static/images/developer-console-network.png
