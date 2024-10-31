# Finding Open Redirect

* Detecting open redirect vulnerabilities can sometimes be straightforward, but other times it can be more complex. Here's a structured approach to identifying and testing for these vulnerabilities in user's application.
* Apart from the below URL checks, check for saved cookies, AJAX request in the client side code, hidden form fields and even session tokens.

## Identify User-controlled URLs

* Look for URL parameters in the application that take user input and could be used to specify a redirection target. Common parameters include `url`, `redirect`, `return`, `next`, `goto`,`q`, `returnUrl`, `link`, `next`, `image_path`, `ret`, `toredirect`, `page`, `forward`, `file` etc.

### Where to look

* **Login redirects**: URLs where the application redirects users after login or logout.
* **Registration processes**: URLs used after user sign-up.
* **Banner click-throughs**: advertisements or internal promotional banners that redirect users.
* **Navigation links**: any functionality where the URL is included as a parameter in a request.

## Identify other parameters that can redirect

* Check all parameters that may accept URLs, especially those related to navigation, redirection after login or registration, and other user actions.

### Check for redirection

* Supply different URLs in the identified parameters to see if the application redirects to these URLs without validation.
* Check if the application performs the redirection to the supplied URL. If it does, it indicates a potential open redirect vulnerability.

### Test for Scheme-less URLs

* Use URLs that don’t specify a protocol, such as `//attacker.tbl`.
* Browsers interpret these as relative URLs, which can lead to redirects to external sites.

### Encode special characters

* Encode special characters to bypass basic filters or checks.
* For example, check adding `https://domain.tbl/login?redirect=%2F%2Fattacker.tbl`. The string `%2F%2F` is an encoded representation of `//`.

### Try different formats

* `Internationalized Domain Names (IDNs)` i.e. Use Unicode characters in domain names.
* Utilize unusual URL formats that might not be handled correctly by the application's validation logic.
* For example, check adding `https://domain.tbl/login?redirect=http://xn--e1awd7f.tbl` (where `xn--e1awd7f.tbl` is the punycode representation of an IDN).

### Use a URL shortening service

* Shortened URLs can sometimes bypass domain validation checks.
* Some applications might only validate the domain of the URL, not the final destination after redirection.
* For example, check adding `https://domain.tbl/login?redirect=https://example.tbl/shortened`, where `example.tbl` can be any URL shortening service.

## Common bypasses for Open Redirect vulnerabilities

* Attackers often use various bypass techniques to manipulate the redirection parameters and exploit open redirect vulnerabilities.

### Using Protocol-relative URLs

* An example for this is `//domain.tbl`.
* Browsers interpret `//` as a protocol-relative URL. If the base URL is `http://domain.tbl`,` //domain.tbl` will redirect to `http://domain.tbl`.

### Using multiple slashes

* An example for this is `////domain.tbl`.
* Similar to `//domain.tbl`, the browser will reduce multiple slashes to a single protocol-relative URL, leading to `http://domain.tbl`.

### Omitting protocol

* An example for this is `https:domain.tbl`.
* The missing slashes after `https:` might be ignored by some parsers, causing a redirect to `https://domain.tbl`.

### Escaping slashes

* An example for this is ` \/\/domain.tbl`.
* This uses escaped slashes, which some URL parsers might interpret as `//`, resulting in a protocol-relative URL leading to `http://domain.tbl`.

### Combining slashes and escaping

* An example for this is `/\/domain.tbl/`.
* Escaped characters might be interpreted as slashes, reducing to `//domain.tbl` and thus redirecting to `http://domain.tbl`.

### Using Unicode characters

* An example for this is `//domain%E3%80%82tbl` or `https://domain.tbl/redirect?url=\uFF04\uFF04attacker.tbl`.
* This uses URL encoding. `%E3%80%82` or `\uFF04` is the UTF-8 encoding for a Unicode character similar to a period(`.`), tricking some parsers into treating it as `domain.tbl`.

### Using Null Byte

* An example for this is `//domain%00.tbl`.
* The `%00` is a URL-encoded null byte. Some parsers might terminate the string early and interpret the URL as `domain.tbl`.

### Using Userinfo in URL

* An example for this is ` http://domain.tbl@attacker.tbl/`.
* The `@` symbol in URLs can be used for userinfo. Here, `http://domain.tbl@attacker.tbl/` appears to be a URL for `attacker.tbl` with `domain.tbl` as userinfo. The validation logic checks the URL and finds it starts with `http://domain.tbl`, so it assumes it’s safe and redirects to `attacker.tbl`.

### Using Data URIs

* An example for this is `data:text/html,<script>window.location="https://attacker.tbl";</script>`.
* Data URIs allow embedding data directly into HTML or CSS. By using a data URI with JavaScript code to redirect, attackers can bypass traditional URL filtering.

### Using Meta refresh

* An example for this is `<meta http-equiv="refresh" content="0;url=https://attacker.tbl">`.
* Meta refresh tags instruct the browser to automatically redirect to another URL after a specified time. Attackers can inject this tag into HTML content to perform redirection.

### Using Double URL encoding

* An example for this is `https://domain.tbl/redirect?url=%2568%2574%2574%2570%253A%252F%252F%252F%252F%252F%252F%252F%252Fattacker.tbl`.
* Double URL encoding converts reserved characters into their percent-encoded equivalents. By double encoding, attackers can bypass filters that decode the URL once.

### Using JavaScript in Event handlers

* An example for this is `<a href="#" onclick="window.location='https://attacker.tbl';return false;">Click Here</a>`.
* Attackers can inject JavaScript code directly into event handlers (e.g. `onclick`, `onmouseover`, etc.) to execute redirects when certain actions are triggered by the user.

### Using Unicode Homoglyphs

* An example for this is `https ：//ⅾomain.tЬｌ/ｒedirect?url=ɑttɑⅽκeｒ.tЬｌ`.
* Attackers can use Unicode characters that resemble ASCII characters (homoglyphs) to deceive users and bypass some URL filters that only consider ASCII characters.

### Using HTML entities

* An example for this is `https://domain.tbl/redirect?url=https://attacker&#46;tbl`.
* Attackers can use HTML entities to obfuscate URLs, making it harder for basic filters to detect and block malicious redirection.
