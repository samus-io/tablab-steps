# File upload extension validation

* Extension validation ensures that uploaded files conform to expected and allowed types by checking their file extensions. This is crucial to prevent malicious files (e.g., scripts or executables) from being uploaded under the guise of harmless files (e.g., images).
* Remember the following points for extension validation:
  * **Decoding File Names:** ensure that validation occurs after decoding the file name to avoid bypass techniques like double extensions (e.g., .jpg.php) or null bytes (e.g., .php%00.jpg).
  * **Proper Filters:** implement robust filters to avoid common pitfalls such as bad regex patterns that can be easily circumvented.
  * **Whitelist Approach:** use a whitelist to only allow necessary extensions based on business requirements (e.g., only .jpg, .png for image uploads).
  * **Disallow Multiple Extensions:** reject files with more than one extension or no extension at all to prevent exploitation.

* Many developers make critical mistakes in implementing file upload security, leaving their applications vulnerable to attacks. Below is an example of a bad implementation that fails to correctly validate file extensions, showcasing the pitfalls to avoid.

## Bad Implementation Example

```js
// Bad implementation: File upload without proper validation
const express = require('express');
const multer = require('multer');
const app = express();
const upload = multer({ dest: 'uploads/' });

app.post('/upload', upload.single('file'), (req, res) => {
    const file = req.file;
    
    // Only checking extension on client-side is not enough
    if (file.originalname.match(/\.(jpg|jpeg|png)$/)) {
        // Saving file without further checks
        res.send('File uploaded successfully');
    } else {
        res.status(400).send('Invalid file type');
    }
});

app.listen(3000, () => {
    console.log('Server started on http://localhost:3000');
});
```

* In this example, the server (expressjs + nodejs) only performs a basic extension check using a regex, which can be easily bypassed with filenames like `image.jpg.php`.
* No checks are performed on the actual content of the file or the presence of null bytes.
* Performing input validation on the front end is not sufficient as it can be bypassed.

## Proper Implementation of Secure File Upload

* To properly secure file uploads, follow these guidelines:
  * **Hardcode Allowed Extensions:** set allowed extensions in the backend.
  * **Use a Whitelist:** check the file extension against a whitelist of allowed extensions.
  * **Disallow Multiple Extensions:** ensure that files with more than one extension or no extension are rejected.
  * **Content Type Validation:** validate the content type to improve user experience but not rely on it for security.

### Good Implementation Example

```js
const express = require('express');
const multer = require('multer');
const path = require('path');
const app = express();

const allowedExtensions = ['.jpg', '.jpeg', '.png'];

// ultimately stores the file 
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/');
    },
    filename: function (req, file, cb) {
        const ext = path.extname(file.originalname).toLowerCase();
        cb(null, `${file.fieldname}-${Date.now()}${ext}`);
    }
});

// filters before the file upload
const fileFilter = (req, file, cb) => {
    const ext = path.extname(file.originalname).toLowerCase();
    
    // Check for null bytes
    if (file.originalname.indexOf('\0') !== -1) {
        return cb(new Error('Null bytes detected in file name'));
    }

    // Ensure there is exactly one extension
    const baseName = path.basename(file.originalname, ext);
    if (!allowedExtensions.includes(ext) || baseName.includes('.')) {
        return cb(new Error('Invalid file type or multiple extensions detected'));
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

* In the above example, we are using **multer** to upload the file uploaded in `multipart/form-data` format. It uploads the data to the location specified in `dest` field.
* Before the storage operation, we are filtering the file with double extension check, null bytes check and allowed extension check. So, when user sumbits the file via `POST` request, the backend performs these checks before uploading to `uploads/` location.

## Content-Type Validation

* Content-Type validation checks the "MIME" type of the uploaded file to ensure it matches expected types. While not reliable for security (as it can be easily spoofed), it helps improve user experience by providing an initial check against incorrect file types.
* Remember the following points for Content-Type validation:
  * **User-Provided MIME Types:** the MIME type provided by the user cannot be trusted completely as it is easy to fake.
  * **Quick Check:** Content-Type validation serves as a quick check to prevent users from unintentionally uploading wrong file types.
  * **Allowlist Approach:** preferably use an allowlist to specify which MIME types are accepted. A denylist approach can be used as a backup, though it is less effective.

### Example

```js
const contentTypeFilter = (req, file, cb) => {
    const mimeTypes = ['image/jpeg', 'image/png'];
    if (!mimeTypes.includes(file.mimetype)) {
        return cb(new Error('Invalid content type'));
    }
    cb(null, true);
};

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

* This code snippet extends the above given good implementation example and ensures only files with MIME types `image/jpeg` or `image/png` are allowed.
* Additional checks using **fileFilter** ensures only appropriate file extensions are permitted. After that the **contentTypeFilter** is applied.
