# Exploiting Path Traversal

* The most common technique used to exploit this vulnerability uses the sequence `../` on Unix/Linux-based systems or `..\` on Windows systems. This technique attempts to "move up" in the directory hierarchy to access files or directories outside the permitted scope.
* The next web application allows users to view images via a parameter in the URL:

  ```
  https://example.tbl/getFile?img=image1.png
  ```

* An attacker could modify the `img` parameter to attempt to access files outside the specified directory.

## Exploiting Path Traversal in Linux servers

* To read the `/etc/passwd` file, which contains critical information about system users, the attacker could manipulate the URL as follows:

  ```
  https://example.tbl/getFile?img=../../../../etc/passwd
  ```

* In this image you can see exactly how the Path Traversal works on Linux servers:

![Path Traversal Example][1]

* First, the attacker makes the request to `http://abc.com/?file=../../../etc/passwd`. When the server receives the request, it interprets what file it is trying to read and accesses previous directories until it reaches the root directory. Once there, it searches for the `etc` directory and accesses the `passwd` file.

## Exploiting Path Traversal in Windows servers

* In Windows environments, the attack is adapted by using different path sequences (`...\`) to navigate the file system. A classic example would be an attempt to access the `web.config` configuration file of an ASP.NET application, which may contain sensitive information such as database access credentials:

  ```
  https://example.tbl/getFile?img=..\..\..\..\web.config
  ```

* On Windows, the attacker could also attempt to access critical system files or directories using absolute or relative paths to obtain sensitive information or to manipulate the behavior of the application.

## Advanced techniques

* In addition to this technique, there are other ways to exploit this vulnerability. For example, one of the most commonly used techniques is to use URL encoding to bypass security filters by converting the string `../` to `%2e%2e%2f`. This way, if the application block the string `../`, it is possible in some applications to bypass security and exploit the vulnerability.
* Another evasion technique involves manipulating the traversal sequence (`....//`) to bypass filters that remove `../` strings.

## Practice

* :writing_hand: This web application uses a parameter to include images in the web page. Exploits the vulnerability by accessing `/etc/passwd`:
@@ExerciseBox@@

[1]: /static/images/path-traversal-example.png
