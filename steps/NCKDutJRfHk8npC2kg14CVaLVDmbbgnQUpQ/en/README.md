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

## Path and Namespace considerations

* Use a backslash (`\`) to separate path components.
* Fully qualified paths (starting with a drive letter or UNC path) should be correctly handled to avoid relative path issues.
* Be aware of special namespace prefixes like `\\?\` which allows bypassing MAX_PATH limitations and accessing extended-length paths.

## Multi-User and Virtualized environments

* In environments with multi-user support or virtual machines, consider namespace isolation to prevent conflicts and unauthorized access. Use symlinks appropriately to ensure paths resolve correctly in virtualized contexts.

## Vulnerable implementation (Unsanitized filenames)

* Below, we will explore how to properly sanitize filenames in Node.js, and illustrate a vulnerable implementation for contrast.

* Add the below dependencies.

```js
const express = require('express');
const multer = require('multer');
const path = require('path');
const app = express();
```

* Create logic to store the file and listen to the upload request from client.

```js
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

### Issues with this implementation

* **No input validation**: the filename is taken directly from the user input without any checks.
* **Directory Traversal**: malicious users can manipulate the filename to traverse directories (e.g., `../etc/passwd`).
* **Reserved Filenames**: users can upload files with reserved names (e.g., `CON`, `PRN`), which can cause issues in Windows.
* **Collision Risks**: users can upload files with the same name, leading to potential overwrites.

## Secure implementation (Sanitized filenames)

* When dealing with file uploads, there are two main situations:
  * **Random File Names**: If you don't need to keep the original file name, save the file with a randomly generated name (like "UUID").
  * **Keeping Original File Names**: If you need to save the file with its original name, follow these steps:
    * **Allowed Characters**: Only allow letters and numbers in the file name. Do not allow “.” or “/” to prevent issues like “../”.
    * **Maximum Length**: Set a limit on how long the file name can be.
    * **Windows Reserved Names**: Avoid using names reserved by Windows (like "CON" or "PRN").
    * **Filename Collisions**: Make sure no two files end up with the same name to prevent overwriting.

### Implementing the sanitized filename by generating random file name

* Initialize the below dependencies.

```js
const express = require('express');
const multer = require('multer');
const uuid = require('uuid');
const path = require('path');
const app = express();
```

* Configure **multer storage** to save files with random **UUID** names.

```js
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/'); // Ensure this directory exists and is outside web root
  },
  filename: (req, file, cb) => {
    cb(null, uuid.v4() + path.extname(file.originalname));
  }
});

const upload = multer({ storage });

app.post('/upload', upload.single('file'), (req, res) => {
  res.send('File uploaded with random name');
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

* The above examples is using **expressjs** along with **multer**. **Multer** is used to build files out of the incoming `POST` request with file in `multipart/form-data` format. It is configured to store files with random **UUID** names.

### Implementing the sanitized filename by keeping original file name

* Initialize the dependencies and build the allowed extension list and also reserved names list.

```js
const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const sanitize = require('sanitize-filename');
const app = express();

const MAX_FILENAME_LENGTH = 255; // Set your max length here
const ALLOWED_EXTENSIONS = ['.jpg', '.png', '.pdf']; // Example allowed extensions
const RESERVED_NAMES = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'LPT1']; // Example reserved names
```

* Create function to check if the file name is reserved.

```js
const isReservedName = (name) => {
  const baseName = path.basename(name, path.extname(name)).toUpperCase();
  return RESERVED_NAMES.includes(baseName);
};
```

* Configure **multer storage** to keep original names with security measures.

```js
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/'); // Ensure this directory exists and is outside web root
  },
  filename: (req, file, cb) => {
    let originalName = file.originalname;
    const ext = path.extname(originalName);

    // Check extension
    if (!ALLOWED_EXTENSIONS.includes(ext.toLowerCase())) {
      return cb(new Error('Invalid file extension'));
    }

    // Sanitize filename
    let baseName = sanitize(path.basename(originalName, ext)).replace(/[^a-zA-Z0-9]/g, '');

    // Ensure length limit
    if (baseName.length > MAX_FILENAME_LENGTH) {
      baseName = baseName.substring(0, MAX_FILENAME_LENGTH);
    }

    // Check reserved names
    if (isReservedName(baseName)) {
      return cb(new Error('Reserved file name'));
    }

    // Ensure no filename collisions
    let finalName = baseName + ext;
    const uploadDir = 'uploads/';
    let counter = 1;
    while (fs.existsSync(path.join(uploadDir, finalName))) {
      finalName = `${baseName}_${counter}${ext}`;
      counter++;
    }

    cb(null, finalName);
  }
});

const upload = multer({ storage });

app.post('/upload', upload.single('file'), (req, res) => {
  res.send('File uploaded with original name and security measures');
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

* In this example, we are taking care of the following:
  * The filename is sanitized to remove any special characters.
  * A check is performed to ensure the file extension is allowed.
  * The filename length is restricted to the maximum length defined.
  * Reserved names are avoided.
  * Filename collisions are prevented by appending a counter if a file with the same name already exists.
