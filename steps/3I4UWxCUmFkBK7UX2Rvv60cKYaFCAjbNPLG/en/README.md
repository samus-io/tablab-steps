# File system permissions

* On Unix-based systems, we can use `fs.chmod` function programmatically or `chmod` command to set the files/folders permissions. Its first argument accepts an octal number of the following format:

  ```bash
  Syntax: 0oOGP

  O: number representing the permission for owner.
  G: number representing the permission for group.
  P: number representing permission for other users.

  Every number is bad of 3 bits. First bit is readable, second bit is writable, third bit is executable.
  ```

  ```javascript
  fs.chmod(<filepath>, <permission in octal or hex>, callback )
  ```

  ```bash
  chmod [options] [mode] [file_name] 

  options: Optional flags that modify the behavior of the chmod command.
  mode: The permissions to be set, represented by a three-digit octal number or symbolic notation.
  file_name: The name of the file or directory for which the permissions are to be changed.
  ```

* On windows, the below are the following ways to set permissions:
* Using File Explorer
  * Navigate to the file or folder, right-click it, and select **Properties**.
  * In the properties window, go to the **Security** tab.
  * Click the **Edit** button to change permissions. Select a user or group from the list. Check or uncheck permissions (Full control, Modify, Read & execute, etc.). Click **Apply** and then **OK**.
* Using Command Prompt (icacls)
  * Search for **cmd** in the Start menu, right-click it, and select **Run as administrator**.
  * Use `icacls` Command:

    ```bash
    Syntax: icacls "C:\path\to\file.txt" /grant username:(permission)
    Example: icacls "C:\path\to\file.txt" /grant Everyone:(R)

    Possible permissions are R: Read, W: Write, M: Modify, X: Execute and all combinations of RWMX.
    ```

* Using `Set-Acl` Cmdlet in powershell. For example:

    ```bash
    // Use Get-Acl to get the current Access Control List (ACL) of the file
    $acl = Get-Acl "C:\path\to\file.txt"

    // Specify the user, permission type, and allow/deny
    $permission = "DOMAIN\User","Read,Write","Allow"

    // Create a new access rule object
    $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission

    // Add the new rule to the ACL
    $acl.SetAccessRule($accessRule)

    // Use Set-Acl to apply the modified ACL to the file
    Set-Acl "C:\path\to\file.txt" $acl
    ```
