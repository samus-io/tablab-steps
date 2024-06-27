# Clone our GitHub repository "tablab-steps" before starting

* First, navigate to [tablab-steps][1] repository and click the *Fork* button. This creates a personal copy of the repository under your GitHub account.
* Then, to clone the repository, open your terminal and run the following command, replacing `username` with your actual GitHub username:

  ```bash
  git clone https://github.com/<username>/tablab-steps.git
  ```

* Afterwards, you can optionally add the original repository as an upstream remote to keep your fork updated:

  ```bash
  git remote add upstream https://github.com/samus-io/tablab-steps.git
  ```

* Before making changes, switch to a new branch to keep your work organized. The branch convention to use is:
  * `lab/<lab-name>`: in case you want to create the entire set of Steps that will formalize a Lab.
  * `step/<step-name>`: if you simply want to create a single, independent Step.

  ```bash
  git checkout -b lab/sqli-in-nodejs
  ```

* Push your new branch to your fork with the `--set-upstream-to` option. This sets the branch to track the branch from your fork on GitHub, which helps in setting up pull requests later:

  ```bash
  git push --set-upstream origin lab/sqli-in-nodejs
  ```

* When the content is done, go to your fork on GitHub, click `New pull request` near your branch, and review your changes. You can push your changes to our `main` branch. Once ready, submit your pull request with a detailed title and description, explaining what Steps you have added. We will take it from here on out :slightly_smiling_face:
* Remember to write your name and your GitHub profile ID as attributes of the `properties.json` file of each Step to be able to reference your contribution on the platform.

[1]: https://github.com/samus-io/tablab-steps
