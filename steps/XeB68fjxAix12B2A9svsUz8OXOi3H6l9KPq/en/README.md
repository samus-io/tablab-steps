# Applying Git security best practices on GitLab

## Steps to enable and enforce 2FA on GitLab

* To enable `2-Factor Authentication` in GitLab, there are two available methods: **One-time password authenticator** and **WebAuthn device**.

### One-time password authenticator

* Here are the steps to enable 2FA with a one-time password in GitLab:

  1. Navigate to your **User settings** in GitLab.
  1. Within the settings, choose the **Account** option.
  1. Look for the option to **Enable Two-factor Authentication** and select it.
  1. On your device (typically your phone), install a compatible application. Some recommended options include Authy, Google Authenticator, or FreeOTP.
  1. In the authentication application, add a new entry by scanning the code displayed by GitLab or entering the details manually.
  1. Back in GitLab, enter the six-digit pin number from the entry on your device into the Pin code field.
  1. Input your current password in the provided field.
  1. Once all information is entered correctly, select the **Submit** button.
  1. If successful, GitLab will display a list of recovery codes. Download and keep these codes in a secure location for future use.

### WebAuthn device

* To set up 2FA with a WebAuthn-compatible device in GitLab, follow these steps:

  1. If desired, set up a one-time password for additional security.
  1. Navigate to your **User settings** in GitLab.
  1. Choose the **Account** option within the settings.
  1. Look for the option to **Enable Two-Factor Authentication** and select it.
  1. Select **Set up new device**.
  1. Follow the prompts on your device. Depending on the device, you might need to press a button or scan a QR.
  1. Give the name of the device and click on **Register device**. Then, after downloading the recovery code click on **Proceed**.
  1. Once the setup is complete, you may receive a message indicating that your device has been successfully linked and you will login with your device for the next attempt.

* When setting up 2FA with a WebAuthn-compatible device, it's important to note that the device becomes linked to a specific browser on a specific computer. Depending on the browser and device, you may have the option to configure settings to use the WebAuthn device on a different browser or computer.
* If this is your first time setting up 2FA, be sure to download recovery codes to ensure you can recover access to your account if you ever lose access.

## Limit access to repositories

* To limit access to repositories or Projects in GitLab, follow these steps:

  1. Navigate to the project for which you want to limit access.
  1. Inside the project, locate the **Manage** option.
  1. In the Manage tab, find the **Members** section.
  1. Determine the access levels for different users or groups. GitLab typically provides options like Guest, Reporter, Developer, Maintainer, and Owner. Choose the appropriate level for each user or group.
  1. Add individual users or user groups to the repository access settings. Users can be added by their GitLab username or email address, while groups can be added by their group name.
  1. After configuring the access levels and adding users or groups, save the changes.

### Creating user groups

1. Navigate to the **Groups** section in GitLab.
1. If the desired group does not exist, create a new group by clicking on the **New group** button.
1. Provide a name and description for the group. Optionally, set the group's visibility level (public, internal, or private).
1. Add members to the group by specifying their GitLab usernames or email addresses.
1. Determine the group's access level to projects, issues, merge requests, and other project features, if you want to edit.
1. Once all details are entered and permissions are configured, save the changes to create the group.
1. After creating the group, you can manage group members by adding or removing users as needed. You can also adjust group permissions and settings at any time.

## Steps to rotate SSH tokens and personal keys in GitLab

* To rotate SSH tokens and personal keys in GitLab, follow these steps:

  1. Log in to your GitLab account and navigate to your **user settings**.
  1. In the settings menu, locate the **SSH Keys** section.
  1. Take note of the SSH keys currently associated with your account.
  1. Use the appropriate tool to generate a new SSH key pair on your local machine if you haven't already done so. You can use the ssh-keygen command on Unix-based systems or tools like PuTTYgen on Windows.
  1. Copy the public key generated in the previous step. In GitLab, navigate to the SSH Keys section and click on the **Add SSH key** button. Paste the copied public key into the provided field and give it a descriptive title.
  1. If you're using the new SSH key for specific repositories or servers, update your SSH configurations accordingly. For example, you might need to update the `~/.ssh/config` file on your local machine.
  1. Before proceeding further, test the new SSH key to ensure it works as expected. Attempt to clone or push to a repository using the new SSH key to verify its functionality.
  1. Once you've confirmed that the new SSH key works correctly, you can remove the old SSH keys from your GitLab account. Navigate to the **SSH Keys** section in your **user settings** and delete the outdated keys.
  1. If you're using personal access tokens for authentication, consider rotating them as well. Navigate to the **Access tokens** section in your user settings, revoke any old tokens, and generate new ones if needed.

### Automate token and key rotation

* To automate the process of rotating SSH tokens and personal keys in GitLab, you can utilize scripting and automation tools. Here are the steps to automate this process:

  1. Write a script to generate a new SSH key pair using the ssh-keygen command or an equivalent tool. Ensure the script can accept parameters such as key type, key size, and output directory.
  1. Use GitLab's API to programmatically add the new SSH public key to your account. You can utilize tools like cURL or programming languages like Python with libraries such as requests to make API calls.
  1. Incorporate tests into your automation script to verify that the new SSH key works as expected. This can involve attempting to clone or push to a repository using the new key.
  1. Write logic in your script to identify and remove any outdated SSH keys associated with your GitLab account. Again, you can utilize GitLab's API for this purpose.
  1. If you're also rotating personal access tokens, integrate logic into your script to revoke old tokens and generate new ones as needed using GitLab's API.
  1. Use a scheduling tool or a task runner like cron (on Unix-based systems) or Task Scheduler (on Windows) to regularly execute your automation script at predefined intervals.
  1. Implement logging and error handling mechanisms in your script to monitor the execution and identify any issues or failures that may occur during the automation process.

#### Example script in Node.js

* Here's an example of how to automate the process of rotating SSH tokens and personal keys in GitLab using Node.js:

  ```javascript
  const { execSync } = require('child_process');
  const axios = require('axios');

  // Step 1: script SSH Key Generation
  function generateSSHKey() {
    try {
      execSync('ssh-keygen -t rsa -b 4096 -f new_key -N ""');
    } catch (error) {
      console.error('Error generating SSH key:', error);
    }
  }

  // Step 2: update SSH Keys in GitLab
  async function updateSSHKeys() {
    try {
      const pubkey = require('fs').readFileSync('new_key.pub', 'utf8');

      const gitlabApiUrl = 'https://gitlab.com/api/v4/user/keys';
      const privateToken = 'YOUR_PRIVATE_TOKEN';
      const data = { title: 'New SSH Key', key: pubkey };
      const headers = { 'Private-Token': privateToken };

      const response = await axios.post(gitlabApiUrl, data, { headers });
      console.log('SSH key added successfully:', response.data);
    } catch (error) {
      console.error('Error updating SSH keys:', error);
    }
  }

  // Step 3: test SSH Key
  function testSSHKey() {
    // Add your test commands here, such as attempting to clone a repository using the new SSH key
  }

  // Step 4: remove Old SSH Keys
  function removeOldSSHKeys() {
    // Implement logic to identify and remove outdated SSH keys using GitLab's API
  }

  // Step 5: update access tokens (optional)
  function updateAccessTokens() {
    // Implement logic to revoke old access tokens and generate new ones using GitLab's API
  }

  // Main function to execute all steps
  async function rotateSSHKeys() {
    generateSSHKey();
    await updateSSHKeys();
    testSSHKey();
    removeOldSSHKeys();
    updateAccessTokens();
  }

  // Execute the main function
  rotateSSHKeys();
  ```

  * The `child_process` module to execute shell commands for generating SSH keys.
  * The `axios` library to make HTTP requests to the GitLab API for updating SSH keys.
  * It's needed to replace the `'YOUR_PRIVATE_TOKEN'` string with your GitLab private token.
  * The `new_key.pub` is the path to the file in which public key is stored.
  * Specific logic needs to be implemented for testing SSH keys, removing old SSH keys, and updating access tokens according to your requirements and GitLab's API documentation.
  * The GitLab API references provide detailed information to help understand how the API endpoints work.

## Tracking activities via audit logs on GitLab

* There are two types of auditing options in GitLab, **Authentication log** and **Audit events**. The following sections will cover how to access and filter both types of logs.

### Accessing audit events

1. Navigate to the desired level where you want to view audit events (group, project, instance, or sign-in).
1. For group and project events, locate the respective group or project from the left sidebar under **Search** or by direct URL access.
1. For instance events, navigate to **Admin area** from the left sidebar.
1. For sign-in events, click on your avatar and select **Edit profile** > **Authentication log**.

### Filtering audit events

1. Once on the audit events page, select **Secure** > **Audit events for groups and projects, or Monitoring** > **Audit events for instances**.
1. For sign-in events, go to **Authentication log**.
1. Use filters to narrow down the events based on the member of the project (user), group, project, and date range.

### Viewing sign-in audit events

1. For sign-in events, successful sign-ins are available at all tiers.
1. Access them by clicking on your avatar, selecting **Edit profile**, and then navigating to **Authentication log**.
1. After upgrading to a paid tier, successful sign-in events are also visible on audit event pages.

### Syncing audit log service to notification channel

* Here are the steps to sync audit logs from GitLab to a communication channel:

  1. Choose a communication channel where you want to receive the audit logs. Common options include Slack, Microsoft Teams, Discord, or email. Ensure you have the necessary permissions to create integrations or channels within the chosen platform.
  1. In your chosen communication channel, create a webhook or integration to receive external data. Obtain the webhook URL provided by the communication channel. This URL will be used to send data from GitLab.
  1. Go to your GitLab project or instance settings, depending on the scope of the audit logs you want to sync. Navigate to Integrations or Webhooks settings. Add a new webhook and paste the webhook URL obtained from the communication channel. Optionally, configure any additional settings such as triggers, payloads, or authentication methods.
  1. Send a test payload from GitLab to the communication channel to ensure the webhook is properly configured. Verify that the test message appears in the chosen communication channel.

### Example for audit logs synced to Slack

* To sync audit logs from a specific GitLab project to a Slack channel, let's say named **#gitlab-audit-logs**, follow these steps:

  1. In Slack, navigate to the channel settings for **#gitlab-audit-logs**. Add an incoming webhook integration and note down the webhook URL provided by Slack.
  1. Go to the settings of your GitLab project. Navigate to **Integrations** and **Add a new webhook**. Paste the Slack webhook URL in the designated field. Customize any additional settings such as triggers or payloads.
  1. Send a test payload from GitLab to the Slack channel. Verify that the test message appears in the **#gitlab-audit-logs** channel.
  1. Monitor the Slack channel for incoming audit log messages from GitLab. Review the synced audit logs to ensure they contain the relevant information.

## How to backup the GitLab hosting environment?

* To take backups of repositories in GitLab, utilize GitLab's built-in backup functionality.
* To take a backup of GitLab projects using the export feature, follow these steps:

  1. Ensure that the export feature is enabled on your GitLab instance. As an administrator, you can do this by navigating to **Admin Area** > **Settings** > **General** > **Import and export settings** and selecting the **GitLab export** checkbox.
  1. Log in to your GitLab instance. Navigate to the project you want to export. Go to **Settings** > **General**. Under the **Advanced** section, click on **Export project**. Once the export is generated, you can download it immediately or follow a link contained in an email that you'll receive.
  1. If you plan to import the project into another GitLab instance, you can do so by going to the target instance, creating a new project or group, and then selecting **Import project** or **Import group**. Choose the GitLab export file you downloaded earlier to import the project or group.
  1. The exported project includes various items such as repositories, uploads, project configuration, issues, merge requests, labels, milestones, snippets, releases, CI/CD pipelines, protected branches, project members, etc. Refer to the provided list of exported items to get a detailed overview.
  1. It's essential to note that certain items are not exported, including child pipeline history, pipeline triggers, build traces and artifacts, CI/CD variables, webhooks, encrypted tokens, number of required approvals, repository size limits, deploy keys, activity logs for Git-related events, security policies, links between issues and linked items, links to related merge requests, and more. Ensure you have additional backups for these items if needed.

## Using private repositories on GitLab

* In GitLab, you can change the **Project** and **Group** visibility.
* There are 3 types of repos in GitLab:
  * **Private**: only members of the private project or group can clone the project, and view the public access directory (/public). Users with the Guest role cannot clone the project. Private groups can have only private subgroups and projects.
  * **Internal**: any authenticated user, including users with the Guest role, can clone the project, and view the public access directory (/public). Only internal members can view internal content. External users cannot clone the project. Internal groups can have internal or private subgroups and projects.
  * **Public**: unauthenticated users, including users with the Guest role, can clone the project, and view the public access directory (/public). Public groups can have public, internal, or private subgroups and projects.
* To change the visibility of projects and groups in GitLab, follow the steps given below.

### Changing project visibility

1. On the left sidebar, navigate to the Search bar or directly find your project. Once in the project, click on **Settings** and then select **General**.
1. Within the General settings, locate the **Visibility, project features, permissions** section.
1. From the **Project visibility** dropdown list, choose the desired visibility option: **Private**, **Internal**, or **Public**. Note that the visibility setting for a project must be at least as restrictive as the visibility of its parent group.
1. Once you've selected the appropriate visibility level, click on **Save changes** to apply the new visibility settings to your project.

### Changing group visibility

1. On the left sidebar, navigate to the Search bar or directly find your group. Once in the group, click on **Settings** and then select **General**.
1. Within the General settings, locate the **Naming, visibility** section.
1. From the **Visibility level** dropdown list, choose the desired visibility option: **Private** or **Public**. Remember that projects and subgroups within the group must already have visibility settings that are at least as restrictive as the new setting of the parent group.
1. After selecting the appropriate visibility level, click on **Save changes** to apply the new visibility settings to your group.

## How to disable forking on private projects in GitLab groups?

* To prevent projects from being forked outside the group:

  1. On the left sidebar, select **Search or go to** and find your group.
  1. Select **Settings** > **General**.
  1. Expand the **Permissions and group features** section.
  1. Check prevent project forking outside current group.
  1. Select **Save changes**.

## Steps to ensure code branch protection on GitLab

* To create and add protection rules to a branch in GitLab, follow these steps:

  1. On the left sidebar, navigate to the Search bar or directly find your project. Once in the project, click on **Settings** and then select **Repository**.
  1. Within the Repository settings, locate and expand the **Protected branches** section.
  1. Click on **Add protected branch** to initiate the process of protecting a branch.
  1. From the dropdown list labeled **Branch**, choose the specific branch you want to protect.
  1. From the **Allowed to merge** dropdown list, specify the role or roles that can merge changes into this branch. Options typically include Maintainer, Developer, or custom roles if configured.
  1. In the **Allowed to push and merge** dropdown list, select the role or roles that can push changes directly to this branch.
  1. In GitLab Premium and Ultimate, you can also add individual users or groups to the merge and push permissions.
  1. After configuring the desired permissions, click on **Protect** to enforce the protection rules on the selected branch.
  1. All the protected branches appear as a branch rule.

* Here are some additional important points to note about branch protection:
  * The default branch of your repository is protected by default.
  * Protected branches control various actions such as merging, pushing, and force pushing.
  * GitLab allows for granular control over branch protection, including permissions for merge requests, force pushes, and code owner approvals.
  * Group-level protection settings can be applied to all projects within a group and override project-level settings.
  * Wildcard rules can be used to protect multiple branches simultaneously, with the most permissive rule taking precedence.
  * Code owner approval can be required for merge requests on protected branches, ensuring proper review processes.
  * Deploy keys can be permitted to push to protected branches, provided they have the necessary access permissions.
  * Administrators can set default branch protection levels in the Admin Area for consistency across projects.

## Signing commits and tags in GitLab

* There are three ways to sign commits or tags in GitLab.

### Sign commits with GPG key

#### Create a GPG Key

1. Install GPG on your system.
1. Generate a GPG key pair using the command `gpg --gen-key` or `gpg --full-gen-key`.
1. Choose the algorithm, key length, validity period, and enter your name, email, and optional comment.
1. Set a strong passphrase for your key.

#### Find your GPG key ID

1. List your private GPG key using the command `gpg --list-secret-keys --keyid-format LONG <EMAIL>`.
1. Copy the GPG private key ID starting with "sec".

#### Add your GPG key to GitLab

1. Sign in to GitLab and go to your user settings.
1. Navigate to **Edit profile** > **GPG Keys**.
1. Add a new key and paste your public key.
1. Click **Add key**.

#### Associate your GPG key with Git

1. Run `gpg --list-secret-keys --keyid-format LONG <EMAIL>` to list your private GPG key.
1. Copy the GPG private key ID.
1. Configure Git to use your key with `git config --global user.signingkey <keyId>`.

#### Sign your Git commits

1. Manually sign individual commits using `git commit -S -m <Your commit message>`.
1. Enter your GPG key passphrase when prompted.
1. Alternatively, sign all commits by default with `git config --global commit.gpgsign true`.

### Sign commits with SSH Key

#### Build your SSH Key

* To see if you have an existing SSH key pair and generate a new one if needed, follow these steps:

  1. Open a terminal.
  1. Navigate to your home directory:

    ```bash
    cd ~
    ```

  1. Check if the `.ssh/` directory exists:

    ```bash
    ls -la .ssh/
    ```

      * If the directory doesn't exist, you either aren't in the home directory or haven't used SSH before.

  1. If the `.ssh/` directory exists, check for existing SSH key files:

    ```bash
    ls -la .ssh/
    ```

  * Look for files with one of the following formats:
    * `id_ed25519.pub` (public key) / `id_ed25519` (private key)
    * `id_rsa.pub` (public key) / `id_rsa` (private key)
    * `id_dsa.pub` (public key) / `id_dsa` (private key)
    * `id_ecdsa.pub` (public key) / `id_ecdsa` (private key)

  1. If you don't have an existing SSH key pair, generate a new one:
  * Open a terminal.
  * Run the following command for ED25519 (preferred):

      ```bash
      ssh-keygen -t ed25519 -C "<comment>"
      ```

      Or for 2048-bit RSA:

      ```bash
      ssh-keygen -t rsa -b 2048 -C "<comment>"
      ```

        * Replace `<comment>` with an optional comment, such as your email address.
        * Make sure you have openssh 8.1 or newer installed.
  1. Press Enter to accept the suggested filename and directory for storing the key pair.
  1. Specify a passphrase when prompted:

    ```bash
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    ```

  1. After confirmation, your public and private SSH key files are generated. Add the public key to your GitLab account and keep the private key secure.

#### Add SSH key to GitLab account

* To copy your public SSH key to your GitLab account and verify the connection, follow these steps:

  1. Open a terminal on your local machine.
  1. Use one of the following commands to copy the contents of your public key to the clipboard:
      * For macOS:

        ```bash
        tr -d '\n' < ~/.ssh/id_ed25519.pub | pbcopy
        ```

      * For Linux (requires the xclip package):

        ```bash
        xclip -sel clip < ~/.ssh/id_ed25519.pub
        ```

      * For Git Bash on Windows:

        ```bash
        cat ~/.ssh/id_ed25519.pub | clip
        ```

        * Replace `id_ed25519.pub` with your filename if necessary.
  1. Sign in to your GitLab account.
  1. Navigate to your user profile by clicking on your avatar.
  1. Select **Edit profile** from the sidebar.
  1. Choose **SSH Keys** from the left sidebar.
  1. Click on **Add new key**.
  1. Paste the contents of your public key into the **Key** box. Ensure that you include the entire key, starting with `ssh-rsa` or similar, and ending with the comment if applicable.
  1. Optionally, enter a title and select the usage type and expiration date.
  1. Click on **Add key** to save.
  1. Open a terminal on your local machine.
  1. Run the following command, replacing `gitlab.example.com` with your GitLab instance URL:

    ```bash
    ssh -T git@gitlab.example.com
    ```

  1. If prompted, verify the authenticity of the GitLab host by typing **yes** and pressing Enter.
  1. Run the `ssh -T git@gitlab.example.org` command again. You should receive a **Welcome to GitLab, @username!** message.
  1. If the welcome message doesn't appear, troubleshoot by running SSH in verbose mode:

    ```bash
    ssh -Tvvv git@gitlab.example.com
    ```

#### Configure Git to sign commits with your SSH key

* To configure Git to use your SSH key for commit signing, follow these steps:

  1. Open a terminal on your local machine.
  1. Run the following command to configure Git to use SSH for commit signing:

    ```bash
    git config --global gpg.format ssh
    ```

  1. Specify which public SSH key to use as the signing key by running the following command:

    ```bash
    git config --global user.signingkey ~/.ssh/examplekey.pub
    ```

        * Replace `~/.ssh/examplekey.pub` with the location of your SSH public key. The filename might differ based on how you generated your key.

### Sign commits and tags with x.509

* To obtain an X.509 key pair for signing commits in Git, follow these steps:

#### Check Git version

* Ensure you have Git version 2.19.0 or later installed. You can check your Git version by running the command `git --version`.

#### Obtain X.509 key pair

* **From PKI**: if your organization has a Public Key Infrastructure (PKI), you can obtain an S/MIME key from there.
* **Self-signed**: if you don't have an S/MIME key pair from a PKI, you can create your own self-signed pair.
* **Purchase**: alternatively, you can purchase an X.509 key pair.

#### Associate X.509 certificate with Git

* For Linux:
  * Configure Git to use your key for signing:

     ```bash
     signingkey=$( gpgsm --list-secret-keys | egrep '(key usage|ID)' | grep -B 1 digitalSignature | awk '/ID/ {print $2}' )
     git config --global user.signingkey $signingkey
     git config --global gpg.format x509
     ```

* For Windows and macOS:
  * Install S/MIME sign downloading the installer manually or running `brew install smimesign` on macOS.
  * Get the ID of your certificate by running `smimesign --list-keys`.
  * Set your signing key by running `git config --global user.signingkey <ID>`, replacing `<ID>` with the certificate ID.
  * Configure X.509 with these commands:

     ```bash
     git config --global gpg.x509.program smimesign
     git config --global gpg.format x509
     ```

#### Sign and verify Commits

* When creating a Git commit, add the `-S` flag:

     ```bash
     git commit -S -m "feat: x509 signed commits"
     ```

* Push to GitLab, and verify that your commits are verified with the `--show-signature` flag:

     ```bash
     git log --show-signature
     ```

#### Automate commit signing

* To sign your commits automatically every time, run:

     ```bash
     git config --global commit.gpgsign true
     ```

#### Sign and verify tags

* When creating a Git tag, add the `-s` flag:

     ```bash
     git tag -s v1.1.1 -m "My signed tag"
     ```

* Verify your tags are signed with:

     ```bash
     git tag --verify v1.1.1
     ```

* To sign your tags automatically each time, run:

     ```bash
     git config --global tag.gpgsign true
     ```

## Using pre-commit hook to scan repositories on GitLab

* Using a pre-commit Git hook to scan repositories on GitLab is a proactive approach to ensure code quality and security before committing changes. Here's how you can set up a pre-commit hook and integrate it into your GitLab workflow:

  1. Create a script named `pre-commit` in your repository's `.git/hooks/` directory. This script will run before each commit and perform checks or scans. Here's a simple example of a pre-commit hook script that runs a code formatter and linter for Python projects using Black and Flake8:

      ```bash
      #!/bin/bash

      # Path to the Black executable
      BLACK_PATH="/path/to/black"

      # Path to the Flake8 executable
      FLAKE8_PATH="/path/to/flake8"

      # Run Black to format code
      $BLACK_PATH .

      # Run Flake8 to lint code
      $FLAKE8_PATH
      ```

      * Ensure the script is executable by running `chmod +x .git/hooks/pre-commit`.

  1. Commit the pre-commit hook script to your repository and push it to GitLab.

## Using CI pipeline to scan repositories on GitLab

1. Create or update your `.gitlab-ci.yml` file to include a job that runs the same checks as the previous pre-commit hook. This ensures that code pushed to GitLab is also scanned during the Continuous Integration (CI) process. Here's an example configuration:

  ```yaml
  linting:
    stage: test
    image: python:3.8
    script:
      - /path/to/black .
      - /path/to/flake8
  ```

    * Replace `/path/to/black` and `/path/to/flake8` with the actual paths to the Black and Flake8 executables.
    * Ensure that your GitLab CI pipeline is enabled and configured to run on every commit or merge request.

## Scanning incoming merge requests on GitLab

* To scan incoming pull requests (merge request) on GitLab for code quality, security vulnerabilities, and other issues, you can set up GitLab CI jobs that run on every pull request. Here's a step-by-step guide:

  1. Determine the checks you want to perform on incoming pull requests. This could include:
      * Code linting.
      * Unit tests.
      * Security scans.
      * Code coverage analysis.
      * Dependency vulnerability scanning.
      * Custom checks specific to your project.
  1. Create or update your `.gitlab-ci.yml` file to include jobs that run the necessary checks. Define stages and jobs for each type of check you want to perform. The below code snippet is the example for this:

      ```yaml
      stages:          # List of stages for jobs, and their order of execution
        - build
        - test
        - deploy

      build-job:       # This job runs in the build stage, which runs first.
        stage: build
        script:
          - echo "Compiling the code..."
          - echo "Compile complete."

      unit-test-job:   # This job runs in the test stage.
        stage: test    # It only starts when the job in the build stage completes successfully.
        script:
          - echo "Running unit tests... This will take about 60 seconds."

      lint-test-job:   # This job also runs in the test stage.
        stage: test    # It can run at the same time as unit-test-job (in parallel).
        script:
          - echo "Linting code... This will take about 10 seconds."

      deploy-job:      # This job runs in the deploy stage.
        stage: deploy  # It only runs when *both* jobs in the test stage complete successfully.
        environment: production
        script:
          - echo "Deploying application..."
          - echo "Application successfully deployed."
      ```

        * The above is just a template that simulates the scanning of incoming merge requests in GitLab.

  1. Configure GitLab CI to run jobs only on pull requests(in GitLab, it is called as `merge_requests`). Modify the above code and add the only property below every stage:

      ```yaml
      ...

      build-job:       # This job runs in the build stage, which runs first.
        stage: build
        script:
          - echo "Compiling the code..."
          - echo "Compile complete."
        only:
          - merge_requests

      ...
      ```

  1. After the CI jobs complete, review the results in the GitLab merge request interface or in the **Pipelines** tab and **Jobs** tab. Address any issues found, and once you're satisfied with the changes, merge the pull request into the target branch.

## Automatically update dependencies on GitLab

* To automatically update dependencies on GitLab, leverage Continuous Integration (CI) pipelines along with dependency management tools like Pipenv, npm, Maven, or Composer. Here's a general guide along with an example using npm for javascript projects:

  1. Ensure your project is using a dependency management tool compatible with GitLab CI. For example, Pipenv for Python, npm for JavaScript, Maven for Java, or Composer for PHP.
  1. Create or update your `.gitlab-ci.yml` file to include a job that updates dependencies. The below code snippet is the example using npm for node projects.

      ```yaml
      stages:
        - update_dependencies
        - push_artifacts

      update_dependencies:
        stage: update_dependencies
        image: node:14
        script:
          - npm install -g npm-check-updates
          - ncu -u
          - npm install
        artifacts:
          paths:
            - package.json
            - package-lock.json

      push_artifacts:
        stage: push_artifacts
        image: alpine:latest
        dependencies:
          - update_dependencies
        script:
          - apk --no-cache add git
          - git config user.email "my-email@email.com"
          - git config user.name "ci-bot"
          - git remote add gitlab_origin https://oauth2:$ACCESS_TOKEN@gitlab.com/path-to-project.git
          - git add .
          - git commit -m "push back from pipeline"
          - git push gitlab_origin HEAD:main -o ci.skip # prevent triggering pipeline again

      ```

      * This configuration creates two jobs named `update_dependencies` and `push_artifacts` in two stage process. It uses the `node:14` Docker image, installs npm package `ncu`, and the `package.json` dependencies in the script. Just ensure that you also add `package.json` file the root of your repository.
      * The `push_artifacts` pushes the updates `package.json` and `package-lock.json` to the repo. The job runs only when triggered by a **Pipeline schedules**. Add a variable `ACCESS_TOKEN` with the value of Personal Access Token while you create a new schedule.
      * Add this file to the root of the project or use `Pipeline editor` in `Build` section to paste the above code

  1. Configure a pipeline schedule in your GitLab project settings to trigger these jobs at regular intervals using the below steps:
      1. Navigate to your project in GitLab.
      1. Go to **Build** > **Pipeline schedules**.
      1. Create a new schedule, set the frequency, and choose the branch.
      1. Add a variable with the Access Token value to avoid authentication issues.
  1. Monitor your pipeline runs to ensure that dependency updates are applied successfully. Review the Pipeline logs from the **Jobs** tab and any changes made to dependencies.
