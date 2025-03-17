# Information disclosure via default files of software installation

* Default files left from software installations, such as WordPress installation files, can inadvertently provide attackers with useful information to identify the software version and exploit other vulnerabilities.
* These files, often overlooked, can reveal software versions, configuration settings, and operational practices, posing significant security risks.

## How information disclosure occurs?

* Default files often remain in the system after installation, and if not removed, they can be accessed directly through their URL. Attackers frequently scan for these files to gather insights about the application's configuration, versions, and potential vulnerabilities.
* Web servers with improper configurations may allow directory listing, making it easy for anyone to browse and locate sensitive files. If directory indexing is enabled, attackers can explore exposed folders, retrieve documentation, backups, or configuration files, and use this information to plan further attacks.
* Developers may overlook the security risks posed by default documentation, installation scripts, or log files. These files can contain database credentials, API keys, internal paths, or debugging information, which could be exploited by attackers to gain deeper access to the system.

## Common default files

|Filename|Description|
|:--:|:--:|
|`README.md`|Offers detailed descriptions of the software, including how to configure or use it, which might include sensitive hints.|
|`INSTALL.md`|Provides installation steps, which may reveal system paths, dependencies, or security recommendations.|
|`CHANGELOG.txt`|Lists software updates, including fixed vulnerabilities that attackers can exploit in older versions.|
|`phpinfo.php`|Displays detailed PHP environment information, including loaded modules, file paths, and configuration settings.|
|`install.php`|Used for initial setup; if left exposed, attackers might be able to reinitialize the application or extract database credentials.|
|`setup.php`|Similar to `install.php`, it may allow an attacker to reconfigure the application or gain sensitive information.|
|`/server-status`|Provides real-time information about the web server, including active connections, request details, and system paths.|
|`/server-info`|Displays detailed configuration settings of the Apache server, revealing software versions and modules.|
|`/manual/`|Default Apache manual directory, potentially revealing server details and module documentation.|
|`/docs/`|Often contains software documentation, which may expose internal workings or unpatched vulnerabilities.|
|`/iisstart.htm`|Default IIS startup page, indicating an unconfigured or exposed Microsoft IIS server.|

### Prevention techniques

* After installing software, carefully **review and remove unnecessary files** to minimize potential information disclosure. Default installation files such as documentation, configuration samples, and outdated scripts can reveal sensitive details about the system, software version, or internal structure, making them a target for attackers.
* If deleting these files is not an option, **restrict file permissions** to prevent unauthorized access. By limiting read, write, or execute permissions, sensitive files remain inaccessible through web requests, ensuring that only authorized users or processes can interact with them.
  * In Linux, file permissions can be adjusted to restrict public access, allowing only the file owner to read, write, or execute the file while preventing access from other users or services:

    ```bash
    chmod 700 README.md
    ```
  
  * On Windows, access control lists (ACLs) provide a method to remove read permissions, preventing unauthorized users from viewing sensitive files. This can be done using `powershell.exe` or `cmd.exe` to modify file access rules:

    ```powershell
    icacls "C:\inetpub\wwwroot\README.md" /remove:g "Authenticated Users":R
    ```

* By implementing these security measures, default installation files can be effectively managed, reducing the risk of information disclosure and unauthorized access.
