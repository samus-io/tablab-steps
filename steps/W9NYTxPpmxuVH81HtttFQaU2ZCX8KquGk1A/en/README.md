# Preventing Open Redirect in NodeJS

* let's build a Node.js application that is hosted on `localhost` with `/redirect?url=` as the redirection path and query string parameter. It only allows for valid and whitelisted absolute URLs and also allows for the relative URLs that belong to allowed domains. Below sections will explain to implement the preventive measures to avoid Open Redirection.

## Maintaining Server-side URL whitelist with URL validation

* First, set up a whitelist and validate the input URL against common bypasses:
  * **URL whitelist**: define a whitelist of allowed URLs using a dictionary.
  * **Redirect handling**: In the `/redirect` route:
    * Retrieve the target URL from the query parameters.
    * If the URL is valid, perform the redirect; otherwise, return an error.
* This setup ensures that any user-controllable input is validated against known bypass techniques, enhancing the security of the redirection function.

```javascript
const express = require('express');
const app = express();

// Whitelist of allowed URLs
const urlWhitelist = ['https://domain.tbl/', 'https://example.tbl/'];

// Checking for valid URLs
function isValidUrl(fullUrl) {
  return urlWhitelist.includes(fullUrl);
}

app.get('/redirect', (req, res) => {
  const target = req.query.url; 
  try {
     const url = new URL(target);
     if (url && isValidUrl(`${url.protocol}//${url.hostname}/`)) {
       res.redirect(`${url.protocol}//${url.hostname}/`);
     } else {
       res.status(400).send('Invalid redirect URL');
     }
  } catch(err) {
     res.status(400).send('Invalid redirect URL');
  }
  
});

```

## Canonicalize URLs

* To canonicalize URLs in Node.js, you can use **url** and **path** modules, which provide methods to parse, format, and normalize URLs. Below is an example code snippet demonstrating how to canonicalize a URL using the **url** and **path** modules.

```javascript
const url = require('url');
const path = require('path');

// This function normalizes the URL path and converts all the back slashes to forward slash
function getCanonicalUrl(inputUrl) {
  const parsedUrl = url.parse(inputUrl);
  const normalizedPathname = path.normalize(parsedUrl.pathname).replaceAll(/[\\]+/gi,'/');

  const canonicalUrl = url.format({
    protocol: parsedUrl.protocol,
    host: parsedUrl.host,
    pathname: normalizedPathname,
    search: parsedUrl.search,
  });

  return canonicalUrl;
}
```

## Using URLs Relative to the Web Root

* Validate that the URL starts with a slash character, has valid ASCII characters and prepend the domain:

```javascript
app.get('/redirect', (req, res) => {
  const target = req.query.url;

   // Check if it starts with forward slash and has valid ASCII character
  if (!(/^\/(?!\/)[^\s]*$/).test(target)) {
    return res.status(400).send('Invalid redirect URL');
  }

  const fullUrl = `http://domain.tbl${target}`;
  res.redirect(fullUrl);
});

```

## Using Absolute URLs with Domain Validation

* If it is an absolute URL then verify that the user-supplied URL begins with the domain name and allowed whitelisted domains.

```javascript
const allowedDomains = ['domain.tbl', 'example.tbl'];

// This returns TRUE for allowed domains only
function isAllowedDomain(url) {
  return allowedDomains.some(domain => url.startsWith(domain));
}

app.get('/redirect', (req, res) => {
  const target = req.query.url;
  try{
    const url = new URL(target);
    if (!isAllowedDomain(url.hostname)) {
      return res.status(400).send('Invalid redirect URL');
    }
  } catch(err) {
      return res.status(400).send('Invalid redirect URL');
  }

  res.redirect(target);
});

```

## Intermediary Page for Confirmation

* To implement an intermediary page for confirmation, you can create a separate route where users are redirected first before proceeding to the final destination. This page will display a message informing users that they are leaving the site and provide a link to confirm redirection.

```javascript
app.get('/redirect', (req, res) => {
  const target = req.query.url;
  try{
    const url = new URL(target);
    if (!isAllowedDomain(url.hostname)) {
      return res.status(400).send('Invalid redirect URL');
    }
  } catch(err) {
      return res.status(400).send('Invalid redirect URL');
  }

  res.send(`
    <html>
      <body>
        <p>You are about to leave our site and be redirected to: ${target}</p>
        <a href="${target}">Click here to proceed</a>
      </body>
    </html>
  `);
});

```

* Users will first land on this page and must click the provided link to confirm redirection to the final destination.

## Putting it all together

* The below code can listen at `http://localhost:3000/redirect?url=example.tbl`, where one can pass any relative or absolute URL to `url` parameter. It will allow for the listed redirection URLs only. For relative URL, it is prepending the `domain.tbl` domain as an example.

```javascript
const express = require('express');
const url = require('url');
const path = require('path');
const app = express();

const urlWhitelist = ['https://domain.tbl/', 'https://example.tbl/'];

function isValidUrl(relativeUrl) {

  // Regular expression to match valid relative URLs starting with a slash
  const relativeUrlPattern = /^\/(?!\/)[^\s]*$/;
  if (!relativeUrlPattern.test(relativeUrl)) {
    return false;
  }

  return true;
}

// Checking for allowed URLs or domains
function isAllowedUrl(fullUrl) {
  return urlWhitelist.includes(fullUrl)
}

// Building the canonical URL from the user given URL
function getCanonicalUrl(inputUrl) {
  const parsedUrl = url.parse(inputUrl);
  const normalizedPathname = path.normalize(parsedUrl.pathname).replaceAll(/[\\]/gi,'/');

  const canonicalUrl = url.format({
    protocol: parsedUrl.protocol,
    host: parsedUrl.host,
    pathname: normalizedPathname,
    search: parsedUrl.search,
  });

  return canonicalUrl;
}

// Listening for redirection request
app.get('/redirect', (req, res) => {
  const target = req.query.url;
  const inputUrl = getCanonicalUrl(target);
  if (inputUrl  && isAllowedUrl(inputUrl)) {
      res.send(`
        <html>
          <body>
            <p>You are about to leave our site and be redirected to: ${fullUrl}</p>
            <a href="${fullUrl}">Click here to proceed</a>
          </body>
        </html>
      `);
  } else if (inputUrl && isValidUrl(inputUrl)) {
    const appendedFullUrl = `http://domain.tbl${inputUrl}`;
    res.send(`
        <html>
          <body>
            <p>You are about to leave our site and be redirected to: ${appendedFullUrl}</p>
            <a href="${appendedFullUrl}">Click here to proceed</a>
          </body>
        </html>
      `);
  } else {
    res.status(400).send('Invalid redirect URL');
  }
});

// Start the server
app.listen(3000, () => {
  console.log('Server running on port 3000');
});

```
