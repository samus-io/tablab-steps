# User and Filesystem Permissions in File Upload

## Filesystem Permissions

* The files uploaded must be stored in a way that guarantee:
  * Allowed system users are the only ones capable of reading the files.
  * Required modes **(read, write, execute)** only are set for the file.

* If execution is required, scanning the file before running it is required as a security best practice, to ensure that no macros or hidden scripts are available.

## User permissions

* The file upload must be protected with authentication and authorization, as much as it is possible.
* Set the permissions to the file to write only.
* If read is required, set a proper control as:
  * Only internal IPs.
  * Only authorized users.

## Vulnerable Implementation

* This example shows how neglecting security measures can expose the system to various risks, such as unauthorized access, file tampering, and potential execution of malicious scripts.

```js
const express = require('express');
const multer = require('multer');
const fs = require('fs');
const path = require('path');

const app = express();
const upload = multer({ dest: 'uploads/' });

// File upload endpoint without authentication or authorization
app.post('/upload', upload.single('file'), (req, res) => {
    const filePath = path.join(__dirname, 'uploads', req.file.filename);

    // Incorrectly set permissions (readable, writable, and executable by anyone)
    fs.chmod(filePath, 0o777, (err) => {
        if (err) return res.status(500).send('Error setting file permissions');

        res.status(200).send('File uploaded successfully');
    });
});

// Endpoint to read the file without authorization or internal IP check
app.get('/file/:filename', (req, res) => {
    const filePath = path.join(__dirname, 'uploads', req.params.filename);
    
    res.sendFile(filePath);
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
```

* In this insecure implementation:
  * **No Authentication or Authorization**: Anyone can upload and access files.
  * **No Internal IP Check**: Files can be accessed from any IP address.
  * **Insecure File Permissions**: Files are set to be readable, writable, and executable by anyone (`0o777`), which is a significant security risk.

## Secure implementation

* In this secure implementation:
  * **Authentication and Authorization**: we use **JSON Web Token(JWT)** to ensure that only authenticated and authorized users can upload and read files.
  * **Internal IP Check**: we restrict file access to specific internal IP addresses.
  * **File Permissions**: after uploading a file, we set the file permissions to **write-only**. For read access, permissions are set to **read-only** and verified against user authorization.
  * The user uploads the file with `authorization` header containing **JWT** token when reading and writing the file.

* Add the dependencies and initialize.

```js
const express = require('express');
const jwt = require('jsonwebtoken');
const fs = require('fs');
const path = require('path');
const multer = require('multer');

const app = express();
const upload = multer({ dest: 'uploads/' });

// Secret key for JWT
const SECRET_KEY = 'your_secret_key';

app.use(express.json());
```

* Middleware for checking authentication and authorization. Here we verify the token with `SECRET_KEY` that was planned previously.

```js
function authenticateToken(req, res, next) {
    const token = req.header('Authorization').replace('Bearer ', '');
    if (!token) return res.sendStatus(401);

    jwt.verify(token, SECRET_KEY, (err, user) => {
        if (err) return res.sendStatus(403);
        req.user = user;
        next();
    });
}
```

* Function to check internal IP. Allowing access to specific IPs only

```js
function checkInternalIP(req, res, next) {
    const internalIPs = ['127.0.0.1', '::1']; // Example IPs, replace with actual internal IPs
    if (!internalIPs.includes(req.ip)) {
        return res.status(403).send('Access denied: Unauthorized IP');
    }
    next();
}
```

* File upload endpoint with authentication, authorization, and internal IP check. And, setting permission of file to **write-only**.

```js
app.post('/upload', authenticateToken, checkInternalIP, upload.single('file'), (req, res) => {
    const filePath = path.join(__dirname, 'uploads', req.file.filename);

    // Set permissions to write only
    fs.chmod(filePath, 0o200, (err) => {
        if (err) return res.status(500).send('Error setting file permissions');
        
        res.status(200).send('File uploaded successfully');
    });
});
```

* The permissions for the file is in octal format.It has 3 parts. All the three are 3 bit numbers representing file permission for different users. First bit indicates read permission, second bit for write and third for execute.

```bash
Syntax: 0o[owner][group][others]
Example: 0o777 // all permissions
```

* Endpoint to read the file, with authorization and internal IP check.

```js
app.get('/file/:filename', authenticateToken, checkInternalIP, (req, res) => {
    const filePath = path.join(__dirname, 'uploads', req.params.filename);

    // Check if the user has the right to read the file
    if (!req.user.canReadFiles) {
        return res.status(403).send('Access denied: Unauthorized user');
    }

    // Set read permission only if the user is authorized
    fs.chmod(filePath, 0o400, (err) => {
        if (err) return res.status(500).send('Error setting file permissions');

        res.sendFile(filePath);
    });
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
```
