# Vulnerability examples

* Here are some examples of insecure code snippets illustrating these vulnerabilities, with different functions and libraries.

## Command Injection examples

* **Executing a command with user input using `exec`**

  ```javascript
  const { exec } = require('child_process');
  const userInput = '8.8.8.8'; // Assume this comes directly from user input
  exec(`ping ${userInput}`, (err, stdout, stderr) => {
    if (err) {
      console.error(`Error: ${err.message}`);
      return;
    }
    console.log(`Ping output: ${stdout}`);
  });
  ```

  * **Vulnerability**
    * The exec function in Node.js spawns a shell and then executes the specified command string within that shell environment.
    * This makes it highly vulnerable to command injection attacks if the command string includes untrusted user input without proper validation or escaping.
    * In this example, if the `userInput` parameter is directly appended to the command string, an attacker can inject additional commands that the shell will execute.
    * For example, an attacker could submit `8.8.8.8; rm -rf /`, which translates to `ping 8.8.8.8; rm -rf /` when executed by the shell. This would not only ping the specified IP address but also delete all files from the root directory (rm -rf /), potentially destroying the system.
    * This attack is possible because the shell interprets the semicolon (`;`) as a command separator, allowing multiple commands to be executed in sequence.

* **Listing directory contents with user input using `spawn`**

  ```javascript
  const { spawn } = require('child_process');
  const dir = '/user/files'; // Assume this comes from user input
  const ls = spawn('ls', [dir]);

  ls.stdout.on('data', (data) => {
    console.log(`Directory listing: ${data}`);
  });

  ls.stderr.on('data', (data) => {
    console.error(`Error: ${data}`);
  });
  ```

  * **Vulnerability**
    * The `spawn` function in Node.js creates a new process and runs the specified command with the given arguments.
    * Unlike `exec`, it does not spawn a shell, which reduces the risk of command injection but does not eliminate it entirely.
    * If `dir` (directory path) is directly taken from user input without validation, it can be exploited by an attacker to pass malicious arguments.
    * For example, if the user input is `; rm -rf /`, the command executed becomes `ls ; rm -rf /`.
    * While spawn does not directly execute this in a shell, it can still be used to pass unexpected inputs, which might lead to unintended command execution in certain contexts.
    * This highlights the importance of validating and sanitizing user inputs even when using functions like spawn, which are generally considered safer than exec.

* **Running a script with user input using `execFile`**

  ```javascript
  const { execFile } = require('child_process');
  const script = 'myscript.sh'; // Assume this comes from user input
  execFile(script, ['arg1'], (err, stdout, stderr) => {
    if (err) {
      console.error(`Error: ${err.message}`);
      return;
    }
    console.log(`Script output: ${stdout}`);
  });
  ```

  * **Vulnerability**
    * The `execFile` function is similar to exec, but it is generally considered safer because it does not spawn a shell.
    * It directly executes a file (like a script) with the specified arguments.
    * However, if user input is used to determine which script to execute (as in the `script` variable), an attacker could exploit this by supplying a malicious script name.
    * For example, if the attacker replaces `myscript.sh` with a script they control, they could execute arbitrary code.
    * This scenario is particularly dangerous in environments where users might have the ability to upload files or otherwise control file paths, leading to the execution of unintended or malicious scripts.

## Argument Injection examples

* **Downloading a file using `spawn` with curl:**

  ```javascript
  const { spawn } = require('child_process');
  const validatedUserInput = '--output downloaded.txt'; // Assume this comes from user input
  const curl = spawn('curl', [validatedUserInput, 'https://example.com']);

  curl.stdout.on('data', (data) => {
    console.log(`Output: ${data}`);
  });

  curl.stderr.on('data', (data) => {
    console.error(`Error: ${data}`);
  });
  ```

  * **Vulnerability**
    * In this example, `validatedUserInput` is used as an argument for the `curl` command.
    * If this input is not properly validated, an attacker could use it to manipulate the output of the command in unintended ways.
    * For example, if the attacker sets `validatedUserInput` to `--output /etc/passwd`, the curl command would write the downloaded file to `/etc/passwd`, potentially overwriting a critical system file that contains user account information.
    * This could lead to a system compromise.
    * This type of injection is particularly dangerous because it can allow attackers to manipulate file paths and overwrite important files, leading to privilege escalation or denial of service.

* **Encrypting a file with `openssl`**

  ```javascript
  const { exec } = require('child_process');
  const validatedUserInput = 'inputFile.txt'; // Assume this comes from user input and is validated
  exec(`openssl enc -aes-256-cbc -in ${validatedUserInput} -out encryptedFile.enc`, (err, stdout, stderr) => {
    if (err) {
      console.error(`Error: ${err.message}`);
      return;
    }
    console.log(`File encrypted: ${stdout}`);
  });
  ```

  * **Vulnerability**
    * Here, the `exec` function is used to run an `OpenSSL` command to encrypt a file.
    * However, if the validatedUserInput (which is supposed to be the input file name) is manipulated by an attacker, it can lead to serious security issues.
    * For example, if validatedUserInput is set to `-K 0123456789abcdef0123456789abcdef -iv 0123456789abcdef`, the OpenSSL command would use these as encryption keys, potentially compromising the encryption process.
    * An attacker could manipulate the encryption parameters to weaken the encryption or to use keys they already know, making the encrypted file vulnerable to decryption.
    * This example demonstrates the importance of thoroughly validating and sanitizing inputs that are used as arguments in security-critical commands.

* **Compressing files with user input using execFile with `tar`**

  ```javascript
  const { execFile } = require('child_process');
  const files = 'myFiles'; // Assume this comes from user input
  execFile('tar', ['-cvf', 'archive.tar', files], (err, stdout, stderr) => {
    if (err) {
      console.error(`Error: ${err.message}`);
      return;
    }
    console.log(`Archive created: ${stdout}`);
  });
  ```

  * **Vulnerability**
    * In this case, the `execFile` function is used to run the `tar` command to create an archive of files.
    * If the `files` variable is directly taken from user input, it could lead to dangerous consequences if the input is not validated.
    * For example, if the attacker sets files to `--directory=/`, the tar command could end up archiving the entire root directory, or if `files` is set to `; rm -rf /`, it could lead to the deletion of all files on the system.
    * While `execFile` doesn’t directly execute shell commands, misuse or incorrect inputs can still lead to severe security breaches.
    * This example underlines the importance of proper input validation and sanitization when dealing with file paths and command arguments, as even non-shell commands can be exploited if given improper input.
