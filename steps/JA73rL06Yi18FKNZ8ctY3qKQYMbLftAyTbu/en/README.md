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
  * **Prevents Direct URL Access**: direct access to file URLs (e.g., `http://example.org/uploads/file.ext`) can expose your application to several security risks, such as unauthorized file access, directory traversal attacks, or exposing sensitive information through predictable URLs.
  * **Hides File Structure**: using IDs instead of filenames in URLs helps hide the actual file structure and names, making it more difficult for attackers to guess and access files directly.
  * **Adds a Layer of Access Control**: a handler can include logic to check permissions or other access controls before serving a file, ensuring that only authorized users can access certain files.
* When a file is uploaded, it is stored on the server with a **unique identifier (ID)**. The mapping between this **ID** and the actual filename is stored in a database or similar storage system.
* When a user requests a file, they do so via the handler with the **unique ID** (e.g., `http://example.org/file/12345`). The handler then looks up the **ID** in the mapping system, retrieves the corresponding file, and serves it.

## Vulnerable implementation

* Below is an example of a Node.js application that does not correctly implement these security measures.

```js
const express = require('express');
const multer = require('multer');
const path = require('path');

const app = express();

// Bad implementation: direct file storage without validation
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'public/uploads/'); // Files are stored in webroot, accessible via URL
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

* **Storage in Webroot**: files are stored in the public/uploads/ directory, making them directly accessible via URL (`http://example.org/uploads/filename.ext`). This exposes files to potential unauthorized access.
* **No Temporary Storage for Validation**: files are saved directly without being stored temporarily for validation. This means any file, even if it is malicious, can be saved and accessed immediately.
* **No internal logic to map files**: the original filename is used without any mapping of file with internal identifier.

## Secured implementation

* To correct these issues, follow the below points:
  * **Temporary Storage and Validation**: save files temporarily and move them to the permanent location only after passing validation.
  * **Store Files Outside Webroot**: store files in a directory not accessible via the web, such as outside the public directory.
  * **Internal filename Handling**: sanitize filenames and map internal identifiers to filenames for public access.

* To implement the described functionality in Node.js, we'll use the `express` framework for handling HTTP requests, `multer` for handling file uploads, and `fs` for file system operations.

### Setting Up the Project

* First, make sure you have Node.js installed. Initialize your project and install the necessary dependencies:

```bash
npm init -y
npm install express multer uuid fs-extra
```

### Project Structure

* Create the following structure for your project:

```js
project-root
└───app.js
└───package.json
└───uploads
└───temp
```

### Implementing the Functionality

* Here's a complete implementation based on the requirements:

```js
// app.js
const express = require('express');
const multer = require('multer');
const fs = require('fs-extra');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

const app = express();
const port = 3000;

// Configure multer for temporary storage
const tempStorage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'temp/');
  },
  filename: (req, file, cb) => {
    const tempFilename = `${uuidv4()}-${file.originalname}`;
    cb(null, tempFilename);
  }
});

const upload = multer({ storage: tempStorage });

// Middleware to validate files
const validateFile = (req, res, next) => {
  // Dummy validation logic: check if file size is less than 5MB
  if (req.file.size > 5 * 1024 * 1024) {
    return res.status(400).send('File is too large');
  }
  next();
};

// Route to handle file upload
app.post('/upload', upload.single('file'), validateFile, async (req, res) => {
  try {
    const tempPath = req.file.path;
    const targetDir = 'uploads'; // Storing outside webroot
    const targetPath = path.join(targetDir, req.file.filename);

    // Ensure uploads directory exists
    await fs.ensureDir(targetDir);

    // Move file from temp to uploads directory
    await fs.move(tempPath, targetPath);

    // return the filename to the app for further fetches
    res.status(200).send(`File uploaded successfully: ${req.file.filename}`);
  } catch (error) {
    res.status(500).send('Error uploading file');
  }
});

// Public access handler
app.get('/files/:id', async (req, res) => {
  try {
    const fileId = req.params.id;
    const files = await fs.readdir('uploads');
    const file = files.find(f => f.includes(fileId));

    if (!file) {
      return res.status(404).send('File not found');
    }

    const filePath = path.join('uploads', file);
    res.download(filePath);
  } catch (error) {
    res.status(500).send('Error retrieving file');
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
```

#### Explanation on the above implementation

* **Multer Configuration**: we configure multer to store files temporarily in the `temp` directory using a unique filename.
* **Validation Middleware**: we validate the uploaded file (e.g., checking the file size) before moving it to the final directory.
* **File Upload Route**: the `/upload` route handles file uploads, validates the file, and moves it from the `temp` directory to the `uploads` directory.
* **Public Access Handler**: the `/files/:id` route serves files securely by mapping file IDs to filenames and ensuring the files are served from outside the webroot.
