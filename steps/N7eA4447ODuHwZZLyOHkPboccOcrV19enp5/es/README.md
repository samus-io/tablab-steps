# Ejemplos de la cabecera CSP

* Una vez entendido el funcionamiento, las directivas y los valores de la CSP, se mostraran algunos ejemplos de como crearla, repasando las directivas y valores explicados anteriormente.
* La primera directiva que se añade al crear una CSP es la `default-src`, ya que esta define que orígenes pueden acceder por defecto a recursos, a menos que se especifique lo contrario en otras directivas. Por lo general el valor de esta directiva será `'none'` para luego especificar en cada directiva que orígenes pueden cargar cada recurso.
* La siguiente CSP permite a la propia aplicación web y al origen `domain.tbl` cargar código JavaScript. Además, permite añadir código inline y ejecutar la función `eval()`:

  ```
  default-src: 'none'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://domain.tbl
  ```

* Un ejemplo de código que podría ser cargado con esta CSP sería el siguiente:

  ```html
  <!DOCTYPE html>
  <html>
    <head>
      <script src=https://domain.tbl/script.js></script>
    </head>
    <body>
      <script>
        alert(eval(2 + 2))
      </script>
      <div onload=alert("Hello!")>Hello!</div>
    </body>
  </html>
  ```

* Si se añadiera código CSS y fuentes de texto al código anterior, habría que modificar la CSP, un ejemplo de código podría ser el siguiente:

  ```html
  <!DOCTYPE html>
  <html>
    <head>
      <script src=https://domain.tbl/script.js></script>
      <style>
        @font-face {
          font-family: 'ExternalFont';
          src: url('https://example.tbl/fonts/font.ttf');
        }
        div {
            color: blue;
        }
    </style>
    </head>
    <body>
      <script>
        alert(eval(2 + 2))
      </script>
      <div onload=alert("Hello!")>Hello!</div>
    </body>
  </html>
  ```

* Para que el código que se ha añadido no sea bloqueado por el navegador, se tiene que modificar la CSP y añadir las siguientes directivas:

  ```
  default-src: 'none'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://domain.tbl; style-src 'self'; font-src https://example.tbl/ 
  ```
