# How to implement headers in IIS 10.0

* To add a header to the IIS only the following content should be added to the `web.config` file:

  ```xml
  <configuration>
    <system.webServer>
    <httpProtocol>
     <customHeaders>
        <add name="Content-Security-Policy" value="default-src 'none'" />
      </customHeaders>
    </httpProtocol>
    </system.webServer>
  </configuration>
  ```

* In this example the `Content-Security-Policy` header has been added with the `default-src 'none'` value.
* Note that the `configuration` tag will already be added to the `web.config` file, it is important not to repeat it and just add the content inside the tag.
* Once the modifications have been applied to the `web.config` file you will need to restart IIS for it to take effect.
