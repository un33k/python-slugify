Python Slugify
====================

**A Python slugify application that handles unicode**.

[![status-image]][status-link]
[![version-image]][version-link]
[![coverage-image]][coverage-link]

Overview
====================

**Best attempt** to create slugs from unicode strings while keeping it **DRY**.

Notice
====================

This module, by default installs and uses [text-unidecode](https://github.com/kmike/text-unidecode) *(GPL & Perl Artistic)* for its decoding needs.

However, there is an alternative decoding package called [Unidecode](https://github.com/avian2/unidecode) *(GPL)*. It can be installed as `python-slugify[unidecode]` for those who prefer it.


How to install
====================
    easy_install python-slugify |OR| easy_install python-slugify[unidecode]
    -- OR --
    pip install python-slugify |OR| pip install python-slugify[unidecode]

How to use
====================

   ```python
    from slugify import slugify

    txt = "This is a test ---"
    r = slugify(txt)
    self.assertEqual(r, "this-is-a-test")

    txt = '影師嗎'
    r = slugify(txt)
    self.assertEqual(r, "ying-shi-ma")

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

    txt = 'one two three four five'
    r = slugify(txt, max_length=13, word_boundary=True, save_order=True)
    self.assertEqual(r, "one-two-three")

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

    from slugify import UniqueSlugify

    unique_slugify = UniqueSlugify()

    txt = 'this is a test'
    r = unique_slugify(txt)
    self.assertEqual(r, 'this-is-a-test')

    txt = "___This is a test ---"
    r = unique_slugify(txt)
    self.assertEqual(r, 'this-is-a-test-1')

   ```
   
For more examples, have a look at the [test.py](test.py) file.


Running the tests
====================

To run the tests against the current environment:

    python test.py


License
====================

Released under a ([MIT](LICENSE)) license.


Version
====================
X.Y.Z Version

    `MAJOR` version -- when you make incompatible API changes,
    `MINOR` version -- when you add functionality in a backwards-compatible manner, and
    `PATCH` version -- when you make backwards-compatible bug fixes.

[status-image]: https://secure.travis-ci.org/un33k/python-slugify.png?branch=master
[status-link]: http://travis-ci.org/un33k/python-slugify?branch=master

[version-image]: https://img.shields.io/pypi/v/python-slugify.svg
[version-link]: https://pypi.python.org/pypi/python-slugify

[coverage-image]: https://coveralls.io/repos/un33k/python-slugify/badge.svg
[coverage-link]: https://coveralls.io/r/un33k/python-slugify

[download-image]: https://img.shields.io/pypi/dm/python-slugify.svg
[download-link]: https://pypi.python.org/pypi/python-slugify


Sponsors
====================

[![Surge](https://www.surgeforward.com/wp-content/themes/understrap-master/images/logo.png)](https://github.com/surgeforward)
