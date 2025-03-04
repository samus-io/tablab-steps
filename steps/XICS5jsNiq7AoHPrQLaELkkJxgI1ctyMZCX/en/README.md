# URL encoding basics

* As defined in [RFC 3986][1], URIs transmitted over the Internet must only contain ASCII standard characters.
* Therefore, there is a limit to the number of characters that can be used in a URL, since a URL is a specific subtype of URI.

> :older_man: ASCII was the first character set (encoding standard) used for internet-based computer communications.

* The following table defines the encoding requirements for various characters belonging to the ASCII standard based on four groupings:

  |Classification|Character set|Description|Encoding required|
  |:--:|:--:|:--:|:--:|
  |Safe characters|`[a-zA-z]`, `[0-9]`, *Unreserved characters* and *Reserved characters* (when the latter are used for their reserved purpose)|Allowed in a URI|No|
  |Unreserved characters|`-` `.` `_` `~`|Allowed in a URI but since they do not have a reserved purpose they are defined as *Unreserved characters*|No|
  |Reserved characters|`:` `/` `?` `#` `[` `]` `@` `!` `$` `&` `"` `(` `)` `*` `+` `,` `;` `=`|They have a specific purpose|Yes, when **not** used for their reserved purpose|
  |Unsafe characters|`"` `<` `>` `%` `{` `}` `\|` `\` `^` and blank/empty space (` `)|These characters may be considered *unsafe* for various reasons, although it generally occurs because they can be interpreted differently or even modified by intermediary transport agents (e.g., trailing spaces in the URL may be removed)|Sí|

* *Non-ASCII*, *Unsafe characters* and *Reserved characters* (when the latter are **not** used for their reserved purpose) must be encoded using the *Percent-encoding* mechanism, also called *URL encoding*, which consists of blocks formed by the character `%` followed by two hexadecimal digits:

  |Type|Character|Purpose in URI|Encoding|
  |:--:|:--:|:--:|:--:|
  |Reserved character|`/`|Delimits path segments in the *URL-path*.|`%2F`|
  |Reserved character|`?`|Delimits the start of the query string|`%3F`|
  |Reserved character|`#`|Delimits the fragment identifier|`%23`|
  |Reserved character|`&`|Separates query elements|`%26`|
  |Reserved character|`+`|Indicates a space. Alternative to blank/empty space (` `, `%20`)|`%2B`|
  |Non-ASCII|`ö`|None|`%C3%B6`|
  |Non-ASCII|`ڃ`|None|`%DA%83`|

  * The reserved character `/`, for example, when used as part of the definition syntax of a URI has the special meaning of being a delimiter between path segments. However, if, according to a particular URI scheme, the `/` character should be included in the path component as merely a value, then the three `%2F` (or `%2f`) characters should be used instead so that it is not properly interpreted as a delimiter.
  * On the other hand, regarding characters that belong to the Unicode standard, it was determined that the URL encoding to be used should adhere to the UTF-8 encoding system. In effect, the character `ö` is URL-encoded as `%C3%B6`, since in the UTF-8 system it has the hexadecimal value of `0xC3 0xB6`.

> Warning: Although URL encoding appears to be a security feature, it is not. In other words, it does not provide any benefit in terms of application security.

[1]: https://datatracker.ietf.org/doc/html/rfc3986
