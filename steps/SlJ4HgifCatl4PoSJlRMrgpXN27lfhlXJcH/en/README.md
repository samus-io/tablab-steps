# End-to-End Testing

* `End-to-End Testing` (or E2E) is a high level **user-centric** software testing technique that evaluates an entire application flow from start to finish.
* E2E tests focus mainly on user expectations, and the tested software's ability to meet them.
* Although it is common for these tests to assess the entire application, the term `E2E` can also be used more broadly to describe narrower tests, so long as they maintain the user's perspective, such as a specific user journey through your application.
* E2E tests' unique focus allows for further scrutiny of the application behavior under user-simulated actions, inputs and workflows, providing validation and reliability in a real-world context.
* Generally, E2E tests are ran after `Unit & Integration Tests`, and before `Quality Assurance & User Acceptance Tests`.

## Drawbacks

* Testing user-like interactions and real-world scenarios is by nature more complex than other tests.
* E2E tests are sensitive to their environments, and dependent on the methods and units inside them, which make them fragile and tends to increase maintenance overhead.
* To maximize efficiency, it is important to use the right tool for the right job; E2E tests are most appropiate for validating **user workflows and experiences**.

## Tools

* Testers use tools through CLIs, Programming APIs and GUIs to streamline the E2E testing process.
* These tools provide a **user-friendly interface** to interact with a live environment running your app as an end user would.
* This interface supports manual interaction, and sometimes scripting and automation, allowing testers to create and execute test scripts that replicate specific user journeys and scenarios, allowing for `non-functional testing`.
  > Non-functional testing evaluates software aspects beyond features, some like performance and usability, which are well-suited for examination using these testing tools.
* They enhance the test writing and running experience, often providing features like browser/platform simulation, parallel test execution and test reporting and analytics.
* Some of them, like [Cypress][1] or [Puppeteer][2], are designed to simulate the browser and test Javascript code.
* Others like [Selenium][3] or [Appium][4] are language agnostic and allow for testing in most programming languages and aim to support different platforms, such as web, mobile, TV, etc.

## Test Breakdown

* When End-to-End testing, a certain functionality will be broken down into testable segments from the user's perspective.
* This breakdown helps us quickly ensure that the entire workflow remains functional, and if not, helps to diagnose and correct the error.

### E-Commerce Checkout Flow

* **1.** Should add items to cart.
* **2.** Should start checkout.
* **3.** Should enter payment information.
* **4.** Should provide billing information.
* **5.** Should process payment.
* **6.** Should verify order.
* **7.** Should Receive order confirmation.
* **8.** Should update tracking status.

[1]: https://www.cypress.io/
[2]: https://pptr.dev/
[3]: https://www.selenium.dev/
[4]: https://appium.io/docs/en/2.1/
