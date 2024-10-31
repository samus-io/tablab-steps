# Aspectos avanzados de la cabecera CSP

## Otras directivas y valores

* A demás de las directivas y valores explicados anteriormente, hay dos directivas mas que son importantes para los frames de las aplicaciones web. También existen otros valores pero son poco utilizados dada su naturaleza.

> :older_man: Los frames son etiquetas HTML como `iframe` o `frame` que añaden en una ventana una página web dentro de la misma aplicación web.

### Directiva `frame-src`

* La directiva `frame-src` define los orígenes desde los cuales se deben cargar los frames. En este ejemplo se permite añadir a la página web frames que carguen la misma aplicación web o el origen `https://domain.tbl`:

  ```
  frame-src 'self' https://domain.tbl
  ```

### Directiva `frame-ancestors`

* Esta directiva permite especificar los orígenes desde los cuales se deben permitir crear frames de la aplicación web. Su función es similar a la cabecera `X-Frame-Options` pero con mas opciones, dejando obsoleta a la cabecera `X-Frame-Options` aunque es recomendable seguir utilizándola para los navegadores que no soporten esta directiva.
* Esta directiva es especialmente útil para prevenir ataques de `Clickjacking`, ya que permite restringir los orígenes que pueden utilizar la aplicación web en un `iframe`.
* Este ejemplo permite al origen `https://example.tbl` incluir etiquetas `frame` que añadan la aplicación web:

  ```
  frame-ancestors 'self' https://example.tbl
  ```

### El valor `unsafe-hashes`

* El valor `'unsafe-hashes'` funciona de forma parecida al valor `'unsafe-inline'` pero con la diferencia que en vez de permitir que se añada cualquier código en línea, únicamente se permitirá añadir el contenido especificado en la CSP. Para determinar qué código se puede añadir, primero hay que crear el hash `SHA-256` del código en cuestión y posteriormente se procederá a añadir `sha256-` en conjunto con el hash.
* Por ejemplo si se quisiera añadir el siguiente atributo a una etiqueta HTML `style='color:red'`, primero se crea el hash del código y se añade.
* En el caso de utilizar `'unsafe-hashes'`, si se quiere añadir el siguiente atributo a una etiqueta HTML `onClick="submit();"` para evitar usar `'unsafe-inline'` se tiene que especificar en la CSP el siguiente contenido:

  ```
  Content-Security-Policy: script-src 'unsafe-hashes' 'sha256-o3A3EpEj/sJu6V6W8bXUlCd9vaQ4N6MXlyeKjrePpZ4='
  ```

* Al añadir un hash este va precedido por la cadena `sha-256` y posteriormente se añade el hash `o3A3EpEj/sJu6V6W8bXUlCd9vaQ4N6MXlyeKjrePpZ4=` que hace referencia al código `submit();`.
* Esto permite que se ejecute la función `submit();` en cualquier atributo HTML.
* Para generar este hash, hay que ejecutar el siguiente comando en una distribución Linux o Mac:

  ```bash
  echo -n 'submit();' | openssl sha256 -binary | openssl base64
  ```

* Es importante recordar que si se añade un espacio o un salto de linea, el hash cambiará y por lo tanto no se podrá añadir el atributo.

### El valor `data:`

* El valor `data:` permite añadir recursos que están codificados e incrustados en la aplicación web. Un ejemplo muy común es cuando se añade una imagen en Base64:

  ```html
  <img src="data:image/png;base64,<base64>" alt="Base64 Image">
  ```

En este ejemplo, para que la CSP permita cargar la imagen en el navegador del usuario se tendría que añadir el valor `data:` de la siguiente forma:

  ```
  Content-Security-Policy: img-src data:
  ```
  