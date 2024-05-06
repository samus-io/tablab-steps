# Implementing Git security best practices on GitHub

## Steps to enable and enforce 2FA on GitHub

* To set up two-factor authentication (2FA) on GitHub, you can choose from several methods, each with simple steps. Here are the steps for each method:

### Configuring Two-Factor Authentication using a TOTP App

1. Download a TOTP app to your phone or desktop.
2. Go to **Settings** > **Password and authentication** on GitHub.
3. Click Enable two-factor authentication.
4. Scan the QR code with your TOTP app or manually enter the TOTP secret.
5. Enter the authentication code from the app to verify.
6. Download and save your recovery codes.
7. Enable two-factor authentication after saving recovery codes.

### Configuring Two-Factor Authentication using Text Messages

1. Go to **Settings** > **Password and authentication** on GitHub.
2. Click **Enable two-factor authentication**.
3. Complete the CAPTCHA challenge.
4. Enter your mobile phone number and select your country code.
5. Receive a text message with a security code.
6. Enter the code on GitHub to verify.
7. Download and save your recovery codes.
8. Enable two-factor authentication after saving recovery codes.

### Configuring Two-Factor Authentication using a Passkey

1. Ensure you've already configured 2FA via a TOTP app or SMS.
2. Go to **Settings** > **Password and authentication** on GitHub.
3. Under Passkeys, click **Add a passkey**.
4. Authenticate with your password if prompted.
5. Follow the steps outlined by the passkey provider.
6. Review the confirmation and click Done.

### Configuring Two-Factor Authentication using a Security Key

1. Ensure you've already configured 2FA via a TOTP app or SMS.
2. Insert a WebAuthn compatible security key.
3. Go to **Settings** > **Password and authentication** on GitHub.
4. Click **Add** or **Edit** next to **Security keys**.
5. Register a new security key and follow the prompts.
6. Confirm that you've downloaded and can access your recovery codes.

### Configuring Two-Factor Authentication using GitHub Mobile

1. Install GitHub Mobile and sign in to your account.
2. After signing in, you can use your device for 2FA without relying on TOTP.
3. If you lose access to GitHub Mobile in the future, you can still use other 2FA methods.

* Choose the method that best suits your preferences and follow the simple steps to enable two-factor authentication on GitHub, enhancing the security of your account.

## Limit access to repositories

* To limit access to repositories in GitHub, follow these steps:

1. Navigate to the repository in GitHub that you want to limit access to.
2. Click on the **Settings** tab located on the repository's menu bar.
3. In the settings menu, find the **Manage access** or **Collaborators** section.
4. If you want to grant specific individuals access to the repository, you can invite them as collaborators by entering their GitHub usernames or email addresses.
5. If you want to restrict access to specific individuals or teams within your organization, set the repository visibility to **Private** instead of **Public**. This limits access to only those users who have been explicitly granted access as collaborators or members of teams with access permissions.
6. For existing collaborators, you can adjust their permissions to control what actions they can perform within the repository. GitHub provides options to set permissions such as read-only access, write access, or administrative privileges.
7. If you need to revoke access for certain collaborators, you can remove them from the repository's access list.
8. If you are using GitHub organizations, you can manage access to repositories through teams. You can create teams within your organization and grant them specific access permissions to repositories.

### Create User Groups to limit Access

* GitHub does not have a built-in feature for creating user groups directly within the platform. However, you can leverage teams within GitHub organizations to achieve similar functionality. Here's how to create user groups using teams within GitHub organizations:

1. If you haven't already, create an organization on GitHub by navigating to your profile, clicking on the **Your Organizations** tab, and then selecting **New organization**. Follow the prompts to create the organization.
2. Once the organization is created, navigate to its settings by clicking on the organization's name and then selecting **Settings**. Go to **Authentication Security** tab and eanble 2FA for everyone. In **Member Privilege** tab, set the **Base permissions** to **read** only by default.
3. In the organization settings, click on the **Teams** tab to manage teams within the organization.
4. Click on the **New team** button to create a new team within the organization. Give your team a descriptive name that reflects its purpose or the group of users it will include.
5. Click on **Add member** and invite people on GitHub, Choose the appropriate permissions for the team members, such as read access, write access, or administrative privileges for repositories within the organization using **People** tab.
6. Specify which repositories the team members will have access to. You can grant access to specific repositories or add teams within the organization by navigating to repo **Settings > Access >  Collaborators & teams**.
7. Under **Manage access**, next to the team or person whose role you'd like to change, select the Role dropdown menu, and click a new role.

## Steps to Rotate SSH Tokens and Personal Keys in GitHub

1. **Generate New SSH Key:** If you're rotating SSH keys, generate a new SSH key pair using the ssh-keygen command on your local machine.
2. **Update SSH Key on GitHub:** Go to your GitHub account settings, navigate to the SSH and GPG keys section, and delete the old SSH key. Then, add the new SSH public key by clicking on **New SSH key** and pasting the contents of the newly generated public key.
3. **Update Personal Access Tokens:** Go to your GitHub account settings, navigate to the Developer settings section, and click on **Personal access tokens**. Revoke the old personal access token and generate a new one with the necessary permissions.
4. **Update Git Configurations:** If you use Git credentials or SSH keys in your local Git configurations, update them to use the new credentials or keys.

### Automate token and key rotation

1. **Use GitHub Actions:** Set up GitHub Actions workflows to periodically rotate SSH tokens and personal access tokens. You can create workflows that use the GitHub API to generate new tokens and keys and update them in your account settings.
2. **Leverage CI/CD Pipelines:** If you use CI/CD pipelines for your projects, incorporate token and key rotation tasks into your pipeline scripts. Use GitHub API calls or command-line tools to automate the generation and update of tokens and keys.
3. **Implement Scheduled Jobs:** Use external scheduling tools or services to trigger token and key rotation tasks at regular intervals. You can write scripts or use existing tools to automate the rotation process and integrate them with your GitHub account via the GitHub API.
4. **Monitor and Alert:** Set up monitoring and alerting mechanisms to notify you of any issues or failures during the token and key rotation process. Monitor logs, API responses, and account activity to ensure that rotation tasks are executed successfully.

* Here's an example of how to automate the rotation of personal access tokens in GitHub using GitHub Actions:

```bash
name: Rotate Personal Access Token

on:
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC

jobs:
  rotate-token:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v2

      - name: Rotate Token
        run: |
          # Generate a new personal access token
          NEW_TOKEN=$(gh auth refresh-token --scopes <scopes> --with-token <current_token>)
          
          # Update the token in GitHub settings using GitHub API
          curl -X PATCH \
            -H "Authorization: token <github_token>" \
            -d '{"token": "'"$NEW_TOKEN"'"}' \
            https://api.github.com/user/token

        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

```

* To run the above GitHub Actions workflow for rotating personal access tokens:

1. In your GitHub repository, navigate to the `.github/workflows` directory(create it if it doesn't exist). Create a new YAML file (e.g., rotate-token.yml).
2. Copy the example GitHub Actions workflow provided above. Paste it into the newly created YAML file (rotate-token.yml).
3. Replace `<scopes>` with the desired scopes for the new personal access token. Replace `<current_token>` with your current personal access token. Replace `<github_token>` with a personal access token that has the repo scope (you can create one in your GitHub account settings).
4. Commit the changes to the repository. Push the changes to GitHub.
5. GitHub Actions will automatically execute the workflow according to the schedule specified (0 0 ** *, which runs daily at midnight UTC). You can monitor the workflow's execution by navigating to the **Actions** tab in your repository on GitHub.

## Tracking Activities via Audit Logs on GitHub

1. Navigate to your GitHub organization settings by clicking on your profile photo, then selecting **Settings**, and choosing the organization.
2. Enable Audit Logging: In the organization settings, locate the audit log section. Enable audit logging to start recording activities within your organization. GitHub Enterprise Cloud and GitHub Enterprise Server offer audit log capabilities.You can enable to view IP addresses of current members for organization audit log events.
3. Once audit logging is enabled, you can view audit logs to track various activities such as user logins, repository access, permission changes, and more. Audit logs provide detailed information about who performed an action, what action was taken, and when it occurred.

### Syncing Audit Log Service to Notification Channel

1. Select an audit log service that integrates with GitHub and offers notification capabilities. For this example, we'll use Loggly.
2. Access the settings or configuration options of your chosen audit log service. Look for GitHub integration options or methods to ingest GitHub audit logs. For example, To integrate GitHub audit logs with the Loggly app:

* If you don't already have one, sign up for a Loggly account at loggly.com.
* Log in to your Loggly account. Navigate to the "Source Setup" tab. Copy the Customer Token, which you'll use to send logs to Loggly.
* In your GitHub repository, go to the Settings tab. Select **Webhooks** from the left menu. Click on the **Add webhook** button. In the **Payload URL** field, enter the Loggly HTTP/S Event Endpoint. This endpoint should look like `https://logs-01.loggly.com/inputs/{CUSTOMER_TOKEN}/tag/http/`.
  Set the Content type to application/json. In the **Which events would you like to trigger this webhook?** section, select the audit events you want to log. Click on the **Add webhook** button to save your settings.
* Perform actions in your GitHub repository that trigger the selected audit events. Go back to Loggly and navigate to the **Search** tab. Search for the logs using the source name or any other identifying information.

3. Determine the notification channel where your team prefers to receive alerts. This could be a Slack channel, email distribution list, or a dedicated communication platform. For example, Decide on the Slack channel where you want to receive audit log notifications. let's use #audit-logs.
4. Follow the instructions provided by your audit log service to set up integration with your chosen notification channel. For example, In Slack go to the channel settings and select **Add an app or integration**. Search for and install the Loggly app. Follow the prompts to authorize the Loggly app and configure the integration with your Loggly account. Enter the **HTTP Event Collector token** generated earlier as the endpoint for Loggly to send audit log data.
5. Perform testing to ensure that the integration between the audit log service and the notification channel is functioning correctly. Trigger test events in GitHub or the audit log service and verify that notifications are delivered promptly to the designated channel.

## How to backup the Github hosting environment?

1. Decide which repositories you want to backup.
2. Choose between manual or automated backup.
    * **Manual Backup:** Download repository files from GitHub or clone repositories using Git commands.
    * **Automated Backup:** Write a script or use a third-party tool to automate backups.
Schedule backups to run regularly based on your needs.
3. Keep backup files in a secure location to prevent data loss or unauthorized access.
4. Regularly test backup and restore procedures to ensure they work correctly.
Monitor: Keep an eye on the backup process and set up alerts for any issues.

## Using Private repositories on GitHub

* To disable public repositories on GitHub, follow these steps:

1. Sign in to your GitHub account and Open your repository.
2. Scroll down to the **Features** or **Danger Zone** section in Settings tab.
3. Find the option labeled **Change Repository visibility**.
4. Choose the option to set the default repository visibility to **Private**.

* For Organizations, you can allow members to create only Private Repositories in GitHub Entreprise version:

1. In the upper-right corner of GitHub.com, select your profile photo, then click  **Your organizations**.
2. Next to the organization, click **Settings**.
3. In the **Access** section of the sidebar, click **Member privileges**.
4. Under **Repository creation**, select one or more options and save.

## How to disable forking on private repositories in Github Organizations?

* You can disable or enable the forking of Private repositories.

1. Open Your Organization and navigate to the Organization you want.
2. Click of the Repositories tab and select your repository.
3. Go to **Settings** > **Member privileges**.
4. Under **Repository forking**, keep forking of private repositories disabled.

* Note that you cannot perform this on any Public repositories and Private repositories of your Github Account which do not belong to any organization.

## Steps to ensure code branch protection on GitHub

* To set up branch protection rules in GitHub, follow the steps below:

1. Navigate to your GitHub repository, and go to the **Settings** tab.
2. In the left sidebar, click **Branches**.
3. Under Branch protection rules, click **Add rule**.
4. In the **Branch name pattern** field, enter the name of the branch you want to protect.
5. Under Protect matching branches, select the requirements you want to enforce.
    * **Require a pull request before merging:** When enabled, all commits must be made to a non-protected branch and submitted via a pull request before they can be merged into a branch that matches this rule.
    * **Require status checks to pass before merging:** When enabled, commits must first be pushed to another branch, then merged or pushed directly to a branch that matches this rule after status checks have passed.
    * **Require conversation resolution before merging:** When enabled, all conversations on code must be resolved before a pull request can be merged into a branch that matches this rule. Learn more about requiring conversation completion before merging.
    * **Require signed commits:** Commits pushed to matching branches must have verified signatures.
    * **Require linear history:** Prevent merge commits from being pushed to matching branches.
    * **Require deployments to succeed before merging:** Choose which environments must be successfully deployed to before branches can be merged into a branch that matches this rule.
    * **Lock branch:** Branch is read-only. Users cannot push to the branch.
    * **Do not allow bypassing the above settings:** The above settings will apply to administrators and custom roles with the **bypass branch protections** permission.
    * **Allow force pushes:** Permit force pushes for all users with push access.
    * **Allow deletions:** Allow users with push access to delete matching branches.
6. Click **Create** to save your new branch protection rule.

## How to Sign commits on GitHub?

* You will use GPG to sign commits. GPG (GNU Privacy Guard) is widely used for cryptographic operations, including signing messages and files. While GPG is complex and has various functionalities, signing Git commits is relatively straightforward once it's set up.

* GPG facilitates the distribution of public keys, which are identified by an ID and typically associated with an email address.
* Here are the steps to follow:

### Install GPG

1. Install Git command line tool for Git related operations beacuse it come pre-installed with GPG or To install GPG, follow these steps:
    * **For Windows**: Download the Gpg4win distribution from the GPG website and follow the installation instructions.
    * **For macOS**: Install Homebrew if you haven't already. Open Terminal and run `brew install gpg`.
    * **For Linux**: Most Linux distributions come with GPG pre-installed. If not, you can install it from your distribution's official repositories.

#### Additional Configuration for Linux and macOS

1. Enable the GPG agent to avoid typing the secret key’s password every time:
   * Add `use-agent` to `~/.gnupg/gpg.conf`.
2. Add the following lines to your profile file (`~/.bashrc`, `~/.bash_profile`, `~/.zprofile`, etc.):

   ```bash
   export GPG_TTY=$(tty)
   gpgconf --launch gpg-agent
   ```

3. Restart your shell or run `source ~/.bashrc` (or equivalent) to apply the changes.

* These steps will ensure that GPG is installed and properly configured on your system.

### Generate a GPG Key

* To generate a GPG key pair, follow these steps:

1. Open your terminal or command prompt.
2. Run the following command to generate a new GPG key pair:

   ```bash
   gpg --full-gen-key
   ```

3. When prompted, choose the following options:
   * Kind of key: Type 4 for RSA (sign only).
   * Keysize: Enter 4096.
   * Expiration: Choose a reasonable value, for example, 2y for 2 years.
4. Follow the prompts to provide:
   * Your real name (you can use your GitHub username).
   * Email address (you can use the @users.noreply.github.com email generated by GitHub).
   * Passphrase: Type a passphrase to encrypt your secret key on disk.

5. After generating the key pair, verify it was created by running:

   ```bash
   gpg --list-secret-keys --keyid-format SHORT
   ```

    * You should see output similar to the example provided, confirming your key ID and details.

6. To confirm that GPG is working and able to sign messages, run:

   ```bash
   echo "hello world" | gpg --clearsign
   ```

7. If your GPG agent encounters issues, you can restart it with:

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

2. Make sure the same email address is added to your GPG key.
3. Upload your public GPG key to GitHub.
   * Generate your public key:

     ```bash
     gpg --armor --export <keyId>
     ```

   * Copy the output, which starts with `-----BEGIN PGP PUBLIC KEY BLOCK-----` and ends with `-----END PGP PUBLIC KEY BLOCK-----`.
   * Go to the "SSH and GPG keys" settings page on GitHub.
   * Click on **New GPG key** and paste your public key.

### Configure Git to sign your commits

* Once you have your private key, you can configure Git to sign your commits using.

```bash
git config --global user.signingkey <keyId>
```

* Now, you can sign Git commits and tags by adding the `-S` flag when creating a commit.

```bash
git commit -S -m <your commit message>
```

* And, creating a tag with `git tag -s`.
* Use below command in Git to automatically sign all your commits

```bash
git config --global commit.gpgSign true
git config --global tag.gpgSign true
```

## Using Pre-commit hook to scans repositories on GitHub

* Here are the steps to set up and use a client-side pre-commit hook in your Git repository:

1. Open your terminal or command prompt and navigate to the root directory of your Git repository.
2. Inside the `.git/hooks` directory of your repository, create a new file named `pre-commit`. This file will contain the script for your pre-commit hook.
3. Open the `pre-commit` file in a text editor and write the script to execute your pre-commit checks. This script will run every time you attempt to make a commit.

### Example pre-commit hook script

```bash
    #!/bin/bash
        
    # Run linters
    echo "Running linters..."
```

4. Ensure that the `pre-commit` script is executable by running the following command:

  ```bash
  chmod +x .git/hooks/pre-commit
  ```

5. Make some changes to your files and attempt to commit them using Git. The pre-commit hook should automatically run before the commit is finalized. If any of your pre-commit checks fail (e.g., linting errors), the commit will be aborted, and you'll need to address the issues before committing again.
6. Customize the pre-commit hook script to include additional checks or actions tailored to your project's requirements. You can incorporate linting, formatting, testing, or any other checks that you deem necessary.

## Scanning incoming pull requests on GitHub

* To set up scanning for incoming pull requests on GitHub, you can use GitHub Actions to automate the process. Here are the steps:

1. In your repository, create a directory named `.github/workflows`. Inside this directory, create a YAML file, for example, `scan-pr.yml`. This file will define your GitHub Actions workflow.
2. In the YAML file, define the workflow to scan incoming pull requests. You can use the `pull_request` event trigger to specify when the workflow should run.

### Example workflow file (`scan-pr.yml`)

```yaml
     name: Scan Pull Requests

     on:
       pull_request:
         types: [opened, synchronize]

     jobs:
       scan:
         runs-on: ubuntu-latest

         steps:
           - name: Checkout code
             uses: actions/checkout@v2

           - name: Run scanning tool
             # Replace this with the command to run your scanning tool
             run: |
               # Example command to run a security scanning tool
               npm install --save-dev snyk
               npx snyk test
```

3. In the `on` section of the workflow file, specify the conditions under which the workflow should run. For example, you might want it to trigger when a pull request is opened or when changes are synchronized with the base branch.
4. Inside the `jobs` section, define the steps to be executed as part of the workflow. This typically includes checking out the code and running the scanning tool. Replace the placeholder commands with the actual commands required to run your scanning tool. For example, if you're using a security scanning tool like Snyk, you would install it and then run the `snyk test` command.
5. Commit and push the workflow file (`scan-pr.yml`) to your GitHub repository.
6. With the workflow file in place, GitHub Actions will automatically run the scanning tool whenever a pull request is opened or changes are synchronized with the base branch.
7. After each pull request event, you can view the workflow results in the **Checks** tab of your GitHub repository. This will show whether the scanning tool passed or failed.

## Automatically update dependencies on GitHub

* To automatically update dependencies on GitHub, you can use GitHub Actions to create a workflow that periodically checks for updates and automatically creates pull requests to update dependencies. Here are the steps:

1. In your repository, create a directory named `.github/workflows`. Inside this directory, create a YAML file, for example, `update-dependencies.yml`. This file will define your GitHub Actions workflow.
2. In the YAML file, define the workflow to automatically update dependencies. You can use scheduled events (`schedule`) to trigger the workflow at specified intervals.

### Example workflow file (`update-dependencies.yml`)

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

3. In the `on` section of the workflow file, specify the schedule for triggering the workflow. You can use cron syntax to define the schedule. For example, `'0 0 * * *'` runs the workflow every day at midnight UTC.
4. Inside the `jobs` section, define the steps to be executed as part of the workflow. This typically includes checking out the code, updating dependencies, committing the changes, and pushing them back to the repository. Replace the placeholder commands with the actual commands required to update dependencies. For example, if you're using npm, you can use `npm-check-updates` (`ncu`) to update dependencies.
5. Commit and push the workflow file (`update-dependencies.yml`) to your GitHub repository.
6. After each scheduled event, you can view the workflow results in the **Actions** tab of your GitHub repository. This will show whether the dependency updates were successful or encountered any issues.

* By setting up this GitHub Actions workflow, you can automate the process of updating dependencies in your project, ensuring that you're always using the latest versions and staying up-to-date with security patches and improvements.
