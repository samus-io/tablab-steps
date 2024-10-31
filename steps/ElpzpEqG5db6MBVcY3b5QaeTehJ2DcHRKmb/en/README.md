# Applying Git security best practices on GitHub

## Steps to enable and enforce 2FA on GitHub

* To set up Two-factor authentication (2FA) on GitHub, you can choose from several below methods, each with simple steps.

### Configuring two-factor authentication using a TOTP app

1. Download a `Time-Based One Time Password (TOTP)` app to your phone or desktop.
1. Go to **Settings** > **Password and authentication** on GitHub.
1. Click Enable two-factor authentication.
1. Scan the QR code with your TOTP app or manually enter the TOTP secret.
1. Enter the authentication code from the app to verify.
1. Download and save your recovery codes.
1. Enable two-factor authentication after saving recovery codes.

### Configuring two-factor authentication using text messages

1. Go to **Settings** > **Password and authentication** on GitHub.
1. Click **Enable two-factor authentication** and then on **Add** button beside **SMS/Test message**.
1. Complete the CAPTCHA challenge.
1. Enter your mobile phone number and select your country code.
1. Receive a text message with a security code.
1. Enter the code on GitHub to verify.
1. Download and save your recovery codes.
1. Enable two-factor authentication after saving recovery codes.

### Configuring two-factor authentication using a passkey

1. Ensure you've already configured 2FA via a TOTP app or SMS.
1. Go to **Settings** > **Password and authentication** on GitHub.
1. Under Passkeys, click **Add a passkey**.
1. Authenticate with your password if prompted.
1. Follow the steps outlined by the passkey provider.
1. Review the confirmation and click Done.

### Configuring two-factor authentication using a security key

1. Ensure you've already configured 2FA via a TOTP app or SMS.
1. Insert a WebAuthn compatible security key.
1. Go to **Settings** > **Password and authentication** on GitHub.
1. Click **Add** or **Edit** next to **Security keys**.
1. Register a new security key and follow the prompts.
1. Confirm that you've downloaded and can access your recovery codes.

### Configuring two-factor authentication using GitHub mobile

1. You must have already configured 2FA via a TOTP mobile app or via SMS.
1. Install GitHub Mobile and sign in to your account.
1. After signing in, you can use your device for 2FA without relying on TOTP.
1. If you lose access to GitHub Mobile in the future, you can still use other 2FA methods.

## Limit access to repositories

* To limit access to repositories in GitHub, follow these steps:

  1. Navigate to the repository in GitHub that you want to limit access to.
  1. Click on the **Settings** tab located on the repository's menu bar.
  1. In the settings menu, find the **Manage access** or **Collaborators** section.
  1. If you want to grant specific individuals access to the repository, you can invite them as collaborators by entering their GitHub usernames or email addresses.
  1. If you want to restrict access to specific individuals or teams within your organization, set the repository visibility to **Private** instead of **Public**. This limits access to only those users who have been explicitly granted access as collaborators or members of teams with access permissions.
  1. For existing collaborators, you can adjust their permissions to control what actions they can perform within the repository. GitHub provides options to set permissions such as read-only access, write access, or administrative privileges.
  1. If you need to revoke access for certain collaborators, you can remove them from the repository's access list.
  1. If you are using GitHub organizations, you can manage access to repositories through teams. You can create teams within your organization and grant them specific access permissions to repositories.

### Create user groups to limit Access

* GitHub does not have a built-in feature for creating user groups directly within the platform. However, you can leverage teams within GitHub organizations to achieve similar functionality.
* Here's how to create user groups using teams within GitHub organizations:

  1. If you haven't already, create an organization on GitHub by navigating to your profile, clicking on the **Your Organizations** tab, and then selecting **New organization**. Follow the prompts to create the organization.
  1. Once the organization is created, navigate to its settings by clicking on the organization's name and then selecting **Settings**. Go to **Authentication Security** tab and eanble 2FA for everyone. In **Member Privilege** tab, set the **Base permissions** to **read** only by default.
  1. In the organization settings, click on the **Teams** tab to manage teams within the organization.
  1. Click on the **New team** button to create a new team within the organization. Give your team a descriptive name that reflects its purpose or the group of users it will include.
  1. Go to your team and click on **Add a member** and invite people on GitHub choosing the appropriate permissions for the team members, such as read access, write access, or administrative privileges for repositories within the organization using **People** tab.
  1. Add repositories to the team or organization and specify which repositories the team members will have access to. You can grant access to specific repositories or add teams within the organization with appropriate roles by navigating to repo **Settings** > **Access** > **Collaborators & teams**.
  1. Under **Manage access**, next to the team or person whose role you'd like to change, select the Role dropdown menu, and click a new role.

## Steps to rotate SSH tokens and personal keys in GitHub

1. **Generate new SSH key**: if you're rotating SSH keys, generate a new SSH key pair using the ssh-keygen command on your local machine.
1. **Update SSH key on GitHub**: go to your GitHub account settings, navigate to the **SSH and GPG keys** section, and delete the old SSH key. Then, add the new SSH public key by clicking on **New SSH key** and pasting the contents of the newly generated public key.
1. **Update personal access tokens**: go to your GitHub account settings, navigate to the Developer settings section, and click on **Personal access tokens**. Revoke the old personal access token and generate a new one with the necessary permissions.
1. **Update Git configurations**: if you use Git credentials or SSH keys in your local Git configurations, update them to use the new credentials or keys.

### Automate token rotation

1. **Use GitHub Actions**: set up GitHub Actions workflows to periodically rotate SSH Key. You can create workflows that use the GitHub API to generate new keys and update them in your account settings.
1. **Leverage CI/CD pipelines**: if you use CI/CD pipelines for your projects, incorporate Key rotation tasks into your pipeline scripts. Use GitHub API calls or command-line tools to automate the generation and update of key.
1. **Implement scheduled jobs**: use external scheduling tools or services to trigger key rotation tasks at regular intervals. You can write scripts or use existing tools to automate the rotation process and integrate them with your GitHub account via the GitHub API.
1. **Monitor and alert**: set up monitoring and alerting mechanisms to notify you of any issues or failures during the key rotation process. Monitor logs, API responses, and account activity to ensure that rotation tasks are executed successfully.

* Here's an example of how to automate the rotation of SSH Key in GitHub using GitHub Actions:

  ```yaml
  name: Change SSH Key

  on:
    workflow_dispatch:
    schedule:
      - cron: '0 0 * * *' # Runs daily at midnight UTC

  jobs:
    change_ssh_key:
      runs-on: ubuntu-latest

      steps:
        - name: Checkout Repository
          uses: actions/checkout@v2

        - name: Retrieve Current SSH Keys
          id: get_keys
          run: |
            keys=$( curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer ${{ secrets.GITHUB_TOKEN}}" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/user/keys/KEY_ID )
            echo "::set-output name=keys::$keys"

        - name: Delete Old SSH Key (optional)
          if: steps.get_keys.outputs.keys != ''
          run: |
            # Replace OLD_KEY_ID with the ID of the SSH key you want to delete
            curl -L \
            -X DELETE \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer ${{ secrets.GITHUB_TOKEN}}" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/user/keys/KEY_ID

        - name: Add New SSH Key
          run: |
            # Replace NEW_SSH_KEY with the content of your new SSH key and TITLE with a descriptive title
            curl -L \
            -X POST \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer ${{ secrets.GITHUB_TOKEN}}" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/user/keys \
            -d '{"title":"ssh-rsa AAAAB3NzaC1yc2EAAA","key":"2Sg8iYjAxxmI2LvUXpJjkYrMxURPc8r+dB7TJyvv1234"}'
  ```

  * The workflow runs either manually (workflow_dispatch) or on a schedule (schedule), triggering once a day at midnight UTC.
  * The `change_ssh_key` job runs on the latest version of Ubuntu.
  * It starts by checking out the repository.
  * The `Retrieve Current SSH Keys` step retrieves the list of current SSH keys associated with your GitHub account and sets the output variable keys.
  * If there are existing SSH keys (`if: steps.get_keys.outputs.keys != ''`), the `Delete Old SSH Key` step deletes the specified old SSH key (replace `OLD_KEY_ID` with the ID of the SSH key you want to delete).
  * Finally, the `Add New SSH Key` step adds the new SSH key to your GitHub account.

* To run the above GitHub Actions workflow for rotating SSH Key:

  1. In your GitHub repository, navigate to the `.github/workflows` directory (create it if it doesn't exist). Create a new YAML file (e.g., `rotate-key.yml`).
  1. Copy the example GitHub Actions workflow provided above. Paste it into the newly created YAML file (i.e., `rotate-key.yml`).
  1. Commit the changes to the repository. Push the changes to GitHub.
  1. GitHub Actions will automatically execute the workflow according to the schedule specified (`0 0 ** *`, which runs daily at midnight UTC). You can monitor the workflow's execution by navigating to the **Actions** tab in your repository on GitHub.

* The automation is possible only if there is an API endpoint available for the key or token change.  

## Tracking activities via audit logs on GitHub

1. Navigate to your GitHub organization settings by clicking on your profile photo, then selecting **Settings**, and choosing the organization.
1. In the organization settings, locate the **audit log** section. Enable audit logging to start recording activities within your organization. GitHub Enterprise Cloud and GitHub Enterprise Server offer audit log capabilities. You can enable to view IP addresses of current members for organization audit log events.
1. Once audit logging is enabled, you can view audit logs to track various activities such as user logins, repository access, permission changes, and more. Audit logs provide detailed information about who performed an action, what action was taken, and when it occurred.

### Syncing audit log service to notification channel

1. Select an audit log service that integrates with GitHub and offers notification capabilities. For this example Loggly will be used.
1. Access the settings or configuration options of your chosen audit log service. Look for GitHub integration options or methods to ingest GitHub audit logs. For example, to integrate GitHub audit logs with the Loggly app:

    * If you don't already have one, sign up for a Loggly account at [loggly.com][1].
    * Log in to your Loggly account. Navigate to the **Source setup** tab. Copy the customer token, which you'll use to send logs to Loggly.
    * In your GitHub repository, go to the Settings tab. Select **Webhooks** from the left menu. Click on the **Add webhook** button. In the **Payload URL** field, enter the **Loggly HTTP/S Event Endpoint**. This endpoint should look like `https://logs-01.loggly.com/inputs/{CUSTOMER_TOKEN}/tag/http/`. Set the Content type to `application/json`. In the **Which events would you like to trigger this webhook?** section, select the audit events you want to log. Click on the **Add webhook** button to save your settings.
    * Perform actions in your GitHub repository that trigger the selected audit events. Go back to Loggly and navigate to the **Search** tab. Search for the logs using the source name or any other identifying information.

1. Determine the notification channel where your team prefers to receive alerts. This could be a Slack channel, email distribution list, or a dedicated communication platform. For example, decide on the Slack channel where you want to receive audit log notifications. In this case, let's use `#audit-logs`.
1. Follow the instructions provided by your audit log service to set up integration with your chosen notification channel. For example, in Slack go to the channel settings and select **Add an app or integration**. Search for and install the Loggly Incoming WebHooks app. Follow the prompts to authorize the Loggly app and configure the integration with your Loggly account. Copy the Webhook from Slack and add it to loggly by creating alert endpoint.
1. Perform testing to ensure that the integration between the audit log service and the notification channel is functioning correctly. Trigger test events in GitHub or the audit log service and verify that notifications are delivered promptly to the designated channel.

## Backup the Github hosting environment

1. Decide which repositories you want to backup.
1. Choose between manual or automated backup.
    * **Manual Backup**: download repository files from GitHub or clone repositories using Git commands.
    * **Automated Backup**: write a script or use a third-party tool to automate backups.
1. Schedule backups to run regularly based on your needs.
1. Keep backup files in a secure location to prevent data loss or unauthorized access.
1. Regularly test backup and restore procedures to ensure they work correctly.
1. Keep an eye on the backup process and set up alerts for any issues.

## Using private repositories on GitHub

* To disable public repositories on GitHub, follow these steps:

  1. Sign in to your GitHub account and Open your repository.
  1. Scroll down to the **Features** or **Danger Zone** section in Settings tab.
  1. Find the option labeled **Change repository visibility**.
  1. Choose the option to set the default repository visibility to **Private**.

* For Organizations, you can allow members to create only private repositories in GitHub Entreprise version:

  1. In the upper-right corner of [github.com][2], select your profile photo, then click  **Your organizations**.
  1. Next to the organization, click **Settings**.
  1. In the **Access** section of the sidebar, click **Member privileges**.
  1. Under **Repository creation**, select one or more options and save.

## Disable forking on private repositories in Github organizations

* To disable or enable the forking of private repositories:

  1. Open **Your Organization** and navigate to the organization you want.
  1. Click of the repositories tab and select your repository.
  1. Go to **Settings** > **Member privileges**.
  1. Under **Repository forking**, keep forking of private repositories disabled.

* Note that it is not possible to perform this on any public repositories and private repositories of your Github Account which do not belong to any organization.

## Steps to ensure code branch protection on GitHub

* To set up branch protection rules in GitHub, follow the steps below:

  1. Navigate to your GitHub repository, and go to the **Settings** tab.
  1. In the left sidebar, click **Branches**.
  1. Under Branch protection rules, click **Add branch protection rule**.
  1. In the **Branch name pattern** field, enter the name of the branch you want to protect.
  1. Under **Protect matching branches**, select the requirements you want to enforce.
      * **Require a pull request before merging**: when enabled, all commits must be made to a non-protected branch and submitted via a pull request before they can be merged into a branch that matches this rule.
      * **Require status checks to pass before merging**: when enabled, commits must first be pushed to another branch, then merged or pushed directly to a branch that matches this rule after status checks have passed.
      * **Require conversation resolution before merging**: when enabled, all conversations on code must be resolved before a pull request can be merged into a branch that matches this rule. Learn more about requiring conversation completion before merging.
      * **Require signed commits**: commits pushed to matching branches must have verified signatures.
      * **Require linear history**: prevent merge commits from being pushed to matching branches.
      * **Require deployments to succeed before merging**: choose which environments must be successfully deployed to before branches can be merged into a branch that matches this rule.
      * **Lock branch**: branch is read-only. Users cannot push to the branch.
      * **Do not allow bypassing the above settings**: the above settings will apply to administrators and custom roles with the **bypass branch protections** permission.
      * **Allow force pushes**: permit force pushes for all users with push access.
      * **Allow deletions**: allow users with push access to delete matching branches.
  1. Click **Create** to save your new branch protection rule.

## Sign commits on GitHub

* GPG can be used to sign commits. GPG is widely used for cryptographic operations, including signing messages and files. While GPG is complex and has various functionalities, signing Git commits is relatively straightforward once it's set up.
* GPG facilitates the distribution of public keys, which are identified by an ID and typically associated with an email address.
* Follow all the steps given below to keep your commits signed and achieve the verified tag on GitHub.

### Install GPG

1. Install Git command line tool for Git related operations because it comes pre-installed with GPG or to install GPG, follow these steps:
    * **For Windows**: download the `Gpg4win` distribution from the GPG website and follow the installation instructions.
    * **For macOS**: install `Homebrew` if you haven't already. Open Terminal and run `brew install gpg`.
    * **For Linux**: most Linux distributions come with GPG pre-installed. If not, you can install it from your distribution's official repositories.

#### Additional configuration for Linux and macOS

1. Enable the GPG agent to avoid typing the secret key’s password every time:
   * Add `use-agent` to `~/.gnupg/gpg.conf`.
1. Add the following lines to your profile file (`~/.bashrc`, `~/.bash_profile`, `~/.zprofile`, etc):

   ```bash
   export GPG_TTY=$(tty)
   gpgconf --launch gpg-agent
   ```

1. Restart your shell or run `source ~/.bashrc` (or equivalent) to apply the changes.

* These steps will ensure that GPG is installed and properly configured on your system.

### Generate a GPG Key

* To generate a GPG key pair, follow these steps:

  1. Open your terminal or command prompt.
  1. Run the following command to generate a new GPG key pair:

    ```bash
    gpg --full-gen-key
    ```

  1. When prompted, choose the following options:
      * Kind of key: type 4 for RSA (sign only).
      * Keysize: enter 4096.
      * Expiration: choose a reasonable value, for example, 2y for 2 years.
  1. Follow the prompts to provide:
      * Your real name (you can use your GitHub username).
      * Email address (you can use the @users.noreply.github.com email generated by GitHub).
      * Passphrase: type a passphrase to encrypt your secret key on disk.

  1. After generating the key pair, verify it was created by running:

    ```bash
    gpg --list-secret-keys --keyid-format SHORT
    ```

      * Output is similar to the example provided, confirming your key ID and details.

  1. To confirm that GPG is working and able to sign messages, run:

    ```bash
    echo "hello world" | gpg --clearsign
    ```

  1. If your GPG agent encounters issues, you can restart it with:

    ```bash
    gpgconf --kill gpg-agent
    gpgconf --launch gpg-agent
    ```

* Following these steps will generate a GPG key pair and ensure that GPG is functioning properly on your system.
* You can add multiple email addresses by editing the key:

  ```bash
  gpg --edit-key <keyId>
  ```

### Add the GPG key to GitHub

* To add your GPG key to GitHub and start signing commits, follow these steps:

  1. Ensure your Git email address used below is verified on GitHub.

    ```bash
    git config --global user.email <your emailId>
    ```

  1. Make sure the same email address is added to your GPG key.
  1. Upload your public GPG key to GitHub.

* Generate your public key:

  ```bash
  gpg --armor --export <keyId>
  ```

* Copy the output, which starts with `-----BEGIN PGP PUBLIC KEY BLOCK-----` and ends with `-----END PGP PUBLIC KEY BLOCK-----`.
* Go to the **SSH and GPG keys** settings page on GitHub.
* Click on **New GPG key** and paste your public key.

### Configure Git to sign your commits

* Once you have your private key, you can configure Git to sign your commits using:

  ```bash
  git config --global user.signingkey <keyId>
  ```

* Now, you can sign Git commits and tags by adding the `-S` flag when creating a commit:

  ```bash
  git commit -S -m <your commit message>
  ```

* And, same when creating a tag with `git tag -s`.
* Use below command in Git to automatically sign all your commits:

  ```bash
  git config --global commit.gpgSign true
  git config --global tag.gpgSign true
  ```

## Using pre-commit hook to scans repositories on GitHub

* Here are the steps to set up and use a client-side pre-commit hook in your Git repository:

  1. Open your terminal or command prompt and navigate to the root directory of your Git repository.
  1. Inside the `.git/hooks` directory of your repository, create a new file named `pre-commit`. This file will contain the script for your pre-commit hook.
  1. Open the `pre-commit` file in a text editor and write the script to execute your pre-commit checks. This script will run every time you attempt to make a commit. The below the example of pre-commit hook script:

      ```bash
        #!/bin/bash
            
        # Run linters
        echo "Running linters..."
      ```

  1. Ensure that the `pre-commit` script is executable by running the following command:

      ```bash
      chmod +x .git/hooks/pre-commit
      ```

  1. Make some changes to your files and attempt to commit them using Git. The pre-commit hook should automatically run before the commit is finalized. If any of your pre-commit checks fail (e.g., linting errors), the commit will be aborted, and you'll need to address the issues before committing again.
  1. Customize the pre-commit hook script to include additional checks or actions tailored to your project's requirements. You can incorporate linting, formatting, testing, or any other checks that you deem necessary.

## Scanning incoming pull requests on GitHub

* To set up scanning for incoming pull requests on GitHub, you can use GitHub Actions to automate the process. Here are the steps:

  1. In your repository, create a directory named `.github/workflows`. Inside this directory, create a YAML file, for example, `scan-pr.yml`. This file will define your GitHub Actions workflow.
  1. In the YAML file, define the workflow to scan incoming pull requests. You can use the `pull_request` event trigger to specify when the workflow should run. The below is the code snippet of workflow file (`scan-pr.yml`):

    ```yaml
    name: Pull Request Validation

    on:
      pull_request:
        branches:
          - main

    jobs:
      scan_pull_request:
        runs-on: ubuntu-latest

        steps:
          - name: Checkout Repository
            uses: actions/checkout@v2

          - name: Validate Pull Request
            run: |
              # Get the list of changed files in the pull request
              if [ "$(git rev-parse HEAD)" = "$(git rev-list --max-parents=0 HEAD)" ]; then
                echo "This is the initial commit. No validation checks needed."
                exit 0
              fi

              changed_files=$(git diff --name-only HEAD^)

              # Perform validation checks on each changed file
              for file in $changed_files; do
                # Check if the file contains any forbidden patterns
                if grep -q "forbidden_pattern" $file; then
                  echo "Error: File $file contains forbidden pattern."
                  exit 1
                fi

                # Add more custom validation checks as needed...
              done
    ```

    1. In the `on` section of the workflow file, specify the conditions under which the workflow should run. For example, you might want it to trigger when a pull request is opened or when changes are synchronized with the base branch.
    1. Inside the `jobs` section, define the steps to be executed as part of the workflow. This typically includes checking out the code and running the scanning tool. Replace the placeholder commands with the actual commands required to run your scanning tool.
    1. Commit and push the workflow file (`scan-pr.yml`) to your GitHub repository.
    1. With the workflow file in place, GitHub Actions will automatically run the scanning tool whenever a pull request is opened or changes are synchronized with the base branch.
    1. After each pull request event, you can view the workflow results in the **Checks** tab of your GitHub repository. This will show whether the scanning tool passed or failed.

## Automatically update dependencies on GitHub

* To automatically update dependencies on GitHub, you can use GitHub Actions to create a workflow that periodically checks for updates and automatically creates pull requests to update dependencies. Here are the steps:

  1. In your repository, create a directory named `.github/workflows`. Inside this directory, create a YAML file, for example, `update-dependencies.yml`. This file will define your GitHub Actions workflow.
  1. In the YAML file, define the workflow to automatically update dependencies. You can use scheduled events (`schedule`) to trigger the workflow at specified intervals.

    ```yaml
        name: Update Dependencies

        on:
          schedule:
            - cron: '0 0 * * *' # Run every day at midnight UTC

        jobs:
          update:
            runs-on: ubuntu-latest

            steps:
              - name: Checkout code
                uses: actions/checkout@v2

              - name: Update dependencies
                run: |
                  # Replace this with the command to update dependencies
                  npm install -g npm-check-updates
                  ncu -u
                  npm install
                  git commit -am "chore: Update dependencies" && git push
    ```

    1. In the `on` section of the workflow file, specify the schedule for triggering the workflow. You can use cron syntax to define the schedule. For example, `'0 0 * * *'` runs the workflow every day at midnight UTC.
    1. Inside the `jobs` section, define the steps to be executed as part of the workflow. This typically includes checking out the code, updating dependencies, committing the changes, and pushing them back to the repository. Replace the placeholder commands with the actual commands required to update dependencies. For example, if you're using npm, you can use `npm-check-updates` (`ncu`) to update dependencies.
    1. Commit and push the workflow file (`update-dependencies.yml`) to your GitHub repository.
    1. After each scheduled event, you can view the workflow results in the **Actions** tab of your GitHub repository. This will show whether the dependency updates were successful or encountered any issues.

* By setting up this GitHub Actions workflow, you can automate the process of updating dependencies in your project, ensuring that you're always using the latest versions and staying up-to-date with security patches and improvements.

[1]: https://www.loggly.com/
[2]: https://github.com/
