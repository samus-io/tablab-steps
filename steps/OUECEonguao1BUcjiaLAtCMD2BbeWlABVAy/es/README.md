# Aprovechando FortiWeb Cloud 24.3 para analizar archivos al cargarlos

* FortiWeb Cloud es un `Web Application Firewall (WAF)` diseñado para proteger las aplicaciones web de una amplia variedad de amenazas, incluidas las asociadas con la carga de archivos. Las cargas de archivos pueden servir potencialmente como vectores para actividades maliciosas y FortiWeb Cloud proporciona mecanismos de análisis completos para detectar y mitigar los riesgos potenciales.
* Cuando se configura correctamente, FortiWeb Cloud puede efectuar análisis de los archivos que se cargan para detectar varios tipos de *malware*, *greyware*, scripts maliciosos y otros contenidos dañinos. Esto incluye la detección de virus, troyanos y scripts potencialmente peligrosos escritos en lenguajes del lado del servidor como PHP o ASP, que suelen utilizarse para ejecutar ataques del lado del servidor.

## Mecanismos de análisis en FortiWeb Cloud

* FortiWeb Cloud emplea un enfoque de análisis multicapa, el cual combina la detección basada en firmas y el análisis de comportamiento para garantizar una protección completa.

### Detección basada en firmas

* La detección basada en firmas, también conocida como detección estática, consiste en comparar las características de un archivo cargado con una base de datos que contiene firmas de *malware* conocido, incluidos troyanos y otras amenazas. FortiWeb Cloud utiliza definiciones de virus actualizadas e información sobre amenazas para garantizar una inspección fiable.
* Además de identificar *malware* común, también identifica archivos que contienen scripts en lenguajes como PHP, ASP y JavaScript, los cuales los usuarios maliciosos podrían utilizar potencialmente para obtener acceso no autorizado o control sobre servidores web.
* Esta detección basada en firmas constituye una línea de defensa primaria esencial contra las amenazas reconocidas.

  > :warning: Debido a los límites de almacenamiento en caché, la detección basada en firmas actualmente solo procesa archivos de menos de 5 MB.

### Behavioral analysis through FortiSandbox

* Además del análisis estático de archivos, FortiWeb Cloud utiliza FortiSandbox para proporcionar un análisis dinámico y de comportamiento. Los archivos se ejecutan dentro de un entorno aislado y controlado para supervisar su comportamiento en tiempo real.
* Este método es crucial para detectar amenazas avanzadas como el *malware* de día cero o ataques sofisticados que pueden no detectarse mediante los métodos tradicionales basados en firmas. Al simular la ejecución de archivos en un entorno real, FortiSandbox puede descubrir comportamientos maliciosos ocultos, como intentos de acceder a recursos no autorizados o ejecutar comandos dañinos.

  > :older_man: La evaluación de archivos en *sandbox* se realiza en la misma región en la que se encuentra el clúster de FortiWeb Cloud, lo que garantiza el cumplimiento de diversas regulaciones de datos, como GDPR.

## Cómo enviar archivos para que sean escaneados al cargarlos

* Los archivos deben enviarse en formatos compatibles para que FortiWeb Cloud pueda escanearlos. Seguidamente se indican los métodos disponibles para el envío de archivos.

### Carga de archivos mediante `multipart/form-data`

* El formato `multipart/form-data` es el más común y sugerido para la carga de archivos, ya que maneja eficientemente datos binarios. FortiWeb Cloud puede procesar y analizar archivos directamente desde este formato, sin necesidad de pasos adicionales.
* Este es un ejemplo de una petición HTTP que envía un archivo en formato `multipart`:

  ```text
  POST /upload HTTP/2
  Host: domain.tbl
  User-Agent: Mozilla/5.0 (compatible; MSIE 11.0; Windows; Windows NT 6.2; Win64; x64; en-US Trident/7.0)
  Accept-Encoding: gzip, deflate, br, zstd
  Content-Type: multipart/form-data; boundary=---------------------------41762806061171117218568726803
  Content-Length: 656499
  Connection: keep-alive
  
  -----------------------------41762806061171117218568726803
  Content-Disposition: form-data; name="file"; filename="landscape.png"
  Content-Type: image/png
  
  [binary file data]
  
  -----------------------------41762806061171117218568726803--
  ```

* El siguiente código JavaScript utiliza el paquete `axios` para crear una petición HTTP similar a la anterior:

  ```javascript
  const sendFile = (formFile) => {
    const formData = new FormData();
    formData.append("file", formFile);

    return axios.post("/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    });
  };
  ```

### Carga de archivos mediante `application/json` y base64

* En  FortiWeb Cloud los archivos se pueden cargar a través de objetos JSON y ser escaneados, pero con ciertas limitaciones. Cuando se utiliza JSON para la carga de archivos, el nombre del atributo que contiene el archivo codificado en base64 en el objeto JSON debe configurarse manualmente en la aplicación FortiWeb Cloud y debe colocarse en la raíz del mismo.
* El uso de un nombre de atributo distinto del especificado en la configuración de la aplicación FortiWeb Cloud causará que no se analice el archivo.

  > :warning: La compatibilidad de FortiWeb Cloud con la carga de archivos dentro de un objeto JSON está limitada actualmente a un archivo por petición HTTP.

* Procede una muestra de una petición HTTP que envía un archivo, codificado en base64, dentro de un objeto JSON y utilizando el nombre de atributo `file`:

  ```text
  POST /upload HTTP/2
  Host: domain.tbl
  User-Agent: Mozilla/5.0 (compatible; MSIE 11.0; Windows; Windows NT 6.2; Win64; x64; en-US Trident/7.0)
  Accept-Encoding: gzip, deflate, br, zstd
  Content-Type: application/json
  Content-Length: 875047
  Connection: keep-alive
  
  {
    "file": "<base64-encoded-file-data>"
  }
  ```

* Seguidamente se muestra código JavaScript que utiliza `axios` para generar una petición HTTP similar a la anterior:

  ```javascript
  const sendFile = async (formFile) => {
    const readFileAsBase64 = (file) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = () => {
          const base64File = reader.result.split(",")[1]; // Extract the Base64 part
          resolve(base64File);
        };

        reader.onerror = (error) => reject(error);
        reader.readAsDataURL(file);
      });
    };

    const base64File = await readFileAsBase64(formFile);

    // Create a JSON object with the Base64 encoded file
    const jsonPayload = {
      file: base64File
    };

    return axios.post("/upload", jsonPayload, {
      headers: {
        "Content-Type": "application/json"
      }
    });
  };
  ```

## Cómo confirmar si un archivo está siendo analizado por FortiWeb Cloud

* Se puede utilizar un archivo de prueba EICAR para verificar que los mecanismos de carga de archivos están correctamente implementados y que FortiWeb Cloud detecta y bloquea eficazmente *malware*.
* Esto permite validar las capacidades de análisis de FortiWeb Cloud sin poner en riesgo el sistema frente al malware real.

### ¿Qué es un fichero de prueba EICAR?

* Un archivo de prueba EICAR es un archivo informático no malicioso desarrollado por el `European Institute for Computer Antivirus Research (EICAR)` para probar de forma segura sistemas antivirus y de protección.
* Su objetivo es activar las respuestas del antivirus y del sistema de seguridad como lo haría un archivo de *malware* auténtico, pero sin ningún riesgo de daño real.
* El fichero EICAR consiste en un simple archivo de texto ASCII con una secuencia de caracteres específica que los programas antivirus reconocen como fichero malicioso. La versión más simple del contenido de un archivo EICAR es la siguiente:

  ```text
  X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
  ```

* Para crear un fichero de prueba EICAR, se puede copiar y pegar la secuencia de caracteres anterior en un editor de texto y guardarlo con extensión `.txt`. Otra posibilidad es descargarlo directamente del sitio web oficial [EICAR][1].

### Pruebas de análisis con FortiWeb Cloud

* Como práctica de seguridad, una vez implementada la funcionalidad de carga de archivos en una aplicación web, es esencial verificar si FortiWeb Cloud identifica y bloquea correctamente los archivos potencialmente dañinos.
* Con una correcta configuración de FortiWeb Cloud, este debería interceptar la carga del fichero EICAR bloqueando la petición HTTP antes de que llegue al servidor. En este escenario, FortiWeb devolverá una respuesta de código de estado HTTP `403 Forbidden` al cliente, indicando que el archivo fue bloqueado debido a potenciales riesgos de seguridad y mostrando el siguiente contenido:

![FortiWeb Cloud EICAR file block page][2]

[1]: https://www.eicar.org/download-anti-malware-testfile/
[2]: /static/images/fortiweb-eicar-alert.png
