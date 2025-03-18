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

* This web application has an exposed `.git` directory in its root folder, enabling a malicious user to retrieve the repository. This security flaw enables unrestricted access to download the entire repository.
* The objective of this exercise is to retrieve the `.git` folder and reconstruct the repository from it through the `Open Code Editor` button.
* Keep in mind that the `$APP_URL` is an environment variable that represents the base path of the application, so you can make a request to `.git` using the following command:

  ```bash
  curl -L $APP_URL/.git
  ```

* For the exercise to be completed properly, the repository must be reconstructed in `/home/coder/app/git-repo`.
* Once the repository is extracted successfully, press the `Verify Completion` button to confirm that the exercise has been completed.

@@ExerciseBox@@

[1]: https://github.com/arthaud/git-dumper
