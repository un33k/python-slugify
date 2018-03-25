## 1.2.5
  - Add support for using text-unidecode (@bolkedebruin)
  - Switch to pycodestyle instead of pep8

## 1.2.4
  - Remove build artifacts during packaging
  - Simplify the setup.py file (@reece)

## 1.2.3
  - Republish - possible corrupt 1.2.2 build

## 1.2.2
  - Add `regex_pattern` option. (@vrbaskiz)
  - Add Python 3.6 support

## 1.2.1
  - Including certain files (e.g. license.md) in sdists via MANIFEST.in (@proinsias)
  - Relax licensing by moving from BSD to MIT
  - Add Python 3.5 support
  - Add more tests

## 1.2.0

Backward incompatible change: (@fabiocaccamo)

  - In version < 1.2.0 all single quotes ( ' ) were removed, and
    moving forward, >= 1.2.0, they will be replaced with ( - ).
    Example:
      <  1.2.0 -- ('C\'est déjà l\'été.' -> "cest-deja-lete")
      >= 1.2.0 -- ('C\'est déjà l\'été.' -> "c-est-deja-l-ete")

## 1.1.4

Bugfix:

  - Add more test cases, dropped `official` support for python 3.2


## 1.1.3

Bugfix:

  - Handle unichar in python 3.x


## 1.1.2

Enhancement:

  - Ability to remove `stopwords` from string


## 1.0.2

Enhancement:

  - A new PyPI release


## 1.0.1

Enhancement:

  - Promoting to production grade


## 0.1.1

Enhancement:

  - Added option to save word order
  - Removed 2to3 dependency
  - Added more tests


## 0.1.0

Enhancement:

  - Added more test
  - Added test for python 3.4


## 0.0.9

Enhancement:

  - Enable console_scripts


## 0.0.8

Enhancement:

  - Move logic out of __init__.py
  - Added console_scripts (@ekamil)
  - Updated pep8.sh
  - Added pypy support


## 0.0.7

Enhancement:

  - Handle encoding in setup file
  - Update ReadME, ChangeLog, License files


## 0.0.6

Enhancement:

  - Update for smart_truncate


## 0.0.5

Features:

  - Added Python 3.2 and 3.3 support (work by: arthurdarcet@github)


## 0.0.4

Features:

  - Added option to choose non-dash separators (request by: danilodimoia@github)


## 0.0.3

Features:

  - Added the ability to truncate slugs (request by: juanriaza@github)


## 0.0.2

Enhancement:

  - Incremental update


## 0.0.1

  - Initial version
