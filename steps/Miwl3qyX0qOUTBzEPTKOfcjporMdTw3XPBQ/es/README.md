# Aplicación de restricciones de extensión de archivo mediante validación de lista de permitidos en Node.js

* Una estrategia de validación de lista de permitidos implica la creación de una lista de valores o caracteres aprobados que son considerados seguros, rechazando cualquier entrada que no se ajuste a la lista para mantener la integridad y seguridad de los datos.

## Ejercicio para practicar :writing_hand:

* La siguiente aplicación permite a los usuarios subir cualquier tipo de archivo. El objetivo en este caso es modificar el código fuente haciendo clic en el botón `Open Code Editor` e implementar una estrategia de validación de lista de permitidos del lado del servidor que acepte cargas de archivos únicamente con extensiones `.jpg`, `.jpeg` y `.png`.
* Más concretamente, el endpoint POST `/upload` de la aplicación Express en `app.js` debería tener modificaciones de código para soportar esta funcionalidad.
* La aplicación debe devolver un código de estado de respuesta `400` cuando un usuario sube un archivo con una extensión distinta de `.jpg`, `.jpeg` y `.png`.
  @@ExerciseBox@@
