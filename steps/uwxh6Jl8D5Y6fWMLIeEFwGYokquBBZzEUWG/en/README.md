# Enforcing a custom error handler using Express in Node.js

* Handling errors properly in an Express application is crucial to ensuring a robust, secure, and maintainable backend.
* Express should be run in production mode using `NODE_ENV=production` environment variable to disable detailed error messages that could expose sensitive information.
* There are multiple ways to manage errors, each with its own advantages and drawbacks.

## Try/Catch blocks

* Wrapping every route handler inside a `try/catch` block is a straightforward way to handle errors. This approach ensures that errors are caught and handled within each route.
* The example shows how `try/catch` is used to return an `HTTP 500` error when an error occurs:

  ```javascript
  app.get('/data', async (req, res) => {
      try {
          const data = await fetchData();
          res.json(data);
      } catch (err) {
          res.status(500).json({ message: 'An unexpected error occurred' });
      }
  });
  ```

* However, this approach quickly becomes repetitive and increases the risk of missing a handler, leading to uncaught errors.
* Repeating `try/catch` in every route increases code duplication and makes it easier to overlook error handling and missing one can result in uncaught errors that crash the application.

## Global error handler

* A global error handler centralizes error management and ensures consistent processing of unhandled errors.
* Express natively supports error-handling middleware, allowing developers to streamline error management.
* The following example illustrates how a global error-handling middleware captures and processes errors, returning a standardized response:

  ```javascript
  /**
   * Middleware for centralized error handling.
   * Logs the error and responds with a generic message to prevent sensitive data exposure.
   */
  const errorHandlerMiddleware = (err, req, res, next) => {
    console.error(`Error: ${err.message}`);

    res.status(err.status || 500).json({
      message: err.status ? err.message : 'Internal Server Error',
    });
  };

  app.get('/error', (req, res) => {
    throw new Error('Error'); // Automatically handled
  });

  app.use(errorHandlerMiddleware);
  ```

* When an unhandled error occurs, Express automatically executes the `errorHandlerMiddleware` middleware, preventing sensitive information from being displayed.
* However, it is best practice to handle errors with `try/catch` while relying on the global error handler as a fallback for any unhandled exceptions due to missing `try/catch` blocks.

### Handling async errors

* When an `async` function throws an error, Express does not handle it properly by default, returning an empty HTTP response.
* Middleware alone is not sufficient to catch errors from `async` functions, as unhandled rejections are not automatically forwarded.
* The following code resolves this problem by resolving all promises before returning a response:

```javascript

  /**
   * Higher-order function that wraps async route handlers.
   * Catches errors and forwards them to Express error handling automatically.
   */
  const catchAsyncErrors = (fn) => (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };

app.get('/error-async', catchAsyncErrors(async (req, res) => {
  const content = await fs.readFile('./invalid-file.txt', 'utf8'); // Will throw an error
  res.send(content);
}));
```

* The `catchAsyncErrors` function wraps asynchronous route handlers, ensuring that any thrown error is forwarded to Express' error-handling middleware.

## Exercise to practice :writing_hand:

* The following web application includes a registration form that does not handle errors properly, which could reveal internal details about how the application works.
* The purpose of this exercise is to modify the source code using the `Open Code Editor` button to implement a custom error handler that meets the following requirements:
  * If any field in the registration form is incorrect, the application must return the JSON `{"message": "The registration form is not correct."}` with a 400 HTTP code.
  * If another kind of error occurs, such as a malformed JSON request, the application must return the JSON `{"message": "Bad Request"}` with a 400 HTTP code.
* More precisely, the `/register` endpoint of the Express application in `app.js` should have code modifications to support this functionality.
* After making the changes, press the `Verify Completion` button to confirm that the exercise has been completed.

@@ExerciseBox@@
