# Types of XSS

## Reflected XSS

* It occurs when the malicious payload is sent to a web application, and it's immediately echoed back as the untrusted content. Then, as usual, the browser receives the code from the web server response and renders it.
* Victims bring the payload in their HTTP request to the vulnerable website, which means that the attacker has to trick the victim into starting a specially crafted request (e.g. clicking on a link) to the vulnerable website page.
* A simple example of vulnerable PHP code is:

  ```php
  <?php $name = @$_GET['name']; ?>
  Welcome <?=$name?>
  ```

## Stored XSS

* It occurs when the payload is sent to the vulnerable web server and then stored (e.g. a comment stored in the database). When a web page of the vulnerable website pulls the stored malicious code and puts it within the HTML output, it will deliver the XSS payload.
* It's the most useful for an attacker because by exploiting the website once, any visitor that visits the page will execute the malicious code and will be affected.
* Persistent XSS is capable of defacing a web page, altering the original appearance, for all visitors instead of reflected XSS, which would deface the appearance of the website only for the intended victim carrying the payload. This is why is the only form of XSS actually targeting the website itself.
* It's very dangerous in applications such as blogs, comment systems and social networks.

## DOM XSS

* It's a form of XSS that exists only within client-side code (typically JavaScript). It lives inside the `Document Object Model (DOM)` environment and doesn't reach server-side code.
* A web application can echo the welcome message in a different way than before:

  ```javascript
  <script>
    var w = "Welcome";
    document.getElementById('welcome').innerHTML = w + name;
  </script>
  ```

* Despite this, the DOM is a jungle, and finding this type of XSS is not the easiest of the tasks.
* DOM-based XSS can even be persistent if the malicious payload is saved by the web application within a cookie.
* It is also known as `Type-0` or `Local XSS`.

### Mutation-based XSS

* `Mutation-based XSS (mXSS)` is a kind of XSS vulnerability that occurs when the untrusted data is processed in the context of DOM's `innerHTML` property and get mutated by the browser, resulting as a valid XSS vector.
* mXSS happens when the attacker injects something that is seemingly safe but rewritten and modified by the browser while parsing the markup. This is due to the fact that the browser manipulates the content to fix and optimize errors with the HTML:
  * Input example:

    ```html
    <listing>&lt;img src=1 onerror=alert(1)&gt;</listing>
    ```

  * Output after parsing the markup:

    ```html
    <listing><img src=1 onerror=alert(1)></listing>
    ```

* There is an excellent client-side library for XSS sanitization called [DOMPurify][1].
  * [Write-up of DOMPurify 2.0.0 bypass using mutation XSS][2]

## Universal XSS

* It is a particular type of XSS that does not leverage the flaws against web applications but the browser, its extensions or its plugins.

[1]: https://github.com/cure53/DOMPurify
[2]: https://research.securitum.com/dompurify-bypass-using-mxss/
