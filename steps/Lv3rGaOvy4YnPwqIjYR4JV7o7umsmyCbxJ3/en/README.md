# Enforcing access control to file upload functionalities using Express in Node.js

* When applying access control to file upload functionalities, it's essential to consider both access to the file upload feature of the web application and access to the actual uploaded files.
* Generally, the file upload feature of the application might be open to the public or restricted to users, whereas file access could be public, restricted to certain users, or entirely disallowed.
* Authentication, authorization and access control are the terms involved in this process:
  * Authentication is the process of verifying the identity of a user or system.
  * Authorization is the process of specifying which actions or resources are allowed to a user or system.
  * Access control refers to the mechanisms that enforce both authentication and authorization, determining who can access which resources and under what circumstances.
* Putting these concepts in place help prevent unauthorized file uploads, data breaches, and access to sensitive information.

## Non-compliant code in Node.js using `multer`

* The code snippet below lacks access control mechanisms, exposing the web application to broken access control and potential information disclosure:

  ```javascript
  const express = require("express");
  const multer = require("multer");
  const path = require("path");
  const fs = require("fs");

  const app = express();

  // Define the path to the folder where uploaded files will be stored
  const uploadFolderPath = path.join(__dirname, "uploads");

  // Check if the 'uploads' folder exists; if not, create it
  if (!fs.existsSync(uploadFolderPath)) fs.mkdirSync(uploadFolderPath, { recursive: true });

  const storage = multer.diskStorage({
    destination: (req, file, cb) => {
      cb(null, uploadFolderPath);
    },
    filename: (req, file, cb) => {
      cb(null, file.originalname); // Use the original filename provided by the user
    }
  });

  const upload = multer({
    storage: storage
  });

  app.post("/upload", upload.single("file"), (req, res) => {
    if (!req.file) {
      res.status(400).json({ message: "No file uploaded" });
      return;
    }

    res.send("File uploaded successfully");
  });

  app.get("/download/:filename", (req, res) => {
    const { filename } = req.params;
    const options = {
      root: uploadFolderPath,
      dotfiles: "deny"
    };

    res.sendFile(filename, options, (err) => {
      if (err) {
        res.status(404).send("File not found");
      }
    });
  });
  ```

## Compliant code in Node.js using `multer` and `express-session`

* The following code snippet uses the `express-session` package to restrict file upload and file access to authenticated users exclusively:

  ```javascript
  const session = require("express-session");
  ```

  ```javascript
  app.use(
    session({
      secret: "sessionsecret",
      saveUninitialized: true,
      resave: false,
      cookie: {
        secure: true
      }
    })
  );

  const authMiddleware = (req, res, next) => {
    if (req.session?.user) next();
    else res.sendStatus(401);
  };
  ```

  ```javascript
  app.post("/upload", authMiddleware, upload.single("file"), (req, res) => {
    if (!req.file) {
      res.status(400).json({ message: "No file uploaded" });
      return;
    }

    res.send("File uploaded successfully");
  });

  app.get("/download/:filename", authMiddleware, (req, res) => {
    const { filename } = req.params;
    const options = {
      root: uploadFolderPath,
      dotfiles: "deny"
    };

    res.sendFile(filename, options, (err) => {
      if (err) {
        res.status(404).send("File not found");
      }
    });
  });
  ```

  * Notice how the `authMiddleware` middleware ensures that only authenticated users (those with an active session containing a `user` object) can access the `/upload` and `/download/:filename` routes, otherwise returning a `401 Unauthorized` status.

## Exercise to practice :writing_hand:

* The following application, despite appearances, lacks access control mechanisms, as there are no server-side measures to prevent anonymous users from uploading or downloading files.
* As can be demonstrated by opening the code editor via the `Open Code Editor` button and launching the integrated terminal, anyone can run the following commands to upload and download a file, with `APP_URL` set as an environment variable pointing to the web application's base path:

  ```bash
  curl -F "formFile=@landscape.png" $APP_URL/upload
  ```

  ```bash
  curl $APP_URL/download/landscape.png -o landscape.png
  ```

* Additionally, any user registered to the application can freely use the upload and download features without restrictions once logged in, such as:
  * `jackson01` (role: `admin`, password: `dX2%V5h|s5>C}]V`).
  * `johndoe` (role: `moderator`, password: `7j@H!3p%!&8l^S2`).
  * `alice99` (role: `member`, password: `u^#B&2y!F7@d$E9`).
* The goal here is to edit the source code to enforce a server-side access control policy, limiting file uploads to authenticated users (those with an active session) and allowing only users with the `admin` or `moderator` role to download files. Successful requests should return a `200 OK` status, while unauthorized attempts should result in a `401 Unauthorized` status.
  * More precisely, the modifications should be made in the `app.js` file, located in `/home/coder/app/`.
* After making the changes, press the `Verify Completion` button to confirm that the exercise has been completed.

  @@ExerciseBox@@
