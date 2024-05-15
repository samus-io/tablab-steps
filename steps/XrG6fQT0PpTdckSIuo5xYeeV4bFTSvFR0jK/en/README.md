# How to create a practical training exercise in a Step

* A Step can include no more than one exercise, since a single containerized application is instanced per Step when a user desploys a Lab.

## First, create a web app that provides the exercise

* For any type of exercise you want to create, make sure to create an application that can be executed in [Cloud Run][1] on Google Cloud Platform. This is where our docker images are instantiated when a Lab is deployed.
* Ensure that the exercise is available at the root path of the application `/`.

## Second, build a Docker image

* Use the `docker` folder created in your Step structure. You should place inside this directory the web application, which must be containerized.
* Write in the `Dockerfile` file all instructions to generate the Docker image.
* Note that the base image of the `Dockerfile` must be an official image from the [Docker Hub][2]. If you need an image that is not official, [contact the tablab.io team][3] and they will provide it for you.

## Third, include the exercise in the content

* When you want to add an exercise at some point in the content of the Step, just add the following special tag:

  ```markdown
  @@ExerciseBox@@
  ```

## Last, but not least

* Please be aware that the tablab.io team will review all submitted steps and changes or corrections may be made if they do not adhere to the required format.
* Remember that making [tablab.io][4] a collaborative platform is our mission, and that means offering extensive support during the Step generation process. For any inquiries or suggestions please [contact us][3], our team is here to help.

[1]: https://cloud.google.com/run
[2]: https://hub.docker.com/search?q=&image_filter=official
[3]: mailto:hello@samus.io
[4]: https://tablab.io
