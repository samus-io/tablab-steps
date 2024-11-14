# Aplicación de control de acceso a funciones de carga de archivos usando Express en Node.js

* Al aplicar control de acceso a las funcionalidades de carga de archivos, es esencial tener en cuenta tanto el acceso a la propia función de carga de archivos de la aplicación como el acceso a los archivos cargados.
* Generalmente, la función de carga de archivos de la aplicación se encuentra abierta al público o restringida a ciertos usuarios, mientras que el acceso a los archivos se encuentra abierto al público, restringido a ciertos usuarios o totalmente prohibido.
* Autenticación, autorización y control de acceso son los términos que intervienen en este proceso:
  * La autenticación es el proceso de verificación de la identidad de un usuario o sistema.
  * La autorización es el proceso de especificar qué acciones o recursos están permitidos a un usuario o sistema.
  * El control de acceso se refiere a los mecanismos que imponen tanto la autenticación como la autorización, determinando quién puede acceder a qué recursos y en qué circunstancias.
* La aplicación de estos conceptos ayuda a evitar la carga no autorizada de archivos, las filtraciones de datos y el acceso a información confidencial.

## Código de incumplimiento en Node.js usando `multer`

* El siguiente fragmento de código carece de mecanismos de control de acceso, lo que expone a la aplicación web a ser susceptible de vulnerabilidades de *broken access control* y a una potencial filtración de información:

  <details>
    <summary>Dependencias</summary>

    ```javascript
    const express = require("express");
    const multer = require("multer");
    const path = require("path");
    const fs = require("fs");
    ```

  </details>

  ```javascript
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

## Código de cumplimiento en Node.js usando `multer` y `express-session`

* El siguiente fragmento de código utiliza el paquete `express-session` para permitir la carga de archivos y el acceso a los mismos exclusivamente a usuarios autenticados:

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

  * Se puede observar cómo el middleware `authMiddleware` garantiza que únicamente los usuarios autenticados (aquellos con una sesión activa que contenga un objeto `user`) puedan acceder a las rutas `/upload` y `/download/:filename`, devolviendo en caso contrario un estado `401 Unauthorized`.

## Ejercicio para practicar :writing_hand:

* La siguiente aplicación, a pesar de las apariencias, carece de mecanismos de control de acceso, ya que no existen medidas en el servidor para evitar que usuarios anónimos carguen o descarguen archivos.
* Como puede demostrarse abriendo el editor de código mediante el botón `Open Code Editor` e iniciando la terminal integrada, cualquiera puede ejecutar los siguientes comandos para cargar y descargar un archivo, siendo `APP_URL` una variable de entorno que apunta a la ruta base de la aplicación web:

  ```bash
  curl -F "formFile=@landscape.png" $APP_URL/upload
  ```

  ```bash
  curl $APP_URL/download/landscape.png -o landscape.png
  ```

* Asimismo, cualquier usuario registrado en la aplicación puede utilizar libremente las funciones de carga y descarga sin restricciones una vez iniciada la sesión, como por ejemplo:
  * `jackson01` (rol: `admin`, contraseña: `3YD8v=Smlv=!CAM(`).
  * `johndoe` (rol: `moderator`, contraseña: `(JI+zM2k-qZdOzwz`).
  * `alice99` (rol: `member`, contraseña: `W-KTJ_!3r*8HwRE^`).
* El objetivo aquí es editar el código fuente para aplicar una política de control de acceso en el servidor, limitando la subida de archivos a los usuarios autenticados (aquellos con una sesión activa) y permitiendo únicamente a los usuarios con el rol `admin` o `moderator` la descarga de archivos. Las peticiones exitosas deberían devolver un estado `200 OK`, mientras que los intentos no autorizados deberían resultar en un estado `401 Unauthorized`.
  * Más concretamente, las modificaciones de código deben realizarse en el archivo `app.js`, ubicado en `/home/coder/app/`.
* Una vez realizados los cambios, se debe pulsar el botón `Verify Completion` para confirmar que se ha completado el ejercicio.

  @@ExerciseBox@@
