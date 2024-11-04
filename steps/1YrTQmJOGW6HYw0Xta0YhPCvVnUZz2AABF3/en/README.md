# Information disclosure through response headers

* If you are using a web server, such as `Apache`, it will by default add the `Server` response header to all requests it sends. Not only web servers include headers, there are also frameworks or programming languages that include them, as is the case with PHP in the `X-Powered-By` header.
* The `Server` header usually has the web server and its version as its value.
* From a security perspective, this can allow an attacker to find vulnerabilities associated with that version.
* To avoid this information leakage, the best recommendation is to remove these headers.
* In the following image, you can see the response headers of a web application that reveal which web server it is using and its version:
![Server Header of Apache][1]

[1]: /static/images/apache-server-header.png
