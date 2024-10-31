# How to prevent CORS configuration errors

* Failure to properly configure CORS can have a major impact on the security of the web application, exposing sensitive user information or even introducing other vulnerabilities.
* Therefore, it is important to configure CORS only when it is necessary for the operation of the web application.
* To avoid misconfiguration of `CORS` it is important to follow the next points:
  * Specify which origins are allowed. It is crucial not to use a wildcard (`*`), as this would allow any source to access the web application response.
  * Allow only trusted origins:

    ```
    Access-Control-Allow-Origin: https://domain.tbl
    ```

  * Never use the `Access-Control-Allow-Origin` header with the value `null`. Using this value is almost identical to using a wildcard.
  * Use the `Access-Control-Allow-Credential: true` header only when absolutely necessary.
  * Use the `Access-Control-Allow-Methods` header to specify which methods the server must accept.
  * Note that setting the `CORS` policy correctly is not a replacement for server-side protection. Even if it is set correctly, the server must implement other security protections, such as authentication and preventing the leakage of sensitive data.
