# Directivas y valores de la cabecera CSP

* La CSP tiene distintas directivas que se pueden utilizar para especificar las reglas para cargar recursos en una página web. Las directivas permiten acceder a todo tipo de recursos por defecto si no se especifica lo contrario, por ese motivo es útil utilizar la directiva `default-src`. A continuación se mostraran algunas de las directivas mas comunes:

|Directiva|Descripción|
|:--:|:--:|
|default-src|Permite cargar todos los tipos de recursos desde los orígenes especificados, a menos que se especifique lo contrario en otras directivas.|
|script-src|Esta directiva define que recursos JavaScript se cargan en el navegador.|
|img-src|Define que fuentes de imágenes son válidas.|
|style-src|Especifica que elementos CSS y stylesheets puede cargar el navegador.|
|font-src|Se utiliza para definir que fuentes (como archivos WOFF o TTF) puede utilizar l'aplicación web.|
|connect-src|Determina a que orígenes pueden realizarse peticiones del tipo `XMLHttpRequest (AJAX)`, `WebSocket`, `fetch()`, `<a ping>` y `EventSource`. En caso que el origen al que se realice la petición no este definido, el navegador emulará que la respuesta ha sido un código HTTP 400.|
|form-action|Especifica que orígenes pueden utilizarse en el atributo `action` de los formularios HTML (`<form>`).|

## Valores de las directivas

* La CSP define uno o mas valores a cada directiva para definir los orígenes asocia a cada directiva.

|Valor|Descripción|
|:--:|:--:|
|`*`|El valor `*` permite cargar contenido desde cualquier origen, como podría ser `https://domain.tbl` o bien desde la misma aplicación web.|
|`'none'`|Por el contrario, el valor `'none'` evita que se cargue contenido desde cualquier origen.|
|`'self'`|Permite cargar recursos únicamente desde la misma aplicación web, por ejemplo, no se podría cargar un recurso del origen `https://domain.tbl`.|
|`https://domain.tbl`|En este caso tenemos como valor una URL, esto significa que los recursos solamente se podrán cargar si provienen de esa URL.|
|`'unsafe-inline'`|El valor `'unsafe-inline'` permite ejecutar código inline de JavaScript o CSS. Un ejemplo de código inline podría ser `<form onsubmit="alert(1)">`. Este valor solo puede ser utilizado por las directivas `script-src` y `style-src`.|
|`'unsafe-eval'`|Por último, este valor permite que se ejecute la función `eval()` en el código JavaScript. Cabe destacar que este valor es único para la directiva `script-src`.|

* :warning: Hay que resaltar que los valores `self`, `none`, `unsafe-inline` y `unsafe-eval` tienen que ir entre comillas simples para que la CSP funcione correctamente.
