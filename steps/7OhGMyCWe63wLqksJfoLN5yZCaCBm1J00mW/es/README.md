# Atributo de las Cookies HttpOnly

* El atributo `HttpOnly` impide al navegador del usuario que JavaScript pueda acceder al valor de las Cookies utilizando, por ejemplo, la propiedad `document.cookie`. Aun así, las peticiones realizadas mediante JavaScript (como las llamadas con `fetch` o `XMLHttpRequest`) continuarán incluyendo las Cookies.
* Esta medida permite mitigar el impacto de ataques del lado del cliente (como vulnerabilidades `XSS`) que permiten el robo de las Cookies por parte de un adversario, al evitar que se pueda acceder directamente al valor las Cookies.

> :older_man: La vulnerabilidad XSS permite a un adversario añadir código JavaScript al navegador de un usuario, permitiendo robar las Cookies o hacer peticiones suplantando la identidad del usuario.

* Hay que tener en cuenta que en caso de tener que acceder a una Cookie mediante JavaScript, no se podrá añadir este atributo. En este caso, hay que asegurarse que esa Cookie no se utilice en el backend.
* Para establecer el atributo `HttpOnly`, basta con añadirlo en la cabecera `Set-Cookie`:

  ```
  Set-Cookie: <cookie-name>=<cookie-value>; Secure
  ```
