# Finding XSS

* Look for all points where the application outputs data (totally or partially) supplied by the user and track it back to the source where is received.
  * If there is a correlation between both output-input and the user-supplied data is part of the output, then we have found a potential mount point for an XSS attack.
* Think of input as:
  * GET/POST variables.
  * Cookies.
  * HTTP headers.
* Then, try to inject HTML code into the input (e.g. the HTML `<plaintext>` tag, which instructs the browser to treat the remaining web page source as plain text, thus breaking the appearance of the site).
* Injecting the `<plaintext>` tag is still not indicative of the possibility of injection scripts, so later on, try to inject JavaScript code (e.g. the `<script>` tag).
  * When the browser encounters the `<script>` tag, it switches from the HTML parser to the JavaScript parser until the closing tag is found.
