Python Slugify
===============

**A Python slugify application that handles unicode**

[![build-status-image-travis]][travis]
[![build-status-image-fury]][fury]
[![build-status-image-pypi]][pypi]
[![build-status-image-coverage]][coverage]


Overview
========

A Python **slugify** application that handles **unicode**.


How to install
==============

    1. easy_install python-slugify
    2. pip install python-slugify
    3. git clone http://github.com/un33k/python-slugify
        a. cd python-slugify
        b. run python setup.py
    4. wget https://github.com/un33k/python-slugify/zipball/master
        a. unzip the downloaded file
        b. cd into python-slugify-* directory
        c. run python setup.py


How to use
===========

   ```python
    from slugify import slugify

    txt = "This is a test ---"
    r = slugify(txt)
    self.assertEqual(r, "this-is-a-test")

    txt = "___This is a test ---"
    r = slugify(txt)
    self.assertEqual(r, "this-is-a-test")

    txt = "___This is a test___"
    r = slugify(txt)
    self.assertEqual(r, "this-is-a-test")

    txt = "This -- is a ## test ---"
    r = slugify(txt)
    self.assertEqual(r, "this-is-a-test")

    txt = '影師嗎'
    r = slugify(txt)
    self.assertEqual(r, "ying-shi-ma")

    txt = 'C\'est déjà l\'été.'
    r = slugify(txt)
    self.assertEqual(r, "cest-deja-lete")

    txt = 'Nín hǎo. Wǒ shì zhōng guó rén'
    r = slugify(txt)
    self.assertEqual(r, "nin-hao-wo-shi-zhong-guo-ren")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt)
    self.assertEqual(r, "jaja-lol-mememeoo-a")

    txt = 'Компьютер'
    r = slugify(txt)
    self.assertEqual(r, "kompiuter")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=9)
    self.assertEqual(r, "jaja-lol")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=15)
    self.assertEqual(r, "jaja-lol-mememe")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=50)
    self.assertEqual(r, "jaja-lol-mememeoo-a")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=15, word_boundary=True)
    self.assertEqual(r, "jaja-lol-a")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=17, word_boundary=True)
    self.assertEqual(r, "jaja-lol-mememeoo")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=18, word_boundary=True)
    self.assertEqual(r, "jaja-lol-mememeoo")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=19, word_boundary=True)
    self.assertEqual(r, "jaja-lol-mememeoo-a")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=20, word_boundary=True, separator=".")
    self.assertEqual(r, "jaja.lol.mememeoo.a")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=20, word_boundary=True, separator="ZZZZZZ")
    self.assertEqual(r, "jajaZZZZZZlolZZZZZZmememeooZZZZZZa")

    txt = 'one two three four five'
    r = slugify(txt, max_length=13, word_boundary=True, save_order=True)
    self.assertEqual(r, "one-two-three")

    txt = 'one two three four five'
    r = slugify(txt, max_length=13, word_boundary=True, save_order=False)
    self.assertEqual(r, "one-two-three")

    txt = 'one two three four five'
    r = slugify(txt, max_length=12, word_boundary=True, save_order=False)
    self.assertEqual(r, "one-two-four")

    txt = 'one two three four five'
    r = slugify(txt, max_length=12, word_boundary=True, save_order=True)
    self.assertEqual(r, "one-two")

    txt = 'this has a stopword'
    r = slugify(txt, stopwords=['stopword'])
    self.assertEqual(r, 'this-has-a')

    txt = 'the quick brown fox jumps over the lazy dog'
    r = slugify(txt, stopwords=['the'])
    self.assertEqual(r, 'quick-brown-fox-jumps-over-lazy-dog')

    txt = 'Foo A FOO B foo C'
    r = slugify(txt, stopwords=['foo'])
    self.assertEqual(r, 'a-b-c')

    txt = 'Foo A FOO B foo C'
    r = slugify(txt, stopwords=['FOO'])
    self.assertEqual(r, 'a-b-c')

    txt = 'the quick brown fox jumps over the lazy dog in a hurry'
    r = slugify(txt, stopwords=['the', 'in', 'a', 'hurry'])
    self.assertEqual(r, 'quick-brown-fox-jumps-over-lazy-dog')
   ```

Running the tests
=================

To run the tests against the current environment:

    python test.py


License
====================

Released under a ([BSD](LICENSE.md)) license.


Version
====================
X.Y.Z Version

MAJOR version when you make incompatible API changes,
MINOR version when you add functionality in a backwards-compatible manner, and
PATCH version when you make backwards-compatible bug fixes.

[build-status-image-travis]: https://secure.travis-ci.org/un33k/python-slugify.png?branch=master
[travis]: http://travis-ci.org/un33k/python-slugify?branch=master

[build-status-image-fury]: https://badge.fury.io/py/python-slugify.png
[fury]: http://badge.fury.io/py/python-slugify

[build-status-image-pypi]: https://pypip.in/d/python-slugify/badge.png
[pypi]: https://crate.io/packages/python-slugify?version=latest

[build-status-image-coverage]: https://coveralls.io/repos/un33k/python-slugify/badge.svg
[coverage]: https://coveralls.io/r/un33k/python-slugify
