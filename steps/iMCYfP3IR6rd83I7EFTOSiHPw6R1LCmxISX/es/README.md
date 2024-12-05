# Integración de análisis de malware en cargas de archivos con React y FortiWeb Cloud 24.3

* FortiWeb Cloud es un servicio de cortafuegos de aplicaciones web (WAF) basado en la nube proporcionado por Fortinet, diseñado para proteger las aplicaciones web y APIs frente a diversas amenazas de seguridad, como inyecciones SQL, Cross-Site Scripting (XSS), ataques de denegación de servicio (DoS) y otras vulnerabilidades comunes, incluidas las asociadas con la carga de archivos.
* Es apropiado para organizaciones que buscan seguridad de aplicaciones web robusta, escalable y fácil de gestionar, especialmente cuando se gestionan múltiples aplicaciones o servicios en diferentes entornos (en la nube, *on-premises* o híbrido).

## Ejercicio para practicar :writing_hand:

* Detrás de este formulario de carga de archivos, se encuentra cierto código de *backend* que simula las condiciones en las que FortiWeb Cloud tiene la capacidad de analizar un archivo basándose en el formato en que la petición HTTP ha sido enviada por el cliente.
* El objetivo aquí es editar el código fuente abriendo el editor de código a través del botón `Open Code Editor` y modificar la función `sendFile` en `app/src/send-file.js` para realizar una petición POST a través de `axios` al endpoint `/upload`, con el fin de subir el archivo seleccionado en el formulario tras pulsar el botón `Submit`.
  * El código de *backend* enviará una respuesta HTTP de estado `200 OK` si FortiWeb Cloud pudo haber escaneado el archivo, o un estado `400 Bad Request` si no hubiera podido, junto con un mensaje informativo mostrado directamente en el formulario de subida de ficheros.
* Hay que tener en cuenta que la modificación de la aplicación React en el editor de código requiere volver a compilar la aplicación y hacer clic en el enlace `reload` del formulario para cargar el código JavaScript más reciente en el navegador.
* Para completar el ejercicio con éxito, una vez introducido el código JavaScript adecuado, se debe utilizar el formulario para subir una de las imágenes de muestra proporcionadas.
  * Esto debería enviar una petición HTTP con la imagen bajo un parámetro llamado `file` y recibir una respuesta `200 OK`, indicando que podría haber sido analizado por FortiWeb Cloud.

  @@ExerciseBox@@
