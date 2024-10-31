# Fundamentos de la cabecera Referrer-Policy

* Para entender qué es la cabecera `Referrer-Policy`, hay que conocer la cabecera `Referer`, pues la cabecera `Referrer-Policy` se encarga de establecer la política de esta cabecera.
* La cabecera `Referer` se envía junto con las peticiones HTTP y su valor corresponde a la URL desde la cual se ha originado la petición. Para entender mejor la cabecera observa el siguiente ejemplo:
  * La aplicación web `https://domain.tbl` tiene un enlace que apunta a la URL `https://example.tbl`.
  * Cuando un usuario realiza una petición a este enlace, el valor de la cabecera `Referer` será `https://domain.tbl`.
  * Si bien a primera vista parece que no tiene ningún efecto en la seguridad, podría darse el caso en que la aplicación web de `https://domain.tbl` originara la petición desde la URL `https://domain.tbl/users/<user>`, donde `<user>` es el nombre del usuario. Esto enviaría el nombre del usuario a la página `https://example.tbl`, provocando una filtración de información.
* Aunque este ejemplo puede no ser muy grave para la seguridad, es crucial saber qué información se envía a otras páginas, ya que según el caso podría tener un alto impacto.
* La cabecera `Referrer-Policy` se utiliza para controlar qué información se envía a otras páginas con la cabecera `Referer`. Es importante definir bien esta cabecera para evitar la filtración de información enviando rutas o parámetros de la aplicación web.
* Esta cabecera esta formada por directivas que son interpretadas por el navegador y según su directiva se adjunta la información correspondiente. Un ejemplo de la `Referrer-Policy` podría ser el siguiente:

  ```
  Referrer-Policy: no-referrer
  ```
