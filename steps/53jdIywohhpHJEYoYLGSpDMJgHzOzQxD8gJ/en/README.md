# Information disclosure via web crawlers

* Web crawlers, also known as search bots, are essential tools for search engines. Their primary function is to index website content, significantly improving the search experience for users.
* These bots operate by accessing specific URLs, extracting all page links, and systematically following them to continue their indexing process.

## Files intended for web crawlers

* Some files are designed to guide crawlers on site paths, being `robots.txt` and `sitemap.xml` the most common.
* A security concern arises when these files disclose paths that should be kept hidden from potential adversaries.
* An evident case of this risk is when a `robots.txt` file inadvertently reveals access to an administrative section:

  ```plaintext
  User-agent: *
  Allow: /
  Disallow: /sup3r-s3cr3t-admin-login
  ```

* Although the intent behind the previous `robots.txt` is to prevent indexing of certain paths, it may paradoxically alert adversaries to their existence.
* Furthermore, Google advises against relying on these files to prevent paths from being indexed, as restricted paths may still be discovered and indexed through other means.

## How to find search engine indexed pages

* Beyond avoiding the inclusion of sensitive paths in crawler-specific files, it is also crucial to understand that pages with sensitive details may still be indexed. To verify which pages of a domain have been indexed, the following search query can be performed in a search engine:

  ```plaintext
  site:example.tbl
  ```

  * Where `example.tbl` is the domain hosting the web application.

* Specific search engine commands can be used to locate sensitive indexed pages. For example, to find exposed login pages or configuration files, the following queries can be executed:

  ```plaintext
  site:example.tbl inurl:login
  ```

  * To search for URLs containing "login", which may indicate authentication entry points.

  ```plaintext
  site:example.tbl ext:env | ext:sql | ext:log
  ```

  * To attempt to locate exposed `.env`, `.sql`, or `.log` files that could contain sensitive information.

## Recommended security approaches to prevent page indexing

* To block search engines from indexing specific pages, the HTML `meta` tag with `noindex` is recommended over using files like `robots.txt`:

  ```html
  <meta name="robots" content="noindex">
  ```

  * This strategy ensures that the specified page is not indexed by search engines. It is important to refrain from adding these pages to `robots.txt`, as Google has stated that such paths can still be indexed through different mechanisms and may also be effortlessly discovered by malicious actors.
* An alternative way to prevent page indexing is to send the following HTTP response header:

  ```http
  X-Robots-Tag: noindex
  ```

  * This method is particularly useful for non-HTML resources, such as PDFs, images, or videos.
