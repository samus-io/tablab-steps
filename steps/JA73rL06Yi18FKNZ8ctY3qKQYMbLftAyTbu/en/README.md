# File storage location in File Upload

* Note the following points before storing the uploaded file to the planned storage location.

## Do not upload files to the server's permanent filesystem until they have been fully validated

* Files should be stored temporarily and only moved to the permanent location after all validation checks are passed.

## Store the files on a different server

* If possible, files should be stored on a separate server dedicated to handling file storage to minimize the impact of potential vulnerabilities.

## Store them outside of the webroot

* Files should be stored in directories not accessible via the web to prevent direct URL access.
* Below are the implementation phases:
  * Create a directory for storing uploaded files outside the web-accessible root directory of the application.
  * Use a file storage configuration that directs uploads to the secure directory.
  * Implement a server-side handler that retrieves files from the secure directory and serves them to authenticated users.

## Use a handler for public access

* If files need to be accessed publicly, use a handler that maps internal file identifiers to filenames (e.g., mapping **unique Id** to **filename**).
* Instead of allowing direct access to uploaded files through URLs, implement a server-side handler that serves the files. This handler should use an internal mapping system to reference files by **unique identifiers (IDs)** rather than their actual filenames.
* This is Important because it:
  * **Prevents direct URL access**: direct access to file URLs (e.g., `http://example.org/uploads/file.ext`) can expose your application to several security risks, such as unauthorized file access, directory traversal attacks, or exposing sensitive information through predictable URLs.
  * **Hides file structure**: using IDs instead of filenames in URLs helps hide the actual file structure and names, making it more difficult for attackers to guess and access files directly.
  * **Adds a layer of access control**: a handler can include logic to check permissions or other access controls before serving a file, ensuring that only authorized users can access certain files.
* When a file is uploaded, it is stored on the server with a **unique identifier (ID)**. The mapping between this **ID** and the actual filename is stored in a database or similar storage system.
* When a user requests a file, they do so via the handler with the **unique ID** (e.g., `http://example.org/file/12345`). The handler then looks up the **ID** in the mapping system, retrieves the corresponding file, and serves it.

## Vulnerable implementation

* Below is an example of a Node.js application that does not correctly implement the above security measures and is using **multer** to store file.

```js
const express = require('express');
const multer = require('multer');
const path = require('path');

const app = express();

// Bad implementation: direct file storage without validation
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, '<absolute path to public folder>'); // Files are stored in webroot, accessible via URL
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname); // Original filename is used without sanitization
  }
});

// this is used to store uploaded files
const upload = multer({ storage });

// listener and upload request handler
app.post('/upload', upload.single('file'), (req, res) => {
  res.send('File uploaded');
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

### Breakdown of the above implementation

* **Storage in Webroot**: files are stored in the public directory, making them directly accessible via URL. This exposes files to potential unauthorized access.
* **No temporary storage for validation**: files are saved directly without being stored temporarily for validation. This means any file, even if it is malicious, can be saved and accessed immediately.
* **No internal logic to map files**: the original filename is used without any mapping of file with internal identifier.

## Secured implementation

* To correct these issues, follow the below points:
  * **Temporary storage and validation**: save files temporarily and move them to the permanent location only after passing validation.
  * **Store files outside Webroot**: store files in a directory not accessible via the web, such as outside the public directory.
  * **Internal filename handling**: sanitize filenames and map internal identifiers to filenames for public access.

* To implement the described functionality in Node.js, we'll use the `express` framework for handling HTTP requests, `multer` for handling file uploads, and `fs-extra` for file system operations.

### Setting up the project

* First, make sure you have Node.js installed. Initialize your project and install the necessary dependencies:

```bash
npm init -y
npm install express multer uuid fs-extra
```

### Project structure

* Create the following structure for your project:

```js
project-root
└───app.js
└───package.json
└───uploads
└───temp
```

* The `package.json` is used just to simplify the process of executing `app.js` via `scripts`

### Implementing the functionality

* Initialize all the below dependencies.

```js
// app.js
const express = require('express');
const multer = require('multer');
const fs = require('fs-extra');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

const app = express();
const port = 3000;
```

* Configure multer for temporary storage. Point the destination to some temporary folder. Name the file using **UUID** before storing it.

```js
const tempStorage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, '<absolute path to temp folder>'); // Files are initially stored in temporary folder
  },
  filename: (req, file, cb) => {
    const tempFilename = `${uuidv4()}`; // Naming the file using UUID V4 only
    cb(null, tempFilename);
  }
});

```

* Create a function to validate files.

```js
const validateFile = (req, file, cb) => {
  // Dummy validation logic: check if file size is less than 5MB
  if (req.file.size > 5 * 1024 * 1024) {
    return cb(null, false);
  }
  cb(null, true);
};
```

* Add both the **validateFile** and **tempStorage** to **multer**.

```js
const upload = multer({ storage: tempStorage, fileFilter: validateFile });
```

* Create a route to handle file upload. This will make the **multer** to handle the storing operation first and then a callback is attached to move the file to permanent location.

```js
app.post('/upload', upload.single('file'), async (req, res) => {
  try {
    const tempPath = path.resolve(req.file.path);
    const targetDir = '<absolute path to uploads folder>'; // Storing outside webroot
    const targetPath = path.join(targetDir, req.file.filename); // Creating path to move the file in uploads folder

    // Ensure uploads directory exists
    await fs.ensureDir(targetDir);

    // Move file from temp to uploads directory
    await fs.move(tempPath, targetPath);

    // return the filename to the app for further fetches
    res.status(200).send(`File uploaded successfully: ${path.resolve(req.file.path)}`);
  } catch (error) {
    res.status(500).send('Error uploading file');
  }
});
```

* Create a route to download the Publicly accessible files.

```js
app.get('/files/:id', async (req, res) => {
  try {
    const fileId = req.params.id;

    // Validate fileId to match UUID v4 format
    const uuidv4Regex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
    if (!uuidv4Regex.test(fileId)) {
      return res.status(400).send('Invalid file ID format');
    }

    // List the files in ./uploads folder
    const files = await fs.readdir('uploads');

    // Check the file availability
    const file = files.find(f => f.includes(fileId));

    if (!file) {
      return res.status(404).send('File not found');
    }

    // resolve to the file's absolute path and send it to the client
    const filePath = path.resolve('uploads', file);
    res.download(filePath);
  } catch (error) {
    res.status(500).send('Error retrieving file');
  }
});

// Start the server here...

```

#### Explanation on the above implementation

* **Multer configuration**: we configure multer to store files temporarily in the `temp` directory using a unique filename.
* **Validation middleware**: we validate the uploaded file (e.g., checking the file size) before moving it to the final directory.
* **File upload route**: the `/upload` route handles file uploads, validates the file, and moves it from the `temp` directory to the `uploads` directory.
* **Public access handler**: the `/files/:id` route serves files securely by mapping file IDs to filenames and ensuring the files are served from outside the webroot with validation.
