# Cómo prevenir el Path Traversal en Java Jakarta 10.0 (Caso 1)

## Normalización del input del usuario

* Este fragmento de código implementa la normalización del nombre del archivo solicitado utilizando la forma canónica NFC (Normalización de Composición):

    ```java
    String filename = request.getParameter("filename");
    Normalizer.normalize(filename, Normalizer.Form.NFC);
    ```

* Esta práctica es esencial para unificar diferentes representaciones de caracteres Unicode que, aunque visualmente idénticas, pueden ser digitalmente distintas.
* La normalización previene técnicas de evasión que explotan estas variaciones para burlar controles de seguridad, garantizando así que todos los caracteres se evalúen de manera consistente.
  * Esta medida hay que aplicarla inmediatamente después de recibir el nombre del archivo como parte de la solicitud, antes de cualquier otra validación o procesamiento.

## Implementación de una lista de archivos permitidos (whitelist)

* Añadiendo el siguiente código, se logra permitir que únicamente se consulten archivos predefinidos en el código:

    ```java
    final Set<String> ALLOWED_FILES = Set.of("info", "policy", "cookies");
    
    String filename = request.getParameter("filename");
    if (!ALLOWED_FILES.contains(filename)){
        // Reject request
    }
    ```

* En este caso, se utiliza una lista de archivos predefinidos en el código pero estos podrían ser obtenidos de una base de datos o otras fuentes de información.
  * Si los archivos permitidos se obtienen, por ejemplo, a través de una base de datos, hay que asegurarse que el usuario no puede modificar arbitrariamente cual será el contenido de la lista.

## Validación de caracteres alfanuméricos

* Utilizando la siguiente expresión regular, se garantiza que el nombre de archivo sea exclusivamente alfanumérico y permita, como máximo, un punto:

    ```java
    String filename = request.getParameter("filename");
    if (!filename.matches("^[a-zA-Z0-9]+(\\.[a-zA-Z0-9]+)?$")){
        // Reject request
    }
    ```

* Este código previene la incorporación de caracteres especiales, tales como `/`, `\`, `..`, entre otros, que podrían ser explotados en un ataque de Path Traversal.
* En el caso que la extensión sea controlada por la aplicación y no por el usuario, la expresión regular deberá ser la siguiente:

    ```java
    String filename = request.getParameter("filename");
    if (!filename.matches("^[a-zA-Z0-9]+$")){
        // Reject request
    }
    ```

## Restricción sobre el control de la extensión de archivo

* Limitar las extensiones de archivo que pueden ser solicitadas a un conjunto predefinido de tipos seguros (en este caso, `png`, `jpg`, `jpeg`) reduce el riesgo de servir archivos maliciosos o sensibles que no estén destinados a ser accesibles. Para obtener este comportamiento en Java, una de las posibles soluciones podría ser:

    ```java
    public static String getFileExtension(String filename) {
        if (filename == null || !filename.contains(".")) {
            return "";
        }
        return filename.substring(filename.lastIndexOf(".") + 1);
    }
    ...

    String filename = request.getParameter("filename");
    final Set<String> ALLOWED_EXTENSIONS = Set.of("png", "jpg", "jpeg");
    
    if (!ALLOWED_EXTENSIONS.contains(getFileExtension(filename))){
        return;
    }
    ```

## Validación y normalización de la ruta de acceso

* El siguiente código es la última verificación que hay que ejecutar, este convierte la ruta del archivo solicitado a su forma canónica y verifica que comience con el directorio base especificado, además de confirmar su existencia:

    ```java
    final String BASE_DIRECTORY = "/var/www/files";
    String filename = request.getParameter("filename");
    File file = new File(BASE_DIRECTORY, filename);
    if (!file.getCanonicalPath().startsWith(BASE_DIRECTORY) || !file.exists()){
        return;
    }
    ```

* Comprobar que la ruta canónica del archivo solicitado comience con el directorio base esperado (`/var/www/files`) previene el acceso a archivos fuera de este directorio.
* Utilizar `getCanonicalPath()` resuelve cualquier símbolo, como `..`, asegurando que la ruta final sea absoluta y no relativa, evitando así la explotación de referencias a directorios superiores.

## Casos de uso

* Estos dos ejemplos cubren los distintos casos sobre como implementar las distintas funciones de seguridad en un endpoint donde lee archivos del servidor.
* En estos, si un usuario intenta acceder a un archivo que no satisface los criterios de seguridad establecidos, el método concluye prematuramente, resultando en la devolución de una respuesta sin contenido.
* Este enfoque de gestión de errores, que consiste en terminar la ejecución y devolver una página en blanco, puede no ser el más adecuado en todos los contextos. La manera óptima de manejar tales situaciones varía significativamente según las especificaciones y necesidades particulares de cada aplicación. En otro `Lab`, se explicará como manejar correctamente este tipo de excepciones.
* Con el objetivo de preservar la simplicidad en este ejemplo, se ha optado por la estrategia más directa y sencilla para el manejo de errores.

### Acceso a archivos predefinidos con una única extensión

```java
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.*;
import java.text.Normalizer;
import java.util.Set;

@WebServlet("/getFile")
public class FileServlet extends HttpServlet {
    private static final Set<String> ALLOWED_FILES = Set.of("info", "policy", "cookies");
    private static final String BASE_DIRECTORY = "/var/www/files";

    private static String normalizeString(String s) {
        return Normalizer.normalize(s, Normalizer.Form.NFC);
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String filename = request.getParameter("filename");
        if (filename == null || filename.isEmpty()) {
            return;
        }
        // Normalize input
        filename = normalizeString(filename);

        // Files whitelist
        if (!ALLOWED_FILES.contains(filename)){
            return;
        }
        
        // Set the txt extension
        filename = filename.concat(".txt");

        // Get file
        File file = new File(BASE_DIRECTORY, filename);
        if (!file.getCanonicalPath().startsWith(BASE_DIRECTORY) || !file.exists()){
            return;
        }

        // Process file
        FileInputStream fileInputStream = new FileInputStream(file);
        BufferedInputStream bufferedInputStream = new BufferedInputStream(fileInputStream);
        BufferedOutputStream out = new BufferedOutputStream(response.getOutputStream());

        byte[] buffer = new byte[1024];
        int length;
        while ((length = bufferedInputStream.read(buffer)) > 0) {
            out.write(buffer, 0, length);
        }

        bufferedInputStream.close();
        out.close();
    }
}
```

### Acceso a archivos alfanuméricos con multiples extensiones

```java
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.*;
import java.text.Normalizer;
import java.util.Set;

@WebServlet("/getFile")
public class FileServlet extends HttpServlet {
    private static final Set<String> ALLOWED_EXTENSIONS = Set.of("png", "jpg", "jpeg");
    private static final String BASE_DIRECTORY = "/var/www/files";

    private static String normalizeString(String s) {
        return Normalizer.normalize(s, Normalizer.Form.NFC);
    }

    public static String getFileExtension(String filename) {
        if (filename == null || !filename.contains(".")) {
            return "";
        }
        return filename.substring(filename.lastIndexOf(".") + 1);
    }

    public static boolean isFileAlphanumeric(String input) {
        // Allows files with alfanumeric characters, including one dot
        return input.matches("^[a-zA-Z0-9]+(\\.[a-zA-Z0-9]+)?$");
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String filename = request.getParameter("filename");
        if (filename == null || filename.isEmpty()) {
            return;
        }
        // Normalize input
        filename = normalizeString(filename);

        // Alfanumeric characters
        if (!isFileAlphanumeric(filename)){
            return;
        }

        // Extensions whitelist
        if (!ALLOWED_EXTENSIONS.contains(getFileExtension(filename))){
            return;
        }

        // Get file
        File file = new File(BASE_DIRECTORY, filename);
        if (!file.getCanonicalPath().startsWith(BASE_DIRECTORY) || !file.exists()){
            return;
        }

        // Process file
        FileInputStream fileInputStream = new FileInputStream(file);
        BufferedInputStream bufferedInputStream = new BufferedInputStream(fileInputStream);
        BufferedOutputStream out = new BufferedOutputStream(response.getOutputStream());

        byte[] buffer = new byte[1024];
        int length;
        while ((length = bufferedInputStream.read(buffer)) > 0) {
            out.write(buffer, 0, length);
        }

        bufferedInputStream.close();
        out.close();
    }
}
```
