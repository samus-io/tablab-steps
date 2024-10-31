# Complete solution for command injection

* Let's imagine a file management service that allows users to upload, delete, and view files on a server.
* The service follows secure practices to prevent command injection while interacting with the file system.

## Secure file management system service

* This system allows users to:

  * Upload files.
  * Delete files.
  * List available files in a directory.

* We will integrate secure practices into every file-related operation to mitigate command injection risks.

* Avoid direct OS command calls
  * Use the Node.js `fs` module to handle file operations without directly calling OS commands.

* File system API for safe operations
  * Use `fs` to copy, delete, and read files safely.

* Parameterization with Input validation
  * Ensure any user input, like filenames or directory paths, is validated and sanitized.

* Whitelist valid inputs
  * Only allow filenames with safe extensions (e.g., `.txt` and `.md`).

* Use regular expressions for validation
  * Limit accepted file names to only alphanumeric characters and underscores using regex.

* Escape special characters
  * Use libraries like `shell-quote` or` escape-shell` to ensure input is safely escaped when unavoidable shell commands are needed.

* Use `execFile()` instead of `exec()`
  * Use `execFile()` for running safe system commands without spawning a shell.

* Blacklist limitations
  * Do not rely solely on blacklists—combine with whitelisting and input validation for maximum security.

### Code implementation

```javascript
const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');
const shellQuote = require('shell-quote');

// Constants
const SAFE_DIRECTORY = '/safe/directory/';
const ALLOWED_EXTENSIONS = ['.txt', '.md'];

// Input validation
function validateFilePath(filePath) {
  const fullPath = path.join(SAFE_DIRECTORY, filePath);
  const isValidExtension = ALLOWED_EXTENSIONS.includes(path.extname(filePath));
  const regex = /^[a-zA-Z0-9_-]+$/;
  if (!regex.test(path.basename(filePath))) {
    throw new Error('Invalid filename format.');
  }
  if (!isValidExtension) {
    throw new Error('Invalid file extension.');
  }
  return fullPath;
}

// Upload a file
function uploadFile(filename, content) {
  try {
    const filePath = validateFilePath(filename);
    fs.writeFile(filePath, content, (err) => {
      if (err) {
        throw err;
      }
      console.log('File uploaded successfully.');
    });
  } catch (err) {
    console.error(`Error: ${err.message}`);
  }
}

// Delete a file using the fs module safely
function deleteFile(filename) {
  try {
    const filePath = validateFilePath(filename);
    fs.rm(filePath, { force: true }, (err) => {
      if (err) {
        throw err;
      }
      console.log('File deleted successfully.');
    });
  } catch (err) {
    console.error(`Error: ${err.message}`);
  }
}

// List files in the directory securely
function listFiles() {
  fs.readdir(SAFE_DIRECTORY, (err, files) => {
    if (err) {
      throw err;
    }
    console.log('Files in directory:', files);
  });
}

// Unsafe command demonstration using execFile with parameterization
function getFileDetails(filename) {
  try {
    const filePath = validateFilePath(filename);
    execFile('/usr/bin/file', [filePath], (error, stdout, stderr) => {
      if (error) {
        console.error(`Error: ${error.message}`);
        return;
      }
      console.log(`File details: ${stdout}`);
    });
  } catch (err) {
    console.error(`Error: ${err.message}`);
  }
}

// Escape special characters in file names (if needed)
function escapeFileName(filename) {
  const safeFilename = shellQuote.quote([filename]);
  console.log(`Escaped filename: ${safeFilename}`);
  return safeFilename;
}

// Example usage
try {
  uploadFile('test_file.txt', 'This is the content of the test file.');
  listFiles();
  getFileDetails('test_file.txt');
  deleteFile('test_file.txt');
} catch (error) {
  console.error(`Error: ${error.message}`);
}
```

* In this example, below functions were implemented to prevent command injection:

* **File upload**
  * The `uploadFile()` function validates the filename, ensuring that only safe filenames and extensions are accepted.
  * It uses the `fs.writeFile()` function to safely write the file content.

* **File deletion**
  * The `deleteFile()` function safely deletes the file using `fs.rm()` after validating the filename.

* **List files**
  * The `listFiles()` function lists all the files in a safe directory using `fs.readdir()`, with no external shell commands involved.

* **File details**
  * The `getFileDetails()` function uses `execFile()` instead of exec() to safely run the file command, ensuring that the file path is validated and provided as a parameter, avoiding shell injection.

* **Escaping Input**
  * The `escapeFileName()` function demonstrates how special characters in a filename can be safely escaped using shell-quote.

### Libraries used

* **shell-quote**: Escapes special characters in shell arguments.
* **fs**: Safely handles file system operations, such as reading, writing, and deleting files.
