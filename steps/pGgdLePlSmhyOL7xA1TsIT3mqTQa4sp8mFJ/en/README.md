# Configuring CORS in IIS

* CORS enforcement in IIS can be cleanly managed using the official IIS CORS module, which allows CORS rules to be defined declaratively in the `web.config` file.
* This approach is more reliable and maintainable than manually setting custom headers.

## Adding CORS headers in IIS

* The IIS CORS module can be installed by running the following PowerShell command:

  ```powershell
  Install-WindowsFeature -Name Web-CORS
  ```

* Once installed, restart IIS to apply the changes:

  ```powershell
  iisreset
  ```

* CORS behavior is configured through the application's `web.config` file. The module automatically handles preflight (`OPTIONS`) requests and appends the appropriate CORS response headers based on the defined policy.
* To allow cross-origin requests from a specific origin and restrict methods and headers, the following configuration can be added:

  ```xml
    <configuration>
    <system.webServer>
      <cors enabled="true">
        <add origin="https://example.tbl">
          <allowMethods>
            <add method="DELETE" />
          </allowMethods>
          <allowHeaders>
            <add header="X-CSRF-Token" />
          </allowHeaders>
        </add>
      </cors>
    </system.webServer>
  </configuration>
  ```

* This configuration instructs IIS to send the necessary CORS headers with responses, enabling secure cross-origin requests only from `https://example.tbl`, using the `DELETE` method and the custom header `X-CSRF-Token`.
