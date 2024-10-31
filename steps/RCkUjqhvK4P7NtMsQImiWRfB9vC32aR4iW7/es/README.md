# Validación con RegEx

* Las expresiones regulares, en Inglés `Regular Expressions (RegEx)`, son esenciales en el desarrollo de software para la comparación y validación de patrones, lo que hace que se utilicen ampliamente para garantizar que los datos proporcionados por el usuario se ajustan a criterios específicos.

## Perspectiva de vulnerabilidad de ReDos

* El uso de RegEx complejas debe ser abordado con precaución debido al riesgo potencial de una vulnerabilidad de `Regular expression Denial of Service (ReDoS)`, la cual puede ocurrir cuando la entrada maliciosa hace que el motor RegEx se ejecute de manera ineficiente, derivando a una denegación de servicio.

## Validaciones RegEx comunes

* El sitio web [ihateregex.io][1] proporciona varios patrones de expresiones regulares que son frecuentemente utilizados en el desarrollo web. Algunos de ellos se muestran a continuación.

### Caracteres alfanuméricos (sin espacios)

* Garantiza que una cadena sólo contenga caracteres alfanuméricos (letras y dígitos) sin espacios, permitiendo una cadena vacía:

  ```regex
  ^[a-zA-Z0-9]*$
  ```

### Número entero positivo

* Coincide con una cadena que contiene exclusivamente uno o más dígitos:

  ```regex
  ^\d+$
  ```

### Contraseña

* Mínimo ocho caracteres, al menos una letra mayúscula, una letra minúscula, un número y un carácter especial:

  ```regex
  ^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$
  ```

### Email validación simple

* Es importante tener en cuenta que la validación de un correo electrónico mediante expresiones regulares puede ser complicada debido a los distintos formatos permitidos, pero seguidamente se presenta una expresión regular sencilla que resulta efectiva en la gran mayoría de casos:

  ```regex
  ^[^\s@]+@[^\s@]+\.[^\s@]+$
  ```

### Email validación compleja

* El sitio web [emailregex.com][2] ofrece una expresión regular que funciona bien en el 99,99% de los casos según la especificación oficial de direcciones de correo electrónico [RFC 5322][3]:

  ```regex
  (?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])
  ```

### Direcciones IPv4

* Verifica que una dirección IP consta de 4 conjuntos de números (0-255) separados por puntos:

  ```regex
  ^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$
  ```

### Puerto TCP/UDP

* Garantiza que el número de puerto proporcionado está comprendido entre 1 y 65535:

  ```regex
  ^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$
  ```

### URL

* Compara las URL mediante el reconocimiento opcional de los protocolos "http" o "https" seguidos de "www." y, a continuación, captura los nombres de dominio con caracteres válidos y los dominios de nivel superior (de 2 a 6 letras), incluidos los componentes de URL posteriores, como rutas y cadenas de consulta:

  ```regex
  (https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)
  ```

### Fecha (DD/MM/AAAA)

* Siguiendo el formato `DD/MM/AAAA`, comprueba que el día esté comprendido entre el 01 y el 31, el mes entre el 01 y el 12, y el año sea un número de cuatro dígitos que empiece por 19 o 20:

  ```regex
  \b(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)\d{2}\b
  ```

### HH:MM (12 horas)

* Comprueba una hora en el formato de 12 horas, asegurándose de que la hora está entre 01 y 12 y los minutos entre 00 y 59. Los ceros a la izquierda para las horas de un solo dígito son opcionales:

  ```regex
  ^(0?[1-9]|1[0-2]):[0-5][0-9]$
  ```

### Número de teléfono con código de país

* Valida un número de teléfono internacional confirmando que el número empieza por el signo `+`, seguido de un código de país válido y con un máximo de 15 dígitos:

  ```regex
  \+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$
  ```

### IBAN

* Concuerda con un número de International Bank Account Number (IBAN), el cual comienza con un código de país de dos letras, seguido de dos dígitos de control e incluye hasta 30 caracteres alfanuméricos:

  ```regex
  ^([A-Z]{2}[0-9]{2})([A-Z0-9]{1,30})$
  ```

### Tarjeta de crédito

* Verifica los números de tarjetas de crédito emitidas por Visa, MasterCard, American Express, Diners Club, Discover y JCB:

  ```regex
  (^4[0-9]{12}(?:[0-9]{3})?$)|(^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$)|(3[47][0-9]{13})|(^3(?:0[0-5]|[68][0-9])[0-9]{11}$)|(^6(?:011|5[0-9]{2})[0-9]{12}$)|(^(?:2131|1800|35\d{3})\d{11}$)
  ```

## Cómo utilizar expresiones regulares

@@TagStart@@java

### Fragmento de código en Java

* El siguiente ejemplo realiza una comprobación de un formato de correo electrónico válido:

  ```java
  import java.util.regex.Pattern;
  import java.util.regex.Matcher;

  public static Boolean isValidEmail(String email) {
      Pattern pattern = Pattern.compile("^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$");
      Matcher matcher = pattern.matcher(email);

      return matcher.matches();
  }
  ```

  > :warning: En Java, las barras invertidas `\` en RegEx deben escaparse.

@@TagEnd@@
@@TagStart@@node.js

### Fragmento de código en Node.js

* El siguiente ejemplo realiza una comprobación de un formato de correo electrónico válido:

  ```javascript
  function isValidEmail(email) {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    return pattern.test(email);
  }
  ```

@@TagEnd@@

[1]: https://ihateregex.io/
[2]: https://emailregex.com/
[3]: https://www.ietf.org/rfc/rfc5322.txt
