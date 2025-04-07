# Preventing CSRF using synchronizer token pattern in Jakarta EE 10 with OWASP CSRFGuard

* The synchronizer token pattern has been the most widely used method for anti-CSRF protection.
* When implementing CSRF tokens, adherence to the following security principles is essential:
  * Nonce (a number used once and then discarded): each token must be unique for every user's session to ensure they cannot be reused.
  * Unpredictable: tokens must be generated randomly, making them impossible to guess.
  * Session-tied: each token must be uniquely generated for a session and remain valid only within that session.
  * Strictly validated: the server must validate the token before executing the associated action.

## Understanding the synchronizer token pattern

* A unique CSRF token must be generated per session and securely stored on the server. The method below illustrates a simple way to generate and store the token:

  ```java
  public void setCSRFToken(HttpServletRequest request) {
      // Generate a cryptographically secure token
      String token = UUID.randomUUID().toString();
      request.getSession(true).setAttribute(CSRF_SESSION_KEY, token);
  }
  ```

  * To validate incoming requests and confirm their legitimacy, the token must be sent to the frontend application. This enables `POST`, `PUT`, or `DELETE` requests to include the token for server-side validation.
* As a common example, in `Server-Side Rendering (SSR)` applications, such as those using `(Java Server Pages) JSP`, the easiest way to pass a CSRF token to the front-end is by embedding it directly in the server-rendered HTML response:

  ```java
  @Override
  protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
      // Generate and store the CSRF token in the session
      setCSRFToken(request);
      request.getRequestDispatcher("/WEB-INF/views/pages/csrf-protected.jsp").forward(request, response);
  }
  ```

* Before handling state-changing requests, the server must retrieve the CSRF token from the session and compare it with the client's submitted token. The following method serves as a simple demonstration, which rejects requests if the token is missing or invalid:

  ```java
  @Override
  protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
      // Get the CSRF token from the request
      String requestCsrfToken = request.getParameter("csrf-token");

      // Get the CSRF token stored in the session
      HttpSession session = request.getSession(false);
      String sessionCsrfToken = (String) session.getAttribute(CSRF_SESSION_KEY);

      // Validate the CSRF token
      if (requestCsrfToken == null || !sessionCsrfToken.equals(requestCsrfToken)) {
          response.sendError(HttpServletResponse.SC_FORBIDDEN, "Invalid CSRF token.");
          return;
      }

      // CSRF token is valid, then process the request
  }
  ```

## OWASP CSRFGuard

* The [OWASP CSRFGuard][1] library is a security framework designed to protect Java EE web applications against `Cross-Site Request Forgery (CSRF)` attacks.
* The library enforces the synchronizer token pattern, requiring every state-changing HTTP request to include a unique and valid CSRF token, which prevents unauthorized actions from being executed on behalf of an authenticated user.

### How the OWASP CSRFGuard works

* OWASP CSRFGuard is built as a JavaEE filter, meaning it intercepts incoming HTTP requests before they reach the application's core logic.
* It verifies whether the request contains a valid CSRF token and blocks it if the validation fails.
* The library provides several automated ways to integrate CSRF protection into an application such as:
  * Automatic token injection into forms.
  * Automatic token injection into JavaScript requests.
  * Token validation on protected methods (e.g., `POST`, `PUT`, `DELETE`).
  * Customizable actions on CSRF detection as logging or redirecting the user.

### CSRFGuard properties

* The OWASP CSRFGuard library provides a wide range of configuration options to allow fine-grained control over CSRF protection mechanisms.
* To configure CSRFGuard, properties must be defined in the file `src/main/webapp/WEB-INF/csrfguard.properties`.
* The configuration of CSRFGuard requires defining properties in the `src/main/webapp/WEB-INF/csrfguard.properties` file.
* Below are common properties that define the behavior of CSRFGuard:

  |Property|Description|
  |:--:|:--:|
  |`org.owasp.csrfguard.Enabled`|Determines whether CSRFGuard is active (`true` or `false`).|
  |`org.owasp.csrfguard.TokenName`|Specifies the name of the CSRF token parameter included in requests. The default value is `OWASP-sessionCsrfToken`.|
  |`org.owasp.csrfguard.Rotate`|Defines whether the CSRF token should be regenerated after each successful validation. However, this functionality may cause navigation problems in applications, specifically, the `Back` button in the browser will often cease to function properly.|
  |`org.owasp.csrfguard.UnprotectedMethods`|Lists HTTP methods that should be excluded from CSRF protection (e.g., `GET`, `HEAD`, `OPTIONS`, `TRACE`).|
  |`org.owasp.csrfguard.ValidateWhenNoSessionExists`|Determines whether CSRFGuard should enforce token validation even when no session exists. Only set this to `false` if the web application is not susceptible to CSRF if the user has no session.|
  |`org.owasp.csrfguard.Ajax`|Enables CSRF protection for AJAX requests automatically including the CSRF token in all requests.|
  |`org.owasp.csrfguard.JavascriptServlet.injectIntoForms`|Defines whether CSRF tokens should be injected as hidden fields into HTML forms.|
  |`org.owasp.csrfguard.JavascriptServlet.injectGetForms`|Determines whether CSRF tokens should be injected into forms that use the `GET` method. Developers who ensure that their server-side controllers handle state-changing actions exclusively via POST requests should disable this property.|
  |`org.owasp.csrfguard.JavascriptServlet.injectFormAttributes`|Specifies whether CSRF tokens should be injected into the `action` attribute of forms.|
  |`org.owasp.csrfguard.JavascriptServlet.injectIntoAttributes`|Defines whether CSRF tokens should be injected into `src` and `href` attributes of HTML elements. If server-side controllers handle state-changing actions exclusively via POST requests, then its recommended to disable this property.|
  |`org.owasp.csrfguard.JavascriptServlet.injectIntoDynamicNodes`|Enables automatic injection of CSRF tokens into dynamically created HTML elements. If set to `true`, a `MutationObserver` monitors the DOM and injects tokens when necessary.|
  |`org.owasp.csrfguard.action.Error`|Configures an action to return an error when a CSRF violation occurs. This can be used to block the request and respond with an error message.|
  |`org.owasp.csrfguard.action.Code`|Specifies the HTTP status code to return when a CSRF violation occurs (e.g., 403, 401, etc).|
  |`org.owasp.csrfguard.action.Log`|When enabled, details about the violation are logged. The default behavior is `true`.|
  |`org.owasp.csrfguard.action.Log.Message`|Defines the log message format for CSRF violation attempts. Variables such as `%user%`, `%request_uri%`, and `%remote_ip%` can be used.|
  |`org.owasp.csrfguard.Logging`|Enables or disables logging of CSRFGuard activities, including violations. The default value is `true`.|
  |`org.owasp.csrfguard.LogLevel`|Specifies the logging level for CSRFGuard messages. The possible values are `DEBUG`, `INFO`, `WARN` and `ERROR`.|
  |`org.owasp.csrfguard.configuration.provider.factory`|Defines the configuration provider that CSRFGuard should use to load properties.|
  |`org.owasp.csrfguard.LogicalSessionExtractor`|Determines how CSRFGuard identifies a user's session. Defaults to `org.owasp.csrfguard.session.SessionTokenKeyExtractor`, which relies on `HttpSession`. Custom implementations can be used for stateless architectures.|

  * The definition of all properties and an extended explanation can be found in [Owasp.CsrfGuard.properties][2].

### Steps to integrate the library

* To successfully implement OWASP CSRFGuard, the following sections must be properly configured:
  1. To enable CSRFGuard functionality, the necessary dependencies must be specified in `pom.xml`.
  1. The `web.xml` file needs to be configured to register the CSRFGuard filter, servlet, and listeners for request validation.
  1. The `csrfguard.properties` file should contain essential settings that define token behavior, logging, and protection mechanisms.
  1. The `csrfguard.js` script must be requested from the frontend application to automatically handle CSRF token injection and validation in form submissions and AJAX requests.

#### 1. Add dependencies

* The following dependencies provide the core CSRF protection functionalities, session-based token management, and JSP tag support for CSRF token injection:
  
  ```xml
  <dependency>
      <groupId>org.owasp</groupId>
      <artifactId>csrfguard</artifactId>
      <version>4.4.0-jakarta</version>
  </dependency>

  <dependency>
      <groupId>org.owasp</groupId>
      <artifactId>csrfguard-extension-session</artifactId>
      <version>4.4.0-jakarta</version>
  </dependency>

  <dependency>
      <groupId>org.owasp</groupId>
      <artifactId>csrfguard-jsp-tags</artifactId>
      <version>4.4.0-jakarta</version>
  </dependency>
  ```

#### 2. Set filters and listeners

* In a JavaEE application, OWASP CSRFGuard is enabled by setting up JavaEE filters and listeners in `web.xml`, which enforce CSRF token validation and inject necessary JavaScript functionality:
  
  ```xml
  <!-- CSRFGuard filter-->
  <filter>
      <filter-name>CSRFGuard</filter-name>
      <filter-class>org.owasp.csrfguard.CsrfGuardFilter</filter-class>
  </filter>

  <!-- Map CSRFGuard filter to all application requests -->
  <filter-mapping>
      <filter-name>CSRFGuard</filter-name>
      <url-pattern>/*</url-pattern>
  </filter-mapping>

  <!-- Servlet to generate csrfguard.js -->
  <servlet>
      <servlet-name>JavaScriptServlet</servlet-name>
      <servlet-class>org.owasp.csrfguard.servlet.JavaScriptServlet</servlet-class>
  </servlet>

  <servlet-mapping>
      <servlet-name>JavaScriptServlet</servlet-name>
      <url-pattern>/csrfguard.js</url-pattern>
  </servlet-mapping>

  <!-- Initialize CSRFGuard on application startup -->
  <listener>
      <listener-class>org.owasp.csrfguard.CsrfGuardServletContextListener</listener-class>
  </listener>

  <!-- Manage CSRF token lifecycle within user sessions -->
  <listener>
      <listener-class>org.owasp.csrfguard.CsrfGuardHttpSessionListener</listener-class>
  </listener>

  <!-- Define the location of the csrfguard.properties configuration file -->
  <context-param>
      <param-name>Owasp.CsrfGuard.Config</param-name>
      <param-value>/WEB-INF/classes/csrfguard.properties</param-value>
  </context-param>
  ```

#### 3. Define CSRFGuard properties

* The `csrfguard.properties` file manages CSRFGuard behavior, providing fine-grained control over CSRF protection within the application.
* Begin by specifying the CSRF token name and configuring its behavior across requests. Additionally, define exempt HTTP methods and determine whether CSRF validation applies when no session exists:

  ```properties
  # If CSRFGuard filter is enabled
  org.owasp.csrfguard.Enabled = true

  # Token name
  org.owasp.csrfguard.TokenName = csrf-token

  # Token rotation on every request
  org.owasp.csrfguard.Rotate = false

  # Unprotected methods
  org.owasp.csrfguard.UnprotectedMethods = GET

  ## Only set this to false if the web application is not susceptible to CSRF if the user has no session
  org.owasp.csrfguard.ValidateWhenNoSessionExists = true

  # Ajax and XMLHttpRequest support
  org.owasp.csrfguard.Ajax = false
  ```

* Then define how CSRF tokens are injected into forms and requests through CSRFGuard's JavaScript handler, allowing CSRFGuard to modify form submissions and dynamic content to include the necessary security tokens automatically:

  ```properties
  # Javascript servlet settings

  ## Inject CSRF token as hidden field into HTML forms
  org.owasp.csrfguard.JavascriptServlet.injectIntoForms = true
  org.owasp.csrfguard.JavascriptServlet.injectGetForms = false

  ## Inject the token in the action form
  org.owasp.csrfguard.JavascriptServlet.injectFormAttributes = false

  ## Inject the CSRF prevention token in the query string of src and href attributes
  org.owasp.csrfguard.JavascriptServlet.injectIntoAttributes = false

  ## Inject in new DOM elements
  org.owasp.csrfguard.JavascriptServlet.injectIntoDynamicNodes = true
  ```

* Next, configure how CSRF violations are handled, including logging and response codes. When a request fails CSRF validation, CSRFGuard can log the event, return an error, or take other actions. Logging settings also define the level of detail stored:

  ```properties
  # Error handling
  org.owasp.csrfguard.action.Error = org.owasp.csrfguard.action.Error
  org.owasp.csrfguard.action.Error.Code = 403
  org.owasp.csrfguard.action.Rotate = org.owasp.csrfguard.action.Rotate
  org.owasp.csrfguard.action.Log = org.owasp.csrfguard.action.Log
  org.owasp.csrfguard.action.Log.Message = Potential CSRF (user:%user%, ip:%remote_ip%, method:%request_method%, uri:%request_uri%, error:%exception_message%)

  # Logging
  org.owasp.csrfguard.Logging = true
  org.owasp.csrfguard.LogLevel = INFO
  ```

* The last set of properties manages advanced CSRFGuard settings, including session token handling and configuration provider factory, affecting how CSRFGuard loads properties and manages session-bound tokens:

  ```properties
  # Other configurations
  org.owasp.csrfguard.configuration.provider.factory = org.owasp.csrfguard.config.overlay.ConfigurationAutodetectProviderFactory
  org.owasp.csrfguard.LogicalSessionExtractor = org.owasp.csrfguard.session.SessionTokenKeyExtractor
  ```

* Note that CSRFGuard settings may vary depending on the application's approach to handling user interactions.
  * In `Server-Side Rendering (SSR)` applications using traditional HTML forms, CSRF tokens must be embedded in form elements for submission with each request, requiring token injection to be enabled.
  * On the other hand, since `Single Page Applications (SPA)` primarily use AJAX requests, CSRF tokens are usually sent in request headers instead of HTML forms, leading to form token injection being typically disabled.

#### 4. Handle automatic CSRF token injection with `csrfguard.js` script

* Including the following JavaScript file in the frontend is required to enable automatic CSRF token management on the client side:

  ```html
  <script src="/csrfguard.js"></script>
  ```

* The `csrfguard.js` script ensures that every request from the browser includes a valid CSRF token by intercepting AJAX requests and modifying form submissions.
* It automatically adds the token as a request header for `XMLHttpRequest` and `fetch` API calls while injecting hidden fields into forms if enabled in the configuration.
* This mechanism protects both AJAX-based interactions and traditional form submissions.

## Exercise to practice :writing_hand:

* The application below is vulnerable to CSRF attacks, as there is no protection that prevents a malicious site forcing a logged-in user to send a request to change their email to any arbitrary address.
* To demonstrate this scenario, log in to the application with valid credentials (i.e., username `johndoe` and password `faBk;bhj7>QL`). Once logged in, check the current email address in the user's profile page, and then visit the attacker website tab in the simulated browser, which includes certain code that tries to change the user's email. Afterwards, confirm the email modification by reviewing the profile again.
* The purpose of this exercise is to edit the `csrfguard.properties` file using the code editor accessed via the `Open Code Editor` button to enforce CSRF protection while employing the synchronizer token pattern with the OWASP CSRFGuard library. The file is found at `src/main/webapp/WEB-INF/classes/csrfguard.properties`, and the configured properties should align with these required features:
  * The CSRF token should be named `X-CSRF-TOKEN` to maintain consistency across requests.
  * The `GET` HTTP method does not require CSRF protection, as it is only used for retrieving data without modifying the application state.
  * CSRF validation is unnecessary when no user session exists, ensuring efficient handling of unauthenticated requests.
  * All client-side interactions occur via AJAX requests.
  * To prevent unauthorized actions, any request that does not meet CSRF validation criteria must return a `403 Forbidden` response.
* It's important to note that since CSRFGuard depends on the `csrfguard.js` script to automatically append CSRF tokens to client-side requests, reloading the frontend web application on the browser after applying any configuration is required.
  * This ensures that any updates to the CSRFGuard settings, such as token injection rules or AJAX handling, take effect. Without a reload, the browser may continue using outdated configurations, potentially leading to failed CSRF validations or missing tokens in requests.

  @@ExerciseBox@@

[1]: https://github.com/OWASP/www-project-csrfguard
[2]: https://github.com/OWASP/www-project-csrfguard/blob/master/csrfguard-test/csrfguard-test-jsp/src/main/webapp/WEB-INF/classes/Owasp.CsrfGuard.properties
