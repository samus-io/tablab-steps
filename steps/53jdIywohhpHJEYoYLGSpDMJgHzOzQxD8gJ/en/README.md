# Information disclosure via web crawlers

* Web crawlers, also known as search bots, are essential tools for search engines. Their primary function is to index website content, significantly improving the search experience for users.
* These bots operate by accessing specific URLs, extracting all the links found on a page, and navigating through them to continue their indexing process.

## Files for web crawlers

* Certain files are designed to inform crawlers about paths within a site, the most common being `robots.txt` and `sitemap.xml`.
* However, a risk arises when these files expose sensitive paths that should be hidden from potential adversaries.
* A clear example of this risk is how a `robots.txt` file could inadvertently reveal access to an admin section:

  ```
  User-agent: *
  Allow: /
  Disallow: /sup3r-s3cr3t-admin-login
  ```

* Although the intent behind the previous `robots.txt` is to prevent indexing of certain paths, it may paradoxically alert adversaries to their existence.
* Additionally, Google advises against relying on these files to prevent paths from being indexed, as restricted paths may still be discovered and indexed through other means.

## Indexing of pages in search engines

* Beyond avoiding the inclusion of sensitive paths in crawler-specific files, it is crucial to recognize that pages containing sensitive information may still become indexed.
* To verify which pages of a domain have been indexed, the following search query can be used in the search engine:

  ```
  site:example.tbl
  ```

* Where `example.tbl` is the domain hosting the web application.

## Preventing page indexing

* To prevent search engines from indexing certain pages, it is recommended to use the HTML meta tag with `noindex` instead of using files like `robots.txt`:

  ```html
  <meta name="robots" content="noindex">
  ```

* This approach ensures that search engines do not index the specified page. It is crucial not to list these pages in `robots.txt`, as Google has stated that such paths may still be indexed through alternative methods.
* An alternative way to avoid indexing pages is to send the following response header:

  ```http
  X-Robots-Tag: noindex
  ```

* This technique is particularly useful for non-HTML resources, such as PDFs, images, or videos.
