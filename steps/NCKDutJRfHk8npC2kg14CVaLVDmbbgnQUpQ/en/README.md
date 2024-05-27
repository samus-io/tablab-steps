# Filename Sanitization

* Filename sanitization is a crucial process aimed at ensuring filenames are safe and compatible with the system they will be used on. This involves validating and possibly modifying filenames to prevent issues that could compromise system security or functionality.
* The below are the key considerations and strategies for effective filename sanitization.

## Character restrictions

* Different file systems have specific characters that are not allowed in filenames. For Windows, these characters include:
  * < (less than)
  * \> (greater than)
  * : (colon)
  * " (double quote)
  * / (forward slash)
  * \ (backslash)
  * | (vertical bar or pipe)
  * ? (question mark)
  * \* (asterisk)
* ASCII NUL character (integer value zero)
* Characters with integer representations from 1 through 31
* Certain names are reserved and should not be used for files:

```bash
CON, PRN, AUX, NUL, COM0 through COM9, LPT0 through LPT9
```

## Length Limits

* Different file systems impose different limits on filename length. For example, the MS-DOS FAT file system has an 8.3 filename limit (8 characters for the name and 3 for the extension). Modern systems like NTFS allow much longer names, but Windows traditionally has a MAX_PATH limit of 260 characters. Consider these limits and ensure filenames do not exceed them.

## Case sensitivity

* Windows file systems typically do not differentiate between uppercase and lowercase letters in filenames. Treat OSCAR, Oscar, and oscar as identical to avoid conflicts.

## Use of Periods and Spaces

* Avoid ending filenames with a period or a space, as these can cause issues in Windows Explorer and other applications, even if the underlying file system supports them. However, using a period at the beginning of a filename (e.g., `.temp`) is acceptable.

## Random and Unique filenames

* To avoid conflicts and potential malicious exploitation, generate random and unique filenames, such as using UUIDs or GUIDs. This is especially useful when filenames do not need to convey specific information.

## Input validation

* When filenames are required to be user-defined, validate input rigorously:
  * Implement a maximum length for filenames.
  * Restrict characters to a safe subset (e.g., alphanumeric characters, hyphens, spaces, and periods).
  * If a restrictive whitelist is impractical, use a blacklist to block dangerous characters and patterns.

## Path and Namespace considerations

* Use a backslash (`\`) to separate path components.
* Fully qualified paths (starting with a drive letter or UNC path) should be correctly handled to avoid relative path issues.
* Be aware of special namespace prefixes like `\\?\` which allows bypassing MAX_PATH limitations and accessing extended-length paths.

## Multi-User and Virtualized environments

* In environments with multi-user support or virtual machines, consider namespace isolation to prevent conflicts and unauthorized access. Use symlinks appropriately to ensure paths resolve correctly in virtualized contexts.

## Bad implementation (Unsanitized filenames)

* Below, we will explore how to properly sanitize filenames in Node.js, and illustrate a bad implementation for contrast.

```js
const express = require('express');
const multer = require('multer');
const path = require('path');
const app = express();

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/');
    },
    filename: function (req, file, cb) {
        cb(null, file.originalname); // BAD: Directly using the original filename
    }
});

const upload = multer({ storage: storage });

app.post('/upload', upload.single('file'), (req, res) => {
    res.send('File uploaded successfully');
});

app.listen(3000, () => {
    console.log('Server started on http://localhost:3000');
});
```

### Issues with the bad implementation

* **No input validation**: the filename is taken directly from the user input without any checks.
* **Directory Traversal**: malicious users can manipulate the filename to traverse directories (e.g., `../etc/passwd`).
* **Reserved Filenames**: users can upload files with reserved names (e.g., `CON`, `PRN`), which can cause issues in Windows.
* **Collision Risks**: users can upload files with the same name, leading to potential overwrites.

## Good implementation (Sanitized filenames)

* To address these issues, we will:
  * Generate a UUID for each file to avoid collisions and sanitize the filename.
  * Restrict the allowed characters if we must keep the original filename.
  * Implement maximum length checks.
  * Avoid reserved filenames in Windows.

```js
const express = require('express');
const multer = require('multer');
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const app = express();

const MAX_FILENAME_LENGTH = 255;
const allowedExtensions = ['.jpg', '.jpeg', '.png'];
const reservedFilenames = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'];

const sanitizeFilename = (filename) => {
    const ext = path.extname(filename).toLowerCase();
    // get rid of restricted characters
    const baseName = path.basename(filename, ext).replace(/[^a-z0-9\-. ]/gi, '_').slice(0, MAX_FILENAME_LENGTH - ext.length);
    
    // Check for reserved filenames
    if (reservedFilenames.includes(baseName.toUpperCase())) {
        throw new Error('Invalid file name');
    }
    
    return `${baseName}${ext}`;
};

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/');
    },
    filename: function (req, file, cb) {
        const ext = path.extname(file.originalname).toLowerCase();
        const sanitizedFilename = sanitizeFilename(file.originalname);

        // Generate a unique filename using UUID
        const uniqueFilename = `${uuidv4()}${ext}`;
        
        cb(null, uniqueFilename);
    }
});

const fileFilter = (req, file, cb) => {
    const ext = path.extname(file.originalname).toLowerCase();
    
    // Check for null bytes and disallowed extensions
    if (file.originalname.indexOf('\0') !== -1 || !allowedExtensions.includes(ext)) {
        return cb(new Error('Invalid file type or null bytes detected'));
    }

    cb(null, true);
};

const upload = multer({
    storage: storage,
    fileFilter: fileFilter,
    limits: { fileSize: 1024 * 1024 * 5 } // Limit to 5MB
});

app.post('/upload', upload.single('file'), (req, res) => {
    res.send('File uploaded successfully');
});

app.use((err, req, res, next) => {
    if (err) {
        res.status(400).send(err.message);
    }
});

app.listen(3000, () => {
    console.log('Server started on http://localhost:3000');
});
```

* In above example, we are performing all the recommended checks on filename before uploding the file after the user makes a `POST` request to `/upload` route. Additionally, we are also validating the extension name using **fileFilter** function. The above examples are using **expressjs** along with **multer**. Multer is used to build files out of the incoming `POST` request with file in `multipart/form-data` format.

### Explanation of good implementation

* **UUID for filenames**: we use **uuidv4()** to generate a unique filename, avoiding filename collisions.
* **Sanitizing filenames**: **sanitizeFilename** function restricts the allowed characters to alphanumeric, hyphens, dots, and spaces. It also checks for reserved filenames.
* **File Filter**: checks for null bytes and validates allowed extensions.
* **Error handling**: proper error messages are sent back to the client if the upload fails.
