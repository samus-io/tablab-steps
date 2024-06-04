# File upload extension validation

* Extension validation ensures that uploaded files conform to expected and allowed types by checking their file extensions. This is crucial to prevent malicious files (e.g., scripts or executables) from being uploaded under the guise of harmless files (e.g., images).
* Remember the following points for extension validation:
  * **Decoding File Names**: ensure that validation occurs after decoding the file name to avoid bypass techniques like double extensions (e.g., `.jpg.php`) or null bytes (e.g., `.php%00.jpg`).
  * **Proper Filters**: implement robust filters to avoid common pitfalls such as bad regex patterns that can be easily circumvented.
  * **Whitelist approach**: use a whitelist to only allow necessary extensions based on business requirements (e.g., only `.jpg`, `.png` for image uploads).
  * **Disallow multiple extensions**: reject files with more than one extension or no extension at all to prevent exploitation.

* Performing input validation on the front end is not sufficient as it can be bypassed and is just to improve user experience.
* Most important thing to remember is not to allow files without extension.
* Many developers make critical mistakes in implementing file upload security, leaving their applications vulnerable to attacks. Below is an example of a vulnerable implementation that fails to correctly validate file extensions, showcasing the pitfalls to avoid.

## Vulnerable implementation

* Add the below dependencies in your example code.

```js
const express = require('express');
const multer = require('multer');
const app = express();
```

* Use **multer** to store file. Initialize **multer** and add the destination where your file will be stored.

```js
const upload = multer({ dest: '<path to destination folder>' });
```

* Create a listener using **express.js** and listen on `/upload` route. Inside this handler the code is testing for the match of `.jpg` or `.jpeg` extensions in the uploaded file name.

```js
app.post('/upload', upload.single('file'), (req, res) => {
    const file = req.file;
    
    if (file.originalname.match(/\.(jpg|jpeg)$/)) {
        // Saving file without further checks
        res.send('File uploaded successfully');
    } else {
        res.status(400).send('Invalid file type');
    }
});

//Add the code for the server to listen on required port
```

* In this example, the server **(expressjs + nodejs)** only performs a basic extension check using a **regex**, which can be easily bypassed with filenames like `image.jpg.php`.
* No checks are performed on the multiple file extension or the presence of null bytes.

## Proper implementation of Secure File Upload

* To properly secure file uploads, follow these guidelines:
  * **Hardcode allowed extensions**: set allowed extensions in the backend.
  * **Use a Whitelist**: check the file extension against a whitelist of allowed extensions.
  * **Disallow multiple extensions**: ensure that files with more than one extension or no extension are rejected.

### Secure implementation

* Add the below dependencies in your example code.

```js
const express = require('express');
const multer = require('multer');
const path = require('path');
const app = express();
```

* Create a list of allowed extensions

```js
const allowedExtensions = ['jpg', 'jpeg'];
```

* Create a logic to store the uploaded file like using **multer**.

```js
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, '<path to destination folder>'); // specifying the destination for file store
    },
    filename: function (req, file, cb) {
        const ext = path.extname(file.originalname).toLowerCase();
        cb(null, `${file.fieldname}-${Date.now()}`); // changing the filename before storing
    }
});

const upload = multer({
    storage: storage,
    fileFilter: fileFilter, // this is defined in next point
    limits: { fileSize: 1024 * 1024 * 5 } // Limit to 5MB
});
```

* Create a filter fucntion that checks for the invalid file extension and attach it to **multer**.

```js
const fileFilter = (req, file, cb) => {
    const ext = path.extname(file.originalname).toLowerCase();
    
    // Check for null bytes
    if (file.originalname.indexOf('\0') !== -1) {
        return cb(new Error('Null bytes detected in file name'));
    }

    // Ensure there is exactly one extension
    const baseName = path.basename(file.originalname, ext);
    if (!allowedExtensions.includes(ext) || baseName.split('.').length !== 2) {
        return cb(new Error('Invalid file type or multiple extensions detected'));
    }

    cb(null, true);
};
```

* Listen to the file upload request from client.

```js
app.post('/upload', upload.single('file'), (req, res) => {
    res.send('File uploaded successfully');
});

// Add the listener for the server here

```

* In the above example, we are using **multer** to upload the file uploaded in `multipart/form-data` format. It uploads the data to the location specified in `dest` field.
* Before the storage operation, we are filtering the file with multiple extension check (ensuring file has one extension only), null bytes check and allowed extension check. So, when user sumbits the file via `POST` request, the backend performs these checks before uploading to `uploads/` location.

## Content-Type validation

* Content-Type validation checks the "MIME" type of the uploaded file to ensure it matches expected types. While not reliable for security (as it can be easily spoofed), it helps improve user experience by providing an initial check against incorrect file types.
* Remember the following points for Content-Type validation:
  * **User-Provided MIME Types**: the MIME type provided by the user cannot be trusted completely as it is easy to fake.
  * **Quick check**: Content-Type validation serves as a quick check to prevent users from unintentionally uploading wrong file types.
  * **Allowlist approach**: preferably use an allowlist to specify which MIME types are accepted. A denylist approach can be used as a backup, though it is less effective.

### Implementing Content-Type validation

* Add the below function to create the filter for request Content-Type header.

```js
const contentTypeFilter = (req, file, cb) => {
    const mimeTypes = ['image/jpeg'];
    if (!mimeTypes.includes(file.mimetype)) {
        return cb(new Error('Invalid content type'));
    }
    cb(null, true);
};
```

* Update the **multer** to include above filter function.

```js
const upload = multer({
    storage: storage,
    fileFilter: (req, file, cb) => {
        fileFilter(req, file, (err) => {
            if (err) return cb(err);
            contentTypeFilter(req, file, cb);
        });
    },
    limits: { fileSize: 1024 * 1024 * 5 } // Limit to 5MB
});
```

* This code snippet extends the above given secure implementation example and ensures only files with **MIME** types `image/jpeg` or `image/png` are allowed.
* First check done using **fileFilter** (already defined in the previous section) ensures only appropriate file extensions are permitted. After that the **contentTypeFilter** is applied.
