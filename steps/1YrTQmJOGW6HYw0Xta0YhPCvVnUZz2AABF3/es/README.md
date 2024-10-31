# Divulgación de información a través de las cabeceras de respuesta

* Cuando se utiliza un servidor web, como por ejemplo `Apache`, este por defecto añadirá la cabecera de respuesta `Server` a todas las peticiones que se envíen. No solo los servidores web incluyen cabeceras, también hay Frameworks o lenguajes de programación que las incluyen, como es el caso de PHP en la cabecera `X-Powered-By`.
* La cabecera `Server` normalmente tiene como valor el servidor web que se esta utilizando y su versión.
* Desde el punto de vista de la seguridad esto puede tener como consecuencia que un adversario pueda encontrar vulnerabilidades asociadas a esa versión.
* Para evitar esta fuga de información, la mejor recomendación es eliminar estas cabeceras.
* En la siguiente imagen se puede observar las cabeceras de respuesta de una aplicación web que deja al descubierto que servidor web utiliza y su versión:
![Server Header of Apache][1]

[1]: /static/images/learning/apache-server-header.png
