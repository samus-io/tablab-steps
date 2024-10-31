# Fundamentos de *URL encoding*

* Según se define en el [RFC 3986][1], las URIs transmitidas a través de Internet deben estar compuestas únicamente por caracteres pertenecientes al estándar de codificación ASCII.
* De esta forma, existe una restricción de caracteres que se pueden usar en una URL, ya que una URL es simplemente un subtipo específico de URI.

> :older_man: ASCII fue el primer conjunto de caracteres (estándar de codificación) utilizado entre computadoras en Internet.

* La siguiente tabla define la necesidad de codificación de diversos caracteres pertenecientes al estándar ASCII en base a cuatro agrupaciones:

  |Clasificación|Conjunto de caracteres|Descripción|Codificación requerida|
  |:--:|:--:|:--:|:--:|
  |Safe characters|`[a-zA-z]`, `[0-9]`, *Unreserved characters* y *Reserved characters* (cuando estos últimos se utilizan para su propósito reservado)|Están permitidos en una URI|No|
  |Unreserved characters|`-` `.` `_` `~`|Están permitidos en un URI pero dado que no tienen un propósito reservado se definen como *Unreserved characters*|No|
  |Reserved characters|`:` `/` `?` `#` `[` `]` `@` `!` `$` `&` `"` `(` `)` `*` `+` `,` `;` `=`|Tienen un propósito específico|Sí, cuando **no** se utilizan para su propósito reservado|
  |Unsafe characters|`"` `<` `>` `%` `{` `}` `\|` `\` `^` y espacio en blanco/vacío (` `)|Estos caracteres pueden resultar *unsafe* por varias razones, aunque en general se debe a que pueden ser interpretados de forma diferente o incluso modificados por los agentes de transporte intermediarios (ej., los espacios finales de una URL pueden ser eliminados)|Sí|

* Los caracteres de tipo *Non-ASCII*, *Unsafe characters* y *Reserved characters* (cuando estos últimos **no** se utilizan para su propósito reservado) tienen que ser codificados mediante el mecanismo *Percent-encoding*, también denominado *URL encoding*, que consiste en bloques formados por el caracter `%` seguido de dos dígitos hexadecimales:
  |Tipo|Carácter|Propósito en URI|Codificación|
  |:--:|:--:|:--:|:--:|
  |Reserved character|`/`|Delimita segmentos de ruta en el *URL-path*|`%2F`|
  |Reserved character|`?`|Delimita el inicio de la cadena de consulta|`%3F`|
  |Reserved character|`#`|Delimita el identificador de fragmento|`%23`|
  |Reserved character|`&`|Separa elementos de consulta|`%26`|
  |Reserved character|`+`|Indica un espacio. Alternativa a espacio en blanco/vacío (` `, `%20`)|`%2B`|
  |Non-ASCII|`ö`|Ninguno|`%C3%B6`|
  |Non-ASCII|`ڃ`|Ninguno|`%DA%83`|
  
  * El carácter reservado `/`, por ejemplo, cuando es usado como parte de la sintaxis de definición de una URI tiene el significado especial de ser un delimitador entre segmentos de ruta. Ahora bien, si, de acuerdo con un esquema de URI en particular, el carácter `/` debe incluirse en el componente *path* como meramente un valor, entonces se debe usar los tres caracteres `%2F` (o `%2f`) en su lugar para que no sea interpretado propiamente como delimitador.
  * Por otro lado, para los caracteres pertenecientes al estándar Unicode, se decidió que la codificación URL a emplear debía ser en el sistema de codificación UTF-8. En efecto, el carácter `ö` se URL-codifica como `%C3%B6`, ya que en el sistema UTF-8 tiene el valor hexadecimal de `0xC3 0xB6`.

> :warning: Aunque la codificación URL parece ser una función de seguridad, no lo es. En otras palabras, no aporta beneficios en referencia a la seguridad de las aplicaciones de ningún tipo.

[1]: https://datatracker.ietf.org/doc/html/rfc3986
