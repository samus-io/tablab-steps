# Clona nuestro repositorio GitHub "tablab-steps" antes de empezar

* Primero, navega al repositorio [tablab-steps][1] y haz clic en el botón *Fork*. Esto creará una copia personal del repositorio bajo tu cuenta de GitHub.
* A continuación, para clonar el repositorio localmente, abre tu terminal y ejecuta el siguiente comando, sustituyendo `username` por tu nombre de usuario real de GitHub:

  ```bash
  git clone https://github.com/<username>/tablab-steps.git
  ```

* Una vez completado, opcionalmente se puede añadir el repositorio original como remoto para mantener la bifurcación actualizada:

  ```bash
  git remote add upstream https://github.com/samus-io/tablab-steps.git
  ```

* Antes de realizar cambios, cambia a una nueva rama para mantener tu trabajo organizado. La convención de la rama a utilizar es:
  * `lab/<nombre-de-laboratorio>`: en caso de que quieras crear el conjunto completo de Steps que formalizarán un Laboratorio.
  * `step/<step-name>`: si simplemente quieres crear un único Step independiente.

  ```bash
  git checkout -b lab/sqli-in-nodejs
  ```

* Cuando el contenido esté completo, dirígete a tu *fork* en GitHub y haz clic en `New pull request` cerca de tu rama. Puedes enviar tus cambios a nuestra rama `main`. Revisa los cambios efectuados y, una vez listo, crea tu *pull request* con un título y una descripción detallados explicando qué Steps has añadido. A partir de aquí, nosotros nos encargamos del resto :slightly_smiling_face:
* Recuerda poner tu nombre y tu identificador de perfil de GitHub como atributos del archivo `properties.json` de cada Step para poder referenciar tu aporte en la plataforma.

[1]: https://github.com/samus-io/tablab-steps
