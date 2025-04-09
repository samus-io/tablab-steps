# Enforcing a custom error handler using Express in Node.js 20

* Error handling aims to ensure that unexpected or untreated errors are not leaked to the user under any circumstances, thereby protecting sensitive information.
* Proper error handling is essential in any backend application to ensure robustness, security, and long-term maintainability.
* In Express.js, different techniques can be applied to handle errors depending on the architecture and scope of the application.

  > :warning: Setting the `NODE_ENV` variable to `production` in Node.js is strongly recommended to limit error details that might expose sensitive information.

## Using basic try/catch blocks

* Encapsulating every route handler in a `try/catch` block provides a straightforward approach to error handling, allowing errors to be managed within the route itself.
* The following code sample demonstrates how `try/catch` is used to handle errors and return appropriate HTTP status codes based on the type of error:

  ```javascript
  class ValidationError extends Error {
    constructor(message) {
      super(message);
      this.name = "ValidationError";
    }
  }

  class NotFoundError extends Error {
    constructor(message) {
      super(message);
      this.name = "NotFoundError";
    }
  }
  ```

  ```javascript
  app.get("/profile", async (req, res) => {
    const { userId } = req.query;

    try {
      const user = await fetchDatabase(userId); // Error thrown here
      res.json(user);
    } catch (err) {
      if (err instanceof ValidationError) {
        res.status(400).json({ message: "Invalid request data" });
      } else if (err instanceof NotFoundError) {
        res.status(404).json({ message: "Profile not found" });
      } else {
        res.status(500).json({ message: "An unexpected error occurred" });
      }
    }
  });
  ```

* However, this method can quickly become repetitive and may result in missed handlers, accidentally allowing some errors to go uncaught.
* Applying `try/catch` blocks across all routes causes redundancy and raises the chance of overlooking error handling, where a missed case could cause the application to crash. For this reason, it is only recommended in simple applications.

## Using a global error handler

* A global error handler enables centralized control over error management and ensures consistent processing of unhandled errors.
* Express natively supports error-handling middleware, allowing developers to streamline error management.
* The following example illustrates how a global error-handling middleware captures and processes generated errors while returning a standardized response:

  ```javascript
  app.get("/add", (req, res) => {
    const { a, b } = req.query;

    const numA = Number(a);
    const numB = Number(b);

    if (isNaN(numA) || isNaN(numB)) {
      throw new ValidationError("'a' and 'b' must be valid numbers"); // Error thrown here
    }

    const result = numA + numB;
    res.json({ result });
  });

  const errorHandlerMiddleware = (err, req, res, next) => {
    if (err instanceof ValidationError) {
      res.status(400).json({ message: err.message });
    } else {
      res.status(500).json({ message: "An unexpected error occurred" });
    }
  };

  app.use(errorHandlerMiddleware);
  ```

  * In this scenario, when an unhandled error arises, Express automatically triggers the `errorHandlerMiddleware`, which helps prevent the exposure of sensitive information.
* Furthermore, basic `try/catch` blocks can be used alongside a global error handler, serving as a fallback for unhandled exceptions.

### Using a global error handler while wrapping async code

* Express does not handle errors thrown from async functions by default. If an error occurs in an async route handler and isn't properly caught, Express will return an empty HTTP response or fail silently.
* Standard middleware functions, like the one previously shown, are not sufficient to catch exceptions from async functions since unhandled promise rejections are not automatically passed to `next()`, which is what Express relies on to delegate errors to the error-handling middleware.
* A common, simple, and effective solution is to wrap all async route handlers in a utility function that catches errors and forwards them using `next()`:

  ```javascript
  const asyncErrorWrapper = (fn) => (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };

  app.get("/profile", asyncErrorWrapper(async (req, res) => {
    const { userId } = req.query;

    if (!userId) {
      throw new ValidationError("Missing required query parameter: 'userId'");
    }

    const user = await fetchDatabase(userId); // Error thrown here
    res.json(user);
  }));

  const errorHandlerMiddleware = (err, req, res, next) => {
    if (err instanceof ValidationError) {
      res.status(400).json({ message: err.message });
    } else {
      res.status(500).json({ message: "An unexpected error occurred" });
    }
  };

  app.use(errorHandlerMiddleware);
  ```

  * Note how the route handler is currently asynchronous through the use of `async/await`.
  * Within the code, the `asyncErrorWrapper` function can be used to wrap asynchronous route handlers, ensuring that any thrown or rejected error is properly forwarded to Express's error-handling middleware.

## Exercise to practice :writing_hand:

* The following web application includes a registration form that mishandles errors by exposing internal details to the user interface when a field does not meet the expected criteria.
* The goal of this exercise is to use the `Open Code Editor` button to modify the source code and create a proper custom error handler while satisfying the specified requirements:
  * As a representative example, when any field in the registration form is invalid, the application should always return an HTTP 400 status code response with the JSON content of `{"message":"Registration data is not correctly formatted."}`.
  * For any error unrelated to form validation, like a connection failure to the database, the application should return an HTTP 500 status code response with the JSON content of `{"message":"Internal Server Error"}`.
  * More precisely, the Express application in `app.js` should have code modifications to support this functionality.
* After making the changes, press the `Verify Completion` button to confirm the exercise has been completed.

  @@ExerciseBox@@
