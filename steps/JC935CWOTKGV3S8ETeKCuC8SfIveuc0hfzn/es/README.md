# Código vulnerable a Path Traversal en Java Jakarta 10.0

* Este ejemplo de código es vulnerable a Path Traversal debido a que no se comprueba la entrada del usuario de ninguna forma:

    ```java
    import jakarta.servlet.ServletException;
    import jakarta.servlet.annotation.WebServlet;
    import jakarta.servlet.http.HttpServlet;
    import jakarta.servlet.http.HttpServletRequest;
    import jakarta.servlet.http.HttpServletResponse;

    import java.io.BufferedInputStream;
    import java.io.BufferedOutputStream;
    import java.io.FileInputStream;
    import java.io.IOException;

    @WebServlet("/getFile")
    public class FileServlet extends HttpServlet {
        protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
            // Get parameters
            String filename = request.getParameter("filename");
            if (filename == null || filename.isEmpty()){
                return;
            }
            String path = "/var/www/files/" + filename;

            // Reading file using user input
            FileInputStream fileInputStream = new FileInputStream(path);
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

* El endpoint `getFile` únicamente concatena la ruta donde están almacenados los archivos con la entrada del usuario en esta parte del código:

    ```java
    String path = "/var/www/files/" + filename;
    ```

* Este comportamiento provoca que cuando un usuario entre la cadena `../../../` se dirija a la raíz del servidor.
* A partir de aquí, puede dirigirse e incluir cualquier archivo del sistema operativo, siempre y cuando la aplicación tenga permisos de lectura, como por ejemplo `/etc/passwd` o intentar buscar donde esta almacenado el código fuente.
