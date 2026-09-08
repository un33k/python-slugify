# Python Slugify

Unicode-aware slug generation for Python, with explicit transliteration choices.

[![CI](https://github.com/un33k/python-slugify/actions/workflows/main.yml/badge.svg)](https://github.com/un33k/python-slugify/actions/workflows/main.yml)
[![PyPI](https://img.shields.io/pypi/v/python-slugify.svg)](https://pypi.org/project/python-slugify/)

## Quickstart

This checkout targets **9.0.0** and has not been published.
Install from this checkout to use the new APIs demonstrated below.
See the [migration guide](docs/release-9/migration.md) before changing persisted URLs or keys.

Install **python-slugify**, import **slugify**. Other similarly named distributions are not this package.

```sh
python -m pip install -e .
```

```python
from slugify import slugify

assert slugify("C'est déjà l'été.") == 'c-est-deja-l-ete'
assert slugify('影師嗎', backend='text-unidecode') == 'ying-shi-ma'
assert slugify('影師嗎', allow_unicode=True) == '影師嗎'
```

```sh
slugify "Hello, world!"
# hello-world
printf 'Café' | python -m slugify --stdin
# cafe
slugify --regex-pattern '[^-a-z0-9_]+' '___This is a test___'
# ___this-is-a-test___
```

The ordinary `python -m pip install python-slugify` command installs the published release,
which does not yet include the new candidate APIs.

## Python support

| Python | Release family |
| --- | --- |
| 2.7–3.5 | below 5 |
| 3.6 | 5–6 |
| 3.7–3.9 | 7–8 (check each release's Requires-Python) |
| 3.10+ | 9 development series |

The configured release-9 test matrix covers CPython 3.10–3.14 and PyPy 3.11.
Configuration is not proof of a successful run; see [local verification](docs/release-9/verification.md).
Older applications can stay on a pinned 8.x release rather than upgrading Python or regenerating slugs immediately.

## Backends and installation

| `backend` | Runtime selection | Installation |
| --- | --- | --- |
| `auto` (default) | Installed Unidecode first, otherwise text-unidecode | Base install includes text-unidecode |
| `text-unidecode` | Only text-unidecode | Included in base install |
| `unidecode` | Only Unidecode | `python -m pip install -e '.[unidecode]'` |
| `anyascii` | Only AnyASCII | `python -m pip install -e '.[anyascii]'` |

Explicit selection never silently falls back. A missing selected module raises `ModuleNotFoundError`.
Backend imports are lazy; `allow_unicode=True` bypasses transliteration entirely.
**Extras add dependencies; they do not remove text-unidecode.** The AnyASCII extra does not change the default backend.
There is no dependency-free installation extra in this release.

Transliteration is not translation, language detection, or context-sensitive pronunciation.
Backends produce different slugs: for example `影師嗎` becomes `ying-shi-ma` with text-unidecode/Unidecode,
but `yingshima` with AnyASCII. Pin both this package and your explicitly chosen backend for stable persisted identifiers.

## API options

The original positional parameters remain in their original order. New options are keyword-only.

```python
slugify(
    text, entities=True, decimal=True, hexadecimal=True,
    max_length=0, word_boundary=False, separator='-', save_order=False,
    stopwords=(), regex_pattern=None, lowercase=True, replacements=(),
    allow_unicode=False, *, replacement_stage='both', backend='auto',
    algorithm='legacy',
)
```

- `algorithm`: `'legacy'` is the permanent default, preserving the historical output pipeline. `'modern'` explicitly opts into the changes below. Unknown values raise `ValueError`.
- `text`: `str`, or UTF-8 `bytes`/`bytearray` (invalid bytes ignored). Other objects raise `TypeError`.
- `entities`, `decimal`, `hexadecimal`: independently decode named HTML entities, decimal references, and lowercase-`x` hexadecimal references. Legacy decodes after transliteration and numeric substitutions are all-or-nothing per reference kind. Modern decodes before transliteration and handles invalid references independently.
- `max_length`: legacy budgets internal dashes before separator mapping, so wide separators can exceed the limit. Modern budgets final Python characters, including emitted delimiters. Nonpositive means unlimited for slugify; this is not a byte or grapheme limit.
- `word_boundary`: prefer whole words; shorter later words can fill the budget. If none fit, use a hard cut.
- `save_order`: with word boundaries, stop at the first oversized word instead of skipping it.
- `separator`: literal emitted delimiter; may be empty or multiple characters. Existing dashes also map to this delimiter for compatibility. Modern truncation preserves word characters even when they match the output delimiter.
- `stopwords`: iterable of whole normalized, internal dash-separated tokens. Matching is case-insensitive when `lowercase=True`; stopwords themselves are not transliterated. Legacy case-sensitive membership consumes iterators; modern snapshots them once.
- `regex_pattern`: string or compiled regular expression matching **disallowed** characters, not allowed ones. It overrides default filtering. Empty strings retain historical default-pattern behavior.
- `lowercase`: apply `str.lower()`; false preserves case.
- `replacements`: ordered iterable of `(old, new)` literal string rules. Legacy preserves iterator consumption across passes. Modern materializes outer and inner iterables once so generators behave like lists.
- `replacement_stage`: `both` preserves two passes; `pre` runs only before normalization; `post` runs after cleanup and stopword removal, before separator mapping and truncation. Post replacements are **not** re-sanitized. Replacements need not be idempotent.
- `allow_unicode`: retain Unicode word characters after NFKC normalization, not exact original code points; default ASCII mode uses NFKD plus transliteration.
- `backend`: select a backend from the table above. Ignored for transliteration in Unicode mode, but still validated.

`smart_truncate(string, max_length=0, word_boundary=False, separator=' ', save_order=False)`
is also public and retains legacy behavior: `str.strip(separator)` strips a character set, empty separators raise `ValueError`, zero is unlimited, and negative limits retain slicing semantics. Modern slugify uses a separate private token-budget helper; it does not change this public function.

```python
from slugify import slugify

assert slugify('a&#39;b') == 'ab'  # unchanged default
assert slugify('a&#39;b', algorithm='modern') == 'a-b'
assert slugify('xylophone x', separator='x', max_length=100, algorithm='modern') == 'xylophonexx'
```

## Recipes and boundaries

```python
from slugify import slugify, GERMAN

assert slugify('ÜBER', replacements=GERMAN, replacement_stage='pre') == 'ueber'
assert slugify('a', replacements=[('a', 'aa')]) == 'aaaa'  # legacy two passes
assert slugify('a', replacements=[('a', 'aa')], replacement_stage='pre') == 'aa'
assert slugify('one two three four', max_length=12, word_boundary=True) == 'one-two-four'
assert slugify('one two three four', max_length=12, word_boundary=True, save_order=True) == 'one-two'
assert slugify('a b c', separator='---', max_length=5, algorithm='modern') == 'a---b'
assert slugify('Baby’s shoes', replacements=[('’', '-')], replacement_stage='pre') == 'baby-s-shoes'
```

`CYRILLIC`, `GERMAN`, `GREEK`, and their combined `PRE_TRANSLATIONS` are optional substitution lists,
not automatically applied locale rules. `allow_unicode=True` can normalize compatibility jamo, and does not preserve emoji by default.
Disable all three entity flags if encoded markup should not be decoded.
Empty input, whitespace, or entirely filtered content can yield an empty string; callers choose an appropriate fallback.

Slugs are not guaranteed unique, filesystem-safe on every OS, XML-name-safe, or safe as an entire URL.
Choose escaping, reserved-name handling, path validation, and transactional uniqueness for your destination.
Custom regexes and post replacements can intentionally introduce punctuation; do not treat this package as a security sanitizer.

## Command line

`slugify --help` and `python -m slugify --help` describe all options, including `--algorithm` (default `legacy`), `--backend` and `--replacement-stage`.
Use `--` before text when supplying multi-valued options:

```sh
slugify --stopwords the in a hurry -- the quick brown fox jumps over the lazy dog in a hurry
slugify --replacement-stage pre --replacements 'a->aa' -- a
```

## Development and local release checks

```sh
python -m pip install -r dev.requirements.txt
python -m pip install -e '.[unidecode,anyascii]'
python -m pytest
python -m mypy
python tools/check_dist.py
# Full declared interpreter/backend matrix (requires those interpreters):
tox
```

The artifact check builds and installs both wheel and source archive in temporary environments outside the checkout.
It never uploads or tags. Publishing requires a separate maintainer decision; there is no `setup.py publish` shortcut.
See [migration and release notes](docs/release-9/migration.md), [review and draft replies](docs/release-9/recent-review.md),
and the [historical review](docs/release-9/historical-review.md). Please consult the
[contribution wiki](https://github.com/un33k/python-slugify/wiki/Python-Slugify-Wiki) before proposing changes.

## Licensing

python-slugify's own code is [MIT licensed](LICENSE). Dependency licenses are separate:

- [text-unidecode](https://github.com/kmike/text-unidecode): upstream offers the Artistic License or GPL; review the license files for the version you distribute.
- [Unidecode](https://github.com/avian2/unidecode): GPL-licensed; review its upstream license text and version.
- [AnyASCII](https://github.com/anyascii/anyascii): ISC-licensed; review its upstream license text and any bundled notices.

The installed package set and the backend used at runtime are different questions. Selecting AnyASCII does not remove
text-unidecode from a normal installation. This is factual dependency guidance, not legal advice or a blanket assurance
about your application's obligations. Evaluate the actual versions, distribution method, and applicable license terms.

## Sponsors

[Neekware Inc.](https://neekware.com)
