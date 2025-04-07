# Tasks to perform in each DevOps phase

* DevOps is typically divided into eight distinguished phases as an operational model.
* These phases operate in a continuous loop, where each phase is delivering value to the subsequent phase.

![DevOps Lifecycle][1]

## Plan phase

* This phase involves defining or redefining project goals and identifying the required software functionalities.
* The idea is to plan the full workflow before anyone starts to code.

### Key tasks

* Proceed with requirements analysis to gather the specific needs of the business or end users.
* Assign resources including team members and tools to use.
* Create a Roadmap to guide future development.
  * List out all the tasks based on project requirements.
  * Create timelines for the completion of each task.
* Consider to start with a UI/UX Design.
* Consider compliance with the LOPD/LOPDGDD and GDPR.
* Consider `[The Twelve-Factor][1]` methodology.
* Gather feedback and relevant information from customers and stakeholders.

## Code phase

* Developers begin coding according to the requirements and specifications defined in the planning phase.
* All software development takes place here.

### Key tasks

* Use a `Version Control System (VCS)` such as Git to manage changes to the codebase.
* Use version control hosting platform like Bitbucket, GitHub or GitLab as a central repository.
  * Developers typically maintain a copy of the source code on their local machine. Changes are then submitted to a shared repository and integrated into a feature branch.
* Perform peer reviews.
* Focus on linting rather than testing.

## Build phase

* The build phase begins once developers commit code to the source repository.
* It runs automated tests and if there's an issue with the code, the build fails and the relevant developer is notified, ensuring that only error-free code progresses through the pipeline.
* This phase ensambles all components into a binary artifact ready for deployment.

### Key tasks

* Configure dependency management tools to ensure correct library versions are used and conflicts are resolved.
* Integrate and set up triggers for unit and integration testing to be part of the build process to detect any regressions.
* Ensure that all merges into main branches are build-tested.
* Automate the creation of containers that encapsulate the application environment for consistent testing and deployment.
* Set environment-specific parameters that affect how the build is processed, such as development, testing, and production configurations.

## Test phase

* The test phase is initiated after a build artifact is created and successfully deployed to testing or staging environments, occurring only when the build passes.
* It involves running both manual and automated tests to further validate code integrity and conduct deeper, out-of-band testing.

### Key tasks

* Run functional tests to verify that each feature of the software operates according to the requirement specifications:
  * Conduct preliminary smoke testing to reveal simple failures severe enough to reject a prospective software release.
  * Use regression tests to confirm that recent program or code changes haven't negatively impacted existing features
  * Validate the complete and integrated software product by executing system tests.
  * Perform `User Acceptance Testing (UAT)` to verify if the built features work for the user as expected and fulfill all requirements.
* Perform non-functional tests to evaluate the application's operational characteristics:
  * Assess the speed, responsiveness, and stability of the application under a particular workload through performance testing.
  * Run load tests to check the application's behavior under both normal and peak load conditions.
  * Determine the limits of the application in terms of maximum operational capacity with stress testing.
  * Conduct compatibility testing to ensure the application performs well across different browsers, databases, hardware, operating systems, mobile devices, and networks.

## Release phase

* This release phase involves preparing and setting up the necessary steps to deploy the build to a live environment.
* It serves as a milestone within the overall DevOps workflow, marking the transition to the operations-focused part of the process.

### Key tasks

* Apply version tags to the codebase in the version control system, documenting the release with detailed change logs for traceability and future reference.
* Update and finalize release notes, user manuals, and system documentation with comprehensive details on new features, bug fixes, and known issues for transparency and compliance.
* Validate image integrity signatures.
* Perform compliance checks to ensure that the release meets all regulatory and security standards, preventing legal or security issues post-deployment.
* Develop a detailed deployment plan with a clear rollback strategy to quickly revert to a previous version if the deployment encounters significant problems.

## Deploy phase

* This phase refers to the process of deploying the final version of the build artifact to the production environment after it has been created and configured.
* It involves making any necessary infrastructure changes, either through automation using Infrastructure as Code (IaC) frameworks, or manually.
* The outcome of this phase is a deployed and operational application in a live environment available for end users to interact with.
* The main security areas to focus on during the deploy phase are those that exclusively affect the live production system.

### Key tasks

* Configure load balancers to deploy the release in phases to a segment of users first, rather than immediately deploying to all users. This allows for monitoring performance and addressing any additional bugs before rolling out the release to the rest of the users.
* Configure automated rollback procedures to revert to the previous version in case of a deployment failure.
* Configure monitoring tools and set up alert systems to track the application's performance and stability in the production environment, ensuring rapid response to any post-release issues.
* Conduct immediate post-deployment checks to verify that services are operational and behaving as expected.
* Ensure there is a tested and operational alternative method to deploy changes to the application besides relying solely on the standard process with GitHub or GitLab, in case they become unavailable. This alternative method must include the capability to push changes to production directly from a local environment in emergency situations.
* Prepare support teams to handle potential inquiries or issues arising from the new release.
* Notify end users of new updates or downtime expected during the deployment.

## Operate phase

* The release is now live and being used by the customers.
* This phase is where the operations team ensures that the application performs optimally and remains reliable and available for end users.
* It is also where hotfixes are applied to resolve urgent critical bugs or security threats.

### Key tasks

* Regularly schedule and perform data backups to ensure data integrity and availability.
* Develop and test disaster recovery plans to ensure quick recovery in case of a system failure or data loss.
* Establish and publish a set of procedures for individuals to contact the appropriate channels when security issues are discovered in the application.
* Ensure all operational processes comply with legal and regulatory requirements.

## Monitor phase

* Once an application is stable and fully operational in a live production environment, it's crucial to adopt further security measures, such as continuously monitoring the application for any signs of attacks or data leaks.
* It's also critical to keep track of the application's features and performance to detect any system faults or performance issues, helping to identify and resolve problems before they affect the end user.
* As the final phase in the pipeline, the overarching goal is also to gather as much feedback as possible from the entire environment for the next cycle.

### Key tasks

* Implement secure methods for collecting attack logs and consolidate those from all systems and applications into a centralized log management system to streamline analysis and response.
* Identify metrics that directly influence the application's performance and user satisfaction, and determine appropriate limits for each to facilitate the recognition of deviations.
* Design and implement dashboards to visualize the data in an easily digestible format.
* Regularly review collected data to identify patterns or anomalies that could indicate underlying issues.
* Monitor and optimize resource usage to control cloud costs and improve efficiency.

[1]: /static/images/learning/devops-lifecycle.png
