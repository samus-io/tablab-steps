# Information disclosure via hardcoded data

## Developers HTML comments

* During development, developers often leave HTML comments in the code to document functionality, leave notes, or flag areas for future updates.
* These comments are not visible in the rendered page but can be easily viewed by inspecting the page source.
* In some cases, comments may unintentionally expose sensitive information such as hidden directories, internal logic, or feature toggles.
* This type of disclosure can assist attackers in mapping out the application or discovering hidden entry points
* The following example shows a hidden admin path embedded in a comment:

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
    <!-- Admin path
    <a href="/sup3r-s3cr3t-admin-login">Admin Login</a>
    -->

  </body>
  </html>
  ```

* Even though this link is commented out, it still reveals the existence of a sensitive route to anyone viewing the source.
* To avoid this type of information disclosure, avoid including sensitive paths, internal notes, or debug references in frontend comments—especially in production environments.

## Exposure of sensitive API keys

* Web applications often require API keys to interact with third-party services such as Google Maps, Firebase, or payment platforms.
* In some cases, these API calls are made directly from JavaScript running in the browser, exposing the keys in the page source or network requests.
* If the exposed API key has permissions to perform privileged actions, an attacker could exploit it to gain unauthorized access or escalate privileges.
* The following JavaScript snippet demonstrates an insecure pattern where a sensitive key is hardcoded in the frontend:

  ```javascript
  const API_KEY = "sk_live_9a8d7f6g5h4j3k2l1m0n";

  fetch(`https://example.tbl/api/v1/payment`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${API_KEY}`
    }
  })
  .then(response => response.json())
  .then(data => {
    // Process response
  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });
  ```

* In this example, the key could allow actions such as viewing payment details, modifying data, or initiating transactions.
* To prevent sensitive key exposure, these types of requests should always be handled by the backend, which can securely store and use the API key without exposing it to the client.
* Frontend code should never contain secret keys or any credentials that can grant elevated access.
