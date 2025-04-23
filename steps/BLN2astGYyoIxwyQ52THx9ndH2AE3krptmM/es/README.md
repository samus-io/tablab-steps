# Aplicación de saneamiento de nombres de archivo en Java Jakarta

* El saneamiento de los nombres de archivo implica la revisión y posible modificación de los nombres de archivo entrantes para evitar amenazas de seguridad o incidencias operativas que puedan comprometer la integridad del sistema.
* El uso de UUIDs o identificadores aleatorios para el almacenamiento de archivos elimina la necesidad de sanear los nombres de los archivo. Sin embargo, si los requisitos de la organización lo requieren, es entonces necesario aplicar un saneamiento adecuado.

## Ejercicio para practicar :writing_hand:

* La siguiente aplicación permite a los usuarios subir archivos sin imponer ningún control sobre el nombre del archivo, sino que emplea directamente el valor `filename` para el almacenamiento.
* El objetivo aquí es modificar el código fuente haciendo clic en el botón `Open Code Editor` e integrar un mecanismo sólido y seguro de saneamiento de nombres de archivo que cumpla los siguientes criterios:
  * Descartar los nombres reservados y eliminar los caracteres no seguros, conservando únicamente caracteres alfanuméricos, puntos y guiones (i.e., `A-Za-z0-9.-`).
  * Eliminar los puntos iniciales y finales para evitar archivos ocultos o exploits relacionados con el uso del *path*.
  * Normalizar los nombres de archivo convirtiendo las mayúsculas en minúsculas para mantener uniformidad en todos los entornos.
  * Establecer un límite de longitud de nombre de archivo de 100 caracteres.
* La clase `FileUploadServlet` que se encuentra en el archivo `src/main/java/io/ontablab/FileUploadServlet.java` es el punto principal donde es conveniente implementar cambios para habilitar esta funcionalidad.
* **Es importante señalar que, en este caso, no es necesario aplicar ningún mecanismo para tratar las colisiones de nombres de archivo**.
* Una vez realizados los cambios, se requiere pulsar el botón `Verify Completion` para confirmar que el ejercicio se ha completado correctamente.

  @@ExerciseBox@@
