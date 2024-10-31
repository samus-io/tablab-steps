# What is the Path Traversal?

* Path Traversal, also known as Directory Traversal, is a critical server-side vulnerability that allows an attacker to access arbitrary files on the server.
* This vulnerability results from insecure handling of user input used to reference paths to files stored on the server. By manipulating this input, an attacker could include files that are not intended by the application.
* It is common for web applications to use parameters to reference files, such as images, and then to include those images in the web page. However, if the web application does not properly validate these inputs, it could be exploited to access sensitive files.

## Impact of Path Traversal

* **Read system files**: Such as `/etc/passwd` on Linux, or critical configuration files on Windows that contain a list of local system users or sensitive configuration information.
* **Read source code**: Allows the attacker to understand and potentially exploit Web application logic.
* **Remote command execution**: Under certain circumstances, depending on server configuration and other security factors.
* **Internal port and service enumeration**: Reveals information about internal services and possibly infrastructure that is not directly exposed to the Internet.
* **Linux/Windows server and kernel version detection**: Facilitates the identification of vulnerable or outdated systems.
