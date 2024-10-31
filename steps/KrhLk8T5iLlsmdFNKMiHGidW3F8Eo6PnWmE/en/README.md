# Integration Testing

* `Integration Testing` in software aims to verify correct behavior from interacting components or modules within an application.
* While `Unit Testing` focuses on scrutinizing single independent units, Integration Testing broadens its scope to assess the functionality of these units coming together.

## Benefits of Integration Testing

* This specific scope helps identify issues with interactions and data flows between different components, enabling the testing of functionalities made up of inter-connected modules.
* By detecting issues at the integration level, developers can address them earlier in the development cycle, reducing the likelihood of more complex and costly problems arising later in the process.
* While the bulk of non-functional testing typically occurs during systems testing, integration testing can reveal performance bottlenecks, security vulnerabilities, and issues related to scalability resulting from component interactions.

### Mocking

* In complex functionalities with multiple components, testing each one within the context of the full application can be challenging and time-consuming, so mocking is employed as a time-saving technique.
* A `mock` is a simulated component or function that emulates the behavior of the actual components that make up the system, allowing the tested functionality to interact with simulated versions of its dependencies.
* This technique creates a controlled environment for the tester to focus on the specific component's behavior and its integration with others, cutting the time required for full integration testing with real, unmocked components.
* Mocking is particularly effective when real components are unavailable during testing or have dependencies that are challenging/expensive to replicate.
* While mocking saves time and resources, it should not replace all real components during testing. Overreliance on mocking can lead to incomplete testing, potentially missing integration issues.

## Approach

### Gradual

* With the `Bottom-up` approach testers will start at the lowest level components first, gradually integrating them with higher-level ones.
* In contrast, `Top-down` approach testers will start from the top, and work their way down from the bigger picture into smaller segments layer by layer.
* A combination of both approaches is called `Sandwich Testing`.

### Simultaneous

* `Big-Bang testing` attempts to save time by simultaneously testing the entire functionality as a whole, without any priority by hierarchy levels within the system.

## Generic Integration Test Procedure

* The responsible integration test for an application's transaction modules could be broken down into four steps:

  * **1. Request Transaction**: Initiate the transaction and provide key details to the transaction service component.
  * **2. Validate Transaction**: Ensure the transaction complies with business rules and has sufficient funds.
  * **3. Process Transaction**: Transfer funds and record the transaction in the database.
  * **4. Verify Account Balance Update**: Confirm that the account balance reflects the correct post-transaction amount.
