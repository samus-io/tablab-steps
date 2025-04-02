# Information disclosure via directory listing in Apache 2.4

* A directory listing is a web server feature that displays the contents of a directory (files and subdirectories) when a user requests a directory that doesn't have a default page, such as `index.html` or `index.php`.
* If enabled, directory listing can inadvertently expose sensitive files and data to unauthorized users, creating a significant security risk.
  * Malicious users frequently rely on directory listing to map a web application's structure and locate files that may hold credentials, internal APIs, or vulnerabilities, making it a frequently exploited flaw in misconfigured web servers.
* The following image illustrates a web application that exposes its directory contents, revealing a specific file to the public. If directory listing was properly disabled, this information would remain hidden from unauthorized users:

  ![Directory listing example][1]

## Disabling directory listing in Apache

* Apache offers a straightforward method to disable directory listing and prevent unauthorized access to directory contents. This can be done by adding the following directive to the `.htaccess` file or server configuration:

  ```apache
  Options -Indexes
  ```

* This setting ensures that users accessing a directory without an index file, such as `index.html` or `index.php`, receive a `403 Forbidden` error instead of a file listing, thereby protecting existing files from exposure.

[1]: /static/images/directory-listing-example.png
