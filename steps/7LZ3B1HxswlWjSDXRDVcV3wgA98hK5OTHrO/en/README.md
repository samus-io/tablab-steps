# Information disclosure via backup files

* Information disclosure via backup files occurs when backup files containing sensitive data are unintentionally exposed on web applications without proper access controls.
* These files may be generated automatically by backup systems or manually created by developers and administrators.
* Common file extensions for backups include `.bak`, `.zip`, `.tar`, `.old`, among others, which attackers may specifically look for.
* Backup files are often stored in predictable locations such as `/backup` directories, increasing the risk of unauthorized access.
* If exposed, these files may contain sensitive information like database credentials, configuration details, or source code, making them a valuable target for attackers.

## Impact of information disclosure via backup archives

* Exposing backup files unintentionally can lead to serious security risks, including the loss of confidentiality of sensitive data and privacy violations.
* In certain cases, unauthorized access to backup archives may result in non-compliance with data protection regulations, exposing organizations to legal and financial penalties.
* If an attacker gains access to a backup file, they can analyze its contents, such as source code or credentials, to identify and exploit additional vulnerabilities.
  * Backup archives may contain configuration details, database records, or authentication keys, which can be leveraged to compromise systems further.

## Recommendations

* Reducing the risks of data leakage from backup files requires implementing the following key security practices:
  * **Storing backups on dedicated servers** helps prevent accidental exposure by keeping them on internal systems that are not accessible from the internet.
  * **Managing access permissions** carefully minimizes risks by enforcing the principle of least privilege, ensuring that only authorized users can access backup files.
  * **Encrypting backups** ensures that even if unauthorized individuals gain access, the data remains protected and unreadable.
* Implementing these practices strengthens data security and reduces the likelihood of sensitive information being disclosed through backup archives.

## Finding exposed backups

* Identifying and managing backup files is essential to prevent unintended exposure of sensitive data.
* If the existence of backup files on the server is uncertain, specific commands can help locate them:
  * On Linux, searching within the root of the web directory can be done using the `find` command:

    ```bash
    find . -type f -regex ".*\.\(bak\|txt\|src\|dev\|old\|inc\|orig\|copy\|tmp\)$"
    ```

  * On Windows, the `cmd` command can scan for common backup file extensions:

    ```cmd
    dir *.bak *.txt *.src *.dev *.old *.inc *.orig *.copy *.tmp /s /b
    ```

  * `PowerShell` provides an alternative method for identifying backup files across directories:

    ```powershell
    Get-ChildItem -Recurse -File | Where-Object { $_.Name -match "\.(bak|txt|src|dev|old|inc|orig|copy|tmp)$" }
    ```

* Regularly scanning for these files helps in detecting unprotected backups and taking necessary actions to secure them.
