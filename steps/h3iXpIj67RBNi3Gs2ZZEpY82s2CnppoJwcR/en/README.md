# Unit Testing

* Tests ran to assess individual components (or units) within an application are denominated `Unit Tests`; they isolate the logic from the rest of the application for the component to be scrutinized and tested as a single unit.
* They are intended to evaluate only the functionality of the specific unit under testing. Mock data is often used to simulate dependencies and maintain this isolation.
  > Mock data is simulated information, mimicking real dependencies, used in testing to ensure isolation and accurate evaluation of single components.
* Unit tests are typically fast to write, and provide quick feedback in the context of the working module, so developers will run them as frequently as they need to receive this feedback during the development process.

## Benefits of Unit Testing

* **Early bug detection**.
  * Unit tests can be executed in groups (or suites) to ensure code changes don't inadvertedly cause issues elsewhere in the app.
  * By adding these suites to the pipeline these issues can be caught earlier in the development process, saving time that would otherwise be wasted fixing regressions.
* **Bug fixing response time**.
  * When a bug is found, reducing the scope to this "unit" and keeping it independent and encapsulated narrows down the problem.
  * Rather than looking for a needle in a haystack, developers can address bugs quicker using unit tests to pin-point the issues and correct them without the distraction of other potential reasons.
* **Documentation**.
  * A Unit test should aim to implicitly reveal to the reader the intent of the component it covers, how to interact with it and what to expect from it.

## Drawbacks of Unit Testing

* Maintaining a large comprehensive suite of unit tests may involve additional costs and complexities for the team.
* While a single unit test may be quick to write and maintain, the case is not the same for a matured codebase with an ever-expanding test suite, leading to a slower development cycle.
* Each time a change is made to the codebase, the corresponding unit tests must be updated. This process can often accumulate, or even make developers hesitant to make changes, given the associated burden of updating the unit tests.

## Generic Unit Test Procedure

* Representing a unit test for a method that queries a database for a search, the steps would look like:
  * **1. Setup**:
    * Create a test instance of the database search method.
    * Populate a mock database with sample data.
  * **2. Test**:
    * Call the searchDatabase() method with different arguments.
    * Validate response from mock database.
  * **3. Teardown**:
    * Close connection to the mock database.

## Tools

* Most programming languages have dedicated **unit testing frameworks** like _JUnit_ for Java and _Jest_ for JavaScript to streamline the writing and execution of these unit tests. They offer helpful features such as test discovery, setup and teardown methods, and result reporting and can also be used as software development tools if following `Test Driven Development (TDD)`.
  > Test Driven Development (TDD) is a development approach that emphasizes writing unit tests before writing the code for it. Developers create tests that define the expected behavior and then work on writing code that fulfills it.

## Best Practices

* To ensure the reliability and maintainability of a test suite, it is crucial to correctly identify when and where to test, and aim to strike a balance between code coverage and developer agility and flexibility.
* Establishing a **consistent** naming convention for test cases. Using descriptive names that clearly communicate the purpose and expected outcomes of a test and following this convention all through-out the suite.
* Designing unit tests to be as **independent** as possible. This independence prevents one test's outcome from influencing others, while also making it easier to identify issues. Using fake data, like stubs, mocks and fakes if needed to simulate related dependencies to help isolate the module.
* Focusing on what the unit should do, rather than how, creates tests that are more flexible towards code changes.
