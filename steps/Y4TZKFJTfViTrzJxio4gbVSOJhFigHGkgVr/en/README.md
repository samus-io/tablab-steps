# Information disclosure via version control history

* The accidental exposure of the `.git` folder in web applications leads to information disclosure through version control history. If accessible, this folder can disclose the complete version history, including previous changes, commits, and potentially sensitive information.
* Sensitive data such as source code, configuration files, and credentials may be accessed by malicious users if the repository is exposed, enabling them to analyze the code structure, identify vulnerabilities, and exploit security weaknesses.

  > :older_man: The `.git` folder is a hidden directory where Git stores all version control data, including commit history, branch information, configuration settings, and other metadata essential for repository management.

## Rebuilding a repository from the version control data stored in a `.git` folder

* When a `.git` directory is exposed, tools like [git-dumper][1] can be used to extract its contents and restore the repository.
* The following command retrieves the repository from a publicly accessible `.git` folder and places it in the local `git-repo` folder:

  ```bash
  python3 git_dumper.py https://example.tbl/.git git-repo
  ```

* Malicious users can use this tool to rebuild the repository's history, analyze the codebase, uncover credentials, and locate security vulnerabilities.

## Recommended security approaches

* **Review deployment processes** to ensure that `.git` directories are not published to production environments through deployment scripts or CI/CD pipelines.
  * If Docker is used to deploy the web application, add the `.git` directory to the `.dockerignore` file to prevent it from being included in the container.
  * In cases where the repository is cloned onto the web server, remove any `.git` directory post-deployment to eliminate any risk of exposure.
* **Restrict access to `.git` directories by default** by configuring the instance to block unauthorized retrieval of repository data.

  > :warning: Even if the `.git` directory is not publicly accessible, storing it on the instance is discouraged, as it contains commit history that may hold sensitive information. In the event of a compromise, this data could be leveraged by attackers.

@@TagStart@@apache

### Deny access in Apache web server

* The following Apache configuration blocks access to the `.git` directory, ensuring no unauthorized access:

  ```apacheconf
  # Deny access to .git directory
  <DirectoryMatch "^\.git">
    Require all denied
  </DirectoryMatch>
  ```

@@TagEnd@@

@@TagStart@@nginx

### Deny access in Nginx web server

* The following Nginx configuration denies access to `.git` using a regex match, preventing exposure of repository data:

  ```nginx
  location ~ /\.git {
    deny all;
  }
  ```

@@TagEnd@@

@@TagStart@@iis

### Deny access in IIS web server

* The following `web.config` configuration prevents IIS from serving `.git` using `hiddenSegments`, with a rewrite rule returning a `403 Forbidden` HTTP response:

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <configuration>
    <system.webServer>
      <security>
        <requestFiltering>
          <hiddenSegments>
            <add segment=".git"/>
          </hiddenSegments>
        </requestFiltering>
      </security>
      <rewrite>
        <rules>
          <rule name="BlockGitDirectory">
            <match url="\.git" />
            <action type="CustomResponse" statusCode="403" statusReason="Forbidden" statusDescription="Access is forbidden." />
          </rule>
        </rules>
      </rewrite>
    </system.webServer>
  </configuration>
  ```

@@TagEnd@@

## Exercise to practice :writing_hand:

* This web application has an exposed `.git` folder accessible at the `https://ontablab.io/.git` in the simulated browser, allowing unrestricted access of the entire repository.
* The goal of this exercise is to extract the `.git` folder and rebuild the source code with the help of the [git-dumper][1] tool, already available in the `Terminal` tab.
  * An environment variable named `$APP_URL` stores the application's base URL, which can be used to send requests, for example, to fetch the HTML content of the `.git` path:

  ```bash
  curl -L $APP_URL/.git
  ```

  * Note that logging into the presented application is not required for the exercise.
* In order to complete the exercise, **the repository must be reconstructed in a folder named** `git-repo` **located at** `/home/tbl/git-repo`.
* After the repository is successfully extracted, click the `Verify Completion` button to confirm the exercise is complete.
  * Consider analyzing the code to validate how `git-dumper` restored the repository and retrieved the source code from the remote `.git` folder.

  @@ExerciseBox@@

[1]: https://github.com/arthaud/git-dumper
