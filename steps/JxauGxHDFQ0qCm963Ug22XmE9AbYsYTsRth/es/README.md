# Prevención de inyecciones SQL utilizando Jakarta Persistence API en Jakarta EE 10.0

* `Jakarta Persistence API (JPA)` es un estándar de tecnología que proporciona especificaciones para la gestión de datos relacionales en aplicaciones que utilizan plataformas Java.
* A modo de `Object-Relational Mapping (ORM)`, Jakarta Persistence API proporciona una forma de mapear objetos en Java (conocidos como entidades) a tablas de bases de datos. Un contexto de persistencia gestiona las entidades, lo que incluye el manejo de su ciclo de vida, la gestión de mapeos relacionales y la realización de operaciones de base de datos.

  > :older_man: Las librerías ORM evitan la necesidad de escribir código SQL, ya que la librería ORM genera sentencias SQL preparadas directamente a partir de código orientado a objetos.

* Estas operaciones se llevan a cabo típicamente a través de la interfaz `EntityManager`, que actúa como el principal punto de interacción para las transacciones de base de datos.

## Ejemplo de Jakarta Persistence API

* Este ejemplo demuestra el uso de JPA para interactuar con una base de datos:

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

  * Como se puede observar, presenta una clase `Product` definida para representar una tabla de base de datos, donde cada atributo como `id`, `name`, `category` y `rating` se correlaciona con una columna en esa tabla.
* El `EntityManager` se utiliza para buscar una instancia de `Product` en la base de datos utilizando su clave primaria (`id`).

  ```java
  EntityManagerFactory emf = Persistence.createEntityManagerFactory();
  EntityManager entityManager = emf.createEntityManager();
  
  // Find a product by id
  Product product = entityManager.find(Product.class, productId);
  ```

## ¿Cómo se puede producir todavía una inyección SQL en Jakarta Persistence API?

* El uso de `Jakarta Persistence API Query Language (JPQL)` con el método `createQuery` del `EntityManager` puede ser propenso a inyecciones SQL:

  ```java
  String queryString = "SELECT p.id, p.name, p.price, p.category, p.stock, p.rating FROM Product WHERE p.category = '" + category + " AND p.rating >= '" + rating + "'";
  TypedQuery<Product> query = entityManager.createQuery(queryString, Product.class);

  List<Product> products = query.getResultList();
  ```
  
  * En este ejemplo, las variables `category` y `rating` se concatenan con la consulta SQL, evitando las sentencias preparadas y la parametrización de consultas.

  > :warning: Existen otros métodos de Jakarta Persistence API que pueden ser vulnerables a inyección SQL, pero mientras no se concatenen *strings*, la aplicación no será vulnerable a inyecciones SQL.

### Consideraciones de seguridad

* Para protegerse contra los ataques de inyección SQL al usar JPA, es crucial evitar la concatenación directa de *strings* dentro de las consultas SQL. Esto se debe a que los métodos integrados de Jakarta Persistence API, cuando se utilizan correctamente, previenen inherentemente las vulnerabilidades de inyección SQL.
  * Por lo tanto, el uso de estos métodos según lo previsto asegura que las consultas sean seguras contra inyecciones.
* El uso de consultas parametrizadas en lugar de concatenar *strings* puede prevenir las inyecciones SQL:

  ```java
  String queryString = "SELECT p.id, p.name, p.price, p.category, p.stock, p.rating FROM Product WHERE p.category = :category AND p.rating >= :rating";
  
  TypedQuery<Product> query = entityManager.createQuery(queryString, Product.class);
  query.setParameter("category", category);
  query.setParameter("rating", rating);

  List<Product> products = query.getResultList();
  ```

## Ejercicio para practicar :writing_hand:

* El siguiente formulario de inicio de sesión es susceptible a inyecciones SQL debido a que agrega directamente la entrada del usuario a la consulta de la base de datos.
* El objetivo aquí es editar el código fuente abriendo el editor de código a través del botón `Open Code Editor` e implementar correctamente las consultas JPA para eliminar la vulnerabilidad.
  * Más concretamente, el código a modificar se encuentra en el método estático `loginWithCredentials` dentro de la clase `Auth`, ubicada en `src/main/java/io/ontablab/Auth.java`.
* Después de implementar una solución correcta, prueba rellenando el formulario e introduciendo una carga útil en el campo de contraseña que podría haber explotado previamente la vulnerabilidad, como `" OR 1=1 OR "1"="1`, comprobando que ya no funciona. Por último, pulsa el botón `Verify Completion` para confirmar que el ejercicio se ha completado.
* ¿Serás capaz de prevenir la vulnerabilidad de inyección SQL implementando una consulta segura? :slightly_smiling_face::muscle:
  @@ExerciseBox@@
