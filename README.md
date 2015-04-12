Python Slugify
===============

**A Python slugify application that handles unicode**

[![build-status-image-travis]][travis]
[![build-status-image-fury]][fury]
[![build-status-image-pypi]][pypi]


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

    txt = "This -- is a ## test ---"
    r = slugify(txt)
    self.assertEqual(r, "this-is-a-test")

    txt = 'C\'est déjà l\'été.'
    r = slugify(txt)
    self.assertEqual(r, "cest-deja-lete")

    txt = 'Nín hǎo. Wǒ shì zhōng guó rén'
    r = slugify(txt)
    self.assertEqual(r, "nin-hao-wo-shi-zhong-guo-ren")

    txt = 'Компьютер'
    r = slugify(txt)
    self.assertEqual(r, "kompiuter")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt)
    self.assertEqual(r, "jaja-lol-mememeoo-a")

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
    r = slugify(txt, max_length=19, word_boundary=True)
    self.assertEqual(r, "jaja-lol-mememeoo")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=20, word_boundary=True)
    self.assertEqual(r, "jaja-lol-mememeoo-a")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=20, word_boundary=True, separator=".")
    self.assertEqual(r, "jaja.lol.mememeoo.a")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=20, word_boundary=True, separator="ZZZZZZ")
    self.assertEqual(r, "jajaZZZZZZlolZZZZZZmememeooZZZZZZa")

    txt = "___This is a test ---"
    r = slugify(txt)
    self.assertEqual(r, "this-is-a-test")

    txt = "___This is a test___"
    r = slugify(txt)
    self.assertEqual(r, "this-is-a-test")

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
   ```

Running the tests
=================

To run the tests against the current environment:

    python test.py


License
====================

Released under a ([BSD](LICENSE.md)) license.


[build-status-image-travis]: https://secure.travis-ci.org/un33k/python-slugify.png?branch=master
[travis]: http://travis-ci.org/un33k/python-slugify?branch=master

[build-status-image-fury]: https://badge.fury.io/py/python-slugify.png
[fury]: http://badge.fury.io/py/python-slugify

[build-status-image-pypi]: https://pypip.in/d/python-slugify/badge.png
[pypi]: https://crate.io/packages/python-slugify?version=latest

