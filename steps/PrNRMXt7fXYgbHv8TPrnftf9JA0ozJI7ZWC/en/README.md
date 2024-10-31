# Run the helper script to create the directory structure

* Each Step must be uniquely identified by a `nanoid` and also adhered to a specific directory structure designed to organize its contents.

## File and directory organization

* The basic structure of a Step consists of the following, assuming in this case that the `nanoid` assigned for it is `AsRwq6SjrkyTbWhiCJZYgasTmpE5np48bQc`:

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

  * `en`: contains a single file called `README.md`, which is actually the technical content that provides the Step to the learner. This file is mandatory for each Step.
  * `es`: this folder is optional and contains a single file called `README.md`, which is actually the technical content of the `en/README.md` file but properly translated into Spanish.
  * `docker`: this folder is also optional, depending on whether the Step includes hands-on exercises. If so, it contains a small application encapsulated in a Docker image that will be instantiated when deploying a Lab that includes this Step. The `Dockerfile` file is used to generate the Docker image.
  * `properties.json`: contains Step metadata, describing the number of exercises included, expected completion time in minutes, and also authorship details. The content of this file is as follows:

    ```json
    {
      "numExercises": 0,
      "estimatedCompletionTime": 0,
      "author": "samus.io",
      "authorGithubId": "samus-io"
    }
    ```

    * It is right here where you have to write your name and your GitHub profile ID as attributes of the `properties.json` file in order to reference your contribution on the platform.

## [steps-helper][1] script

* To facilitate the process of creating a Step we have included in this repository the script [steps-helper][1]. This little script automates the generation of the directory structure and the necessary files.
* To run the script, since it is written in Node.js, it is essential to first set up the required dependencies. To do so, begin this process by navigating to the `steps-helper` directory within the `scripts` folder and start the installation of dependencies:

  ```bash
  cd ./scripts/steps-helper/
  ```

  ```bash
  npm install
  ```

* Afterwards, continue moving to the `steps` directory and then execute the script:

  ```bash
  cd ../../steps
  ```

  ```bash
  node ../scripts/steps-helper/index.js
  ```

* Executing these commands will effectively generate the predefined structure for a Step. Note that we have created the directory structure for the new Step inside the `steps` folder, where all available steps are actually located.

[1]: /scripts/steps-helper/
