# Information disclosure via hardcoded data

* Hardcoded data like API keys or config values in frontend code can expose sensitive information to attackers via source inspection.

## Developers HTML comments

* Developers occasionally insert HTML comments during development to explain functionality, add notes, or highlight areas needing updates. If not properly removed during the frontend build process, these comments can remain visible through page source inspection.
* In some cases, comments can inadvertently reveal sensitive details like hidden directories, internal logic, or feature toggles, which can assist attackers in mapping out the application or discovering hidden entry points.
* The example below illustrates a comment containing a hidden admin path:

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Welcome</title>
  </head>
  <body>
    <h1>Welcome to the site</h1>
    <p>Select where you want to go:</p>

    <a href="/home">Home</a><br>
    <a href="/about">About</a><br>
    <a href="/contact">Contact</a><br>

    <!-- Path for admins -->
    <!-- <a href="/sup3r-s3cr3t-admin-login">Admin Login</a> -->

  </body>
  </html>
  ```

  * Even though the link is not displayed in the web application, the commented link discloses a sensitive route to anyone checking the source code.
* To prevent this type of information disclosure, avoid including sensitive paths, internal notes, or debug references in frontend comments, especially in production environments, and also ensure comments are stripped during the build process.

## Exposure authentication tokens or sensitive credentials

* Web applications often require API keys to interact with third-party services such as Google Maps, Firebase, or payment platforms. These API calls can sometimes originate from JavaScript in the browser, resulting in key exposure through the page source or network requests.
* If the exposed API key grants privileged access, it can be abused by an attacker for unauthorized actions or privilege escalation.
* The JavaScript snippet below illustrates an insecure approach by embedding a sensitive key directly in the frontend source code:

  ```javascript
  const API_KEY = "sk_live_9a8d7f6g5h4j3k2l1m0n";

  fetch(`https://example.tbl/api/v1/payment`, {
    method: 'GET',
    headers: {
      "Authorization": `Bearer ${API_KEY}`
    }
  })
  .then(response => response.json())
  .then(data => {
    // Process response
  })
  .catch(error => {
    console.error("Error fetching data:", error);
  });
  ```

  * In this example, this key could enable operations such as viewing financial details, editing records, or executing transactions.
* Secret keys or credentials that provide elevated access should never be included in frontend code as a standard security measure.

## Exercise to practice :writing_hand:

* The frontend code of the following web application is suspected of containing exposed sensitive information.
* The purpose of this exercise is to identify an API key and employ `curl` from the `Terminal` tab to interact with a protected endpoint using this schema:

  ```bash
  curl -H "Authorization: Bearer <api_key_value>" "$APP_URL/path/to/endpoint"; echo
  ```

  * Note the environment variable called `APP_URL` that holds the application's base URL, which can be used for sending requests.
* Upon making the request to the protected endpoint with a valid API key, press the `Verify Completion` button to confirm the exercise has been completed.

  @@ExerciseBox@@
