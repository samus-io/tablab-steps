# Writing format to follow and copyright restrictions

* Creating a Step on [tablab.io][1] is about delivering a concise, clear, and engaging learning experience. This guide focuses on the format and writing style essential for crafting an effective Step.

## Follow our writing style convention

* Use Markdown syntax for styling all writings.
* Describe concepts using bulleted lists with short, specific sentences, like this one.
* Every sentence should begin with a bullet point.
* Avoid long sentences. If needed, split them by meaning, concept or context.
* Avoid first-person sentences when explaining a concept, such as "Imagine you are running an online platform where...". Instead, the impersonal approach, like "It can be considered an online platform where..." should be used.

### Defining titles

* It's not necessary to add a colon (`:`) to the end of a title to introduce the bulleted list.
* Do not use capital letters for words that do not represent a concept. For example, the title "Use Case" should simply be "Use case." However, when using "Input Validation" in a title, since it represents a concept by itself, we should opt for "Input Validation overview" in capital letters, for instance.
* If you use bold text to referrer create as a semi-title, it's not necessary to use bold with colon (`:`).

### Using emojis

* :writing_hand: (`:writing_hand:`): is used to indicate to the learner that a practical exercise follows.
* :older_man: (`:older_man:`): is used to explain some concept that is related to the Step but is not specifically covered.
* :warning: (`:warning:`): is used when the learner must pay attention to an important section.

### Adding a table

* You can add tables when necessary. To do so, keep in mind that this is the format that our Markdown render processes:

  ```markdown
  |Column 1|Column 2|Column 3|
  |:--:|:--:|:--:|
  |Field 1|Field 2|Field 3|
  |Field 4|Field 5|Field 6|
  ```

### Adding an image

* When you want to add an image to the content to explain a concept in a more representative way, you first need get the image on your computer and then place it as a static file in the `/static/images/` folder that you will find in this repository.
* Once done, you can embed the image following the Markdown code as shown:

  ```markdown
  ![Image caption here][1]
  ```

  Afterwards, you just need to reference it at the end of the file like this:

  ```markdown
  [1]: /static/images/your-selected-image.png
  ```
  
  Note that the image path `/static/images/your-selected-image.png` refers to the absolute path where the image has supposedly been placed in this repository.
* See that the image names must follow the next pattern: `your-image.png`.
* **Important notice**: you can add any image you want, even if you didn't create it yourself. We will be in charge of creating a new image that represents exactly the same concept but in corporate format (styles and colors) and avoiding any copyright infringement.

### Adding links

* When you add some link you can use a similar format as the images.
* First, add the link with its title (.e.g [tablab.io][1]) using this format: `[tablab.io][1]`. Then, at the end of the page, add the URL:

  ```
  [1]: https://tablab.io
  ```

### Adding code snippets

* To insert code in Steps, you should enclose it with three backticks (```` ``` ````), and specify the programming language immediately after the opening backticks to enable syntax highlighting.
* Ensure there is a blank line before and after the code block to separate it from the surrounding text.
* If your text references the code directly, indent the code block to visually connect the text and the code, improving readability.

  ```html
  <h1>Hello World!</h1>
  ```

### Programming concepts

* The following concepts must be wrapped with backticks(`` ` ``):
  * HTTP headers: `Content-Type`, `Server`, `Host`.
  * HTTP methods: `GET`, `PUT`, `DELETE`.
  * Endpoints or paths: `/admin`, `/var/www/html`.
  * Web parameters: `/users?id=123`, `id=123`.
* Uses Camel case for endpoint or file names(e.g. `/deleteUser`, `userInvoice.pdf`).
* If you need to mention a domain name as an example, you should use `example.org`. Also, the domains must be wrapped with backticks.
  * In the case of an attacker's domain, `attacker.site` should be used and `victim.site` should be used for the victim's domain

### Using Visual Studio Code

* For those using Visual Studio Code, you will find in this repository configurations for several plugins designed to enhance your Markdown writing experience.
* To install the recommended extensions for this project, please follow these steps in Visual Studio Code:
  1. Launch Visual Studio Code loading the [tablab-steps][2] repository.
  1. Navigate to the *Extensions* view by pressing `Ctrl+Shift+X` (or `Cmd+Shift+X` on macOS).
  1. Type `@recommended` into the search bar.
  1. Click on the install button adjacent to the extensions listed under *Workspace Recommendations*.

## Respect copyright

* As a content creator, it's crucial to understand and respect copyright laws, ensuring you do not use or replicate sentences or texts from other websites or material.
* Just exchanging words for similar meanings in a sentence, without making any changes to the sentence structure or grammar, is still recognized as a form of plagiarism.
* AI tools can assist you in content creation, but texts directly produced by artificial intelligence systems are not allowed on [tablab.io][1].

[1]: https://tablab.io
[2]: https://github.com/samus-io/tablab-steps
