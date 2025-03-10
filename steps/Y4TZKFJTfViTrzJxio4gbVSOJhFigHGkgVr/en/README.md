# Information disclosure via version control history

* Information disclosure via version control history occurs when the `.git` folder is unintentionally exposed in web applications, allowing unauthorized access.
* If accessible, this folder can reveal the entire version control history, including previous changes, commits, and potentially sensitive information.
* Attackers can retrieve source code, configuration files, credentials, or other confidential data stored in the repository.
* Access to version control history can help adversaries analyze code structure, identify vulnerabilities, and exploit security weaknesses.

> :older_man: The `.git` folder is a hidden directory used by Git to store version control data, including commit history, branches, and configuration files.

## Extracting repositories from a `.git`

* When a `.git` directory is publicly accessible, tools like [git-dumper][1] can extract its contents and reconstruct the repository.
* The following command retrieves the repository from an exposed `.git` folder:

  ```bash
  python3 git_dumper.py https://example.tbl/.git git-repo
  ```

* These tools help reconstruct the repository's history, allowing attackers to analyze the code, uncover credentials, or identify security vulnerabilities.

## Prevention techniques

* **Review deployment processes** to ensure that `.git` directories are not published to production environments through deployment scripts or CI/CD pipelines.
  * If Docker is used to deploy the web application, add the `.git` directory to the `.dockerignore` file to prevent it from being included in the container.
  * If the repository is cloned directly onto the web server, remove the `.git` directory after deployment to eliminate any risk of exposure.
* **Configure the server to deny access** by updating server settings to block access to `.git` directories and prevent unauthorized retrieval of repository data.

  > :warning: Even if the `.git` directory is not publicly accessible, storing it on the server is not recommended, as it contains commit history that may include sensitive information. If the server is compromised, this data could be exploited.

### Deny access in Apache

* The following Apache configuration blocks access to the `.git` directory, ensuring no unauthorized access:

  ```apacheconf
  # Deny access to .git directory
  <DirectoryMatch "^\.git">
    Require all denied
  </DirectoryMatch>
  ```

### Deny access in Nginx

* The following Nginx configuration denies access to `.git` using a regex match, preventing exposure of repository data:

  ```nginx
  location ~ /\.git {
    deny all;
  }
  ```

### Deny access in IIS

* The following `web.config` configuration prevents IIS from serving `.git` using `hiddenSegments`, with a rewrite rule returning a 403 Forbidden response:

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

## Exercise to practice :writing_hand:

* The web application has an exposed `.git` directory in its root folder, making it possible for an attacker to extract the repository.
* This exposure allows unrestricted access to download the entire repository, including sensitive information.
* The objective of this exercise is to retrieve the `.git` folder and reconstruct the repository from it through the `Open Code Editor` button.
* Keep in mind that the `$APP_URL` is an environment variable that represents the base path of the application, so you can make a request to `.git` using the following command:

  ```bash
  curl -L $APP_URL/.git
  ```

* For the exercise to be completed properly, the repository must be reconstructed in `/home/coder/app/git-repo`.
* Once the repository is extracted successfully, press the `Verify Completion` button to confirm that the exercise has been completed.

@@ExerciseBox@@

[1]: https://github.com/arthaud/git-dumper
