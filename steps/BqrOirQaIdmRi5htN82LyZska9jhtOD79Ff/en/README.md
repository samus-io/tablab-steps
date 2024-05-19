# Prepared Statements in Node.js with SQLite

* Prepared statements in Node.js with SQLite are crucial for enhancing security and performance when executing SQL queries.
* They help prevent SQL injection attacks by separating SQL logic from data.

## Setting Up the Environment

* **Install SQLite3 Module**
  * First, ensure that the SQLite3 module is installed in the Node.js environment.
  * Use the following command to install it:

    ```js
    npm install sqlite3
    ```

* **Import SQLite3 Module**
  * Import the SQLite3 module in the Node.js application.

    ```js
    const sqlite3 = require('sqlite3').verbose();
    ```

* **Import SQLite3 Module**
  * Establish a connection to the SQLite database.
  * If the database file does not exist, it will be created

    ```js
    const db = new sqlite3.Database('example.db');
    ```

## Creating a Table

* Create a table to work with, for instance, create a simple `users` table.

```js
db.serialize(() => {
    db.run("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)");
});

```

## Using Prepared Statements

### Inserting Data with Prepared Statements

* To insert data securely into the `users` table using prepared statements:

  * **Prepare the SQL Statement**: Use the `db.prepare` method to create a prepared statement with placeholders for the parameters.
  * **Bind Parameters and Execute**: Bind the parameters and execute the statement using the `run` method.
  * **Finalize the Statement**: Always finalize the statement after execution to free resources.

    ```js
        const insertUser = db.prepare("INSERT INTO users (name, email) VALUES (?, ?)");
        insertUser.run("John Doe", "john.doe@example.com");
        insertUser.run("Jane Smith", "jane.smith@example.com");
        insertUser.finalize();
    ```

### Querying Data with Prepared Statements

* To query data from the users table using prepared statements:

  * **Prepare the SQL Statement**: Use the `db.prepare` method to create a prepared statement.
  * **Bind Parameters and Execute**: Execute the query using the `all` method to fetch all rows.
  * **Finalize the Statement**: Process the result within the callback function.

    ```js
        const selectUser = db.prepare("SELECT * FROM users WHERE email = ?");
        selectUser.all("john.doe@example.com", (err, rows) => {
            if (err) {
                console.error(err.message);
            } else {
                console.log(rows);
            }
        });
        selectUser.finalize();

    ```

### Updating Data with Prepared Statements

* To update data in the `users` table using prepared statements:

  * **Prepare the SQL Statement**: Create a prepared statement for the `update` operation.
  * **Bind Parameters and Execute**: Use the run method to bind parameters and execute the statement.
  * **Finalize the Statement**: Finalize the statement to release resources.

    ```js
        const updateUser = db.prepare("UPDATE users SET name = ? WHERE email = ?");
        updateUser.run("Johnathan Doe", "john.doe@example.com");
        updateUser.finalize();
    ```

### Deleting Data with Prepared Statements

* To delete data from the `users` table using prepared statements:

  * **Prepare the SQL Statement**:  Use the `db.prepare`method for the delete operation.
  * **Bind Parameters and Execute**:  Bind parameters and execute the statement using the `run` method.
  * **Finalize the Statement**: Finalize the statement to ensure proper resource management.

    ```js
        const deleteUser = db.prepare("DELETE FROM users WHERE email = ?");
        deleteUser.run("john.doe@example.com");
        deleteUser.finalize();

    ```

## Error Handling and Closing the Database

* Proper error handling is essential when working with databases.
* Wrap database operations in try-catch blocks or use callback functions to handle errors gracefully.
* Always close the database connection when it is no longer needed to avoid memory leaks and other issues.

```js
db.close((err) => {
    if (err) {
        console.error(err.message);
    } else {
        console.log('Database connection closed.');
    }
});

```

## Best Practices

* **Always finalize prepared statements**: This ensures that resources are freed properly.
* Avoid dynamic table or column names in prepared statements: Use allow-lists for dynamic table or column selection.
* **Handle errors gracefully**: Implement error handling to manage database operation failures.
* **Close the database connection**: Ensure that the database connection is closed when it is no longer needed.
