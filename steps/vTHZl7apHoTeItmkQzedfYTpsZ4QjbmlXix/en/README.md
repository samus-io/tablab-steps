# Preventing improper error handling in NodeJS 20

* Note that the entire step uses `console.log` to simulate a standard logging system.

## Input validation

### Using string methods to check and sanitize input

* String methods in javascript can be used to perform basic validation and sanitization tasks. Here are examples of how to use string methods to validate and sanitize a user's input.

#### Validating email using string methods

```javascript
function isValidEmail(email) {
    // For example, using includes method to check if email contains "@" and "."
    return email.includes('@') && email.includes('.');
}

const email = 'test@example.tbl';

if (isValidEmail(email)) {
    console.log('Valid email!');
} else {
    console.log('There was a problem with the input provided.');
}
```

#### Sanitizing input by trimming whitespace

```javascript
function sanitizeInput(input) {
    // For example, using trim method to trim whitespace from both ends of the string
    return input.trim();
}

const userInput = '   some user input   ';
const sanitizedInput = sanitizeInput(userInput);

console.log(`Sanitized input: "${sanitizedInput}"`);
```

#### Removing potentially harmful characters

```javascript
function removeSpecialChars(input) {
    // For example, using replace method to remove characters that are not alphanumeric or whitespace
    return input.replace(/[^\w\s]/gi, '');
}

const userInput = 'Hello@#%$!';
const sanitizedInput = removeSpecialChars(userInput);

console.log(`Sanitized input: "${sanitizedInput}"`);
```

### Using libraries for more comprehensive validation

#### Using `validator` library in Node.js

* `validator` is a library used in Node.js to check and sanitize user inputs, ensuring they meet specific criteria like being an email or a URL.
* Install the `validator` library:

```bash
npm install validator
```

* Validate and sanitize user input. For example, check if it is a valid email and then normalize it:

```javascript
const validator = require('validator');

// Sample email ID
const email = 'test@example.tbl';

// Use validator to check the email validity
if (validator.isEmail(email)) {
    console.log('Valid email!');
} else {
    console.log('There was a problem with the input provided.');
}

// Normalize the email ID
const sanitizedEmail = validator.normalizeEmail(email);
console.log(`Sanitized email: ${sanitizedEmail}`);
```

#### Using `express-validator` in an express application

* `express-validator` is an Express middleware that uses the `validator` library to validate and sanitize incoming request data in Express applications.
* Install `express-validator`:

```bash
npm install express-validator
```

* Set up validation middleware. Below code checks three fields (`username`, `password`, `email`) in the user input for length limit and format:

```javascript
const { body, validationResult } = require('express-validator');
const express = require('express');
const app = express();

app.use(express.json());

// Express listener with express-validator as middleware to:
// Check if username contains only alphabets, min. length of 3 and max. length of 30. 
// Check if password contains min. length of 5. 
// Check if the email is valid.
app.post('/register', [
    body('username').isAlphanumeric().isLength({ min: 3, max: 30 }),
    body('password').isLength({ min: 5 }),
    body('email').isEmail()
], (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        return res.status(400).json({ message: "Something was incorrect. Please try again!" });
    }
    res.send('Registration successful!');
});

// Start the listener at a preferred port number
app.listen(3000);
```

* Now, send a `POST` request to this port with body including the `username`, `password` and `email` in JSON format.

### Using regular expressions (RegExp) for validation and sanitization

* Example showing the use of regular expressions in validation and sanitization.

#### Validating email using regular expressions

* Below is a very simple pattern for matching email address, but there is a much standard format defined in RFC 5322.

```javascript
function isValidEmail(email) {
    // Sample pattern for email
    const emailPattern = /[a-z0-9]+@[a-z]+\.[a-z]{2,9}/;
    return emailPattern.test(email);
}

const email = 'test@example.tbl';

if (isValidEmail(email)) {
    console.log('Valid email!');
} else {
    console.log('There was a problem with the input provided.');
}
```

#### Validating phone number using regular expressions

```javascript
function isValidPhoneNumber(phone) {
    // Check if the phone number contains exactly 10 digits
    const phonePattern = /^\d{10}$/;
    return phonePattern.test(phone);
}

const phoneNumber = '1234567890';

if (isValidPhoneNumber(phoneNumber)) {
    console.log('Valid phone number!');
} else {
    console.log('There was a problem with the input provided.');
}
```

#### Validate URL using regular expressions

* Below is a very simple pattern for matching URL, but there is a much standard format defined in RFC 3986.

```javascript
function isValidURL(url) {
    const urlPattern = /(https?:\/\/)[a-z]+\.[a-z]+\.[a-z]{2,9}/i;
    return urlPattern.test(url);
}

const url = 'https://www.example.tbl';

if (isValidURL(url)) {
    console.log('Valid URL!');
} else {
    console.log('There was a problem with the input provided.');
}
```

### Schema validation

* Node.js provides libraries to form a schema to match and validate the input parameters. For example, `joi`.

* Install the `joi` Library

```bash
npm install joi
```

* Define and validate a schema.

```javascript
const Joi = require('joi');

// Represents a structure or format to be accepted for username, paswword and email
const schema = Joi.object({
    username: Joi.string().alphanum().min(3).max(30).required(),
    password: Joi.string().pattern(new RegExp('^[a-zA-Z0-9]{3,30}$')).required(),
    email: Joi.string().email().required()
});

// Sample input
const inputData = {
    username: 'testuser',
    password: 'password123',
    email: 'test@example.tbl'
};

// Validate input as per the schema given above
const { error, value } = schema.validate(inputData);
if (error) {
    console.log('Validation error:', error.details);
} else {
    console.log('Valid input:', value);
}
```

## Using standard error codes in Node.js and generic responses

### Define custom error codes

* Map the custom error codes that the application will use to HTTP response codes. For example:

```javascript
const ERROR_CODES = {
    VALIDATION_ERROR: '400',
    AUTHENTICATION_ERROR: '401',
    NOT_FOUND: '404',
    SERVER_ERROR: '500'
};
```

### Create a custom error class

* Extend the built-in `Error` class to include an error code. For example:

```javascript
class AppError extends Error {
    constructor(message, code) {
        super(message);
        this.code = code;
    }
}
```

### Handle and throw errors in the application

* Build the express app and logic to throw errors in the application when an invalid input is submitted by the client. For example, there is a listener at `/user/:id` that performs login operation and throws error if the ID from client is invalid:

```javascript
const express = require('express');
const app = express();

// Listener for user Id in login process
app.get('/user/:id', (req, res, next) => {
    const userId = req.params.id;

    // Check if the User Id format is not valid
    if (!isValidUserId(userId)) {
        return next(new AppError('We could not match your credentials to a valid account.', ERROR_CODES.VALIDATION_ERROR));
    }

    // Simulate fetching user
    const user = getUserById(userId);
    if (!user) {
        return next(new AppError('There was a problem in the input.', ERROR_CODES.NOT_FOUND));
    }

    res.send(user);
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err);  // Log the error details
    res.status(err.code).json({ error: err.message, code: err.code });
});

function isValidUserId(id) {
    // Implement validation logic here
    return true;
}

function getUserById(id) {
    // Simulate user fetch
    return null;
}
```

* So, when the user enters any invalid user ID and calls the endpoint `/user/:id` (e.g. `/user/123`). `400` is the response if the user ID is invalid, `404` is returned if the user ID is not registered. Similarly, there can be any type of mapping between the error type and HTTP status codes. It is left on the developers discretion.
* Note the generic responses used in the handling of exceptions along with the right HTTP response code.

## Implement robust error handling

### Using try-catch blocks

* `try-catch` blocks is typically used to catch and handle errors that may occur during execution. Here's how they work:

  * **Try block**: contains the synchronous code that may potentially throw an error.
  * **Catch block**: catches and handles the error if it occurs within the `try` block.
  * **Finally block**: executes in all cases.

```javascript
const express = require('express');
const app = express();

app.get('/example', (req, res) => {
    try {
        // Simulating a function that might throw an error
        riskyFunction();
        res.send('Success');
    } catch (error) {
        console.error('Error:', error);
        res.status(500).send('Internal Server Error');
    } finally {
        console.log("Execution completed!");
    }
});

function riskyFunction() {
    throw new Error('Something went wrong!');
}

// Start the server at port 3000
app.listen(3000);
```

* The `try` block can also throw custom errors with `throw` statement. For example, `throw new Error('Synchronous Error');`.

### Asynchronous error handling

* If there is an asynchronous function (declared with `async`), it can contain code that may cause errors, just like regular functions.
* `try-catch` blocks can be used inside `async` functions to catch these errors and handle them locally within the function:

```javascript
const express = require('express');
const app = express();

// Example async route that throws an error
app.get('/example', async (req, res, next) => {
    try {
        await riskyAsyncFunction();
        res.send('Success');
    } catch (error) {
        next(error);
    }
});

// Middleware to handle async errors
app.use(async (err, req, res, next) => {
    console.error('Error:', err.message);
    res.status(500).send('Internal Server Error');
});

async function riskyAsyncFunction() {
    // Simulating some asynchronous operation with setTimeout function
    await new Promise(resolve => setTimeout(resolve, 2000)); // 2 seconds delay
    throw new Error('Something went wrong!');
}

// Start the server
app.listen(3000);
```

#### Using promise

* `Promise` is alternative option to `async/await` to handle asynchronous operations. `try-catch` can also be used with `Promise` like below:

```javascript
const express = require('express');
const app = express();

// Example route with promise that might throw an error
app.get('/example', (req, res, next) => {
    // .catch to handle promise rejection
    riskyPromiseFunction()
    .then(() => {
        res.send('Success');
    })
    .catch((error) => {
        next(error);
    });
});

// Middleware to handle errors
app.use((err, req, res, next) => {
    console.error('Error:', err.message);
    res.status(500).send('Internal Server Error');
});

// Promise that simulates rejection with setTimeout simulating async operation
function riskyPromiseFunction() {
    return new Promise((resolve, reject) => {
        setTimeout(()=> reject(new Error('Something went wrong!')),2000);
    });
}

// Start the server
app.listen(3000);
```

* The `promise` either resolves if everything is fine or rejects if there is some issue.

### Centralized error handling middleware

* Error handling middleware functions in express are designed with four parameters `(err, req, res, next)`. These functions are defined using the `app.use()` method, with the additional error parameter (conventionally named `err`) to catch errors passed by `next()`:

```javascript
const express = require('express');
const app = express();

class AppError extends Error {
    constructor(message, code) {
        super(message);
        this.code = code;
    }
}

// Example route that throws an error
app.get('/routeOne', (req, res, next) => {
   throw new AppError('Something went wrong!', 400);
});

// Example route that throws an error
app.get('/routeTwo', (req, res, next) => {
   throw new AppError('Invalid data', 500);
});

// Middleware to handle errors
app.use((err, req, res, next) => {
    console.error('Error:', err.message);
    res.status(err.code).send(err.message);
});

app.listen(3000);
```

* The developer can avoid repeating the code to handle errors at multiple endpoints and a single middleware added to the end of the code will handle the errors thrown by every endpoint.
* This middleware acts like a centre for error handling. This can also be achieved with a common function call passing the error code and error message. Using `switch` statement in the function to send different response types at different circumstances.

### Using default parameters

* Include default values to parameters and avoid errors due to empty arguments:

```javascript
// Passing default value in the beginning of the function creation
function greet(name = 'Guest') {
    console.log(`Hello, ${name}!`);
}

greet(); // Output: Hello, Guest!
greet('John'); // Output: Hello, John!
```

## Implement unit tests for error handling in Node.js

* In Node.js, use testing frameworks like `mocha`, `jest`, or `ava` to write unit tests for error handling. Below is a guide on how to implement unit tests for error handling using `mocha` and `chai`.

### Mocha framework

* `mocha` is a feature-rich javascript testing framework designed for unit and integration testing in Node.js. It supports both `Test Driven Development (TDD)` and `Behavior Driven Development (BDD)`. Unlike other frameworks like `jasmine` or `jest`, `mocha` offers flexible and accurate reporting, asynchronous testing, test coverage reports, and compatibility with any assertion library.

### Chai library

* `chai` is a behavior and test-driven development assertion library that works well with `mocha` and `jasmine`. It allows to make assertions about values, types, and behaviors in the tests, helping to verify the expected outcomes of the code.

### Set up testing environment

* Ensure there is Node.js and npm installed.
* Create a directory for the application:

```bash
mkdir myapp && cd myapp
```

* Initialize npm to create a `package.json` file:

```bash
npm init
```

* Provide the test command as `./node_modules/.bin/mocha` in the prompt.

### Create app with express

* To build the app, install the `express` framework:

```bash
npm install express --save
```

* Create `app.js` in the `myapp` folder with a simple HTTP server including two endpoint `/api/protected`(for simulating `401` response code) and `/api/login`(for simulating `400` response code):

```javascript
// Load express module
import express from 'express';
var app = express();

// Define request response in root URL (/)
app.get('/', function (req, res) {
    res.send('Hello World');
});

// This endpoint simulates the situation when the user is not authorized
app.get('/api/protected', function (req, res) {
    res.status(401).json({error: "Unauthorized access"});
})

// The endpoint simulates the situation when the user input is not valid
app.post('/api/login', function (req, res) {
    res.status(400).json({error: "Bad request"});
})

// Launch listening server on port 3000
app.listen(3000, function () {
    console.log('App listening on port 3000!');
});

```

* Run the app:

```bash
node app.js
```

### Configuring unit tests with mocha and chai

* Install `mocha` and `chai`:

```bash
npm install mocha chai --save-dev
```

* Create a `test` directory and add a test file:

```bash
mkdir test
touch test/errorHandling.test.js
```

* Install the `request` library for making HTTP requests in the tests:

```bash
npm install request --save-dev
```

* Add the following test to `test/errorHandling.test.js`:

```javascript
import { expect } from 'chai';
import request from 'request';


describe('Error Handling', () => {
    // Testing the error handling for 401 Unauthrized access
    it('should return 401 for unauthorized access', (done) => {
        request('http://localhost:3000/api/protected', function(error, response, body) {
            let data = JSON.parse(body);
            expect(data).to.have.property('error');
            expect(data.error).to.equal('Unauthorized access');
            done();
        });
    });
    // Testing the error handling for 400 Bad request
    it('should return 400 for invalid input', (done) => {
        request.post({url:'http://localhost:3000/api/login', form: {username:'###'}}, function(error, response, body) {
            let data = JSON.parse(body);
            expect(data).to.have.property('error');
            expect(data.error).to.equal('Bad request');
            done();
        });
    });
});

```

* Run the tests after covering all possible erroneous situations:

```bash
npm test
```

## Example of improper error handling in Node.js

* Here's an example of a Node.js application that does not handle errors correctly. This application is a simple express server that processes user input (email for login operation) without proper validation or error handling:

```javascript
const express = require('express');
const app = express();
const bodyParser = require('body-parser');

//simulating database
let db = ["test@example.tbl", "test@domain.tbl"];

// Parsing the user input to JSON
app.use(express.json());

// Route that processes user input
app.post('/login', (req, res) => {
    // No validation on the request body
    const email = req.body.email;
    if(db.indexOf(email) > -1){
        // perform login operation here...
        res.send("Login Successful!");
    }else{
       // Sending more descriptive message to the user
        res.status(401).json({error: "The user does not exists."});
    }
  
});

// Start the server
app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
```

### Issues in the code

* **No input validation**: the user input is directly used without any validation or sanitization, making it vulnerable to injection.

* **Exposing detailed error messages**: detailed error messages are sent to the user, revealing potentially sensitive information about server.

* **No centralized error handling**: errors are handled locally within the route, leading to inconsistent error management across the application.
* **Application crashes**: the app can crash at any moment if the body is not valid for parsing.

### How to improve the code

* Below is an improved version of the above code with proper error handling:

```javascript
const express = require('express');
const app = express();
const { body, validationResult } = require('express-validator');

//simulating database
let db = ["test@example.tbl", "test@domain.tbl"];

// Modified error structure
class AppError extends Error {
    constructor(message, code) {
        super(message);
        this.code = code;
    }
}

// Parsing the user input to JSON
app.use(express.json());

// Route that processes user input with validation
app.post('/login', [
  body('email').isEmail()
], (req, res, next) => {
    try{ 
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            throw new AppError("There is something wrong in the input!",400);
        }
      
        if(db.indexOf(req.body.email) > -1){
            // perform login operation here...
            res.send("Login Successful!");
        }else{
            // Sending smart and safe message to the user
            throw new AppError("The given credentials do not match with the valid account!",401);
        }
     
        res.send("Login Successful!");
    } catch (err) {
        console.error(err);
        throw new AppError("Something went wrong!",500);
    }
});

// Middleware for centralized error handling
app.use((err, req, res, next) => {
    console.log(err.stack);
    res.status(err.code || 500).send((err.code)? err.message : "Something went wrong!");
});

// Start the server
app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
```

### Improvements in the code

* **Input validation**: the `email` field is validated to ensure it is a string, trimmed, and escaped to prevent Injection.

* **Centralized error handling**: errors are passed to a centralized error handling middleware that logs the error and sends a generic message to the user.

* **Consistent error responses**: ensures that users receive consistent and non-revealing error messages, improving security and user experience.
