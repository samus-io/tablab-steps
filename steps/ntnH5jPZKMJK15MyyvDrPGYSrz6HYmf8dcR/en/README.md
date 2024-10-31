# Advanced aspects of Cross-Origin Resource Sharing (CORS)

## Cross-Origin request types

### Simple request

* Simple requests are those that are sent to the same origin from which they are made. In other words, as long as the request is not cross origin, it will be simple.
* In the case that it is made to another origin, the request will be considered simple in the following cases:
  * If the methods it uses are `GET`, `POST` or `HEAD`.
  * In case the request uses the `POST` method, the `Content-Type` header must contain one of the following values:
    * `application/x-www-form-urlencoded`
    * `multipart/form-data`
    * `text/plain`
  * These types of requests cannot use non-standard headers.
* An example of a simple request with JavaScript could be the following:

  ```javascript
  const xhttp = new XMLHttpRequest();
  xhttp.onload = function() {
    document.getElementById("info").innerHTML = this.responseText;
  }
  xhttp.open("GET", "info.html");
  xhttp.send();
  ```

* In this code JavaScript sends a request to the `info.html` file and then accesses its contents. This is possible because the file is in the same origin but if it were in another origin and did not have the `CORS` configured, it would not be possible because of the `SOP`.

### Preflight request

* The `Preflight` requests are used to make up for the shortcomings of simple requests when making requests against another origin. Some of its advantages are:
  * Make a request with other methods, such as `PUT`.
  * Sending a `POST` request with another `Content-Type`, as could be `Content-Type: application/xml`.
  * Define non-standard headers in the request such as `Front-End-Https`.
  * Attach credentials to requests to different origins.
* Unlike simple requests, `Preflight` requests need to send two requests. The first one simply sends a request with the `OPTIONS` method, this is necessary for the browser to determine if the request can be made, by evaluating the headers that correspond to `CORS`.
* The following code represents an example of JavaScript code performing a `Preflight` request:

  ```javascript
  const xhttp = new XMLHttpRequest();
  const jsonData = JSON.stringify({ "page": 1 });

  xhttp.open("POST", "https://domain.tbl/info");
  xhttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  xhttp.setRequestHeader('Front-End-Https', 'on'); // Optional header

  xhttp.onload = function() {
    document.getElementById("info").innerHTML = this.responseText;
  }
  xhttp.send(jsonData);
  ```

* This JavaScript code sends a `POST` request with JSON content to the origin `https://domain.tbl` and then gets the response from the `info` endpoint. Since this is not a simple request, a request with the `OPTIONS` method will be sent first and then the `POST` request will be processed. A header that is not in the standard `HTTP` header is also sent.
* If the JavaScript code were executed at the origin `https://example.tbl`, the first request with the `OPTIONS` method would be as follows:

  ```
  OPTIONS /info HTTP/1.1
  Host: domain.tbl
  User-Agent: Mozilla/5.0
  Origin: https://example.tbl
  Access-Control-Request-Method: POST
  Access-Control-Request-Headers: Front-End-Https
  ```

* And this would be the server's response:

  ```
  HTTP/1.1 200 OK
  Content-Type: application/json; charset=UTF-8
  Access-Control-Allow-Origin: https://example.tbl
  Access-Control-Allow-Methods: POST, GET, OPTIONS, DELETE
  Access-Control-Allow-Headers: Front-End-Https
  Access-Control-Max-Age: 3600
  ```

* This response informs the browser that the origin `https://example.tbl` can make requests using the `POST`, `GET`, `OPTIONS`, and `DELETE` methods. In addition, the `Front-End-Https` header can be sent.
* Once the browser has determined that the `CORS` policy allows the request to be made to `https://domain.tbl`, it sends the `POST` request:

  ```
  POST /info HTTP/1.1
  Host: domain.tbl
  User-Agent: Mozilla/5.0
  Origin: https://example.tbl
  Connection: keep-alive
  Front-End-Https: on
  Content-Type: application/json; charset=UTF-8
  Content-Lenght: 11
  
  { 
    "page": 1 
  }
  ```

### Request with credentials

* In some cases it will be necessary to attach the credentials to the requests in order to authenticate against the origin, in this case there is the option to specify that the credentials are added along with the request.
* Cookies and authentication `HTTP` headers are considered credentials. By default, the browser prevents credentials from being sent in cross-origin requests, unless this is allowed through `CORS`.
* This will not only have to be done at the JavaScript code, you will also have to add the `Access-Control-Allow-Credentials` header with the value `true` in the origin that the request is to be made.
* An example of JavaScript code adding the credentials to a request could be the following:

  ```javascript
  const xhttp = new XMLHttpRequest();
  const jsonData = JSON.stringify({ "page": 1 });

  xhttp.open("POST", "https://domain.tbl/info");
  xhttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  xhttp.setRequestHeader('Front-End-Https', 'on'); // Optional header
  xhttp.withCredentials = true;

  xhttp.onload = function() {
    document.getElementById("info").innerHTML = this.responseText;
  }
  xhttp.send(jsonData);
  ```

* In this example, Cookies from the origin of `domain.tbl` will be added when making the request against `https://domain.tbl/info` in order to authenticate against the `info` endpoint.
