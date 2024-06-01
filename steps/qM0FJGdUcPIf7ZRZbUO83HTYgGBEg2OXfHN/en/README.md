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

## Directory Structure

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
const fileType = require('file-type');
const sharp = require('sharp');
const rateLimit = require('express-rate-limit');
const fs = require('fs-extra');
const path = require('path');

const app = express();
const PORT = 3000;

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
        const validExtensions = ['jpg', 'jpeg'];
        const ext = path.extname(file.originalname).toLowerCase().slice(1);
        if (!validExtensions.includes(ext)) {
            return cb(new Error('Invalid file extension'), false);
        }
        cb(null, true);
    }
}).single('file');

// Middleware to sanitize filenames
const sanitizeFilename = (filename) => {
    return filename.replace(/[^a-zA-Z0-9_\-\.]/g, '_');
};

// File content validation for images (removing metadata)
const validateImageContent = async (buffer) => {
    const { ext } = await fileType.fromBuffer(buffer) || {};
    if (['jpg', 'jpeg'].includes(ext)) {
        return sharp(buffer).withMetadata({ remove: true }).toBuffer();
    }
    return buffer;
};

// Upload endpoint
app.post('/upload', uploadLimiter, (req, res) => {
    upload(req, res, async (err) => {
        if (err) {
            return res.status(400).send({ message: err.message });
        }

        if (!req.file) {
            return res.status(400).send({ message: 'No file uploaded' });
        }

        const sanitizedFilename = sanitizeFilename(req.file.originalname);
        const uploadPath = path.join(__dirname, 'uploads', sanitizedFilename);

        try {
            // Validate and process file content
            const validatedBuffer = await validateImageContent(req.file.buffer);
            await fs.writeFile(uploadPath, validatedBuffer);

            fs.chmod(filePath, 0o200, (err) => {
            if (err) return res.status(500).send('Error setting file permissions');
              res.status(200).send({ message: 'File uploaded successfully', filename: sanitizedFilename });
            });
            
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

app.get('/download/:filename', downloadLimiter, (req, res) => {
    const filename = sanitizeFilename(req.params.filename);
    const filePath = path.join(__dirname, 'uploads', filename);

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

* **Filename Sanitization**: the **sanitizeFilename** function replaces all non-alphanumeric characters (excluding `_`, `-`, `.`) with underscores to prevent directory traversal attacks and other filename-based exploits.

* **Upload/Download Limits**: rate limiting is implemented using **express-rate-limit** to limit the number of upload and download requests per IP address in a given time window, preventing DoS attacks.

* **File Content Validation**: for image files, the **validateImageContent** function uses the sharp library to remove metadata, which can contain harmful scripts or data.

* **User and Filesystem Permissions**: the uploads directory is ensured to exist with **fs.ensureDirSync**, and all file operations are performed using fs-extra which handles file system operations safely.
