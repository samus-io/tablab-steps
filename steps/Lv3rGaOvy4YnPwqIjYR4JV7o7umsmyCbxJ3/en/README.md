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

## Vulnerable implementation

* This example shows how neglecting security measures can expose the system to various risks, such as unauthorized access, file tampering, and potential execution of malicious scripts. It uses **multer** to store file and stores it to some **uploads** folder.

```js
const express = require('express');
const multer = require('multer');
const fs = require('fs');
const path = require('path');

const app = express();
const upload = multer({ dest: '<absolute path to uploads folder>' }); // path to desired location

// File upload endpoint without authentication or authorization
app.post('/upload', upload.single('file'), (req, res) => {
    const filePath = path.join(__dirname, 'uploads', req.file.filename); // ./uploads is the destination

    res.status(200).send('File uploaded successfully');
});

// Endpoint to read the file without authorization or internal IP check
app.get('/file/:filename', (req, res) => {
    const filePath = path.join(__dirname, 'uploads', req.params.filename); // ./uploads is the destination
    
    res.sendFile(filePath);
});

// Start your server
app.listen(3000, () => {
    console.log('Server running on port 3000');
});
```

* In this insecure implementation:
  * **No Authentication or Authorization**: Anyone can upload and access files.
  * **No internal IP check**: Files can be accessed from any IP address.
  * **Insecure file permissions**: there is no permission explicitly set to the file.

## Secure implementation

* In this secure implementation:
  * **Authentication and Authorization**: we use **JSON Web Token(JWT)** to ensure that only authenticated and authorized users can upload and read files.
  * **Internal IP check**: we restrict file access to specific internal IP addresses.
  * **File permissions**: we will set the permission of the folder where the files are stored.
    * On Unix-based systems, we can use `fs.chmod` function programmatically or `chmod` command to set the files/folders permissions. Its first argument accepts an octal number of the following format:

    ```bash
    Syntax: 0oOGP

    O: number representing the permission for owner.
    G: number representing the permission for group.
    P: number representing permission for other users.

    Every number is bad of 3 bits. First bit is readable, second bit is writable, third bit is executable.
    ```

    ```js
        fs.chmod(<filepath>, <permission in octal or hex>, callback )
    ```

    ```bash
        chmod [options] [mode] [file_name] 

        options: Optional flags that modify the behavior of the chmod command.
        mode: The permissions to be set, represented by a three-digit octal number or symbolic notation.
        file_name: The name of the file or directory for which the permissions are to be changed.
    ```

  * On windows, the below are the following ways to set permissions:
    * Using File Explorer
      * Navigate to the file or folder, right-click it, and select **Properties**.
      * In the properties window, go to the **Security** tab.
      * Click the **Edit** button to change permissions. Select a user or group from the list. Check or uncheck permissions (Full control, Modify, Read & execute, etc.). Click **Apply** and then **OK**.
    * Using Command Prompt (icacls)
      * Search for **cmd** in the Start menu, right-click it, and select **Run as administrator**.
      * Use `icacls` Command:

        ```bash
        Syntax: icacls "C:\path\to\file.txt" /grant username:(permission)
        Example: icacls "C:\path\to\file.txt" /grant Everyone:(R)

        Possible permissions are R: Read, W: Write, M: Modify, X: Execute and all combinations of RWMX.
        ```

    * Using `Set-Acl` Cmdlet in powershell. For example:

        ```bash
        // Use Get-Acl to get the current Access Control List (ACL) of the file
        $acl = Get-Acl "C:\path\to\file.txt"

        // Specify the user, permission type, and allow/deny
        $permission = "DOMAIN\User","Read,Write","Allow"

        // Create a new access rule object
        $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission

        // Add the new rule to the ACL
        $acl.SetAccessRule($accessRule)

        // Use Set-Acl to apply the modified ACL to the file
        Set-Acl "C:\path\to\file.txt" $acl

        ```

  * The user uploads the file with `authorization` header containing **JWT** token when reading and writing the file.

* Add the dependencies and initialize. Do not forget to install all these modules.

```js
const express = require('express');
const jwt = require('jsonwebtoken');
const path = require('path');
const multer = require('multer');
const uuid = require('uuid');

const app = express();
const upload = multer({ 
    dest: '<absolute path to uploads folder>',
    filename: (req,file,cb)=>{
        const fileName = `${uuid.v4()}`; // Naming the file using UUID V4 only
        cb(null, fileName);
    }
});

// Create your own secret key for JWT
const SECRET_KEY = 'your_secret_key';

app.use(express.json());
```

* Middleware for checking authentication and authorization. Here, we verify the token with `SECRET_KEY` that was planned previously. It verifies the `authorization` header from the client request.

```js
function authenticateToken(req, res, next) {
    const token = req.header('Authorization')?.replace('Bearer ', '');
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

* File upload endpoint with authentication, authorization, and internal IP check. The **multer** sets the permission of the file while storing it to the `./uploads` (your destination folder) folder.

```js
app.post('/upload', authenticateToken, checkInternalIP, upload.single('file'), (req, res) => {
            res.send(`File uploaded successfully!`);
});
```

* Endpoint to read the file, with authorization and internal IP check.

```js
app.get('/file/:filename', authenticateToken, checkInternalIP, (req, res) => {
    const filePath = path.join(__dirname, 'uploads', req.params.filename);
    // This will allow to send the file if there is correct permission set during the upload
    res.sendFile(filePath);
});

// Start your express server here...
```

* Note that **multer** sets the permission to system default when we upload the file. On Unix-based system, you can use `fs.chmod` to explicitly change the permission. On Windows system, it is typically done using the **Security** property. For handling file permissions programmatically on Windows, you can use the built-in icacls command-line utility, which allows you to manipulate file and folder ACLs (Access Control Lists).
