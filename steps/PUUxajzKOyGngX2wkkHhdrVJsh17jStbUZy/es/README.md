# Cómo implementar el atributo de las Cookies Secure en IIS 10.0

* Para implementar el flag `Secure` hay que modificar el `web.config` y añadir el siguiente contenido:

  ```xml
  <system.web>
    ...
    <httpCookies requireSSL="true" />
    ...
  </system.web>
  ```

* Sin embargo, si se utiliza el elemento `<form>` en el bloque de `<authentication>`, como en el siguiente ejemplo, este elemento sobrescribirá el comportamiento de la etiqueta `httpCookies` definido anteriormente:

  ```xml
  <system.web>  
      <authentication mode="Forms">  
          <forms>  
              <!-- forms content -->  
          </forms>  
      </authentication>  
  </system.web>
  ```

* Para asegurar que los formularios únicamente envían las Cookies por `HTTPS`, entonces hay que añadir el siguiente atributo en el campo `forms`:

  ```xml
    <system.web>  
        <authentication mode="Forms">  
            <forms requireSSL="true">  
                <!-- forms content -->  
            </forms>  
        </authentication>  
    </system.web>
  ```
