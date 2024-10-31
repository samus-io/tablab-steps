# Fundamentos de la cabecera X-Frame-Options

* La cabecera de respuesta `X-Frame-Options` se utiliza para evitar que otros orígenes puedan crear un `frame` de la aplicación web.
* Por ejemplo, si la aplicación web `https://domain.tbl` crea un `iframe` de la página `https://example.tbl`, si esta tiene configurada la cabecera `X-Frame-Options` no podría crear el `iframe`, ya que el navegador del usuario lo bloquearía.
* Esto a primera vista no parece muy importante de cara a la seguridad pero es muy útil para proteger la aplicación de vulnerabilidades como `Clickjacking` o `Cross-Site Scripting (XSS)`.
* Esta cabecera tiene unas directivas que son interpretadas por el navegador y este se encarga de tomar acciones respecto a la directiva enviada con la cabecera.
* Un ejemplo de esta cabecera sería el siguiente:

```
X-Frame-Options: DENY
```

* Aunque esta funcionalidad es mejor implementarla desde la `Content Security Policy`, se considera una buena práctica utilizarla, ya que los navegadores mas antiguos no soportan la cabecera `Content Security Policy`.

## Directivas

* La cabecera `X-Frame-Options` tiene únicamente dos directivas:
  * La directiva `DENY` que prohíbe crear un `frame` a cualquier página
  * La directiva `SAMEORIGIN` que únicamente permite crear un `frame` al mismo origen.
* Hay otra directiva con el nombre `ALLOW-FROM` que permite crear un `frame` desde las páginas que se especifiquen pero esta directiva esta considerada obsoleta. Para especificar las páginas que están permitidas crear un `frame`, es mejor utilizar la directiva `frame-ancestors` de la `Content Security Policy`.

## Recomendaciones

* Se recomienda que en caso que la aplicación web no utilice las etiquetas HTML `frame` se aplique la directiva `DENY` y en el caso que se utilice un `frame` creado por la misma aplicación web, entonces se aplique la directiva `SAMEORIGIN`.
* Si la aplicación web requiere que otro origen cree un `frame`, entonces se tiene que utilizar la `Content-Security Policy` para especificar los orígenes permitidos.
* En el caso que una aplicación web tenga la cabecera `X-Frame-Options` y `Content Security Policy` con la directiva `frame-ancestors`, siempre tendrá prioridad la cabecera `Content Security Policy` aunque la cabecera `X-Frame-Options` sea mas restrictiva.
