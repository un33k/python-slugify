Python Slugify
==============

|status-image| |version-image| |coverage-image|

Overview
--------

A Python **slugify** application that handles **unicode**.


How to install
--------------

Via ``pip``:

.. code:: bash

    $ pip install python-slugify

Via ``easy_install``:

.. code:: bash

    $ easy_install python-slugify

From sources via ``git``:

.. code:: bash

    $ git clone http://github.com/un33k/python-slugify
    $ cd python-slugify
    $ python setup.py

From sources:

.. code:: bash

    $ wget https://github.com/un33k/python-slugify/zipball/master
    # unzip the downloaded file
    # cd into python-slugify-* directory
    $ python setup.py


How to use
----------

.. code:: python

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
    self.assertEqual(r, "c-est-deja-l-ete")

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

    txt = 'foo &amp; bar'
    r = slugify(txt)
    self.assertEqual(r, 'foo-bar')

    txt = "___This is a test___"
    regex_pattern = r'[^-a-z0-9_]+'
    r = slugify(txt, regex_pattern=regex_pattern)
    self.assertEqual(r, "___this-is-a-test___")

    txt = "___This is a test___"
    regex_pattern = r'[^-a-z0-9_]+'
    r = slugify(txt, separator='_', regex_pattern=regex_pattern)
    self.assertNotEqual(r, "_this_is_a_test_")

Running the tests
-----------------

To run the tests against the current environment:

.. code:: bash

    python test.py


License
-------

Released under a (`MIT`_) license.


Version
-------

X.Y.Z Version

::

    `MAJOR` version -- when you make incompatible API changes,
    `MINOR` version -- when you add functionality in a backwards-compatible manner, and
    `PATCH` version -- when you make backwards-compatible bug fixes.

.. |status-image| image:: https://secure.travis-ci.org/un33k/python-slugify.png?branch=master
    :target: http://travis-ci.org/un33k/python-slugify?branch=master

.. |version-image| image:: https://img.shields.io/pypi/v/python-slugify.svg
    :target: https://pypi.python.org/pypi/python-slugify

.. |coverage-image| image:: https://coveralls.io/repos/un33k/python-slugify/badge.svg
    :target: https://coveralls.io/r/un33k/python-slugify

.. |download-image| image:: https://img.shields.io/pypi/dm/python-slugify.svg
    :target: https://pypi.python.org/pypi/python-slugify

.. _MIT: https://github.com/un33k/python-slugify/blob/master/LICENSE
