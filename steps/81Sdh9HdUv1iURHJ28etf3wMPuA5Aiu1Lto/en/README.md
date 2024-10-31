# Strict-Transport-Security header basics

* The `Strict-Transport-Security (HSTS)` response header is a security mechanism that informs the browser to only access the web application via HTTPS, and that any future attempts to access via HTTP will be automatically redirected to HTTPS. This mechanism is useful for preventing man-in-the-middle attacks.

> :older_man: A `Man-in-the-Middle` attack is a cybersecurity technique in which an attacker intercepts communications between a user and the server in order to intercept, modify, or spoof messages between the two parties.

## Directives

* The `Strict-Transport-Security (HSTS)` header has only two directives:
  * `max-age=<expire-time>`: determines the time in seconds that the browser must remember to access the site in HTTPS only.
  * `includeSubDomains`: if this directive is specified, the header will apply to all subdomains.
* In this example, the header will inform the browser to only HTTPS access your domain and all its subdomains for a period of one year:

  ```
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  ```
