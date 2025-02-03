# Preventing CSRF using synchronizer token pattern in Jakarta EE 10 with OWASP CSRFGuard

## How synchronizer token pattern works

* When implementing CSRF tokens must adhere to the following security principles:
    * Nonce (number used once).
    * Unpredictable.
    * Session-tied.
    * Strictly validated.
* A unique CSRF token must be generated for each session and stored securely in the server-side session. The following method demonstrates how to generate and store the token:

    ```java
    public void setCSRFToken(HttpServletRequest request) {
        // Generate a cryptographically secure token
        String token = UUID.randomUUID().toString();
        request.getSession(true).setAttribute(CSRF_SESSION_KEY, token);
    }
    ```

* This token will later be used to validate incoming requests and confirm that they originate from a legitimate user.
* For CSRF protection to be effective, the generated token must be embedded in the frontend. This ensures that subsequent `POST`, `PUT`, or `DELETE` requests can include the token for server-side validation.
* One way to achieve this is by generating the CSRF token in the server-side logic and embedding it within the response, such as in a `JSP` page:

    ```java
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // Generate and store the CSRF token in the session
        setCSRFToken(request);
        request.getRequestDispatcher("/WEB-INF/views/pages/csrf-protected.jsp").forward(request, response);
    }
    ```

* Before processing state-changing requests, the server must retrieve the session-stored CSRF token and compare it to the token submitted by the client. The following method retrieves and removes the token from the session for validation:

    ```java
    public String getCSRFToken(HttpServletRequest request) {
        HttpSession session = request.getSession(false);

        if (session != null) {
            Object csrfSession = session.getAttribute(CSRF_SESSION_KEY);

            if (csrfSession instanceof String) {
                // Remove token after retrieval (one-time use)
                session.removeAttribute(CSRF_SESSION_KEY);
                return (String) csrfSession;
            }
        }
        return null;
    }
    ```

* When handling state-changing requests, the server must validate the CSRF token. If the token is missing or invalid, the request must be rejected to prevent CSRF attacks:

    ```java
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String clientCsrfToken = request.getParameter("csrf-token");

        // Retrieve the CSRF token stored in the session
        String sessionCsrfToken = getCSRFToken(request);

        if (sessionCsrfToken == null || !sessionCsrfToken.equals(clientCsrfToken)){
            System.out.println("Invalid CSRF Token");
            return;
        }

        System.out.println("Valid CSRF Token");
    }
    ```

## OWASP CSRFGuard

* The [OWASP CSRFGuard][1] library is a security framework designed to protect Java EE web applications against Cross-Site Request Forgery (CSRF) attacks.
* It achieves this by implementing a variant of the synchronizer token pattern, which ensures that every state-changing HTTP request includes a unique and valid CSRF token.
* This mechanism prevents unauthorized actions from being executed on behalf of an authenticated user.

### How OWASP CSRFGuard Works

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
* The following are some common properties used to define the behaviour of CSRFGuard:

|Property|Description|
|:--:|:--:|
|`org.owasp.csrfguard.Enabled`|Determines whether CSRFGuard is active (`true` or `false`).|
|`org.owasp.csrfguard.TokenName`|Specifies the name of the CSRF token parameter included in requests. The default value is `OWASP-CSRFTOKEN`.|
|`org.owasp.csrfguard.Rotate`|Defines whether the CSRF token should be regenerated after each successful validation. However, this functionality generally causes navigation problems in applications, specifically, the `Back` button in the browser will often cease to function properly.|
|`org.owasp.csrfguard.UnprotectedMethods`|Lists HTTP methods that should be excluded from CSRF protection (e.g., `GET`, `OPTIONS`, etc.).|
|`org.owasp.csrfguard.ValidateWhenNoSessionExists`|Determines whether CSRFGuard should enforce token validation even when no session exists. Only set this to false if the web application is not susceptible to CSRF if the user has no session.|
|`org.owasp.csrfguard.Ajax`|Enables CSRF protection for AJAX requests automatically including the CSRF token in all requests.|
|`org.owasp.csrfguard.JavascriptServlet.injectIntoForms`|Defines whether CSRF tokens should be injected as hidden fields into HTML forms.|
|`org.owasp.csrfguard.JavascriptServlet.injectGetForms`|Determines whether CSRF tokens should be injected into forms that use the `GET` method. Developers who ensure that their server-side controllers handle state-changing actions exclusively via POST requests should disable this property.|
|`org.owasp.csrfguard.JavascriptServlet.injectFormAttributes`|Specifies whether CSRF tokens should be injected into the `action` attribute of forms.|
|`org.owasp.csrfguard.JavascriptServlet.injectIntoAttributes`|Defines whether CSRF tokens should be injected into `src` and `href` attributes of HTML elements. If server-side controllers handle state-changing actions exclusively via POST requests, then its recommended to disable this property.|
|`org.owasp.csrfguard.JavascriptServlet.injectIntoDynamicNodes`|Enables automatic injection of CSRF tokens into dynamically created HTML elements. If set to `true`, a `MutationObserver` monitors the DOM and injects tokens when necessary. |
|`org.owasp.csrfguard.action.Error`|Configures an action to return an error when a CSRF violation occurs. This can be used to block the request and respond with an error message.|
|`org.owasp.csrfguard.action.Code`|Specifies the HTTP status code to return when a CSRF violation occurs (e.g., 403, 401, etc).|
|`org.owasp.csrfguard.action.Rotate`||
|`org.owasp.csrfguard.action.Log`|When enabled, details about the violation are logged. The default behavior is `true`.|
|`org.owasp.csrfguard.action.Log.Message`|Defines the log message format for CSRF violation attempts. Variables such as `%user%`, `%request_uri%`, and `%remote_ip%` can be used. |
|`org.owasp.csrfguard.Logging`|Enables or disables logging of CSRFGuard activities, including violations. The default value is `true`.|
|`org.owasp.csrfguard.LogLevel`|Specifies the logging level for CSRFGuard messages. The possible values are `DEBUG`, `INFO`, `WARN` and `ERROR`. |
|`org.owasp.csrfguard.configuration.provider.factory`|Defines the configuration provider that CSRFGuard should use to load properties.|
|`org.owasp.csrfguard.LogicalSessionExtractor`|Determines how CSRFGuard identifies a user’s session. Defaults to `org.owasp.csrfguard.session.SessionTokenKeyExtractor`, which relies on `HttpSession`. Custom implementations can be used for stateless architectures.|

* The definition of all properties and an extended explanation can be found in [Owasp.CsrfGuard.properties][2].

### Implementing CSRFGuard

* To successfully implement OWASP CSRFGuard, the following components must be properly configured:
    * Necessary dependencies must be added to `pom.xml` to integrate CSRFGuard into the application.
    * The `web.xml` file needs to be configured to register the CSRFGuard filter, servlet, and listeners for request validation.
    * The `csrfguard.properties` file contains essential settings that define token behavior, logging, and protection mechanisms.
    * The `csrfguard.js` script must be included on the frontend to automatically inject and validate CSRF tokens in form submissions and AJAX requests.

#### Dependencies

* To integrate OWASP CSRFGuard into a JavaEE application, the necessary dependencies must be included in the `pom.xml` file.
* These dependencies provide the core CSRF protection functionalities, session-based token management, and JSP tag support for CSRF token injection:
  
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

#### Define filters and listeners

* To enable OWASP CSRFGuard in a JavaEE application, JavaEE Filters and listeners must be configured in the `web.xml` file.
* These components ensure that every HTTP request is validated against a CSRF token and that the necessary JavaScript functionality is injected into the application:
  
  ```xml
  <!-- CSRFGuard Filter-->
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

#### CSRFGuard properties

* The CSRFGuard behavior must be defined in the `csrfguard.properties` file. This configuration file allows fine-grained control over how CSRF protection is applied within an application.
* This section enables CSRFGuard, defines the name of the CSRF token, and configures how tokens behave across requests. It also specifies which HTTP methods are exempt from protection and whether CSRF validation should apply when no session exists:

    ```properties
    # If CSRFGuard filter is enabled
    org.owasp.csrfguard.Enabled = true

    # Token name
    org.owasp.csrfguard.TokenName = X-CSRF-TOKEN

    # Token rotation on every request
    org.owasp.csrfguard.Rotate = false

    # Unprotected methods
    org.owasp.csrfguard.UnprotectedMethods = GET

    ## Only set this to false if the web application is not susceptible to CSRF if the user has no session
    org.owasp.csrfguard.ValidateWhenNoSessionExists = true

    # Ajax and XMLHttpRequest support
    org.owasp.csrfguard.Ajax = false
    ```

* This part defines how CSRF tokens are injected into forms and requests through CSRFGuard's JavaScript handler. It allows CSRFGuard to modify form submissions and dynamic content to include the necessary security tokens automatically:

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

* These properties defines how CSRF violations are managed, including logging and response codes. When a request fails CSRF validation, CSRFGuard can log the event, return an error response, or take other actions. Additionally, logging configurations determine the level of detail stored in logs:

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

* The following properties controls advanced CSRFGuard settings, such as the configuration provider factory and session token management. These settings affect how CSRFGuard loads its properties and manages session-bound tokens:

    ```properties
    # Other configuration
    org.owasp.csrfguard.configuration.provider.factory = org.owasp.csrfguard.config.overlay.ConfigurationAutodetectProviderFactory
    org.owasp.csrfguard.LogicalSessionExtractor = org.owasp.csrfguard.session.SessionTokenKeyExtractor
    ```

* The configuration of CSRFGuard may vary depending on how the application handles user interactions.
* For Single Page Applications (SPA), which rely primarily on AJAX requests, CSRF tokens are usually sent in request headers rather than being injected into HTML forms.
* Therefore, form token injection is typically disabled, and dynamic DOM elements may require special handling to ensure proper token propagation.
* For Multi-Page Applications (MPA), where interactions are handled through traditional HTML forms, CSRF tokens must be injected into form elements to be submitted with each request. This requires enabling token injection for forms.

#### Automatic CSRF token handling with `csrfguard.js`

* To enable automatic CSRF token handling on the client side, the following JavaScript file must be included in the frontend:

```html
<script src="/csrfguard.js"></script>
```

* The `csrfguard.js` script ensures that every request from the browser includes a valid CSRF token by intercepting AJAX requests and modifying form submissions.
* It automatically adds the token as a request header for `XMLHttpRequest` and `fetch` API calls while injecting hidden fields into forms if enabled in the configuration.
* This mechanism protects both AJAX-based interactions and traditional form submissions.

## Exercise to practice :writing_hand:

* The application below is vulnerable to CSRF attacks, as there is no protection that prevents a malicious site forcing a logged-in user to send a request to change their email to any arbitrary address.
* To demonstrate this scenario, log in to the application with valid credentials (i.e., username `johndoe` and password `faBk;bhj7>QL`). Once logged in, check the current email address in the user's profile page, and then visit the attacker website tab in the simulated browser, which includes certain code that tries to change the user's email. Afterwards, confirm the email modification by reviewing the profile again.
* The purpose of this exercise is to edit the source code using the `Open Code Editor` button to implement a CSRF protection based on the synchronizer token pattern via the OWASP CSRFGuard library.
* In order to complete the exercise, the file located in `src/main/webapp/WEB-INF/classes/csrfguard.properties` is where code modifications should be added to support these features.
* The web application is a Single Page Application (SPA) with the following security requirements:
    * The CSRF token should be named `X-CSRF-TOKEN` to maintain consistency across requests.
    * The `GET` method does not require CSRF protection, as it is only used for retrieving data without modifying the application state.
    * CSRF validation is unnecessary when no user session exists, ensuring efficient handling of unauthenticated requests.
    * All client-side interactions occur via AJAX requests.
    * Any request failing CSRF validation must result in an immediate `403 Forbidden` response to prevent unauthorized actions.
* Since CSRFGuard relies on a JavaScript library (`csrfguard.js`) to automatically append CSRF tokens to frontend requests, it is essential to reload the browser after modifying the configuration.
* This ensures that any updates to the CSRFGuard settings, such as token injection rules or AJAX handling, take effect. Without a reload, the browser may continue using outdated configurations, potentially leading to failed CSRF validations or missing tokens in requests.

  @@ExerciseBox@@

[1]: https://github.com/OWASP/www-project-csrfguard
[2]: https://github.com/OWASP/www-project-csrfguard/blob/master/csrfguard-test/csrfguard-test-jsp/src/main/webapp/WEB-INF/classes/Owasp.CsrfGuard.properties
