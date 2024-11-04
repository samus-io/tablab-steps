# Validación mediante lista de permitidos

* La validación mediante lista de permitidos, antes conocida como validación de lista blanca o *whitelist*, es una práctica de seguridad fundamental que se emplea para especificar explícitamente las entradas de datos aceptables y rechazar todo lo que no se encuentre explícitamente listado.

![Allow-list validation overview][1]

* Consiste en definir una lista de valores o caracteres permitidos que se consideran seguros o válidos. De esta forma, cualquier entrada que no coincida con los elementos de la lista se rechaza para garantizar la integridad y seguridad de los datos.
* Este enfoque puede utilizarse para mitigar diversos riesgos de seguridad, como los ataques de inyección y los accesos no autorizados.

## Entendiendo la validación mediante lista de permitidos

* La validación mediante lista de permitidos funciona según el principio de **aceptación explícita**, por lo que en lugar de intentar identificar y rechazar entradas maliciosas, se centra en definir un conjunto de entradas permitidas y denegar el resto.
* Al especificar explícitamente lo que está permitido, la validación de listas permitidas ayuda a mitigar una amplia gama de riesgos de seguridad, proporcionando muchos **beneficios de seguridad**.
* Garantiza que los datos de entrada **se adhieran a los formatos establecidos**, reduciendo la probabilidad de que se introduzcan en el sistema datos malformados o incorrectos.

## Estrategias de implementación

* **Definir una lista de valores** es el método más sencillo, el cual consiste en utilizar listas de valores o caracteres permitidos para validar las entradas comprobando su existencia en dichas listas.
* **Utilizar expresiones regulares** ofrece un enfoque alternativo al establecer un patrón que aprueba específicamente ciertos valores y excluye el resto.

## Escenarios prácticos

* Seguidamente se muestran algunos fragmentos de código que ilustran diversos casos de uso.

### Restricción de extensión de ficheros

* Garantizar únicamente determinadas extensiones de archivos.

@@TagStart@@java

#### Fragmentos de código en Java

* Se define un *set* denominado `allowedFileExtensions` que contiene las extensiones de archivo permitidas. A continuación, el método estático `isAllowedFileExtension` recupera el segmento de extensión de archivo de un nombre de fichero y verifica su presencia en la lista de extensiones de archivo permitidas:

  ```java
  import java.util.Set;

  public class FileExtensionValidator {

      private static final Set<String> allowedFileExtensions = Set.of(".jpg", ".jpeg", ".png");

      public static boolean isAllowedFileExtension(String filename) {
          int lastDotIndex = filename.lastIndexOf('.');
          if (lastDotIndex == -1) return false; // No extension found

          String extension = filename.substring(lastDotIndex);

          return allowedFileExtensions.contains(extension);
      }
  }
  ```

* Se puede utilizar como se muestra a continuación:

  ```java
  public static void main(String[] args) {
      String filename = "photo.webp";

      if (!FileExtensionValidator.isAllowedFileExtension(filename)) {
          System.out.println("File type not allowed.");
      }
  }
  ```

@@TagEnd@@
@@TagStart@@node.js

#### Fragmentos de código en Node.js

* Se define una matriz denominada `allowedFileExtensions` que contiene las extensiones de archivo permitidas. A continuación, la función `isAllowedFileExtension` recupera el segmento de extensión de archivo de un nombre de fichero y verifica su presencia en la lista de extensiones de archivo permitidas:

  ```javascript
  const allowedFileExtensions = [".jpg", ".jpeg", ".png"];

  function isAllowedFileExtension(filename) {
    const lastDotIndex = filename.lastIndexOf(".");
    if (lastDotIndex === -1) return false; // No extension found

    const extension = filename.slice(lastDotIndex);

    return allowedFileExtensions.includes(extension);
  }
  ```

* Se puede utilizar como se muestra a continuación:

  ```javascript
  const filename = "photo.webp";

  if (!isAllowedFileExtension(filename)) {
    console.log("File type not allowed.");
  }
  ```

@@TagEnd@@

### Validación del dominio de correo electrónico

* Permitir determinados dominios de correo electrónico para el registro o el acceso a ciertos servicios.

@@TagStart@@java

#### Fragmentos de código en Java

* Se define un *set* denominado `allowedEmailDomains` que contiene los dominios de correo electrónico permitidos. A continuación, el método estático `isAllowedEmail` recupera el segmento de dominio de una dirección de correo electrónico y verifica su presencia en la lista de dominios permitidos:

  ```java
  import java.util.Set;

  public class EmailValidator {

      private static final Set<String> allowedEmailDomains = new Set.of("example.tbl", "domain.tbl", "trusted.tbl");

      public static boolean isAllowedEmail(String email) {
          String domain = email.substring(email.lastIndexOf("@") + 1);

          return allowedEmailDomains.contains(domain);
      }
  }
  ```

* Se puede utilizar como se muestra a continuación:

  ```java
  public static void main(String[] args) {
      String email = "user@untrusted.tbl";

      if (!EmailValidator.isAllowedEmail(email)) {
          System.out.println("Email domain not allowed.");
      }
  }
  ```

@@TagEnd@@
@@TagStart@@node.js

#### Fragmentos de código en Node.js

* Se define una matriz denominada `allowedEmailDomains`, que contiene los dominios de correo electrónico permitidos. A continuación, la función `isAllowedEmail` recupera el segmento de dominio de una dirección de correo electrónico y verifica su presencia en la lista de dominios permitidos:

  ```javascript
  const allowedEmailDomains = ["example.tbl", "domain.tbl", "trusted.tbl"];

  function isAllowedEmail(email) {
    const domain = email.split("@").pop();
    
    return allowedEmailDomains.includes(domain);
  }
  ```

* Se puede utilizar como se muestra a continuación:

  ```javascript
  const email = "user@untrusted.tbl";

  if (!isAllowedEmail(email)) {
    console.log("Email domain not allowed.");
  }
  ```

@@TagEnd@@

### Limitación a un conjunto específico de valores mediante expresiones regulares

* Se considera un ejemplo en el que una aplicación únicamente permite determinadas abreviaturas de estados de los EEUU.

@@TagStart@@java

#### Fragmentos de código en Java

* El `stateAbbreviationsPattern` representa una lista permitida creada con RegEx para las abreviaturas de los estados de EEUU. A continuación, el método estático `isAllowedStateAbbreviation` comprueba si una abreviatura dada coincide con el patrón, devolviendo `true` en caso afirmativo y `false` en caso contrario:

  ```java
  public class StateAbbreviationValidator {

    private static final Pattern stateAbbreviationsPattern = Pattern.compile("^(AA|AE|AP|AL|AK|AS|AZ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)$");
  
    public static boolean isAllowedStateAbbreviation(String abbreviation) {
        Matcher matcher = stateAbbreviationsPattern.matcher(abbreviation);

        return matcher.matches();
    }
  }
  ```

* Se puede utilizar como se muestra a continuación:

  ```java
  public static void main(String[] args) {
      String abbreviation = "XYZ";

      if (!StateAbbreviationValidator.isAllowedStateAbbreviation(abbreviation)) {
          System.out.println("Abbreviation not allowed.");
      }
  }
  ```

@@TagEnd@@
@@TagStart@@node.js

#### Fragmentos de código en Node.js

* El `stateAbbreviationsPattern` representa una lista permitida creada con RegEx para las abreviaturas de los estados de EEUU. A continuación, la función `isAllowedStateAbbreviation` comprueba si una abreviatura dada coincide con el patrón, devolviendo `true` en caso afirmativo y `false` en caso contrario:

  ```javascript
  const stateAbbreviationsPattern = /^(AA|AE|AP|AL|AK|AS|AZ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)$/;

  function isAllowedStateAbbreviation(abbreviation) {
    return stateAbbreviationsPattern.test(abbreviation);
  }
  ```

* Se puede utilizar como se muestra a continuación:

  ```javascript
  const abbreviation = "XYZ";

  if (!isAllowedStateAbbreviation(abbreviation)) {
    console.log("Abbreviation not allowed.");
  }
  ```

@@TagEnd@@

### Consultas SQL dinámicas con valores no parametrizables

* Según OWASP, puede haber casos poco frecuentes en los que deban definirse consultas SQL dinámicas y los valores que deben ser dinámicos no puedan establecerse como parámetros, como los nombres de las tablas o el indicador de orden de clasificación.

@@TagStart@@java

#### Fragmentos de código en Java

* El método estático `isAllowedTableName` comprueba si un nombre de tabla dado coincide con alguno de los permitidos, devolviendo `true` en caso afirmativo y `false` en caso contrario, y el método estático `getAllowedSortOrder` asegura la obtención del valor de ordenación apropiado para incorporar a la consulta SQL:

  ```java
  public class QueryParamsValidator {
  
    public static boolean isAllowedTableName(String tableName) {
        switch (tableName) {
            case "Format":
            case "Level":
            case "Property":
                return true;
            default:
                return false;
        }
    }

    public static String getAllowedSortOrder(boolean sortOrder) {
        return sortOrder ? "ASC" : "DESC";
    }
  }
  ```

* Ambos se pueden utilizar como se muestra a continuación:

  ```java
  public static void main(String[] args) {
      String tableName = "Condition";
      boolean sortOrder = true;

      if (!QueryParamsValidator.isAllowedTableName(tableName)) {
          System.out.println("Table name not allowed.");
      }

      System.out.println("Order query results using '" + QueryParamsValidator.getAllowedSortOrder(sortOrder) + "'");
  }
  ```

@@TagEnd@@
@@TagStart@@node.js

#### Fragmentos de código en Node.js

* La función `isAllowedTableName` comprueba si un nombre de tabla dado coincide con alguno de los permitidos, devolviendo `true` en caso afirmativo y `false` en caso contrario, y la función `getAllowedSortOrder` garantiza la obtención del valor de ordenación adecuado para incorporarlo a la consulta SQL:

  ```javascript
  function isAllowedTableName(tableName) {
    switch (tableName) {
      case "Format":
      case "Level":
      case "Property":
        return true;
      default:
        return false;
    }
  }

  function getAllowedSortOrder(sortOrder) {
    return sortOrder ? "ASC" : "DESC";
  }
  ```

* Ambas se pueden utilizar como se muestra a continuación:

  ```javascript
  const tableName = "Condition";
  const sortOrder = true;

  if (!isAllowedTableName(tableName)) {
    console.log("Table name not allowed.");
  }

  console.log(`Order query results using '${getAllowedSortOrder(sortOrder)}'`);
  ```

@@TagEnd@@

### Entradas de formularios de aplicaciones web

* Limitar los valores aceptables para un menú desplegable html a opciones predefinidas fomenta que únicamente se envíen selecciones válidas, lo que no es seguro desde el punto de vista de la seguridad pero contribuye al proceso:

  ```html
  <select name="payment_method" required>
    <option value="credit_card">Credit Card</option>
    <option value="paypal">PayPal</option>
    <option value="bank_transfer">Bank Transfer</option>
  </select>
  ```

  > :warning: La validación de la entrada de datos en el *frontend* no aporta ventajas de seguridad debido a la posible manipulación del código, pero facilita otras tareas de normalización y validación de datos y suele mejorar la experiencia del usuario.

[1]: /static/images/allow-list-validation-overview.png
