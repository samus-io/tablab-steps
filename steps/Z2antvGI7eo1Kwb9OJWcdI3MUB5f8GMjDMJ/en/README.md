# Cookie flag Secure

* The `Secure` attribute is essential when setting cookies. This attribute tells the user's browser that it must only send this cookie via HTTPS (over SSL/TLS). This prevents cookies from being stolen by man-in-the-middle (MITM) attacks.

> :older_man: A man-in-the-middle attack occurs when an attacker is on the same network and stands between the user and the gateway to inspect your traffic. This can be avoided by using HTTPS because the connection is encrypted.

* To set the `Secure` attribute, simply add it to the `Set-Cookie` header:

  ```
  Set-Cookie: <cookie-name>=<cookie-value>; Secure
  ```
