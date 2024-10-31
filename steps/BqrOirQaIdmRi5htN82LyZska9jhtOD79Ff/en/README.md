# Prepared Statements in Node.js with SQLite

## Setting Up the Environment

* **Install SQLite3 module**
  * First, ensure that the SQLite3 module is installed in the Node.js environment.
  * Use the following command to install it:

    ```javascript
    npm install sqlite3
    ```

* **Import SQLite3 module**
  * Import the SQLite3 module in the Node.js application.

    ```javascript
    const sqlite3 = require('sqlite3').verbose();
    ```

* **Import SQLite3 module**
  * Establish a connection to the SQLite database.
  * If the database file does not exist, it will be created

    ```javascript
    const db = new sqlite3.Database('example.db');
    ```

## Creating a Table

* Create a table to work with, for instance, create a simple `users` table.

```javascript
db.serialize(() => {
db.run("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)");
});
```

## Using Prepared Statements

### Inserting data with Prepared Statements

* To insert data securely into the `users` table using prepared statements:

  * **Prepare the SQL Statement**: Use the `db.prepare` method to create a prepared statement with placeholders for the parameters.
  * **Bind Parameters and Execute**: Bind the parameters and execute the statement using the `run` method.
  * **Finalize the Statement**: Always finalize the statement after execution to free resources.

    ```javascript
    const insertUser = db.prepare("INSERT INTO users (name, email) VALUES (?, ?)");
    insertUser.run("John Doe", "john.doe@example.com");
    insertUser.run("Jane Smith", "jane.smith@example.com");
    insertUser.finalize();
    ```

### Querying data with Prepared Statements

* To query data from the users table using prepared statements:

  * **Prepare the SQL Statement**: Use the `db.prepare` method to create a prepared statement.
  * **Bind Parameters and Execute**: Execute the query using the `all` method to fetch all rows.
  * **Finalize the Statement**: Process the result within the callback function.

    ```javascript
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

  * **Dynamic table scenario**: To handle scenarios that require dynamic table or column selection in SQL queries, it is essential to use an allow-list (whitelist).
  * This ensures that only permitted values are included in the query.
  * Let us take an example:

    ```javascript
    const allowedTables = ['users', 'orders', 'products'];

    function validateTableName(tableName) {
        return allowedTables.includes(tableName);
    }

    // Example usage
    const tableName = 'users';
    if (validateTableName(tableName)) {
        const query = `SELECT * FROM ${tableName}`;
        // Execute query
    } else {
        throw new Error('Invalid table name');
    }
    ```

    * When dynamic table selection is required for SQL queries, an allow-list should be employed.
    * This list explicitly defines acceptable table names, ensuring that only permitted values are included in the query.

### Updating Data with Prepared Statements

* To update data in the `users` table using prepared statements:

  * **Prepare the SQL Statement**: Create a prepared statement for the `update` operation.
  * **Bind Parameters and Execute**: Use the run method to bind parameters and execute the statement.
  * **Finalize the Statement**: Finalize the statement to release resources.

    ```javascript
    const updateUser = db.prepare("UPDATE users SET name = ? WHERE email = ?");
    updateUser.run("Johnathan Doe", "john.doe@example.com");
    updateUser.finalize();
    ```

### Deleting data with Prepared Statements

* To delete data from the `users` table using prepared statements:

  * **Prepare the SQL Statement**:  Use the `db.prepare`method for the delete operation.
  * **Bind Parameters and Execute**:  Bind parameters and execute the statement using the `run` method.
  * **Finalize the Statement**: Finalize the statement to ensure proper resource management.

    ```javascript
    const deleteUser = db.prepare("DELETE FROM users WHERE email = ?");
    deleteUser.run("john.doe@example.com");
    deleteUser.finalize();
    ```

### Finalize method

* The `finalize method` in SQLite's prepared statements serves an essential purpose in managing resources efficiently.
* When you use prepared statements in SQLite with Node.js, each prepared statement consumes some system resources.
* These resources include memory and handles to SQLite's internal structures.
* The finalize method releases these resources associated with the prepared statement.
* It is crucial to call finalize after you've finished executing the statement to prevent resource leaks and ensure optimal performance.
* Failing to finalize a prepared statement can lead to memory leaks and potential performance degradation, especially in long-running applications.

    ```javascript
    statement.finalize();
    ```

## Error Handling and Closing the Database

* Proper error handling is essential when working with databases.
* Wrap database operations in try-catch blocks or use callback functions to handle errors gracefully.
* Always close the database connection when it is no longer needed to avoid memory leaks and other issues.

```javascript
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
* **Avoid dynamic table or column names in prepared statements**: Use allow-lists for dynamic table or column selection.
* **Handle errors gracefully**: Implement error handling to manage database operation failures.
* **Close the database connection**: Ensure that the database connection is closed when it is no longer needed.
