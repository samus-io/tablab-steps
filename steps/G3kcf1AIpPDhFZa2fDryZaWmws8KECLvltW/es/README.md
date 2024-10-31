# Cómo ver las cabeceras de una respuesta HTTP en Google Chrome

* Las cabeceras de respuesta son elementos esenciales en la comunicación entre un servidor web y un cliente. Estas cabeceras son parte fundamental de la respuesta que el servidor envía al cliente después de recibir una solicitud HTTP. Su contenido proporciona información crucial sobre la respuesta, lo que permite que el cliente interprete y procese adecuadamente los datos recibidos.
* Estas cabeceras proporcionan información sobre la respuesta en sí, como su estado, tipo de contenido, longitud y más. Se incluyen en la parte superior de la respuesta HTTP antes del cuerpo de la respuesta.
* Otro uso que se les da a las cabeceras de respuesta es mejorar la seguridad de la aplicación web en el lado del cliente, con las cabeceras como `Content-Security-Policy`, `Referrer-Policy` o `Strict-Transport-Security`.
* Para ver las cabeceras de respuesta de una aplicación web, hay que acceder a la consola de desarrollador con la tecla `F12` y seleccionar el apartado `Network`.
* Finalmente, hay refrescar la página para que la consola del navegador obtenga todas las peticiones. Posteriormente hay que seleccionar la petición la cual se quiere obtener las cabeceras de respuesta:

![Developer Console Header Response][1]

[1]: /static/images/learning/developer-console-network.png
