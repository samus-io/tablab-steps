# How to implement the Cookie HttpOnly attribute in IIS 10.0

* To set the `HttpOnly` attribute you only need to add the following configuration in the `web.config` file:

  ```xml
  <configuration>
    <system.web>
      ...
      <httpCookies httpOnlyCookies="true"/>
      ...
    </system.web>
  </configuration>
  ```

* With this directive the `HttpOnly` attribute will be added to all Cookies sent by the backend.
