# Information disclosure via default files of software installation

* Files left over from software installations, such as those from web servers or CMS platforms like WordPress, can inadvertently offer attackers information to determine software version details and exploit known vulnerabilities.
* These files, often overlooked, can reveal software versions, configuration settings, and operational practices, posing significant security risks.

## Potential threats arising from software installation files

* Default files often remain in the system after installation, and if not removed, they can be accessed directly through their URL. Attackers frequently scan for these files to gather insights about the application's configuration, versions, and potential vulnerabilities.
* Security risks from these default documentation, installation scripts, or log files may be disregarded, even though they can contain internal paths, debugging information, or database credentials and API keys that attackers could exploit to gain deeper access to the system.
* Web servers with improper configurations may allow directory listing, making it easy for anyone to browse and locate sensitive files. If directory indexing is enabled, malicious users can explore exposed folders, retrieve documentation, backups, or configuration files, and use this information to plan further attacks.

## Common default files

|Filename|Description|
|:--:|:--:|
|`README.md`|Offers detailed descriptions of the software itself, including how to configure or use it, which might include sensitive hints.|
|`INSTALL.md`|Provides installation steps, which may reveal system paths, dependencies, or security recommendations.|
|`CHANGELOG.txt`|Lists software updates, including fixed vulnerabilities that attackers can exploit in older versions.|
|`phpinfo.php`|Displays detailed PHP environment information, including loaded modules, file paths, and configuration settings.|
|`install.php`|Used for initial setup; if left exposed, attackers might be able to reinitialize the application or extract database credentials.|
|`setup.php`|Similar to `install.php`, it may allow a malicious user to reconfigure the application or gain sensitive information.|
|`/server-status`|Provides real-time information about the web server, including active connections, request details, and system paths.|
|`/server-info`|Displays detailed configuration settings of the Apache server, revealing software versions and modules.|
|`/manual/`|Default Apache manual directory, potentially revealing server details and module documentation.|
|`/docs/`|Often contains software documentation, which may expose internal workings or unpatched vulnerabilities.|
|`/iisstart.htm`|Default IIS startup page, indicating an unconfigured or exposed Microsoft IIS server.|

## Recommended security approaches

* After installing software, carefully **review and remove unnecessary files** to minimize potential information disclosure. Default installation files such as documentation, configuration samples, and outdated scripts can reveal sensitive details about the system, software version, or internal structure, making them a target for attackers.
* If deletion of these files is not feasible, **restrict access through the web server configuration** to prevent exposure via HTTP requests. This limits public access while retaining the files on the server or container for internal use:

  @@TagStart@@apache

  * In Apache, access can be denied using the `.htaccess` file:

    ```plaintext
    <FilesMatch "^(README\.md|INSTALL\.md|CHANGELOG\.txt|phpinfo\.php)$">
        Require all denied
    </FilesMatch>
    ```

  @@TagEnd@@

  @@TagStart@@nginx

  * In Nginx, access restrictions can be enforced using `location` blocks:

    ```nginx
    location ~* /(README\.md|INSTALL\.md|CHANGELOG\.txt|phpinfo\.php)$ {
        deny all;
    }
    ```

  @@TagEnd@@

  @@TagStart@@iis

  * In IIS, access can be restricted by modifying the `web.config` file:

    ```xml
    <configuration>
      <system.webServer>
        <security>
          <requestFiltering>
            <fileExtensions>
              <add fileExtension=".md" allowed="false" />
              <add fileExtension=".txt" allowed="false" />
              <add fileExtension=".php" allowed="false" />
            </fileExtensions>
            <hiddenSegments>
              <add segment="README.md" />
              <add segment="INSTALL.md" />
              <add segment="CHANGELOG.txt" />
              <add segment="phpinfo.php" />
            </hiddenSegments>
          </requestFiltering>
        </security>
      </system.webServer>
    </configuration>
    ```

  @@TagEnd@@

* **Disable directory listing** to prevent unauthorized users from browsing the contents of directories. This avoids exposure of sensitive files not meant to be publicly accessible:

  @@TagStart@@apache

  * In Apache, edit the `httpd.conf` or `.htaccess` file:

    ```plaintext
    Options -Indexes
    ```

  @@TagEnd@@

  @@TagStart@@nginx

  * In Nginx, update the `nginx.conf` or site-specific configuration file:

    ```plaintext
    location / {
        autoindex off;
    }
    ```

  @@TagEnd@@

  @@TagStart@@iis

  * In IIS, modify the `web.config` file:
  
    ```xml
    <configuration>
      <system.webServer>
        <directoryBrowse enabled="false" />
      </system.webServer>
    </configuration>
    ```
  
  @@TagEnd@@

* Additionally, **use automated scanning tools** such as Nikto, Dirb, or OWASP ZAP to identify accessible default files and misconfigurations before malicious users do.
* By implementing these security measures, default installation files can be effectively managed, reducing the risk of information disclosure and unauthorized access.
