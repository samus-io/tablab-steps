# Cómo crear un ejercicio de formación práctico en un Step

* Un Step puede contener más de un ejercicio. Lo único que hay que tener en cuenta es que todos ellos deben ser proporcionados por la misma aplicación contenerizada.

## Primero, crea una aplicación web que proporcione el ejercicio

* Para cualquier tipo de ejercicio que quieras crear, asegúrate de crear una aplicación que se pueda ejecutar en [Cloud Run][1] en Google Cloud Platform. Aquí es donde se instancian nuestras imágenes Docker cuando un usuario despliega un Lab.
* Independientemente del número de ejercicios que ofrezca tu aplicación, asegúrate de que siempre los ofrezca de la siguiente manera según el orden en el quieras mostrarlos dentro del contenido:
  * `/0/`: cuando se solicite a la aplicación esta ruta, deberá mostrar el primer ejercicio (aunque sólo haya uno).
  * `/1/`: cuando se solicite a la aplicación esta ruta, deberá mostrar el segundo ejercicio.
  * `/2/`: cuando se solicite a la aplicación esta ruta, deberá mostrar el tercer ejercicio.

## Segundo, construye una imagen Docker

* Utiliza la carpeta `docker` creada en tu estructura de Step. Debes colocar dentro de este directorio la aplicación, que debe estar contenerizada.
* Escribe en el archivo `Dockerfile` las instrucciones para generar la imagen Docker.
* Ten en cuenta que la imagen base del `Dockerfile` debe ser una imagen oficial del [Docker Hub][2]. Si necesitas una imagen que no es oficial, [contacta con el equipo de tablab.io][3] y nosotros te la proporcionaremos.

## Tercero, incluye los ejercicios en el contenido

* Cuando quieras añadir un ejercicio en algún punto del contenido del Step, solo tienes que añadir la siguiente etiqueta:

  ```markdown
  @@ExerciseBox@@
  ```

  * Para la primera etiqueta `@@@ExerciseBox@@` incluida, nuestra plataforma, al procesar el contenido, solicitará la ruta `/0/` a la aplicación intentando alcanzar el primer ejercicio a mostrar.
  * Para la segunda etiqueta `@@ExerciseBox@@` encontrada en el contenido, se solicitará la ruta `/1/` para mostrar el segundo ejercicio.
  * Para la tercera etiqueta `@@ExerciseBox@@` encontrada en el contenido, se solicitará la ruta `/2/` para mostrar el tercer ejercicio.

## Por último, pero no menos importante

* Ten en cuenta que todos los Steps enviados serán revisados por el equipo de tablab.io y en este sentido realizaremos cambios y correcciones si los Steps propuestos no siguen el formato adecuado.
* Recuerda que nuestra misión es hacer de tablab.io una academia colaborativa, por lo que puedes estar seguro de que contarás con todo nuestro apoyo en el proceso de generación de Steps. Para cualquier duda o sugerencia de mejora solo tienes que [contactar con nosotros][3], estamos dispuestos a ayudarte en lo que sea.

[1]: https://cloud.google.com/run
[2]: https://hub.docker.com/search?q=&image_filter=official
[3]: mailto:hello@samus.io
