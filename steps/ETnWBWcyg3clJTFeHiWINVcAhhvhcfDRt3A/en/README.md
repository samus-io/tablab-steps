# RegEx cheat sheet

## Anchors

  |Composition|Recap|Description|Example|
  |:--:|:--:|:--:|:--:|
  |`^`|Input start|Matches the position at the start of the input|`^a` matches *a* in "apple" but does not match *a* in "facebook"|
  |`$`|Input end|Matches the position at the end of the input|`t$` does not match *t* in "eater", but matches *t* in "eat"|
  |`\b`|Word start|Matches a word boundary (the beginning or the end of a word)|`er\b` matches *er* in "never" but not *er* in "verb"|
  |`\B`|Word end|Matches a non-word boundary|`ear\B` matches *ear* in "never early"|

## Character classes

  |Composition|Recap|Description|Example|
  |:--:|:--:|:--:|:--:|
  |`\d`|0 to 9|Matches a digit character|`\d` matches *5* in "Room 5 is ready"|
  |`\D`|Equivalent to `[^\d]`|Matches a non-digit character|`\D` matches *#* in "#1"|
  |`\w`|Equivalent to `[A-Za-z0-9_]`|Matches any word character, including underscore|`\w` matches *f* in "facebook", *7* in "#7", and *m* in "Émanuel"|
  |`\W`|Equivalent to `[^A-Za-z0-9_]`|Matches any non-word character|`\W` matches *%* in "100%" and *É* in "Émanuel"|
  |`\s`|Equivalent to `[\f\n\r\t\v\u0020\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff]`|Matches any white space (*space*, *tab*, *newline*)|`\s` matches " " in "foo bar"|
  |`\S`|Equivalent to `[^\s]`|Matches any non-white space character|`\S` matches *foo* and *bar* in "foo bar"|

## Groups and ranges

  |Composition|Recap|Description|Example|
  |:--:|:--:|:--:|:--:|
  |`.`|Any character except *newline*|Matches any single character except line terminators as `\n`, `\r`, `\u2028` or `\u2029`|`.y` matches *my* and *ay*, but not *yes*|
  |`[]`|Enclosed characters|Matches any of the enclosed characters|`[abc]` matches *a* in "rat"|
  |`[^]`|Negative character set|Matches any character that is not enclosed|`[^abc]` matches *r* and *t* in "rat"|
  |`()`|Grouping and capturing|Matches a pattern and remembers the match|`(a\|b\|cd)\1` matches *aa*, *bb* or *cdcd*. `(a\|b\|cd)` is a capturing group, and `\1` is a backreference that matches the exact text that was captured|

## Assertions

  |Composition|Recap|Description|Example|
  |:--:|:--:|:--:|:--:|
  |`\|`|OR|Combines multiple expressions in one that matches any of single ones|`(t\|z)oo` matches *too* or *zoo*|
  |`(?=pattern)`|Positive lookahead|Asserts that the specified `pattern` matches the subsequent input without consuming any part of the input|`/api(?=\w)` matches */api* in "/apiculture" but does not match */api* in "/api/"|
  |`(?!pattern)`|Negative lookahead|Asserts that the specified `pattern` does not match the subsequent input without consuming any part of the input|`/api(?![A-Za-z])` matches */api* in "/api/" but does not match */api* in "/apiculture"|

## Quantifiers

  |Composition|Recap|Description|Example|
  |:--:|:--:|:--:|:--:|
  |`*`|0 or more|Matches the preceding item (character or group) 0 or more times|`zo*` matches either *z* or *zoo*|
  |`+`|1 or more|Matches the preceding item (character or group) 1 or more times|`zo+` matches *zo* or *zoo*, but no *z*|
  |`?`|0 or once|Matches the preceding item (character or group) 0 or one time|`zo?` matches *zo* in "zoo"|
  |`{n}`|*n* times|Matches the preceding character exactly *n* times|`o{2}` does not match *o* in "Bob", but matches the first two *o*'s in "foooood"|
  |`{n,}`|At least *n* times|Matches the preceding character at least *n* times. `o{0,}` is equivalent to `o*` and `o{1,}` is equivalent to `o+`|`o{2,}` does not match *o* in "Bob" but matches all the *o*'s in "foooood"|
  |`{n,m}`|At least *n*, at most *m* times|Matches the preceding character at least *n* and at most *m* times. `o{0,1}` is equivalent to `o?`|`o{1,3}` matches the first three *o*'s in "fooooood"|

## Metach­ara­cters

* The `.[{()\^$|?*+<>` characters need to be escaped to be interpreted as regular characters. The escape character is usually `\`.
