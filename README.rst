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

**In code:**

.. code:: python

    from slugify import slugify

    slug = slugify("C'est déjà l'été.")
    self.assertEqual(slug, "c-est-deja-l-ete")

See further examples and optional arguments in (`test.py`_).


**On the command line:**

.. code:: bash

    $ slugify "C'est déjà l'été."
    c-est-deja-l-ete


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

.. _test.py: test.py

.. _MIT: https://github.com/un33k/python-slugify/blob/master/LICENSE
