# Aplicación de límites en la carga de archivos con Express en Node.js

* Restringir el tamaño de los archivos, el total de subidas que puede realizar un usuario y las tasas de solicitudes de carga y descarga son consideraciones de seguridad importantes para las aplicaciones que ofrecen funcionalidades de carga y descarga de archivos.
* Seguidamente se muestran algunos ejemplos de cómo implementar estos límites en una aplicación Node.js haciendo uso del framework `express`, el middleware `multer` para gestionar la subida de archivos y el paquete `express-rate-limit` para establecer una limitación básica de las tasas de carga/descarga.

## Limitar el tamaño de los archivos

* El *middleware* `multer` acepta un objeto de tipo `options`, donde la propiedad `limits` permite definir la configuración `fileSize`:

  ```javascript
  const upload = multer({
    storage: storage,
    limits: {
      fileSize: 1 * 1024 * 1024 // 1 MB file size limit
    }
  });
  ```

* Esto permite gestionar los errores relacionados de forma global en la aplicación Express o bien en cada *endpoint* específico, tal como se ilustra en el siguiente caso:

  ```javascript
  const uploadSingleFile = upload.single("file");

  app.post("/upload", (req, res) => {
    uploadSingleFile(req, res, (err) => {
      if (err instanceof multer.MulterError) {
        if (err.code === "LIMIT_FILE_SIZE") {
          res.status(400).json({ message: "File size cannot exceed 1 MB" });
          return;
        }

        // Handle other Multer errors here if needed
      }

      if (err) {
        res.status(500).json({ message: "An unknown error occurred while processing the file" });
        return;
      }

      res.send("File uploaded successfully");
    });
  });
  ```

## Limitar las tasas de carga y descarga

* Limitación de la tasa de carga a un máximo de 100 solicitudes cada 15 minutos por IP:

  ```javascript
  const { rateLimit } = require("express-rate-limit");
  ```

  ```javascript
  const uploadRateLimit = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes window
    max: 100, // Limit each IP to 100 requests per windowMs
    message: "Too many upload requests from this IP, please try again later"
  });

  app.post("/upload", uploadRateLimit, (req, res) => {
    // File upload logic here
  });
  ```

* Limitación de la tasa de descargas a un máximo de 100 solicitudes cada 15 minutos por IP:

  ```javascript
  const downloadRateLimit = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes window
    max: 100, // Limit each IP to 100 requests per windowMs
    message: "Too many download requests from this IP, please try again later"
  });

  app.get("/download/:filename", downloadRateLimit, (req, res) => {
    // File download logic here
  });
  ```

  > :older_man: Siempre que las funciones de carga o descarga de archivos estén disponibles cuando el usuario está autenticado, es muy recomendable aplicar este tipo de restricción a la sesión iniciada por el usuario en lugar de otros valores superficiales como la dirección IP de origen.

### Consideraciones al restringir por dirección IP

* En la mayoría de los casos, la aplicación web no está expuesta directamente al usuario final, sino que suele estar ubicada detrás de un balanceador de carga o de un mecanismo de seguridad como un cortafuegos de aplicaciones web (WAF).
* Esto podría provocar que la dirección IP de origen de los paquetes HTTP recibidos por la aplicación fuera la IP del intermediario, en lugar de la del cliente final. En estos casos, puede ser necesario utilizar cabeceras como `X-Forwarded-For` para proporcionar a la aplicación la dirección IP real del cliente:

  ```javascript
  console.log(req.headers["x-forwarded-for"]);
  ```

* En este caso, cuando se ejecuta una aplicación Express detrás de un proxy inverso, se puede utilizar la configuración de aplicación `trust proxy` para disponer de la información proporcionada por el proxy inverso en los *endpoints* (i.e., como `req.ip`):

  ```javascript
  app.set("trust proxy", 1); // Trust the first hop away from the application and extract the next IP as client's IP address
  ```

  ```javascript
  app.set("trust proxy", "loopback, 172.16.0.10"); // Trust 'loopback' and '172.16.0.10' proxies for getting client's IP address
  ```

## Ejercicio para practicar :writing_hand:

* La aplicación dada ofrece una carga básica de archivos con Express sin ninguna validación de seguridad realizada en el lado del servidor. El objetivo aquí es abrir el editor de código usando el botón `Open Code Editor` y editar el código fuente para incorporar dos medidas de seguridad:
  * Un límite de tamaño de archivo de 1 KB. Si un archivo cargado supera este tamaño, se debe devolver una respuesta HTTP con un código de estado `400 Bad Request`.
  * Cada dirección IP debe estar limitada a 10 subidas de archivos en una ventana de 30 segundos. Si se sobrepasa este límite, se debe recibir una respuesta HTTP con el código de estado `429 Too Many Requests` y la IP debe permanecer bloqueada durante 30 segundos.
    * Hay que tener en cuenta que la aplicación se coloca bajo múltiples capas de proxy inverso, ya que se ejecuta dentro de un contenedor Cloud Run en GCP.
* Con el fin de completar el ejercicio, en la aplicación Express definida en `app.js` es donde se deben añadir las modificaciones de código para soportar estas características.
  @@ExerciseBox@@
