# Complete solution for insecure file upload

* Let's create a realistic scenario of a file upload system in Node.js that incorporates all the security measures.
* In this example, we will build a simple Node.js application using Express and Multer for file uploads. We'll implement security measures for `jpg` or `jpeg` image file extension validation, filename sanitization, upload/download limits, file content validation, and user/filesystem permissions.

## Prerequisites

* Install **Node.js** and **npm**.
* Create a new project directory and run `npm init -y` to initialize a new Node.js project.
* Install necessary packages:

```bash
npm install express multer file-type sharp rate-limit fs-extra
```

## Directory structure

```bash
secure-file-upload/
├── node_modules/
├── uploads/
├── app.js
└── package.json
```

## Implementation

```js
const express = require('express');
const multer = require('multer');
const sharp = require('sharp');
const rateLimit = require('express-rate-limit');
const fs = require('fs-extra');
const path = require('path');
const uuid = require('uuid');

const app = express();
const PORT = 3000;

const MAX_FILENAME_LENGTH = 255; // Set your max length here
const ALLOWED_EXTENSIONS = ['jpg','jpeg']; // Example allowed extensions
const RESERVED_NAMES = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'LPT1']; // Example reserved names

const isReservedName = (name) => {
  const baseName = path.basename(name, path.extname(name)).toUpperCase();
  return RESERVED_NAMES.includes(baseName.substr(0, baseName.length-1));
}

// Create the uploads directory if it doesn't exist
fs.ensureDirSync(path.join(__dirname, 'uploads'));

// Rate limiter for uploads to prevent DoS attacks
const uploadLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5, // Limit each IP to 5 upload requests per windowMs
    message: 'Too many uploads from this IP, please try again later.'
});

// Multer configuration for file upload handling
const storage = multer.memoryStorage();
const upload = multer({
    storage,
    limits: { fileSize: 5 * 1024 * 1024 }, // 5 MB file size limit
    fileFilter: (req, file, cb) => {
        // File extension validation
        const ext = path.extname(file.originalname).toLowerCase().slice(1);
        if (!ALLOWED_EXTENSIONS.includes(ext)) {
            return cb(new Error('Invalid file extension'), false);
        }

        // File name sanitization
        // Check for null bytes
        if (file.originalname.indexOf('\0') !== -1) {
            return cb(new Error('Null bytes detected in file name'));
        }

        // Ensure there is exactly one extension
        const baseName = path.basename(file.originalname, ext);
        if (!ALLOWED_EXTENSIONS.includes(ext) || baseName.split('.').length !== 2) {
            return cb(new Error('Invalid file type or multiple extensions detected'));
        }

        // Check for invalid characters
        if(baseName.substr(0, baseName.length-1).match(/[^a-zA-Z0-9_\-\.]/g)?.length){
           return cb(new Error('Invalid file name'));
        }

        // Ensure length limit
        if (baseName.substr(0, baseName.length-1).length > MAX_FILENAME_LENGTH) {
          return cb(new Error('Invalid file length'));
        }

        // Check reserved names
        if (isReservedName(baseName)) {
          return cb(new Error('This filename is reserved'));
        }
        cb(null, true);
    }
}).single('file');

// File content validation
const validateFileContent = async (buffer) => {
    // Create your own logic to validate the file. Use libraries to parse this buffer
    return buffer;
};

// Authntication and Authorization
function authenticateToken(req, res, next) {
    const token = req.header('Authorization')?.replace('Bearer ', '');
    if (!token) return res.sendStatus(401);

    jwt.verify(token, SECRET_KEY, (err, user) => {
        if (err) return res.sendStatus(403);
        req.user = user;
        next();
    });
}

function checkInternalIP(req, res, next) {
    const internalIPs = ['127.0.0.1', '::1']; // Example IPs, replace with actual internal IPs
    if (!internalIPs.includes(req.ip)) {
        return res.status(403).send('Access denied: Unauthorized IP');
    }
    next();
}

// Upload endpoint
app.post('/upload', authenticateToken, checkInternalIP, uploadLimiter, (req, res) => {
    upload(req, res, async (err) => {
        if (err) {
            return res.status(400).send({ message: err.message });
        }

        if (!req.file) {
            return res.status(400).send({ message: 'No file uploaded' });
        }

        const uploadPath = path.join(__dirname, 'uploads', uuid.v4());

        try {
            // Validate and process file content
            const validatedBuffer = await validateFileContent(req.file.buffer);
            await fs.writeFile(uploadPath, validatedBuffer);
            res.status(200).send({ message: 'Success' });
        } catch (error) {
            res.status(500).send({ message: 'Error processing file' });
        }
    });
});

// Download endpoint with rate limiting
const downloadLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 10, // Limit each IP to 10 download requests per windowMs
    message: 'Too many download requests from this IP, please try again later.'
});

app.get('/download/:fileId', downloadLimiter, (req, res) => {
    // Validate fileId to match UUID v4 format
    const uuidv4Regex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
    if (!uuidv4Regex.test(fileId)) {
      return res.status(400).send('Invalid file ID format');
    }
    const filePath = path.join(__dirname, 'uploads', req.params.fileId);

    // Check if the file exists
    if (!fs.existsSync(filePath)) {
        return res.status(404).send({ message: 'File not found' });
    }

    res.download(filePath);
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
```

## Security Measures in Place

* **File Extension Validation**: implemented in the **fileFilter** function of the **Multer** configuration to only allow specific file extensions (`jpg`, `jpeg`).

* **Filename Sanitization**: the **fileFilter** function checks for all non-alphanumeric characters (excluding `_`, `-`, `.`) with underscores to prevent directory traversal attacks and other filename-based exploits.

* **Upload/Download Limits**: rate limiting is implemented using **express-rate-limit** to limit the number of upload and download requests per IP address in a given time window, preventing DoS attacks.

* **File Content Validation**: the **validateFileContent** function can use any library to validate the file content.

* **User and Filesystem Permissions**: the uploads directory is ensured to exist with **fs.ensureDirSync**, and all file operations are performed using **fs-extra** which handles file system operations safely. Add the explicit READ permissions to the `./uploads` folder if you want to restrict it for public access.

* **File storage location**: the file should be uploaded to a location away from the web-root. So, create the `./uploads` from away from the root.
