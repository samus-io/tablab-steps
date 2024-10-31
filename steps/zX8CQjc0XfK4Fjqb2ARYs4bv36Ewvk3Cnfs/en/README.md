# Referrer-Policy header directives

* The following table defines the different directives of the `Referrer-Policy` header:
  |Directive|Description|Referer header result|
  |:--:|:--:|:--:|
  |no-referrer|If the `Referrer-Policy` header has the `non-referrer` directive, it will prevent the `Referer` header from being sent, thus preventing any leakage of sensitive information.|No `Referer` header is sent.|
  |no-referrer-when-downgrade|This directive prevents the `Referer` header from being sent to non-HTTPS origins. This header is not highly recommended, as it does not prevent sensitive information from being sent to HTTPS origins.|`https://domain.tbl/user?name=User`|
  |origin|With this directive, the `Referer` header contains only the origin from which the request originated.|`https://domain.tbl/user/`|
  |origin-when-cross-origin|This directive is also useful for preventing information leakage, since it only sends the origin if the request is made to a different origin. If the request is made to the same origin, the entire `Referer` header is sent.|`https://domain.tbl`|
  |same-origin|The `same-origin` directive only sends the `Referer` header on requests from the same origin, it is similar to the previous directive except that it only sends the origin if the request is made to the same origin.|No `Referer` header is sent.|
  |strict-origin|When this directive is set, the origin is only sent in the `Referer` header if the security protocol is the same (`HTTP` to `HTTP` or `HTTPS` to `HTTPS`), otherwise the header is not sent. The `strict-origin` directive is similar to the `same-origin` directive, but unlike it, the security protocol must be the same.|`https://domain.tbl`|
  |strict-origin-when-cross-origin|The `strict-origin-when-cross-origin` directive only sends the origin for requests to other origins as long as the security protocol is the same (`HTTP` to `HTTP` or `HTTPS` to `HTTPS`). This directive is similar to `origin-when-cross-origin`, except that the security protocol must be the same.|`https://domain.tbl`|
  |unsafe-url|Finally, `unsafe-url` is the default directive when the `Referrer-Policy` header is not defined. This directive appends the origin, path, and parameters to the `Referer` header. It is important not to use this directive, as it is considered unsafe.|`https://domain.tbl/user?name=User`|

## Referrer-Policy header recommendations

* Note that web analytics services, such as Google Analytics, use the `Referer` header to collect information about what page the user visited. Depending on the policy we apply, it may affect the collection of this information.
* If a data analysis service is used, it is recommended to use the `same-origin`, `origin-when-cross-origin` or `strict-origin-when-cross-origin` directives to avoid errors in its operation.
* If no web analytics service is used, the most recommended directives are `strict-origin`, `origin` and `no-referrer`.
