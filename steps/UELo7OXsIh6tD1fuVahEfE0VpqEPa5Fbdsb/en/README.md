# Data validation in Java Jakarta using Jakarta Bean Validation

* Java Jakarta provides various tools and libraries that facilitate syntax validation ensuring robust and efficient code quality management.

## What is Jakarta Bean Validation?

* `Jakarta Bean Validation` is a framework within the Jakarta EE ecosystem that allows developers to enforce constraints on Java objects through declarative annotations.
* It simplifies validation logic by applying constraints directly to properties, methods, and constructors.
* It ensures that data meets predefined rules before processing, enhancing data integrity and reducing programming errors by automating validation checks within the application.

### Understanding Jakarta Bean Validation key concepts

* A **constraint** refers to a rule adhered to Java properties or methods, such as a string's length or an integer's range.
* An **annotation** is metadata that applies *constraints* to properties, enhancing readability and maintainability of code.
* **Validator** is an object that checks compliance with constraints defined on any Java object. Validators are commonly created using the `ValidatorFactory`, which ensures adherence to these constraints during runtime.

### User registration form use case

* Consider a website's registration form where users sign up for an account. This form asks for a username, password, email and the age of the user.
* Using Jakarta Bean Validation a Java class can be crafted to reflect the form data, where its properties are annotated with validation rules, as shown below:

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

  * Validation will be performed while collecting all violations and reporting errors if the user input does not meet the set constraints, allowing total control in its management:

  ```java
  import jakarta.validation.ConstraintViolation;
  import jakarta.validation.Validation;
  import jakarta.validation.Validator;
  import jakarta.validation.ValidatorFactory;
  import java.util.Set;

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
  
  * The `violations` object retrieves all the validation error messages generated when the `user` object fails to meet certain criteria at creation.

### More constraint definitions

* Below is a table showing the constraint definitions that Java Jakarta establishes by default. Note that all these constraints include a `message` parameter, used to return an error message if the attribute does not satisfy the conditions.

  |Annotation|Description|
  |:-:|:-:|
  |`@Null`|Ensures the annotated element must be null|
  |`@NotNull`|Ensures the annotated element must not be null|
  |`@Min(value)`|Ensures the annotated element is no less than `value`|
  |`@Max(value)`|Ensures the annotated element is no more than `value`|
  |`@DecimalMin(value)`|Ensures the annotated number is no less than the specified decimal `value`|
  |`@DecimalMax(value)`|Ensures the annotated number is no more than the specified decimal `value`|
  |`@Negative`|Ensures the annotated number is strictly negative|
  |`@NegativeOrZero`|Ensures the annotated number is negative or zero|
  |`@Positive`|Ensures the annotated number is strictly positive|
  |`@PositiveOrZero`|Ensures the annotated number is positive or zero|
  |`@Size(min,max)`|Constrains the annotated element's size between `min` and `max`|
  |`@Digits(integer,fraction)`|Limits the number of digits in the `integer` and `fraction` parts of a number|
  |`@Past`|Ensures the annotated `Date` object is in the past|
  |`@PastOrPresent`|Ensures the annotated `Date` object is in the past or the present day|
  |`@Future`|Ensures the annotated `Date` object is in the future|
  |`@FutureOrPresent`|Ensures the annotated `Date` object is in the future or the present day|
  |`@NotEmpty`|Ensures the annotated collection, map, array, or string is not empty or null|
  |`@NotBlank`|Ensures the annotated string is not null and not blank (containing non-whitespace characters)|
  |`@Email`|Ensures the annotated string is a valid email address|
  |`@Pattern(regexp)`|Ensures the annotated string matches the specified regular expression|
  |`@AssertTrue`|Ensures the annotated boolean is true|
  |`@AssertFalse`|Ensures the annotated boolean is false|

* In addition to these standard constraints, developers can define custom constraints by creating a new annotation along with a corresponding constraint validator.

### Jakarta Bean Validation limitations

* Jakarta Bean Validation can't handle validations where the validity of one field depends on the value of another (cross-field validation) or checking if a person's age falls within a specific range based on their birthday. These types of validations require custom logic that must be implemented manually in the application code.

## Exercise to practice :writing_hand:

* The following register form is accepting user-supplied data without conducting any kind of validation on the server-side.
* The purpose here is to open the code editor through the `Open Code Editor` button and apply an input validation strategy on the server-side using either `Jakarta Bean Validation` or `JSON Schema`, with the goal of validating all data entered into the form fields.
* More precisely, some code should be added in the `RegisterForm` class, located in `src/main/java/io/ontablab/RegisterForm.java`.
* This exercise can only be passed if the server-side data validation meets the following requirements:
  * The `firstName` and `lastName` fields only accept alphabetic characters (i.e., A-Z or a-z) between 2 and 50 characters.
  * The `gender` field only accepts one of the listed values explicitly in lowercase (i.e., `female`, `male`, `transgender`, `non-binary/non-conforming`, `other`).
  * The `birthday` field only accepts a valid date in the `dd/mm/yyyy` format (e.g., 23/01/1990).
  * The `email` field only accepts an email in a common valid format, with an existing top-level domain, and no longer than 254 characters (i.e., `johndoe@example.com`).
  * The `phoneNumber` field only accepts a phone number with no prefix consisting of exactly 9 digits.
  * The `password` field only accepts values between 8 and 80 characters containing at least one lowercase letter, one uppercase letter, one number, and one special character (i.e., `@`, `$`, `!`, `%`, `?`, `&`).
  * The `hasAcceptedTerms` field only accepts the boolean value `true`.
  * None of the above fields can be left empty.
* Will you be able to adopt an appropriate input validation strategy? :slightly_smiling_face::muscle:
  @@ExerciseBox@@
