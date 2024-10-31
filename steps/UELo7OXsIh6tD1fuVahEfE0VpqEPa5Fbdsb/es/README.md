# Validación de datos en Java Jakarta utilizando Jakarta Bean Validation

* Java Jakarta proporciona diversas herramientas y librerías que facilitan la validación sintáctica garantizando una gestión de la calidad del código sólida y eficaz.

## ¿Qué es Jakarta Bean Validation?

* `Jakarta Bean Validation` es un framework dentro del ecosistema Jakarta EE que permite a los desarrolladores imponer restricciones a los objetos Java a través de anotaciones declarativas.
* Simplifica la lógica de validación aplicando restricciones directamente a propiedades, métodos y constructores.
* Garantiza que los datos cumplen unas normas predefinidas antes de ser procesados, mejorando la integridad de los mismos y reduciendo los errores de programación al automatizar las comprobaciones de validación dentro de la aplicación.

### Entendiendo los conceptos clave de Jakarta Bean Validation

* Una **constraint** es una regla que se adhiere a las propiedades o métodos, como la longitud de una cadena o el rango de un número entero.
* Una **annotation** es un metadato que aplica *constraints* a las propiedades, mejorando la legibilidad y el mantenimiento del código.
* **Validator** es un objeto que comprueba el cumplimiento de las restricciones definidas en cualquier objeto Java. Los validadores se crean normalmente utilizando `ValidatorFactory`, que garantiza el cumplimiento de estas restricciones durante el tiempo de ejecución.

### Caso de uso de un formulario de registro de usuarios

* Para el siguiente ejemplo se considera un formulario de registro de un sitio web en el que los usuarios se registran para obtener una cuenta. Este formulario solicita un nombre de usuario, una contraseña, un correo electrónico y la edad del usuario.
* Usando Jakarta Bean Validation se puede diseñar una clase Java para reflejar los datos de este formulario, donde sus propiedades están anotadas con reglas de validación, como se muestra a continuación:

  ```java
  import jakarta.validation.constraints.*;

  public class User {
    
      @NotBlank(message = "Username cannot be empty.")
      @Size(min = 4, max = 50, message = "Username must be between 4 and 50 characters.")
      @Pattern(regexp = "^[a-zA-Z0-9_-]*$", message = "Username must contain only letters, numbers, underscores, or hyphens.")
      private String username;

      @NotBlank(message = "Password cannot be empty.")
      @Size(min = 8, max = 80, message = "Password must be between 8 and 80 characters.")
      @Pattern(regexp = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&]).*$", 
              message = "Password must contain at least one lowercase letter, one uppercase letter, " +
                      "one number, and one special character (e.g., @, $, !, %, ?, &).")
      private String password;

      @NotBlank(message = "Email cannot be empty.")
      @Size(max = 254, message = "Email cannot be longer than 254 characters.")
      @Email(message = "Invalid email format.")
      private String email;

      @NotNull(message = "Age cannot be null.")
      @Min(value = 18, message = "You must be at least 18 years old to register.")
      private Integer age;

      // Constructors and methods
  }
  ```

  * La validación se realizará recogiendo todas las infracciones e informando de los errores si la entrada del usuario no cumple las restricciones establecidas, permitiendo un control total en su gestión:

  ```java
  import jakarta.validation.ConstraintViolation;
  import jakarta.validation.Validation;
  import jakarta.validation.Validator;
  import jakarta.validation.ValidatorFactory;

  public void registerUser(String username, String password, String email, int age){

    // Create ValidatorFactory and Validator instances
    ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
    Validator validator = factory.getValidator();

    // Create a User instance and validate its data
    User user = new User(username, password, email, age);
    Set<ConstraintViolation<User>> violations = validator.validate(user);

    // Check for constraint violations
    if (!violations.isEmpty()) {
        for (ConstraintViolation<User> violation : violations) {
            System.out.println(violation.getMessage());
        }
    } else {
        System.out.println("User is valid");
    }
  }
  ```

  * El objeto `violations` recupera todos los mensajes de error de validación generados cuando el objeto `user` no cumple ciertos criterios en el momento de su creación.

### Más definiciones de restricciones

* Seguidamente se muestra una tabla con las definiciones de *constraints* que Java Jakarta establece por defecto. Todas estas restricciones permiten un parámetro `message`, utilizado para devolver un mensaje de error si el atributo no satisface las condiciones.

  |*Annotation*|Descripción|
  |:-:|:-:|
  |`@Null`|Asegura que el elemento anotado sea nulo|
  |`@NotNull`|Asegura que el elemento anotado no sea nulo|
  |`@Min(value)`|Asegura que el elemento anotado no es menor que `value`|
  |`@Max(value)`|Asegura que el elemento anotado no es mayor que `value`|
  |`@DecimalMin(value)`|Asegura que el número anotado no es inferior al valor decimal especificado como `value`|
  |`@DecimalMax(value)`|Asegura que el número anotado no es mayor al valor decimal especificado como `value`|
  |`@Negative`|Asegura que el número anotado es estrictamente negativo|
  |`@NegativeOrZero`|Asegura que el número anotado es negativo o cero|
  |`@Positive`|Asegura que el número anotado es estrictamente positivo|
  |`@PositiveOrZero`|Asegura que el número anotado es positivo o cero|
  |`@Size(min,max)`|Limita el tamaño del elemento anotado entre `min` y `max`|
  |`@Digits(integer,fraction)`|Limita el número de dígitos de las partes enteras y fraccionarias de un número|
  |`@Past`|Asegura que el objeto `Date` anotado está en el pasado|
  |`@PastOrPresent`|Asegura que el objeto `Date` anotado está en el pasado o es el día presente|
  |`@Future`|Asegura que el objeto `Date` anotado está en el futuro|
  |`@FutureOrPresent`|Asegura que el objeto `Date` anotado está en el futuro o es el día presente|
  |`@NotEmpty`|Asegura que la colección, mapa, matriz o cadena anotada no está vacía o es nula|
  |`@NotBlank`|Asegura que la cadena anotada no es nula ni está en blanco (contiene caracteres que no son espacios en blanco)|
  |`@Email`|Asegura que la cadena anotada es una dirección de correo electrónico válida|
  |`@Pattern(regexp)`|Asegura que la cadena anotada coincide con la expresión regular especificada|
  |`@AssertTrue`|Asegura que el booleano anotado es verdadero|
  |`@AssertFalse`|Asegura que el booleano anotado es falso|

* Además de estas restricciones estándar, los desarrolladores pueden definir restricciones personalizadas creando una nueva anotación junto con el correspondiente validador de restricciones.

### Limitaciones de Jakarta Bean Validation

* Jakarta Bean Validation no puede gestionar validaciones donde la validez de un campo depende del valor de otro (validación cruzada de campos) o comprobar si la edad de una persona está dentro de un rango específico basado en su fecha de nacimiento. Este tipo de validaciones requieren una lógica personalizada que debe implementarse manualmente en el código de la aplicación.

## Ejercicio para practicar :writing_hand:

* El siguiente formulario de registro acepta datos proporcionados por el usuario sin realizar ningún tipo de validación en el servidor.
* El objectivo aquí es abrir el editor de código a través del botón `Open Code Editor` y aplicar una estrategia de validación de entrada en el lado del servidor usando `Jakarta Bean Validation`, con el objetivo de validar todos los datos introducidos en los campos del formulario.
* Más concretamente, es necesario modificar la classe `RegisterForm` que se encuentra en `src/main/java/io/ontablab/RegisterForm.java`.
* Este ejercicio solamente se puede superar si la validación de datos del lado del servidor cumple los siguientes requisitos:
  * Los campos `firstName` y `lastName` sólo aceptan caracteres alfabéticos (es decir, A-Z o a-z) de entre 2 y 50 caracteres.
  * El campo `gender` sólo acepta uno de los valores de la lista explícitamente en minúsculas (es decir, `female`, `male`, `transgender`, `non-binary/non-conforming`, `other`).
  * El campo `birthday` sólo acepta una fecha válida en el formato `dd/mm/aaaa` (por ejemplo, 23/01/1990).
  * El campo `email` sólo acepta un correo electrónico en un formato válido común, con un dominio de nivel superior existente y que no supere los 254 caracteres (es decir, `johndoe@example.com`).
  * El campo `phoneNumber` sólo acepta un número de teléfono, sin prefijo, que consta exactamente de 9 dígitos.
  * El campo `password` sólo acepta valores entre 8 y 80 caracteres que contengan al menos una letra minúscula, una mayúscula, un número y un carácter especial (por ejemplo, `@`, `$`, `!`, `%`, `?`, `&`).
  * El campo `hasAcceptedTerms` sólo acepta el valor booleano `true`.
  * Ninguno de los campos anteriores puede dejarse vacío.
* ¿Serás capaz de adoptar una estrategia de validación de entrada adecuada? :slightly_smiling_face::muscle:
  @@ExerciseBox@@
