# Enforcing a custom error handler in Java Jakarta

* Error handling aims to ensure that unexpected or untreated errors are not leaked to the user under any circumstances, thereby protecting sensitive information.
* Proper error handling is essential in any backend application to ensure robustness, security, and long-term maintainability.
* Different techniques can be applied to handle errors depending on the architecture and scope of the application.

## Using basic try/catch blocks

* Encapsulating every route handler in a `try/catch` block provides a straightforward approach to error handling, allowing errors to be managed within the route itself.
* The following code sample demonstrates how `try/catch` is used to handle errors and return appropriate HTTP status codes based on the type of error:

  ```java
  @Override
  protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
      String userId = request.getParameter("userId");

      try {
          User user = fetchDatabase(userId); // Error thrown here

          response.getWriter().println("User profile:");
          response.getWriter().println("ID: " + user.getId());
          response.getWriter().println("Name: " + user.getName());
          
      } catch (ValidationException e) {
          response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
          response.getWriter().println("Invalid request data");

      } catch (NotFoundException e) {
          response.setStatus(HttpServletResponse.SC_NOT_FOUND);
          response.getWriter().println("Profile not found");

      } catch (Exception e) {
          response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
          response.getWriter().println("An unexpected error occurred");
      }
  }
  ```

* However, this method can quickly become repetitive and may result in missed caught exceptions, accidentally allowing some errors to go uncaught.
* Applying `try/catch` blocks across all routes causes redundancy and raises the chance of overlooking error handling, where a missed case could cause the application to crash. For this reason, it is only recommended in simple applications.

## Using a global error handler

* A global error handler enables centralized control over error management and ensures consistent processing of unhandled errors.
* The following example illustrates how a global error-handling filter captures and processes generated errors while returning a standardized response:

  ```java
  @WebFilter("/*")
  public class GlobalErrorHandlerFilter implements Filter {

      @Override
      public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
              throws IOException, ServletException {

          HttpServletResponse httpResponse = (HttpServletResponse) response;

          try {
              chain.doFilter(request, response);

          } catch (ValidationException e) {
            httpResponse.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            httpResponse.getWriter().println("Invalid request data");

          } catch (NotFoundException e) {
              httpResponse.setStatus(HttpServletResponse.SC_NOT_FOUND);
              httpResponse.getWriter().println("Profile not found");

          } catch (Exception e) {
              httpResponse.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
              httpResponse.getWriter().println("An unexpected error occurred");
          }
      }
  }
  ```

  * In this scenario, when an unhandled error arises, the `GlobalErrorHandlerFilter` filter automatically catches the errors, which helps prevent the exposure of sensitive information.
* Furthermore, basic `try/catch` blocks can be used alongside a global error handler, serving as a fallback for unhandled exceptions.

## Exercise to practice :writing_hand:

* The following web application includes a registration form that mishandles errors by exposing internal details to the user interface when a field does not meet the expected criteria.
* The goal of this exercise is to use the `Open Code Editor` button to modify the source code and create a proper custom error handler while satisfying the specified requirements:
  * As a representative example, when any field in the registration form is invalid, the application should always return an HTTP 400 status code response with the JSON content of `{"message":"Registration data is not correctly formatted."}`.
  * For any error unrelated to form validation, like a connection failure to the database, the application should return an HTTP 500 status code response with the JSON content of `{"message":"Internal Server Error"}`.
* To support this functionality, code changes are required in the `RegisterFormServlet.java` and `GlobalErrorHandlerFilter.java` files within the `src/main/java/io/ontablab/` directory.
* After making the changes, press the `Verify Completion` button to confirm the exercise has been completed.

  @@ExerciseBox@@
