# RunTime Environment (RTE)

* In software development, an environment refers to a server tier designated to a specific stage in a release process.

## Types of RTE

* Exact definitions and boundaries between environments vary. Test may be considered part of Dev, Acceptance Testing may be considered part of Test, part of Stage, or be separate, etc.

### Development Environment

* The `Development Environment` is the first environment in software development which acts as the workspace for developers to do programming and other operations related to the creation of software. It covers from the first lines of code to all code updates.
* As the name suggests, this is where the development of the software takes place.
* Part of the development environment is the `Integrated Development Environment (IDE)`, which is a software package with extensive functions for authoring, building, testing, and debugging a program that is commonly used by software developers running on its own workstation. Common IDEs are Microsoft Visual Studio, Eclipse, NetBeans, etc.

### QC/Test Environment

* A `Quality Control (QC) or Test Environment` allows testing engineers to analyze new and changed code whether via automated or non-automated techniques.
* Using a test environment testers make sure that the new code will not have any impact on the existing functionality.
* They also ensure the quality of the code by finding any bugs and reviewing all bug fixes.
* The focus here is testing individual components rather than the entire application, to check the compatibility between old and new code. This is why unit tests are performed at this stage.
* Different types of testing suggest different types of test environments, some or all of which may be virtualized to allow rapid, parallel testing to take place.

### QA/Staging/Pre-Production Environment

* A `Quality Assurance (QA) or Staging Environment` is a nearly exact replica of the production environment so it seeks to mirror an actual production environment as closely as possible to ensure the software works correctly.
* The focus here is to test the application or software as a whole. 
* This is where you can conduct tests to ensure that no problems come up in production and limit negative impact on users. Examples of the kind of test that can be run in this environment include functional and smoke testing.
* Another important use of staging is performance testing, particularly load testing, as this is often sensitive to the environment.
* Depending on any regulatory factors (such as GDPR requirements) and your organization's level of ability to anonymize data, a staging environment may even have anonymized or complete sets of production data in order to more closely mimic the real world production environment.
* The staging environment is frequently restricted to a small group of people. The only groups that can access the application in staging are those with whitelisted emails and IP addresses, as well as your developer team.
* Isolating the staging and production environments on two separate clusters and VPCs is a good practice to avoid any potential issues on your production caused by your staging. This is not a mandatory step, but it is well recommended.

#### How to create a Staging Environment

* Create a staging environment from scratch.
* Clone your production environment and create a staging environment from it.

#### What is the difference between Test Environment and Staging Environment

* The main difference between a staging environment and a testing environment is the level of similarities to the production environment.
* In a staging environment, everything is updated to the latest versions and everything should mirror the live site except for the changes that you just pushed from the development environment. This enables you to make sure that your new changes will not break anything unexpectedly once you deploy them to your live environment.
* In a testing environment, this is not necessarily the case, where the environment is less strict on everything having to be updated to match the live environment. Instead of fully testing everything, in a test environment you will be working on assumptions of how things work and instead focus on testing the specific code you are changing. The benefit of having a test environment is that you can test your changes faster, without having to fully replicate your live environment like you would on a staging site.

### Production/Live Environment

* A `Live or Production Environment` is where the software is produced and is running on a production server. It has officially gone live to real users.
* When deploying a new release to production, rather than immediately deploying to all users, the release can be deployed in phases to a segment of your users first to see how it performs to catch and fix any additional bugs before deploying to the rest of your users.

