# Preventing SQL injections using Jakarta Persistence API in Jakarta EE 10.0

* `Jakarta Persistence API (JPA)` is a standard technology that provides a specification for managing the relational data in applications using Java platforms.
* As an `Object-Relational Mapping (ORM)`, Jakarta Persistence API provides a way to map objects in Java (known as entities) to database tables. A persistence context manages the entities, which includes handling their life cycle, managing relational mappings, and performing database operations.
  > :older_man: ORM libraries avoid the need to write SQL code, since the ORM library generates prepared SQL statements directly from object-oriented code.
* These operations are typically carried out through the `EntityManager` interface, which acts as the primary point of interaction for database transactions.

## Example of Jakarta Persistence API usage

* This example demonstrates using JPA to interact with a database:

  ```java
  @Entity
  public class Product {
      @Id
      @GeneratedValue(strategy = GenerationType.IDENTITY)
      private long id;
      private String name;
      private String category;
      private double price;
      private double rating;
      private int stock;

      // Constructors, getters, and setters
  }
  ```

  * It features a `Product` class annotated to represent a database table, where each attribute like `id`, `name`, `category`, and `rating` correlates to a column in that table.
* Then `EntityManager` is used to fetch a `Product` instance from the database using its primary key (`id`):

  ```java
  EntityManagerFactory emf = Persistence.createEntityManagerFactory();
  EntityManager entityManager = emf.createEntityManager();
  
  // Find a product by id
  Product product = entityManager.find(Product.class, productId);
  ```

## How a SQL injection can still arise on Jakarta Persistence API?

* Using `Jakarta Persistence API Query Language (JPQL)` with the method `createQuery` of `EntityManager`, can leverage to SQL injections:

  ```java
  String queryString = "SELECT p.id, p.name, p.price, p.category, p.stock, p.rating FROM Product WHERE p.category = '" + category + " AND p.rating >= '" + rating + "'";
  TypedQuery<Product> query = entityManager.createQuery(queryString, Product.class);

  List<Product> products = query.getResultList();
  ```

  * In this example, the `category` and `rating` variables are concatenated with the SQL query, avoiding the prepared statements and query parameterization.
  > :warning: There are other Jakarta Persistence API methods that can be vulnerable to SQL injection, but as long as the strings are not concatenated, the application will not be vulnerable to SQL injection.

### Security considerations

* To safeguard against SQL Injection attacks when using JPA, it's crucial to refrain from concatenating strings directly within SQL queries. This is because Jakarta Persistence API's built-in methods, when used correctly, inherently prevent SQL Injection vulnerabilities.
  * Therefore, using these methods as intended ensures that your queries are secure from such attacks.
* Using parameterized queries instead of concatenating strings can prevent SQL injections:

  ```java
  String queryString = "SELECT p.id, p.name, p.price, p.category, p.stock, p.rating FROM Product WHERE p.category = :category AND p.rating >= :rating";
  
  TypedQuery<Product> query = entityManager.createQuery(queryString, Product.class);
  query.setParameter("category", category);
  query.setParameter("rating", rating);

  List<Product> products = query.getResultList();
  ```

## Exercise to practice :writing_hand:

* The following login form is susceptible to SQL injection due to directly appending user input to the database query.
* The objective here is to edit the source code opening the code editor through the `Open Code Editor` button, and implement correctly the JPA queries to eliminate the vulnerability.
* More precisely, the code to be modified resides in the static method `loginWithCredentials` within the `Auth` class, located in `src/main/java/io/ontablab/Auth.java`.
* Will you be able to prevent the SQL injection flaw by implementing a safe query? :slightly_smiling_face::muscle:
* Once you believe you've implemented a correct solution, test it by introducing a payload that previously exploited the vulnerability, such as `" OR 1=1 OR "1"="1`, and verify that no longer works.
  @@ExerciseBox@@
