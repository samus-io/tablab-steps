# Writing format to follow and copyright restrictions

* Creating a Step on [tablab.io][1] is about delivering a concise, clear, and engaging learning experience. This guide focuses on the format and writing style essential for crafting an effective Step.

## Follow our writing style convention

* Use Markdown syntax for styling all writings.
* Describe concepts using bulleted lists with short, specific sentences, like this one.
* Every sentence must begin with a bullet point, like this one.
* Avoid long sentences. If needed, split them by meaning, concept or context.
* All sentences must be impersonal. Avoid first-person sentences when explaining a concept, such as *"You can create groups..."*. Instead, the impersonal approach, like *"Groups can be created..."* should be used.
* Do not use capital letters after a colon (`:`), preferably continue with lowercase (e.g., *"Prepare: the application creates the statement..."*).
* In case of using bold, if the text preceding the colon no longer remains in bold, the bold must be ended before the colon (e.g., *"**Prepare**: the application creates the statement..."*).

### Defining titles

* It's not necessary to add a colon (`:`) to the end of a title to introduce a bulleted list.
* Do not use capital letters in titles, except for acronyms and the first letter (e.g., *"General best practices against SQL injections"*).

### Defining numeric enumerations

* A numerical enumeration should always use only the number `1`, as our markdown render automatically creates an order adding the appropriate numbers. This will make future changes much easier if needed. Here's an example:

  ```markdown
  1. First sentence
  1. Second sentence
  1. Third sentence
  1. Fourth sentence
  ```

* A numerical enumeration will only be used when certain things happen that need to be described in a certain order.

### Using emojis

* :writing_hand: (`writing_hand`): is used to indicate to the learner that a practical exercise follows.
* :older_man: (`older_man`): is used to explain some concept that is related to the Step but is not specifically covered.
* :warning: (`warning`): is used when the learner must pay attention to an important section.

### Adding a table

* Tables can be added when necessary. To do so, it is important to adhere to the format processed by our markdown render:

  ```markdown
  |Column 1|Column 2|Column 3|
  |:--:|:--:|:--:|
  |Field 1|Field 2|Field 3|
  |Field 4|Field 5|Field 6|
  ```

### Adding an image

* When adding an image to content to explain a concept more representatively, the image must first be obtained and then placed as a static file in the `/static/images/` folder found in the repository.
* Once completed, the image can be embedded using the markdown code as shown:

  ```markdown
  ![Image caption here][1]
  ```

  Afterwards, the reference should be included at the end of the file in the following format:

  ```markdown
  [1]: /static/images/your-selected-image.png
  ```
  
  Note that the image path `/static/images/your-selected-image.png` refers to the absolute path where the image has supposedly been placed in this repository.
* Image names should adhere to the following pattern: `image-name-here.png`.
* **Important notice**: any image can be added, even if it was not created by yourself. We will be in charge of creating a new image that represents exactly the same concept but in corporate format (styles and colors) and avoiding any copyright infringement.

### Adding a link

* Links should follow the same convention as images when being used.
* First, the link and its title should be included using this specified format: `[example.com][1]`.
* Then, at the end of the markdown code, the URL should be added:

  ```markdown
  [1]: https://example.com
  ```

### Adding code snippets

* Code inserted into Steps should be enclosed with three backticks (```` ``` ````) and the programming language should be specified immediately after the opening backticks to enable syntax highlighting:

    ``````markdown
    * Here's is an example:

      ```javascript
        console.log("Hello, world!");
      ```

    * This is another sentence.
    ``````

  * Notice a blank line before and after the whole code block to separate it from the surrounding sentences.
  * When text directly references the code as in the example provided, indent the code block to visually connect the previous introductory sentence and the code, improving readability (as the example does too).

### Technical specifications

* Most technical specifications must be enclosed in backticks (`` ` ``).
* Endpoints or filenames must employ *camelCase* (e.g., `/deleteUser`, `userInvoice.pdf`).
* When using a domain name as an example, always use the non-existent top-level domain `tbl` (`<domain-name>.tbl`).
  * Its recommended using the domains `domain.tbl` or `example.tbl`.
  * However, when discussing scenarios with attacker and victim domains, `attacker.tbl` and `victim.tbl` or `trusted.tbl` and `untrusted.tbl` can be used, instead of `domain.tbl` and `example.tbl`.
  * If you are explaining an image in the Step that contains domain names, use the domain names that you want to be in the image, we will create the image using the domain names used in the explanation.

#### Backticks usage examples

* Terminology and concepts (e.g., `JSON Web Token (JWT)`, `Same-Origin Policy (SOP)`).
* HTTP headers (e.g., `Content-Type`, `Server`, `Host`).
* HTTP methods (e.g., `GET`, `PUT`, `DELETE`).
* Endpoints or paths (e.g., `/admin`, `/var/www/html`).
* Web parameters (e.g., `/users?id=123`, `id=123`).

### Using Visual Studio Code

* In this repository, users of Visual Studio Code will discover configurations for a plugin aimed at improving their Markdown writing experience.
* To install the recommended extension for this project, please follow these steps in Visual Studio Code:
  1. Launch Visual Studio Code loading the [tablab-steps][2] repository.
  1. Navigate to the **Extensions** view by pressing `Ctrl+Shift+X` on Windows/Linux or `Cmd+Shift+X` on macOS.
  1. Type `@recommended` into the search bar.
  1. Click on the **Install** button adjacent to the extensions listed under **Workspace Recommendations**.

## Respect copyright

* As a content creator, understanding and respecting copyright laws is crucial, which involves avoiding using or replicating sentences or texts from other websites or materials.
* Just exchanging words for similar meanings in a sentence, without making any changes to the sentence structure or grammar, is still recognized as a form of plagiarism.
* AI tools can assist in content creation, but directly produced texts by artificial intelligence systems are not allowed on [tablab.io][1].

[1]: https://tablab.io
[2]: https://github.com/samus-io/tablab-steps
