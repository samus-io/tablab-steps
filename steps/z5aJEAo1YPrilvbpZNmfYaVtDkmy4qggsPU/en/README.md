# Preventing Open Redirect

* First and foremost strategy is to avoid redirect. If redirect is necessary then follow the below security measures:
  * **Avoid redirection based on user-controlled data**: remove the redirection function from the application and replace links with direct links to relevant target URLs whenever possible.

  * **Maintain server-side whitelists**: maintain a server-side list of permitted URLs for redirection. Use a short name, ID, or token mapped to a full target URL to avoid passing user-controllable data as a parameter.

* Be cautious to avoid introducing enumeration vulnerabilities where users could cycle through IDs to find all possible redirect targets.

## For user-controllable input URLs

* If the redirection function must unavoidably accept user-controllable input, the following security measures should be implemented.

### Validate Redirect URLs

* Use strict validation to ensure that the received URL is safe and legitimate before issuing a redirect.
* Regular expressions can be useful for setting up and enforcing security measures, especially for URL validation and filtering.
* Check if the URL is one among the below two options:
  * **URLs Relative to the web root**: redirects should use URLs relative to the web root whenever possible. The redirection function should validate that the received URL starts with a slash character (`/`) to ensure it's relative to the web root. Before issuing the redirect, prepend `http://domain.tbl` to the URL.
  * **Absolute URLs with domain validation**: if absolute URLs are necessary, ensure they start with required domain name like `http://domain.tbl/`. The redirection function should verify that the user-supplied URL begins with genuine domain before issuing the redirect. If multiple domains are allowed, create a whitelist to restrict redirection to trusted domains.

* Be cautious of allowing domains that provide URL shortening services (e.g., `bit.ly`, `tinyurl.com`). These services can obfuscate the final destination, making it difficult to validate the target URL's authenticity and safety. Avoid redirecting to URLs from such domains.

### Canonicalize URLs

* Normalize and canonicalize the path or URL before using it to mitigate variations and potential vulnerabilities.
* Use functions or methods to ensure URLs are properly formatted and validated.

### User confirmation page

* Implement a user confirmation page for all redirects, displaying the destination URL clearly and requiring users to confirm before proceeding.
* Irrespective of the implemented security measures, a prudent strategy involves directing all redirects through an intermediary page. This page serves to notify users that they are leaving the current site, displaying the destination clearly. Users must then click a link to confirm their intention to proceed.
* An example of this behavior can be experienced by adding `https://www.google.com/url?q=https://domain.tbl` to browser's address bar.
