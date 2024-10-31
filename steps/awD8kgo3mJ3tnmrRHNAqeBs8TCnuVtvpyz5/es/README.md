# Cómo generar la CSP

* La CSP también tiene un mecanismo de reporte de violación, que permite a los desarrolladores recibir informes sobre cualquier violación de la política y tomar medidas para solucionarlo. Para utilizar este mecanismo hay que usar la directiva `report-uri` donde como valor se especifica la ubicación que se enviaran los informes. Estos informes se envían con una petición POST a la ruta especificada y en un objecto JSON.
* Un ejemplo de uso de esta directiva sería el siguiente:

  ```
  default 'none'; report-uri https://domain.tbl/csp-reports
  ```

* El objeto JSON recibido por el endpoint contiene los siguientes campos:

  ```json
  {
    "csp-report": {
      "document-uri": "http://domain.tbl/signup.html",
      "referrer": "http://example.tlb/haxor.html",
      "blocked-uri": "http://example.tlb/injected.png",
      "violated-directive": "img-src https://example.tlb",
      "original-policy": "default-src 'self'; img-src 'self' https://example.tlb; report-uri https://domain.tbl/csp-reports",
    }
  }
  ```

* Cuando la CSP bloquea algún recurso de ser cargado de la aplicación web, muestra un mensaje por la consola de desarrollador, como se observa en la siguiente imagen:

![CSP Console Error][4]

* En este caso se esta advirtiendo que el código JavaScript de `https://tablab.io/script.js` no está pudiendo cargar su contenido debido a que la Content Security Policy tiene la directiva `default-src 'none'`.
* También muestra que no es possible utilizar estilo inline ni JavaScript inline, en este caso el navegador recomienda que añadamos la directiva `'unsafe-inline'` en el `script-src` y `style-src` o bien que se utilice la directiva `unsafe-hashes` con el hash SHA-256 del código en cuestión.

## Generar la CSP mediante la extensión Laboratory

* Implementar la CSP manualmente en una aplicación web puede llegar a ser un trabajo muy tedioso y difícil, para ello se puede utilizar la extensión del navegador [Laboratoy (Content-Security Policy/CSP Toolkit)][1] que genera automáticamente la CSP de una aplicación web.
* La extensión Laboratoy básicamente guarda todos los recursos que son cargados por la página y aplica las directivas correspondientes para que funcione correctamente.
* Después de que se haya descargado la extensión, para usarla solo hay que habilitar la opción de `Record this site` y recorrer toda la aplicación web y utilizar todas sus funcionalidades para que la extensión genere la CSP correspondiente.
* Hay que destacar que una vez se selecciona esta opción, hay que recargar la página actual para que cargue los recursos de esta.

![Laboratory Extension][2]

* En el apartado `Configuration` hay que seleccionar la opción `'self' if same origin, otherwise origin` para todas las directivas, de esta manera solo se añadirá el origen en la CSP en vez de toda la ruta. Se selecciona esta opción para evitar tener muchos cambios en la CSP cada vez que se modifica la aplicación web.

![Laboratory Extension Configuration][3]

* Una vez generada, para comprobar que se ha creado correctamente, hay que habilitar la opción de `Enforce CSP policy` de esta forma se aplicará la CSP generada para comprobar si hay algún error. Posteriormente se procede a visitar toda la aplicación web para detectar posibles recursos que no sean cargados en la aplicación web.
* Finalmente cuando ya se ha comprobado que la CSP se ha generado correctamente, se procede a copiar el valor de la CSP con el botón `Copy`.

[1]: https://chrome.google.com/webstore/detail/laboratory/mjcamldajgnpgjcpacomkgfhccnibldg
[2]: /static/images/learning/laboratory-image.png
[3]: /static/images/learning/laboratory-record-site.png
[4]: /static/images/learning/csp-console-error.png
