# Aspectos avanzados de Cross-Origin Resource Sharing (CORS)

## Tipos de peticiones de origen cruzado

### Petición simple

* Las peticiones simples son aquellas que se envían al mismo origen del que se han hecho. Dicho de otra forma, siempre que la petición no sea de origen cruzado, esta será simple.
* En el caso que se realice hacia otro origen, la petición será considerada simple en los siguientes casos:
  * Si los métodos que utiliza son `GET`, `POST` o `HEAD`.
  * En caso que la petición utilice el método `POST` la cabecera `Content-Type` deberá contener uno de los siguientes valores:
    * `application/x-www-form-urlencoded`
    * `multipart/form-data`
    * `text/plain`
  * Este tipo de peticiones no pueden utilizar cabeceras que no sean estándar.
* Un ejemplo de petición simple con JavaScript podría ser el siguiente:

  ```javascript
  const xhttp = new XMLHttpRequest();
  xhttp.onload = function() {
    document.getElementById("info").innerHTML = this.responseText;
  }
  xhttp.open("GET", "info.html");
  xhttp.send();
  ```

* En este código JavaScript envía una petición al archivo `info.html` y luego se accede a su contenido. Esto es posible porque el archivo esta en el mismo origen pero si este fuera en otro origen y no tuviera el `CORS` configurado, no sería posible por la `SOP`.

### Petición Preflight

* Las peticiones `Preflight` se utilizan para suplir las carencias de las peticiones simples al hacer las peticiones contra otros orígenes. Algunas de sus ventajas son:
  * Hacer una petición con otros métodos, como por ejemplo el `PUT`.
  * Enviar una petición `POST` con otro `Content-Type`, como podría ser `Content-Type: application/xml`.
  * Definir cabeceras no estándar en la petición como `Front-End-Https`.
  * Adjuntar las credenciales a las peticiones a diferentes orígenes.
* A diferencia de las peticiones simples, las peticiones `Preflight` necesitan enviar dos peticiones. La primera simplemente envía una petición con el método `OPTIONS`, esto es necesario para que el navegador determine si se puede realizar la petición, evaluando las cabeceras que corresponden a `CORS`.
* El siguiente código representa un ejemplo de código JavaScript realizando una petición `Preflight`:

  ```javascript
  const xhttp = new XMLHttpRequest();
  const jsonData = JSON.stringify({ "page": 1 });

  xhttp.open("POST", "https://domain.tbl/info");
  xhttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  xhttp.setRequestHeader('Front-End-Https', 'on'); // Optional header

  xhttp.onload = function() {
    document.getElementById("info").innerHTML = this.responseText;
  }
  xhttp.send(jsonData);
  ```

* Este código JavaScript envía una petición `POST` con contenido JSON al origen `https://domain.tbl` para luego obtener la respuesta del endpoint `info`. Como no se trata de una petición simple, primero se enviará una petición con el método `OPTIONS` y luego se tramitará la petición `POST`. También se envía una cabecera que no está en el estándar de las cabeceras `HTTP`.
* Hay que destacar que en las peticiones `Preflight`, el desarrollador no tiene que hacer una petición con el método `OPTIONS`, sino que el mismo navegador al ejecutar la petición valora que tipo es y si es necesario hacer una petición con el método `OPTIONS` con antelación.
* Si se ejecutara el código JavaScript en el origen `https://example.tbl`, la primera petición con el método `OPTIONS` sería la siguiente:

  ```
  OPTIONS /info HTTP/1.1
  Host: domain.tbl
  User-Agent: Mozilla/5.0
  Origin: https://example.tbl
  Access-Control-Request-Method: POST
  Access-Control-Request-Headers: Front-End-Https
  ```

* Y esta sería la respuesta del servidor:

  ```
  HTTP/1.1 200 OK
  Content-Type: application/json; charset=UTF-8
  Access-Control-Allow-Origin: https://example.tbl
  Access-Control-Allow-Methods: POST, GET, OPTIONS, DELETE
  Access-Control-Allow-Headers: Front-End-Https
  Access-Control-Max-Age: 3600
  ```

* En esta respuesta se informa al navegador que el origen `https://example.tbl` puede hacer peticiones usando los métodos `POST`, `GET`, `OPTIONS` o `DELETE`, ademas de permitir enviar la cabecera `Front-End-Https`.
* Una vez el navegador a determinado que la política de `CORS` permite hacer la petición a `https://domain.tbl`, entonces envía la petición `POST`:

  ```
  POST /info HTTP/1.1
  Host: domain.tbl
  User-Agent: Mozilla/5.0
  Origin: https://example.tbl
  Connection: keep-alive
  Front-End-Https: on
  Content-Type: application/json; charset=UTF-8
  Content-Lenght: 11
  
  { 
    "page": 1 
  }
  ```

### Petición con credenciales

* En algunos casos será necesario adjuntar a las peticiones las credenciales para así autenticarse contra el origen, en este caso hay la opción de especificar que se añadan las credenciales junto con la petición.
* Se consideran credenciales las Cookies y las cabeceras `HTTP` de autenticación. Por defecto, el navegador evita que se envíen las credenciales en las peticiones de origen cruzado, a menos que se permita a través de `CORS`.
* Esto no solo se tendrá que hacer a nivel de JavaScript, también se tendrá que añadir la cabecera `Access-Control-Allow-Credentials` con el valor `true` en el origen que se vaya a hacer la petición.
* Un ejemplo de código JavaScript añadiendo las credenciales a una petición podría ser el siguiente:

  ```javascript
  const xhttp = new XMLHttpRequest();
  const jsonData = JSON.stringify({ "page": 1 });

  xhttp.open("POST", "https://domain.tbl/info");
  xhttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  xhttp.setRequestHeader('Front-End-Https', 'on'); // Optional header
  xhttp.withCredentials = true;

  xhttp.onload = function() {
    document.getElementById("info").innerHTML = this.responseText;
  }
  xhttp.send(jsonData);
  ```

* De esta forma, al hacer la petición contra `https://domain.tbl/info`, se  añadirán las Cookies del origen de `domain.tbl` para poder autenticarse contra el endpoint `info`.
