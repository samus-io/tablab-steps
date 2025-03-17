# Information disclosure via directory listing in Apache 2.4

* Directory listing is a server feature that displays a list of all files and directories within a given directory in the absence of an index file (such as `index.html` or `index.php`).
* If enabled, directory listing can inadvertently expose sensitive files and data to unauthorized users, creating a significant security risk.
  * Attackers frequently rely on directory listing to map out the structure of a web application, identifying valuable files that may contain credentials, internal APIs, or vulnerabilities. This makes it a commonly exploited weakness in misconfigured web servers.
* The following image illustrates a web application that exposes its directory contents, making files publicly visible. If directory listing were properly disabled, this information would remain hidden from unauthorized users:

  ![Directory Listing Example][1]

## Disabling directory listing Apache

* To prevent unauthorized access to directory contents, Apache provides a simple way to disable directory listing. Add the following directive in the `.htaccess` file or server configuration:

  ```apacheconf
  Options -Indexes
  ```

* This setting ensures that when users try to access a directory without an index file, they receive a `403 Forbidden` error instead of a file listing, effectively protecting sensitive files from exposure.

[1]: /static/images/directory-listing-example.png