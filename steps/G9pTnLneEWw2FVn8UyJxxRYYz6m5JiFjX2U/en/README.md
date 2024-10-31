# Software Testing Overview

* The primary purpose of software testing is to assess the software's functionality, performance, and stability. This process involves executing the software under various conditions and test cases to detect issues, evaluate performance and ensure functionality requirements are being met.
* Software testing is conducted at different stages of the development lifecycle, with varying objectives.

## Main Purposes

* **Bug detection**.
  * Running tests is the most productive way to identify if an addition to the codebase is not unadvertedly causing bugs in other functionalities.
  * Once a bug has been detected, tests help isolate it from the rest of the code, making it easier for the developer to pinpoint and correct the issue.
* **Developer confidence and efficiency**.
  * Testing provides developers with confidence and a more solid understanding of their code; encouraging developers to make changes without fears of breaking existing functionalities.
  * When functionalities break, tests reduce the time and effort the developer spends on debugging. Automated test suites also save the developer and team time over running manual tests to assure everything still works.
* **Quality Assurance (QA) and User Acceptance**.
  * User-centric tests enable the team to identify and address issues with usability, user satisfaction and behavior.
  * User Acceptance tests give a unique perspective and valuable insights into user's expectations, habits and requirements, contributing towards a satisfying user experience.

## Tests classification

### By Approach

#### `Black-Box Testing`

* Evaluates the software's external behavior without knowledge of its internal code and structure.
* It focuses on the software's functionality and user experience and does not require much technical background.

#### `White-Box Testing`

* Examines the software's internal code, logic, and architecture. Testers have access to the code and structure, allowing them to evaluate code quality and to fix possible issues, and therefore need to understand the inner-workings of the tested entity.

### By goal

#### `Functional Tests`

* Primarily evaluate whether the software functions as intended per the specified requirements, checking that each feature performs its designated task efficiently.
* They aim to improve code quality and user satisfaction through feature validation, code quality assurance and consistency in the application's behavior and output.

#### `Non-functional Tests`

* Focus on software aspects beyond its core functionality; they evaluate performance, security, usability, scalability, and other non-functional characteristics.
* They offer insights into potential bottlenecks, vulnerabilities or areas of optimization.

### By method of execution

#### `Manual Tests`

* They are ran by a human tester who interacts with the application as an end user would. They provide a human perspective and much flexibility, specially in user satisfaction.

#### `Automated Tests`

* Mostly focus on ensuring code quality. Through repetition, we can verify the functionality remains operational and save time that would otherwise be wasted manually running these tests.
* They can be integrated into release pipelines to ensure smooth code integration all throughout the development cycle.

### By Scope

#### `Unit Tests`

* Happen at the lowest level of testing, where a single function, method, or service (unit) can be tested in isolation to verify that individual parts work as expected.

#### `Integration Tests`

* Aim to make sure these individual components behave as expected when working together. They test the functionality of these units cohesively to ensure seamless inter-module interactions.

#### `End-to-End/System Tests`

* Have the broadest scope of the three; they differentiate from Integration tests in that they test the system **as a whole**, also including _non-functional_ aspects. For E2E (End-to-End) tests, this is done from the user perspective.

#### `Smoke Tests`

* Serve as quick preliminary "smoke checks" to determine if the software's major functionalities are intact. Though less reliable, their faster execution time means more frequent feedback, as developers can use them as quick health checks without having to wait for slower, more robust test suites.
  > "You plugin a new board and turn on the power. If you see smoke coming from the board, turn off the power, you don't need to do any more testing" from Kaner, Bach, and Pettichord. _Lessons Learned in Software Testing_

## Considerations

* The best testing configuration will always be different across different projects, balancing the time spent on writing (and re-writing) tests with the safety and confidence they provide is often the most difficult challenge for the tester.
