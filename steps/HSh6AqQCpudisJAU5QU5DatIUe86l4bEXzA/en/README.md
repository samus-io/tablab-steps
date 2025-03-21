# RunTime Environments (RTEs)

* The runtime environment is the space where a program or application runs, considering both the hardware and software infrastructure required for executing the code in real-time.

## Types of RTE in DevOps

* In DevOps, runtime environments encompass all infrastructure and configurations involved in executing applications throughout their entire lifecycle.
* These environments typically include development, test, staging, and production environments, each serving a specific purpose in the software delivery pipeline.

![DevOps Lifecycle: Runtime Environments][1]

* Managing and maintaining consistent and reliable runtime environments is crucial for ensuring the stability, scalability, and performance of applications as they progress from development to deployment.

### Development Environment

* The `Development Environment` is the first environment in software development which acts as the workspace for developers to do programming and other operations related to the creation of software. It covers from the first lines of code to all code updates.
* As the name suggests, this is where the development of the software takes place.
* Part of the development environment is actually the `Integrated Development Environment (IDE)`, which is a software package with extensive functions for authoring, building, testing, and debugging a program that is commonly used by software developers running on its own workstation. Common IDEs are Microsoft Visual Studio, Eclipse, NetBeans, etc.

### Test Environment

* A `Test Environment` allows testing engineers to analyze new and changed code whether via automated or non-automated techniques.
* Using a test environment testers make sure that the new code will not have any impact on the existing functionality.
* They also ensure the quality of the code by finding any bugs and reviewing all bug fixes.
* The primary focus here is testing individual components rather than the entire application, aiming to verify compatibility between old and new code. This is why **unit tests** are performed at this stage.
* Different types of testing suggest different types of test environments, some or all of which may be virtualized to allow rapid, parallel testing to take place.

### Staging/Pre-Production Environment

* A `Staging Environment` is a nearly exact replica of the production environment, aiming to closely mirror the actual production environment to ensure the software works correctly.
* The focus here is to test the application or software as a whole.
* This is where you can conduct tests to ensure that no problems come up in production and limit negative impact on users. The kind of test that can be run in this environment include **functional and smoke testing**.
* Another important use of staging is **performance testing**, particularly **load testing**, as this is often sensitive to the environment.
* Depending on any regulatory factors (such as GDPR requirements) and the organization's level of ability to anonymize data, a staging environment may include anonymized or complete sets of production data to closely replicate the real-world production environment.
* Access to the staging environment is often limited to a small group of individuals. Only those with whitelisted emails or IP addresses, along with the developer team, have access the application in staging.
* Isolating the staging and production environments on two separate clusters and VPCs is a good practice to avoid any potential issues on production caused by the staging environment. This is not a mandatory step, but it is well recommended.

#### How to create a Staging Environment

* Create a staging environment from scratch.
* Clone the production environment and create a staging environment from it.

#### What is the difference between Test Environment and Staging Environment

* The main difference between a staging environment and a testing environment is the level of similarities to the production environment.
* In a staging environment, every element is updated to the latest version, closely reflecting the live site except for the changes recently pushed to the development environment. This configuration ensures that new changes are tested thoroughly to avoid unexpected disruptions when deployed to the production environment.
* In a testing environment, there isn't a strict need to update every element to match the production environment. Testing here is more targeted, focusing on specific code changes rather than a full system test, and it operates on assumptions about how other parts of the system function. This approach speeds up the testing process, as there's no requirement to fully replicate the production setup, unlike in a staging environment.

### Production/Live Environment

* A `Production Environment` is where it runs on a production server and is officially available to real users.
* When deploying a new release to production, rather than immediately deploying to all users, the release should be deployed in phases to a segment of users first to see how it performs to catch and fix any additional bugs before deploying to the rest of the users.

[1]: /static/images/learning/devops-lifecycle-rte-environments.png
