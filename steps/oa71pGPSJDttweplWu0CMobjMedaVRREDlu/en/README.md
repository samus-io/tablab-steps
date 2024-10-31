# Best practices to mitigate command injection in NodeJS 20

## Avoid direct OS command calls

* Deleting a file with `exec` command.

```javascript
const { exec } = require('child_process');

// Risky: Direct OS command
exec('rm -rf /path/to/directory', (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error.message}`);
    return;
  }
  console.log(`Output: ${stdout}`);
});
```

* Use the file system API instead.

```javascript
const fs = require('fs');
const path = '/path/to/directory';

// Safe: Using Node.js file system API
fs.rm(path, { recursive: true, force: true }, (err) => {
  if (err) {
    console.error(`Error: ${err.message}`);
    return;
  }
  console.log(`${path} is deleted`);
});
```

## Utilize file system APIs

* Copying a file using the fs module.

```javascript
const fs = require('fs');

// Safe: Copy a file using fs module
fs.copyFile('/path/to/source', '/path/to/destination', (err) => {
  if (err) {
    console.error(`Error: ${err.message}`);
    return;
  }
  console.log('File was copied successfully');
});
```

## Parameterization with Input Validation

* Using `execFile()` with parameterized arguments.

```javascript
const { execFile } = require('child_process');

// Safe: Use execFile to separate command and parameters
execFile('/path/to/command', ['--arg1', 'value1'], (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error.message}`);
    return;
  }
  console.log(`Output: ${stdout}`);
});
```

* Adding input validation to ensure valid inputs are processed.

```javascript
const path = require('path');

function validateFilePath(filePath) {
  const allowedPath = /^\/safe\/directory\//;
  if (!allowedPath.test(filePath)) {
    throw new Error('Invalid file path');
  }
}

try {
  validateFilePath('/unsafe/directory/file.txt');  // This will throw an error
} catch (err) {
  console.error(err.message);
}
```

## Implement whitelisting

* Creating a whitelist for acceptable file extensions

```javascript
const path = require('path');

function isValidExtension(filePath) {
  const validExtensions = ['.txt', '.md'];
  const ext = path.extname(filePath);
  return validExtensions.includes(ext);
}

const filePath = '/path/to/file.txt';

if (!isValidExtension(filePath)) {
  console.error('Invalid file extension');
} else {
  console.log('Valid file extension');
}
```

## Use regular expressions to restrict input

* Validating filenames with regular expressions

```javascript
function isValidFilename(filename) {
  const regex = /^[a-zA-Z0-9_-]+$/;  // Alphanumeric, underscores, and hyphens
  return regex.test(filename);
}

const filename = 'safe_filename123';

if (!isValidFilename(filename)) {
  console.error('Invalid filename');
} else {
  console.log('Valid filename');
}
```

## Escape special characters when necessary

* Using the shell-quote library to escape special characters

```javascript
const shellQuote = require('shell-quote');

// Safe: Escape special characters in arguments
const args = shellQuote.quote(['arg with space', '$dangerous', '&&']);
const command = `somecommand ${args}`;

console.log(command);  // Outputs: somecommand 'arg with space' '\$dangerous' '&&'
```

## Blacklist limitations

* Using a blacklist for basic filtering but combining it with whitelisting and input validation.

```javascript
const blacklist = [';', '|', '&', '$'];

function isBlacklisted(input) {
  return blacklist.some(char => input.includes(char));
}

const input = 'safeInput';

if (isBlacklisted(input)) {
  console.error('Input contains forbidden characters');
} else {
  console.log('Input is safe');
}
```

## Careful Handling of Command-Line Parameters

* Sanitizing command-line inputs:

```javascript
const { execFile } = require('child_process');
const shellQuote = require('shell-quote');

// Safe: Validate and sanitize command-line arguments
const safeArg = shellQuote.quote(['safeArg']);
execFile('/path/to/command', [safeArg], (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error.message}`);
    return;
  }
  console.log(`Output: ${stdout}`);
});
```

## Libraries to help prevent command injection easily

* **shell-quote**
  * The `shell-quote` library is a popular choice for safely quoting and escaping strings to be used in shell commands.
  * It ensures that the inputs are treated as plain strings and prevents the execution of unintended commands.
  * It helps to safely escape and quote command-line arguments in shell scripts.

  ```javascript
  const sh = require('shell-quote');
  const input = "file.txt; rm -rf /"; // Malicious input
  const safeInput = sh.quote([input]);
  const cmd = `ls ${safeInput}`;
  console.log(cmd); // Outputs: ls 'file.txt; rm -rf /'
  ```

  * In this example, `shell-quote` ensures that the input is properly escaped, preventing the `rm -rf /` command from being executed.

* **escape-shell**
  * The `escape-shell` is a simple and effective library, which is used to escape shell arguments.
  * This is especially useful when there is a need to dynamically construct shell commands with user inputs.
  * It ensures that special characters are handled securely.

  ```javascript
  const escapeShell = require('escape-shell');
  const input = "file.txt; rm -rf /";
  const safeInput = escapeShell(input);
  const cmd = `ls ${safeInput}`;
  console.log(cmd); // Outputs: ls file.txt\;\ rm\ \-rf\ \/
  ```

  * In this example, `escape-shell` helps in escaping special characters in the input string, thereby preventing command injection.

* **popen3**
  * The `popen3` library provides a safe interface to execute commands and handle their input, output, and error streams.
  * It is useful for running commands with controlled input/output in a way that mitigates injection risks.
  * It is a safer alternative to `exec()` that avoids shell expansion vulnerabilities.

  ```javascript
  const { popen3 } = require('popen3');
  popen3('ls', ['-l', 'file.txt'], (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error}`);
      return;
    }
    console.log(`Output: ${stdout}`);
  });
  ```

  * In this example, by using `popen3`, the command and its arguments are kept safe from injection attacks.

## Use of File System in Node.js

* Node.js provides the `fs` module, which offers a range of methods for interacting like reading, writing, and deleting files without needing to invoke shell commands.
* This is a more secure approach because the file system API is less prone to injection attacks, as it handles the operations internally within the language runtime, not through the shell.
* An example of safe file operations:
  
  ```javascript
  const fs = require('fs');

  // Read a file
  fs.readFile('/path/to/file.txt', 'utf8', (err, data) => {
    if (err) {
      console.error(`Error: ${err.message}`);
      return;
    }
    console.log(`File content: ${data}`);
  });

  // Write to a file
  fs.writeFile('/path/to/file.txt', 'Some data', (err) => {
    if (err) {
      console.error(`Error: ${err.message}`);
      return;
    }
    console.log('File written successfully');
  });
  ```
