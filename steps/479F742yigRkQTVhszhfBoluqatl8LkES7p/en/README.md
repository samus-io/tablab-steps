# Command injection

* `Command injection` is a type of vulnerability that allows an attacker to execute arbitrary commands on the host operating system via a vulnerable application.
* This occurs when the application passes unsafe user-supplied data to a system shell.

## How does Command injection works?

* **User input without proper sanitization**:

  * The application takes user input directly to construct a command.
  * **Example**: A web form for deleting a file might take the filename from user input.
  * Input: `file.txt; rm -rf /`
  * The application processes this input without sanitization.

* **Injected command alters expected flow**:

  * The system shell executes the command as it is received.
  * The command `rm -rf /` is executed with the same privileges as the application, leading to potential system-wide damage.
  * This causes the system to execute both `rm file.txt` and `rm -rf /`, leading to the deletion of the root directory.

## Visual representation of Command Injection

## What could be achieved with this vulnerability?

* **Remote Code Execution (RCE)**:
  * Attackers can execute arbitrary code on the target system.
  * **Example**: An attacker might run a command to download and execute malware.
  * Impact: Full control over the system, enabling further malicious activities such as installing backdoors, exfiltrating data, or launching additional attacks.

* **Data Exfiltration**:
  * Attackers can read sensitive data from the system.
  * **Example**: An attacker might read the contents of sensitive files, such as `/etc/passwd`.

* **Privilege Escalation**:
  * Attackers can escalate their privileges to gain higher-level access.
  * **Example**: Exploiting setuid binaries to execute commands as a superuser.

* **Denial of Service (DoS)**:
  * Attackers can disrupt the service by consuming resources or deleting critical files.
  * **Example**: Running commands that exhaust system resources.

## Argument Injection

* `Argument injection` is a vulnerability where untrusted input is improperly handled as part of command arguments.
* This allows attackers to manipulate command arguments, causing unintended command execution.

### How does Argument injection works?

* **Manipulation of Input Parameters**:
  * An attacker manipulates input that is used to build command-line arguments.
  * **Example**: A script for backup using filenames.

* **Injected Command Alters Behavior**:

  * Malicious input: `file.txt; rm -rf /`
  * The command executed becomes: `backup file.txt; rm -rf /`
  * This leads to unintended command execution and potential system compromise.

## Command Injection vs Argument Injection

* **Command Injection**:

* **Definition**: Allows attackers to execute arbitrary commands on the host operating system.
* **Focus**: Inserting and executing entire commands within an application.
* **Impact**: Full control over the system, leading to severe consequences like Remote Code Execution (RCE).

* **Argument Injection**:

* **Definition**: Allows attackers to manipulate command arguments to alter command behavior.
* **Focus**: Modifying arguments passed to commands rather than the commands themselves.
* **Impact**: Causes unintended command execution and can lead to data theft or system compromise.
