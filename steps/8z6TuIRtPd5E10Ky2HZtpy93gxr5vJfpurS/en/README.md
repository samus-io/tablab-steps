# Upload and download limits when uploading files

* When implementing file upload and download functionality in an application, it's crucial to impose certain limits to ensure security and performance. Here are the key limitations you should consider:
  * **Limit the file size**: restrict the maximum size of each uploaded file to prevent excessive use of storage space and to protect the server from handling overly large files that could affect performance or cause crashes.
  * **Limit the number of uploads**: to safeguard your storage capacity and prevent a **Denial of Service (DoS)** attack, restrict the total number of uploads a user can perform. This helps avoid scenarios where a user floods the server with numerous files, depleting storage resources.
  * **Limit the number of files in a given time period**: implement a rate limit on uploads to prevent a single user from overloading the server with multiple upload requests within a short timeframe. This helps manage server load and ensures fair usage.
  * **Limit Download/Request rates**: similar to upload limits, control the number of download requests a user can make within a specific time period to prevent abuse and ensure that the server can handle legitimate traffic efficiently.

## Vulnerable implementation

* Here's an example of a vulnerable implementation where the above security measures are not properly applied in **multer** and **express**:

```js
const express = require('express');
const multer = require('multer');
const app = express();
const uuid = require('uuid');

// No limits on file size or number of uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, '<absolute path to uploads folder>'); // add path to the folder where you would like to store the files
  },
  filename: (req, file, cb) => {
    const filename = `${uuid.v4()}`; // Naming the file using UUID V4 only
    cb(null, filename);
  }
});

const upload = multer({
  storage: storage
});

//endpoint to upload the file
app.post('/upload', upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).send('No file uploaded.');
  }
  res.send('File uploaded successfully.');
});

//endpoint to read the file
app.get('/download/:fileId', (req, res) => {
  // Validate fileId to match UUID v4 format
  const uuidv4Regex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
  if (!uuidv4Regex.test(req.params.fileId)) {
    return res.status(400).send('Invalid file ID format');
  }
  const filePath = req.params.fileId;
  const options = {
    root: __dirname + '/uploads/',
    dotfiles: 'deny',
  };

  res.sendFile(filePath, options, (err) => {
    if (err) {
      res.status(404).send('File not found.');
    }
  });
});

// Start the server at port 3000
app.listen(3000, () => {
  console.log('Server started on port 3000');
});
```

### Issues with this implementation

* **No file size limit**: without a file size limit, users can upload extremely large files, potentially leading to server crashes or excessive use of storage.
* **No upload rate limit**: users can flood the server with upload requests, which can exhaust server resources and cause a DoS attack.
* **No download rate limit**: users can repeatedly request downloads, which can overload the server and affect performance for all users.
* **No proper error handling for uploads**: if an error occurs during the upload process, it is not properly handled, which could lead to issues in user experience and potential security vulnerabilities.

## Secure implementation

* Below is an example of how to implement these limits in a Node.js application using the **express** framework, **multer** middleware for handling file uploads and **express-rate-limit** for upload/download rate limiting. Create `./uploads` folder where you will store the valid uploaded files.

* Initialize the below dependencies.

```js
const express = require('express');
const multer = require('multer');
const rateLimit = require('express-rate-limit');
const app = express();
const uuid = require('uuid');

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, '<absolute path to uploads folder>'); // Add path to the folder where you would like to store the files
  },
  filename: (req, file, cb) => {
    const filename = `${uuid.v4()}`; // Naming the file using UUID V4 only
    cb(null, filename);
  }
});

// Configure multer for file uploads
const upload = multer({
  storage: storage,
  limits: {
    fileSize: 1 * 1024 * 1024 // 1 MB file size limit
  }
});
```

* Rate limit for uploads to max 10 requests per minute per IP

```js
const uploadRateLimit = rateLimit({
  windowMs: 60 * 1000, // 1 minute window
  max: 10, // limit each IP to 10 requests per windowMs
  message: 'Too many upload requests from this IP, please try again after a minute'
});
```

* Rate limit for downloads to max 20 requests per minute per IP.

```js
const downloadRateLimit = rateLimit({
  windowMs: 60 * 1000, // 1 minute window
  max: 20, // limit each IP to 20 requests per windowMs
  message: 'Too many download requests from this IP, please try again after a minute'
});
```

* Listen to the `POST` upload request and apply the upload limit before uploading.

```js
app.post('/upload', uploadRateLimit, upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).send('No file uploaded.');
  }
  res.send('File uploaded successfully.');
});
```

* Listen to the `GET` download request and apply download limit before sending the file.

```js
app.get('/download/:fileId', downloadRateLimit, (req, res) => {

  // Validate fileId to match UUID v4 format
  const uuidv4Regex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
  if (!uuidv4Regex.test(req.params.fileId)) {
    return res.status(400).send('Invalid file ID format');
  }
  const filePath = req.params.fileId;
  const options = {
    root: __dirname + '/uploads/',
    dotfiles: 'deny',
  };

  res.sendFile(filePath, options, (err) => {
    if (err) {
      res.status(404).send('File not found.');
    }
  });
});
```

* Finally, start the server.
