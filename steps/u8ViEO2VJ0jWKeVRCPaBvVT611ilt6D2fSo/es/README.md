# Prepared Statements en Node.js

* El siguiente método `addUser` crea un usuario en la tabla `users` almacenando su nombre y correo electrónico:
  ```javascript
  const addUser = (name, email) => {
    const prepare = await connection.prepare(
      "INSERT INTO users(name, email) VALUES (?,?)"
    );

    await prepare.execute([name, email]);
    prepare.close();
  }

  addUser("brian", "brian.carlson@gmail.com");
  ```
* :writing_hand: El siguiente código debe ser corregido creando un Prepared Statement para prevenir una inyección SQL:
  @@ExerciseBox@@
  
