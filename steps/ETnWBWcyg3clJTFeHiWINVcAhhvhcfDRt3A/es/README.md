# Chuleta de RegEx

## Anclajes

  |Composición|Resumen|Descripción|Ejemplo|
  |:--:|:--:|:--:|:--:|
  |`^`|Inicio de entrada|Coincide con la posición al principio de la entrada|`^a` encuentra *a* en "apple" pero no encuentra *a* en "facebook"|
  |`$`|Final de entrada|Coincide con la posición al final de la entrada|`t$` no encuentra *t* en "eater", pero encuentra *t* en "eat"|
  |`\b`|Inicio de palabra|Coincide con un límite de palabra (el principio o el final de una palabra)|`er\b` encuentra *er* en "never" pero no *er* en "verb"|
  |`\B`|Final de palabra|Coincide con todo excepto un límite de palabra|`ear\B` encuentra *ear* en "never early"|

## Clases de caracteres

  |Composición|Resumen|Descripción|Ejemplo|
  |:--:|:--:|:--:|:--:|
  |`\d`|0 a 9|Coincide con un carácter numérico|`\d` encuentra *5* en "Room 5 is ready"|
  |`\D`|Equivalente a `[^\d]`|Coincide con un carácter no numérico|`\D` encuentra *#* en "#1"|
  |`\w`|Equivalente a `[A-Za-z0-9_]`|Coincide con cualquier carácter alfanumérico o guión bajo|`\w` encuentra *f* en "facebook", *7* en "#7" y *m* en "Émanuel"|
  |`\W`|Equivalente a `[^A-Za-z0-9_]`|Coincide con cualquier carácter que no sea alfanumérico o guión bajo|`\W` encuentra *%* en "100%" y *É* en "Émanuel"|
  |`\s`|Equivalente a `[\f\n\r\t\v\u0020\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff]`|Coincide con cualquier espacio en blanco (*espacio*, *tabulación*, *nueva línea*)|`\s` encuentra " " en "foo bar"|
  |`\S`|Equivalente a `[^\s]`|Coincide con cualquier carácter que no sea un espacio en blanco|`\S` encuentra *foo* y *bar* en "foo bar"|

## Grupos y rangos

  |Composición|Resumen|Descripción|Ejemplo|
  |:--:|:--:|:--:|:--:|
  |`.`|Cualquier carácter excepto *nueva línea*|Coincide con cualquier carácter, excepto los terminadores de línea como `\n`, `\r`, `\u2028` o `\u2029`|`.y` encuentra *my* y *ay*, pero no *yes*|
  |`[]`|Caracteres adjuntos|Coincide con cualquiera de los caracteres incluidos|`[abc]` encuentra *a* en "rat"|
  |`[^]`|Negación de caracteres adjuntos|Coincide con cualquier carácter que no esté incluido|`[^abc]` encuentra *r* y *t* en "rat"|
  |`()`|Agrupación y captura|Coincide con un patrón y recuerda la coincidencia|`(a\|b\|cd)\1` encuentra *aa*, *bb* o *cdcd*. `(a\|b\|cd)` es un grupo de captura, y `\1` es una retro-referencia que coincide con el texto exacto que fue capturado|

## Afirmaciones

  |Composición|Resumen|Descripción|Ejemplo|
  |:--:|:--:|:--:|:--:|
  |`\|`|OR|Combina varias expresiones en una que coincide con cualquiera de las individuales|`(t\|z)oo` encuentra *too* o *zoo*|

## Cuantificadores

  |Composición|Resumen|Descripción|Ejemplo|
  |:--:|:--:|:--:|:--:|
  |`*`|0 o más|Coincide con el elemento precedente (carácter o grupo) 0 o más veces|`zo*` encuentra tanto *z* como *zoo*|
  |`+`|1 o más|Coincide con el elemento precedente (carácter o grupo) 1 o más veces|`zo+` encuentra *zo* o *zoo*, pero no *z*|
  |`?`|0 o una vez|Coincide con el elemento precedente (carácter o grupo) 0 o una vez|`zo?` encuentra *zo* en "zoo"|
  |`{n}`|*n* veces|Coincide con el carácter precedente exactamente *n* veces|`o{2}` no encuentra *o* en "Bob", pero encuentra las primeras dos *o*'es en "foooood"|
  |`{n,}`|Al menos *n* veces|Coincide con el carácter precedente al menos *n* veces. `o{0,}` es equivalente a `o*` y `o{1,}` es equivalente a `o+`|`o{2,}` no encuentra *o* en "Bob" encuentra todas las *o*'es en "foooood"|
  |`{n,m}`|Al menos *n*, como máximo *m* veces|Coincide con el carácter precedente al menos *n* y como máximo *m* veces. `o{0,1}` es equivalente a `o?`|`o{1,3}` encuentra las primeras tres *o*'es en "fooooood"|

## Metacaracteres

* Los caracteres `.[{()\^$|?*+<>` necesitan ser escapados para ser interpretados como caracteres regulares. El carácter de escape suele ser `\`.
