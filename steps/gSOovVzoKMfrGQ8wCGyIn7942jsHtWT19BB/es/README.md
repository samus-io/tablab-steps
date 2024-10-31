# Recomendaciones de la CSP

* Es recomendable utilizar siempre la directiva `default-src` para definir un valor predefinido para todas las directivas y modificar las demás directivas acorde a las necesidades de la aplicación web.
* En aplicaciones web donde no se necesita una interfaz de usuario (como las APIs) utilizar la CSP `default-src: 'none'`.

## Evitando utilizar unsafe-inline

* Se recomienda no utilizar los valores `'unsafe-inline'` y `'unsafe-eval'` ya que son considerados inseguros. Esto es debido a que la función `eval()` y el código en línea añadido en las etiquetas HTML, se utilizan para crear vulnerabilidades de `Cross-Site Scripting (XSS)`.
* El valor `'unsafe-inline'`, en especial, anula muchos beneficios de seguridad de la CSP, asi que siempre es recomendable evitarlo. Aunque a veces por el diseño de la aplicación web es imprescindible tener que utilizar este valor.
* Para evitar usar el valor `'unsafe-inline'`, hay que evitar usar eventos HTML como `onclick`, `onload`, `onerror`, etc.
* En este ejemplo se utiliza el atributo `onclick` para generar una alerta cuando el botón es presionado:

  ```html
  <!DOCTYPE html>
  <html>
  <head>
  </head>
  <body>
      <h1>Example CSP with unsafe-inline</h1>
      <button onclick="alert('Hello, World!')">Haz click</button>
  </body>
  </html>
  ```

* El código anterior tendría la siguiente CSP:

  ```
  Content-Security-Policy: default-src 'none'; script-src 'unsafe-inline'
  ```

* Para convertir este código a un código que no utilice atributos de eventos, hay que manejar el evento mediante la función de JavaScript `addEventListener`:

  ```html
  <!DOCTYPE html>
  <html>
  <head>
  </head>
  <body>
      <h1>Example CSP without unsafe-inline</h1>
      <button id="myButton">Click here</button>
      <script>
          // Add click event safely without inline JavaScript
          document.getElementById("myButton").addEventListener("click", function() {
              alert('Hello, World!');
          });
      </script>
  </body>
  </html>
  ```

* En este caso, al modificar el código eliminando el evento `onclick`, la CSP solamente necesitaría que se pudiera ejecutar código JavaScript de la misma aplicación web:

  ```
  Content-Security-Policy: default-src 'none'; script-src 'self'
  ```

* Como último recurso, si es imprescindible utilizar `unsafe-inline`, es mucho mas recomendable usar el valor `unsafe-hashes`.
