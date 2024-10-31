# Atributo Secure de las Cookies

* El atributo `Secure` es indispensable al establecer las Cookies. Este atributo indica al navegador del usuario que únicamente tiene que enviar esta Cookie por HTTPS (via SSL/TLS). De esta forma, se evita que las Cookies puedan ser robadas con ataques MITM (Man-in-the-middle).

> :older_man: Un ataque Man-in-the-middle ocurre cuando un adversario esta dentro de la misma red y este se coloca entre el usuario y la puerta de enlace (o `gateway`) para inspeccionar su tráfico. Esto puede evitarse utilizando HTTPS, ya que la conexión es encriptada.

* Para establecer el atributo `Secure`, basta con añadirlo en la cabecera `Set-Cookie`:

  ```
  Set-Cookie: <cookie-name>=<cookie-value>; Secure
  ```
