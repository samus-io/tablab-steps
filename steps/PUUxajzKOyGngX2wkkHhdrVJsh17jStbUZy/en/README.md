# How to implement the Cookie Secure attribute in IIS 10.0

* To set the `Secure` flag, you need to modify your `web.config` file and add the following content:

  ```xml
  <system.web>
    ...
    <httpCookies requireSSL="true" />
    ...
  </system.web>
  ```

* However, if the `<form>` element is used in the `<authentication>` block, as in the following example, this element will override the behavior of the `httpCookies` tag defined above:

  ```xml
  <system.web>  
      <authentication mode="Forms">  
          <forms>  
              <!-- forms content -->  
          </forms>  
      </authentication>  
  </system.web>
  ```

* To ensure that forms only send cookies over `HTTPS`, the following attribute must be added to the `forms` field:

  ```xml
    <system.web>  
        <authentication mode="Forms">  
            <forms requireSSL="true">  
                <!-- forms content -->  
            </forms>  
        </authentication>  
    </system.web>
  ```
