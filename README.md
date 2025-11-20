# Python Slugify

**A Python slugify application that handles unicode**.

[![status-image]][status-link]
[![version-image]][version-link]
[![coverage-image]][coverage-link]

# Overview

**Best attempt** to create slugs from unicode strings while keeping it **DRY**.

# Notice

This module, by default installs and uses [anyascii](https://github.com/anyascii/anyascii) _(ISC License)_ for its decoding needs. This is a permissive, non-GPL alternative that works well for most use cases.

However, there are alternative decoding packages available:
- [Unidecode](https://github.com/avian2/unidecode) _(GPL)_ - Can be installed as `python-slugify[unidecode]`. Believed to be more [advanced](https://github.com/un33k/python-slugify/wiki/Python-Slugify-Wiki#notes-on-unidecode).
- [text-unidecode](https://github.com/kmike/text-unidecode) _(GPL & Perl Artistic)_ - Can be installed as `python-slugify[text-unidecode]`.

The library will automatically use `unidecode` or `text-unidecode` (in that order) if either is installed, falling back to `anyascii` if neither is available.

### `Official` Support Matrix

| Python         | Slugify            |
| -------------- | ------------------ |
| `>= 2.7 < 3.6` | `< 5.0.0`          |
| `>= 3.6 < 3.7` | `>= 5.0.0 < 7.0.0` |
| `>= 3.7`       | `>= 7.0.0`         |

# How to install

```bash
# Default installation (uses anyascii - non-GPL)
pip install python-slugify

# With optional GPL-licensed Unidecode (more advanced)
pip install python-slugify[unidecode]

# With optional text-unidecode (GPL or Perl Artistic)
pip install python-slugify[text-unidecode]
```

# Options

```python
def slugify(
    text: str,
    entities: bool = True,
    decimal: bool = True,
    hexadecimal: bool = True,
    max_length: int = 0,
    word_boundary: bool = False,
    separator: str = DEFAULT_SEPARATOR,
    save_order: bool = False,
    stopwords: Iterable[str] = (),
    regex_pattern: str | None = None,
    lowercase: bool = True,
    replacements: Iterable[Iterable[str]] = (),
    allow_unicode: bool = False,
) -> str:
  """
  Make a slug from the given text.
  :param text (str): initial text
  :param entities (bool): converts html entities to unicode (foo &amp; bar -> foo-bar)
  :param decimal (bool): converts html decimal to unicode (&#381; -> Ž -> z)
  :param hexadecimal (bool): converts html hexadecimal to unicode (&#x17D; -> Ž -> z)
  :param max_length (int): output string length
  :param word_boundary (bool): truncates to end of full words (length may be shorter than max_length)
  :param save_order (bool): when set, does not include shorter subsequent words even if they fit
  :param separator (str): separator between words
  :param stopwords (iterable): words to discount
  :param regex_pattern (str): regex pattern for disallowed characters
  :param lowercase (bool): activate case sensitivity by setting it to False
  :param replacements (iterable): list of replacement rules e.g. [['|', 'or'], ['%', 'percent']]
  :param allow_unicode (bool): allow unicode characters
  :return (str): slugify text
  """
```

# How to use

```python
from slugify import slugify

txt = "This is a test ---"
r = slugify(txt)
self.assertEqual(r, "this-is-a-test")

txt = '影師嗎'
r = slugify(txt)
self.assertEqual(r, "ying-shi-ma")

txt = '影師嗎'
r = slugify(txt, allow_unicode=True)
self.assertEqual(r, "影師嗎")

txt = 'C\'est déjà l\'été.'
r = slugify(txt)
self.assertEqual(r, "c-est-deja-l-ete")

txt = 'Nín hǎo. Wǒ shì zhōng guó rén'
r = slugify(txt)
self.assertEqual(r, "nin-hao-wo-shi-zhong-guo-ren")

txt = 'Компьютер'
r = slugify(txt)
self.assertEqual(r, "kompiuter")

txt = 'jaja---lol-méméméoo--a'
r = slugify(txt, max_length=9)
self.assertEqual(r, "jaja-lol")

txt = 'jaja---lol-méméméoo--a'
r = slugify(txt, max_length=15, word_boundary=True)
self.assertEqual(r, "jaja-lol-a")

txt = 'jaja---lol-méméméoo--a'
r = slugify(txt, max_length=20, word_boundary=True, separator=".")
self.assertEqual(r, "jaja.lol.mememeoo.a")

txt = 'one two three four'
r = slugify(txt, max_length=12, word_boundary=True, save_order=False)
self.assertEqual(r, "one-two-four")

txt = 'one two three four'
r = slugify(txt, max_length=12, word_boundary=True, save_order=True)
self.assertEqual(r, "one-two")

txt = 'the quick brown fox jumps over the lazy dog'
r = slugify(txt, stopwords=['the'])
self.assertEqual(r, 'quick-brown-fox-jumps-over-lazy-dog')

txt = 'the quick brown fox jumps over the lazy dog in a hurry'
r = slugify(txt, stopwords=['the', 'in', 'a', 'hurry'])
self.assertEqual(r, 'quick-brown-fox-jumps-over-lazy-dog')

txt = 'thIs Has a stopword Stopword'
r = slugify(txt, stopwords=['Stopword'], lowercase=False)
self.assertEqual(r, 'thIs-Has-a-stopword')

txt = "___This is a test___"
regex_pattern = r'[^-a-z0-9_]+'
r = slugify(txt, regex_pattern=regex_pattern)
self.assertEqual(r, "___this-is-a-test___")

txt = "___This is a test___"
regex_pattern = r'[^-a-z0-9_]+'
r = slugify(txt, separator='_', regex_pattern=regex_pattern)
self.assertNotEqual(r, "_this_is_a_test_")

txt = '10 | 20 %'
r = slugify(txt, replacements=[['|', 'or'], ['%', 'percent']])
self.assertEqual(r, "10-or-20-percent")

txt = 'ÜBER Über German Umlaut'
r = slugify(txt, replacements=[['Ü', 'UE'], ['ü', 'ue']])
self.assertEqual(r, "ueber-ueber-german-umlaut")

txt = 'i love 🦄'
r = slugify(txt, allow_unicode=True)
self.assertEqual(r, "i-love")

txt = 'i love 🦄'
r = slugify(txt, allow_unicode=True, regex_pattern=r'[^🦄]+')
self.assertEqual(r, "🦄")

```

For more examples, have a look at the [test.py](test.py) file.

# Command Line Options

With the package, a command line tool called `slugify` is also installed.

It allows convenient command line access to all the features the `slugify` function supports. Call it with `-h` for help.

The command can take its input directly on the command line or from STDIN (when the `--stdin` flag is passed):

```
$ echo "Taking input from STDIN" | slugify --stdin
taking-input-from-stdin
```

```
$ slugify taking input from the command line
taking-input-from-the-command-line
```

Please note that when a multi-valued option such as `--stopwords` or `--replacements` is passed, you need to use `--` as separator before you start with the input:

```
$ slugify --stopwords the in a hurry -- the quick brown fox jumps over the lazy dog in a hurry
quick-brown-fox-jumps-over-lazy-dog
```

# Running the tests

To run the tests against the current environment:

    python test.py

# Contribution

Please read the ([wiki](https://github.com/un33k/python-slugify/wiki/Python-Slugify-Wiki)) page prior to raising any PRs.

# License

Released under a ([MIT](LICENSE)) license.

### Notes on dependencies
The default dependency, `anyascii`, uses the permissive ISC License (similar to MIT), so there are no licensing concerns.

If you choose to install the optional GPL-licensed packages (`unidecode` or `text-unidecode`), please note that `python-slugify` itself is not considered a derivative work and will remain under the MIT license.

# Version

X.Y.Z Version

    `MAJOR` version -- when you make incompatible API changes,
    `MINOR` version -- when you add functionality in a backwards-compatible manner, and
    `PATCH` version -- when you make backwards-compatible bug fixes.

[status-image]: https://github.com/un33k/python-slugify/actions/workflows/ci.yml/badge.svg
[status-link]: https://github.com/un33k/python-slugify/actions/workflows/ci.yml
[version-image]: https://img.shields.io/pypi/v/python-slugify.svg
[version-link]: https://pypi.python.org/pypi/python-slugify
[coverage-image]: https://coveralls.io/repos/un33k/python-slugify/badge.svg
[coverage-link]: https://coveralls.io/r/un33k/python-slugify
[download-image]: https://img.shields.io/pypi/dm/python-slugify.svg
[download-link]: https://pypi.python.org/pypi/python-slugify

# Sponsors

[Neekware Inc.](http://neekware.com)
