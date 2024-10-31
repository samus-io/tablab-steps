# What is improper error handling?

* Improper error handling vulnerability is a software flaw that occurs when an application fails to manage errors correctly, leading to undesired consequences such as displaying errors to the end user, exposing system vulnerabilities, or causing application crashes.
* This inadequate handling can severely disrupt the normal flow of an application and can assist the attackers to exploit the application in initial phase.
* The most common issue arises when detailed internal error messages, such as stack traces, database dumps, and error codes, are exposed to users. These messages reveal implementation details that should always remain hidden. Such information can provide attackers with valuable insights into potential vulnerabilities within the site and can also be confusing for regular users.
* Various common conditions can trigger errors, including out of memory situations, null pointer exceptions, system call failures, database unavailability, network timeouts. When developers do not effectively anticipate and handle such errors, it can leave the application open to exploitation by attackers.
* Lack of proper logging, insecure error messages, improper input validation, insufficient logging are the common scenarios for improper error handling.
* For instance, when a user attempts to access a non-existent file, the typical error message is `file not found` and when a user tries to access a file they do not have permission to view, the message would be `access denied`. Users should not even be aware of the file’s existence, but such discrepancies can easily reveal the presence or absence of inaccessible files or the directory structure of the site to attackers.

## Example scenarios

### Example of improper error handling with SQL query

![image for SQL improper error handling][1]

* Consider a web application that allows users to search for products in a database by entering search terms in a search bar.
* An attacker enters a malicious search query designed to exploit SQL injection vulnerabilities.
* The application attempts to execute the SQL query and encounters a syntax error due to the malicious input.
* Instead of handling the error gracefully, the application displays the raw SQL error message to the user:

```text
SQL error: syntax error at or near "DROP TABLE products" at character 15
```

* The detailed error message reveals information about the database and the SQL syntax.
* Attackers can use this information to refine their attacks and potentially exploit the application further.

### Example of improper error handling in application backend code

![image for node.js app improper error handling][2]

* Consider a Node.js web application allowing users to submit forms for processing. For example, a user can submit their profile information through a form that sends data to the server for validation and storage.
* An attacker submits a form with malicious input, such as a string containing unexpected or harmful data.
* The server attempts to process the input but encounters an unexpected error due to the malicious data.
* The application does not properly handle the error and instead returns a detailed error stack trace to the user:

```text
TypeError: cannot read property 'name' of undefined
    at /path/to/app/routes/profile.js:15:18
    at layer.handle [as handle_request] (/path/to/app/node_modules/express/lib/router/layer.js:95:5)
    at next (/path/to/app/node_modules/express/lib/router/route.js:137:13)
    at route.dispatch (/path/to/app/node_modules/express/lib/router/route.js:112:3)
    at layer.handle [as handle_request] (/path/to/app/node_modules/express/lib/router/layer.js:95:5)
    at /path/to/app/node_modules/express/lib/router/index.js:281:22
    at function.process_params (/path/to/app/node_modules/express/lib/router/index.js:335:12)
    at next (/path/to/app/node_modules/express/lib/router/index.js:275:10)
    at urlencodedparser (/path/to/app/node_modules/body-parser/lib/types/urlencoded.js:100:7)
    at layer.handle [as handle_request] (/path/to/app/node_modules/express/lib/router/layer.js:95:5)
```

## What is the impact of improper error handling?

* Improper error handling can have significant negative impacts on an application, ranging from security vulnerabilities to poor user experience. Here are some key impacts:

  * **Information leakage**: detailed error messages can reveal sensitive information about the application’s structure, database, and underlying technology. this information can be exploited by attackers to craft more effective attacks.
  * **SQL injection**: improperly handled errors related to database queries can expose the application to SQL injection attacks, where attackers can manipulate queries to gain unauthorized access to data.
  * **Denial of Service (DoS) attacks**: attackers can crash the application or consume excessive system resources, leading to a denial of service.
  * **Unauthorized access**: attackers can gain unauthorized access to the application or the underlying system.
  * **Fail-open conditions**: security mechanisms that fail open (i.e., grant access upon error) can allow unauthorized access if errors are not correctly handled.
  * **Application crashes**: unhandled errors can cause the application to crash, leading to downtime and service interruptions.
  * **Data corruption**: errors that are not properly managed can result in corrupted data, especially if transactions are not rolled back correctly.
  * **Inconsistent behavior**: improper error handling can lead to inconsistent application behavior, making it difficult for users to understand and predict how the application will respond.
  * **Negative reviews**: users who encounter problems due to improper error handling are more likely to leave negative reviews, which can harm the application's reputation.
  * **Increased support costs**: poor error handling can lead to more frequent support requests and higher costs for troubleshooting and resolving issues.
  * **Development and maintenance overhead**: addressing issues caused by improper error handling can increase the workload for developers and maintenance teams, diverting resources from new features and improvements.

## Examples of improper error flaws

* Here are the examples of error handling flaws that can expose sensitive information or lead to security vulnerabilities:

  * **Detailed database error messages**: an error message that shows the SQL query that failed, revealing table names and database schema details.
  * **Environment variables exposure**: an error message that includes environment variables, which might contain sensitive information such as API keys or database connection strings.
  * **File path exposure**: an error message that reveals the full file path on the server, providing insights into the server’s directory structure.
  * **Sensitive parameter values**: error messages that echo back user-provided data without sanitization, potentially exposing sensitive information input by users.
  * **Operating system details**: error messages that include the operating system version or other environment-specific information that can help an attacker profile the system.
  * **Unhandled null pointer exceptions**: an error message that indicates a null pointer exception, revealing internal data flow and potential weak points in the code.
  * **Detailed error codes**: error messages that return specific error codes which can be correlated with known vulnerabilities.
  * **Service configuration information**: an error message that reveals the configuration settings of services, such as memory limits, timeouts, or maximum connection settings.
  * **Backup file information**: an error message that indicates the presence or location of backup files, which might be targeted by attackers.
  * **Debug information in production**: error messages that include debug information intended for development, such as internal state dumps or logging messages.
  * **Error messages with sensitive data**: error messages that accidentally include user data, such as credit card numbers or passwords.
  * **Network configuration details**: an error message that reveals network configuration details, such as IP addresses, port numbers, or firewall settings.
  * **Internal logic flaws**: error messages that inadvertently disclose internal business logic or rules, which could be exploited to bypass validation or authorization checks.
  * **Unhandled third-party library errors**: error messages from third-party libraries that are not properly caught and sanitized, revealing potential vulnerabilities in the external dependencies.
  * **Version control system metadata**: error messages that reveal version control system metadata, such as commit hashes or branch names, which can be used to infer the development process and code changes.

## Importance of proper error handling

* Proper error handling ensures that errors are captured and logged in a controlled manner.
* It prevents the exposure of sensitive information to end users.
* Detailed and consistent logging helps in diagnosing and troubleshooting issues efficiently.
* Accurate logs provide valuable insights for improving application security and stability.

## Where to implement error handling and logging?

* Error handling mechanism can be implemented at multiple points in an application, like at all points where user input is processed, during database operations, in external API calls and integrations or within core application logic to catch and log unexpected behaviors.

[1]: /static/images/improper-error-handling-example1.png
[2]: /static/images/improper-error-handling-example2.png
