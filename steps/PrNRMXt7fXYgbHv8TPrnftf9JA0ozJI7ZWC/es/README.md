# Ejecuta el script auxiliar para crear la estructura de directorios

* Cada Step debe estar identificado de forma única por un `nanoid` y también estar adherido a una estructura de directorios específica diseñada para organizar su contenido.

## Organización de archivos y directorios

* La estructura básica de un Step consiste en la siguiente, suponiendo en este caso que el `nanoid` asignado para este es `AsRwq6SjrkyTbWhiCJZYgasTmpE5np48bQc`:

  ```markdown
  AsRwq6SjrkyTbWhiCJZYgasTmpE5np48bQc
  ├── en
  │   └── README.md
  ├── es
  │   └── README.md
  ├── docker
  │   └── Dockerfile
  └── properties.json
  ```

  * `en`: contiene un único archivo llamado `README.md`, que es en realidad el contenido técnico que proporciona el Step al lector. Este fichero es obligatorio en cada Step.
  * `es`: esta carpeta es opcional y contiene un único archivo llamado `README.md`, que en realidad es el contenido técnico del archivo `en/README.md` pero debidamente traducido al español.
  * `docker`: esta carpeta también es opcional, dependiendo de si el Step incluye ejercicios prácticos. Si es así, contiene una pequeña aplicación encapsulada en una imagen Docker que se instanciará cuando se despliegue un Lab que incluya este Step. El archivo `Dockerfile` se utiliza para generar la imagen Docker.
  * `properties.json`: contiene metadatos del Step, los cuales describen el número de ejercicios incluidos, el tiempo previsto de realización en minutos y también los detalles de autoría. La estructura de este archivo es la siguiente:

    ```json
    {
      "numExercises": 0,
      "estimatedCompletionTime": 0,
      "author": "samus.io",
      "authorGithubId": "samus-io",
  "isChoosable": true
    }
    ```

    * Es justo aquí donde tienes que escribir tu nombre y tu identificador de perfil de GitHub como atributos del archivo `properties.json` para poder hacer referencia a tu contribución en la plataforma.

## Script [steps-helper][1]

* Para facilitar el proceso de creación de un Step se ha incluido en este repositorio el script [steps-helper][1]. Este pequeño script automatiza la generación de la estructura de directorios y los ficheros necesarios.
* Para ejecutar el script, dado que está escrito en Node.js, es imprescindible instalar primero las dependencias necesarias. Para ello, comienza este proceso navegando hasta el directorio `steps-helper` dentro de la carpeta `scripts` e inicia la instalación de dependencias:

  ```bash
  cd ./scripts/steps-helper/
  ```

  ```bash
  npm install
  ```

* Luego, navega al directorio `steps` y ejecuta el script:

  ```bash
  cd ../../steps
  ```

  ```bash
  node ../scripts/steps-helper/index.js
  ```

* La ejecución de estos comandos generará efectivamente la estructura predefinida para un Step. Observa que acabamos de crear la estructura de directorios para el nuevo Step dentro de la carpeta `steps`, donde en realidad se encuentran todos los steps disponibles.

[1]: /scripts/steps-helper/
