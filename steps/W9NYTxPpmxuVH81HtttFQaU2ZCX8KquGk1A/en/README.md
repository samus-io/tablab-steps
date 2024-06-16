# Preventing Open Redirect in NodeJS

* let's build a Node.js application that is hosted on `localhost` with `/redirect?url=` as the redirection path and query string parameter. It only allows for valid and whitelisted absolute URLs and also allows for the relative URLs that belong to allowed domain. Below sections will explain the preventive measures to avoid Open Redirection.

## Maintaining Server-side URL whitelist with URL validation

* First, set up our whitelist and validate the input URL against common bypasses:
  * **URL whitelist**: We define a whitelist of allowed URLs using a dictionary.
  * **Redirect handling**: In the `/redirect` route:
    * Retrieve the target URL from the query parameters.
    * If the URL is valid, perform the redirect; otherwise, return an error.
* This setup ensures that any user-controllable input is validated against known bypass techniques, enhancing the security of the redirection function.

```js
const express = require('express');
const url = require('url');
const app = express();

// Whitelist of allowed URLs
const urlWhitelist = ['https://www.google.com/', 'https://www.example.com/'];

function isValidUrl(fullUrl){
  return urlWhitelist.includes(fullUrl);
}

app.get('/redirect', (req, res) => {
  const target = req.query.url;

  if (target && isValidUrl(target)) {
    res.redirect(fullUrl);
  } else {
    res.status(400).send('Invalid redirect URL');
  }
});

// Start the server
app.listen(3000, () => {
  console.log('Server running on port 3000');
});

```

## Canonicalize URLs

* To canonicalize URLs in Node.js, you can use **url** and **path** modules, which provides methods to parse, format, and normalize URLs. Below is an example code snippet demonstrating how to canonicalize a URL using the **url** and **path** modules.

```js
const url = require('url');
const path = require('path');

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

* Validate that the URL starts with a slash character plus has valid Ascii characters and prepend the domain:

```js
app.get('/redirect', (req, res) => {
  const target = req.query.url;

  if (!target.startsWith('/') && !(/[^\x00-\x7F]+/).test(target)) {
    return res.status(400).send('Invalid redirect URL');
  }

  const fullUrl = `http://yourdomainname.com${target}`;
  res.redirect(fullUrl);
});

```

## Using Absolute URLs with Domain Validation

* If it is an absolute URL then verify that the user-supplied URL begins with the domain name and allowed whitelisted domains.

```js
const allowedDomains = ['http://yourdomainname.com', 'https://anotherdomain.com'];

function isAllowedDomain(url) {
  return allowedDomains.some(domain => url.startsWith(domain));
}

app.get('/redirect', (req, res) => {
  const target = req.query.url;

  if (!isAllowedDomain(target)) {
    return res.status(400).send('Invalid redirect URL');
  }

  res.redirect(target);
});

```

## Intermediary Page for Confirmation

* To implement an intermediary page for confirmation, you can create a separate route where users are redirected first before proceeding to the final destination. This page will display a message informing users that they are leaving the site and provide a link to confirm redirection.

```js
app.get('/redirect', (req, res) => {
  const target = req.query.url;

  if (!isAllowedDomain(target)) {
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

```js
const express = require('express');
const url = require('url');
const path = require('path');
const app = express();

const urlWhitelist = ['https://www.google.com/', 'https://www.example.com/'];

function isValidUrl(relativeUrl){
  // Regular expression to match Ascii characters
  const pattern = /[^\x00-\x7F]+/;
  return pattern.test(relativeUrl);
}

function isAllowedUrl(fullUrl){
  return urlWhitelist.includes(fullUrl)
}

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

app.get('/redirect', (req, res) => {
  const target = req.query.url;
  const fullUrl = getCanonicalUrl(target);

  if (fullUrl  && isAllowedUrl(fullUrl)) {
      res.send(`
        <html>
          <body>
            <p>You are about to leave our site and be redirected to: ${fullUrl}</p>
            <a href="${fullUrl}">Click here to proceed</a>
          </body>
        </html>
      `);
  } else if (fullUrl && fullUrl.startsWith('/') && isValidUrl(fullUrl)) {
    const appendedfullUrl = `http://yourdomainname.com${fullUrl}`;
    res.redirect(appendedfullUrl);
  } else {
    res.status(400).send('Invalid redirect URL');
  }
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});

```
