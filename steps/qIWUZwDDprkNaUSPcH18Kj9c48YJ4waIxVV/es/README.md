# Conceptos básicos de las Cookies

* Las Cookies (o HTTP Cookies), son una cadena de carácteres que se almacena en el navegador del usuario. Su principal uso es para identificar a un usuario y que el servidor reconozca cuando dos solicitudes provienen del mismo navegador.
* Esto es de gran utilidad para que el navegador pueda mantener el estado entre solicitudes HTTP, ya que el protocolo HTTP se define como `stateless`, lo que significa que cada solicitud es independiente de las demás.
* Las Cookies se utilizan principalmente en los siguientes casos:
  * Manejo de la sesión:
    * Se usan para determinar si un usuario ha iniciado sesión en el `login` de una aplicación web. Esto ayuda al servidor a identificar qué usuario ha realizado la solicitud HTTP. También se pueden utilizar para guardar la cesta de la compra en un `e-commerce`.
  * Personalización:
    * En este caso, el uso que se le da a las Cookies es la personalización del sitio web, como podría ser el idioma, el tema de la página (oscuro o claro) y otras preferencias del usuario.
  * Seguimiento:
    * Por último, las Cookies de seguimiento se utilizan para almacenar y analizar el comportamiento del usuario a través de la página web.

## Tipos de Cookies

### Cookies permanentes

* Las Cookies permanentes (o Cookies persistentes) tienen una fecha de expiración establecida por el servidor en los atributos de las Cookies. Principalmente se utilizan para mantener la sesión del usuario, personalización de la aplicación web o también para el seguimiento del usuario.

### Cookies de sesión

* Las Cookies de sesión, a diferencia de las permanentes, no tienen una fecha de expiración. Estas se guardan en memoria y son eliminadas una vez la sesión finaliza.
* Cada navegador define el fin de la sesión de forma distinta, algunos determinan que la sesión ha terminado cuando el navegador se cierra y otros navegadores deciden que se ha finalizado la sesión según otros criterios.
* Normalmente se utilizan para almacenar la cesta de la compra en `e-commerce` o para el seguimiento del usuario.

> :warning: Muchos navegadores tienen una funcionalidad que restablece todas las ventanas la proxima vez que se inicia el navegador. En este caso, las Cookies de sesión también son restauradas, actuando como si el navegador nunca se hubiera cerrado.
Por este motivo, estas Cookies representan un riesgo de seguridad en ciertas circunstancias, ya que puede darse el caso que las Cookies sean almacenadas indefinidamente.

## Cabecera HTTP `Set-Cookie`

* La cabecera de respuesta `Set-Cookie` se encarga de establecer las Cookies en el navegador del usuario para que en las siguientes peticiones, el usuario pueda enviar la cabecera `Cookie` con las Cookies establecidas por el servidor. Cada cabecera `Set-Cookie` únicamente puede tener una Cookie, de forma que si el servidor quiere enviar múltiples Cookies, tendrá que enviar múltiples cabeceras `Set-Cookie`.
* Esta cabecera, además de enviar las Cookies, también tiene atributos que pueden ser definidos para definir su comportamiento, como por ejemplo, que se envíen solamente en peticiones `HTTPS`, donde la conexión está encriptada.
* Este es el ejemplo mas básico de la cabecera:

  ```
  Set-Cookie: <cookie-name>=<cookie-value>
  ```

## Formato de las Cookies

* Estos son algunos de los atributos mas comunes que se utilizan en la cabecera `Set-Cookie`:

  |Atributo|Descripción|
  |:--:|:--:|
  |Domain|El atributo `Domain` especifica que dominio (o subdominio) pertenece la Cookie.|
  |Expires|Establece la fecha en que la Cookie será eliminada del navegador. El formato de la fecha es `<day-name>, <day> <month> <year> <hour>:<minute>:<second> GMT`. Si la Cookie no tiene este atributo, esta se convierte en una Cookie de sesión.|
  |Path|Indica en que ruta de la aplicación web se tiene que enviar la Cookie.|
  |Max-Age|Define el tiempo en segundos en que la Cookie se eliminará del navegador. En caso que `Max-Age` y `Expires` existan, `Max-Age` tendrá preferencia.|

## Limitaciones de las Cookies

* Una Cookie no puede ser mayor a 4096 bytes (el tamaño es la suma del nombre de la Cookie, el valor y sus atributos).
* Un dominio no puede tener más de 50 Cookies.
* Un navegador no puede almacenar más de 3000 Cookies.
