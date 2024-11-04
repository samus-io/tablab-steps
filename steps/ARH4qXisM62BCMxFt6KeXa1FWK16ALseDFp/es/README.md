# Fundamentos de la cabecera CSP

* La cabecera `Content Security Policy (CSP)` es un mecanismo de seguridad que permite a los desarrolladores de aplicaciones web especificar los recursos (como scripts, imágenes, estilos, etc.) desde los cuales una página web puede cargar contenido. Esta cabecera se envía como cabecera de respuesta de la aplicación web y es interpretada por el navegador del usuario.
* La CSP es muy útil para prevenir ataques de inyección de código malicioso, como `Cross-Site Scripting (XSS)`, ya que solo se permite que el contenido se cargue desde orígenes confiables.
* Cuando un navegador recibe una CSP, verifica si el contenido que se está cargando cumple con las reglas establecidas en la cabecera. Si no se cumplen, el navegador bloquea la carga del contenido no especificado en la CSP y muestra un error en la consola de desarrollador, esto es muy útil para saber cuando se esta bloqueando recursos que son confiables y por lo tanto, hay que modificar la CSP.
* Cabe mencionar que no todos los navegadores soportan la CSP, pero los navegadores modernos si lo hacen, y su uso es muy recomendado en cualquier aplicación web para mejorar la seguridad y prevenir vulnerabilidades.

![content-security-policy-graphical-representation.png][1]

* En esta imagen se puede observar como la CSP tiene definida que solo los recursos de la URL `http://example.com` se puedan añadir, por lo tanto, cuando se intenta realizar la petición a `http://malicious.com` desde la aplicación web para cargar un recurso JavaScript, esta petición es bloqueada, previniendo que se ejecute código JavaScript malicioso en el navegador del usuario.

## Partes de la CSP

* La CSP está formada por dos partes, la primera llamada directiva y la segunda el valor de la misma.
* La directiva es una regla que hace referencia a un tipo de recurso, como puede ser imágenes, archivos JavaScript o CSS, conexiones del lado del cliente entre páginas web, frames, etc.
* Por otro lado, el valor es una cadena de texto que esta asociado a una directiva y este indica desde que orígenes se pueden cargar recursos en la aplicación web. En este ejemplo hay diferentes directivas y cada una de ellas tiene asociado uno o varios valores:

  ```
  Content-Security-Policy: default-src 'self'; script-src 'unsafe-inline' 'unsafe-eval' https://example.com; img-src *; style-src 'none'; font-src 'self'; connect-src 'none'
  ```
  
* Al implementar una cabecera CSP se define una lista de orígenes permitidos para todos los tipos de recurso que la aplicación web utiliza y restringe los demás, de esta forma se pueden evitar vulnerabilidades del lado del cliente.

[1]: /static/images/content-security-policy-graphical-representation.png
