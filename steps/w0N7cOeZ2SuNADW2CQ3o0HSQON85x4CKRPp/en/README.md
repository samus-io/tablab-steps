# How to remove response headers in IIS 10.0

* To remove headers in IIS, simply remove the contents of `web.config` which adds the header.
* In some cases this will not be possible because the header is set by IIS itself, as is the case with the `Server` header. It is recommended to remove this header as it provides server information along with the server version.
* To remove the `Server` header you need to install the IIS module `IIS URL Rewrite`. This module will rewrite requests so that the header is not sent.
* To install the module, download and run the installer from the official IIS [URL Rewrite][1] page.
* Once the module is installed, restart the service and add the following content to the `web.config` file:

  ```xml
  <rewrite>
    <outboundRules>
        <rule name="Remove Server header">
            <match serverVariable="RESPONSE_SERVER" pattern=".+" />
            <action type="Rewrite" value="" />
        </rule>
    </outboundRules>
  </rewrite>
  ```

* This configuration will look for the server variable `RESPONSE_SERVER` and rewrite its value, leaving it empty.

[1]: https://www.iis.net/downloads/microsoft/url-rewrite
