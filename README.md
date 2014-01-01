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
    from slugify import slugify

    txt = "This is a test ---"
    r = slugify(txt)
    self.assertEquals(r, "this-is-a-test")

    txt = "This -- is a ## test ---"
    r = slugify(txt)
    self.assertEquals(r, "this-is-a-test")

    txt = 'C\'est déjà l\'été.'
    r = slugify(txt)
    self.assertEquals(r, "cest-deja-lete")

    txt = 'Nín hǎo. Wǒ shì zhōng guó rén'
    r = slugify(txt)
    self.assertEquals(r, "nin-hao-wo-shi-zhong-guo-ren")

    txt = 'Компьютер'
    r = slugify(txt)
    self.assertEquals(r, "kompiuter")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt)
    self.assertEquals(r, "jaja-lol-mememeoo-a")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=9)
    self.assertEquals(r, "jaja-lol")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=15)
    self.assertEquals(r, "jaja-lol-mememe")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=50)
    self.assertEquals(r, "jaja-lol-mememeoo-a")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=15, word_boundary=True)
    self.assertEquals(r, "jaja-lol-a")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=19, word_boundary=True)
    self.assertEquals(r, "jaja-lol-mememeoo")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=20, word_boundary=True)
    self.assertEquals(r, "jaja-lol-mememeoo-a")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=20, word_boundary=True, separator=".")
    self.assertEquals(r, "jaja.lol.mememeoo.a")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=20, word_boundary=True, separator="ZZZZZZ")
    self.assertEquals(r, "jajaZZZZZZlolZZZZZZmememeooZZZZZZa")


Running the tests
=================

To run the tests against the current environment:

    python test.py


Credits
====================
**Author:** Val Neekman, [ info@neekware.com, [@vneekman](https://twitter.com/vneekman) ]

Also:
    -- arthurdarcet@github
    -- danilodimoia@github
    -- juanriaza@github


License (BSD)
====================

Copyright © Val Neekman ([Neekware Inc.](http://neekware.com))

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Note: Django is a registered trademark of the Django Software Foundation.


[build-status-image-travis]: https://secure.travis-ci.org/un33k/python-slugify.png?branch=master
[travis]: http://travis-ci.org/tomchristie/python-slugify?branch=master

[build-status-image-fury]: https://badge.fury.io/py/python-slugify.png
[fury]: http://badge.fury.io/py/python-slugify

[build-status-image-pypi]: https://pypip.in/d/python-slugify/badge.png
[pypi]: https://crate.io/packages/python-slugify?version=latest

