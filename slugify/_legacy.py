"""Frozen legacy slugify implementation.

DO NOT MODIFY. This module is the permanently frozen legacy output pipeline.
Many deployed sites depend on its exact output, so its behavior must never
change. All improvements belong in the modern path (slugify/slugify.py).
Any change to this file that alters legacy output is rejected on principle;
the only acceptable edits are non-behavioral (e.g. this docstring) verified
byte-for-byte against the frozen 2,688-case differential baseline.
"""
from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable
from html.entities import name2codepoint
from importlib import import_module
from typing import Literal

CHAR_ENTITY_PATTERN = re.compile(r'&(%s);' % '|'.join(name2codepoint))
DECIMAL_PATTERN = re.compile(r'&#(\d+);')
HEX_PATTERN = re.compile(r'&#x([\da-fA-F]+);')
QUOTE_PATTERN = re.compile(r"[']+")
DISALLOWED_CHARS_PATTERN = re.compile(r'[^-a-zA-Z0-9]+')
DISALLOWED_UNICODE_CHARS_PATTERN = re.compile(r'[\W_]+')
DUPLICATE_DASH_PATTERN = re.compile(r'-{2,}')
NUMBERS_PATTERN = re.compile(r'(?<=\d),(?=\d)')
DEFAULT_SEPARATOR = '-'

Backend = Literal['auto', 'text-unidecode', 'unidecode', 'anyascii']
ReplacementStage = Literal['both', 'pre', 'post']


def _decode_entities(text: str, entities: bool, decimal: bool, hexadecimal: bool) -> str:
    if entities:
        text = CHAR_ENTITY_PATTERN.sub(lambda m: chr(name2codepoint[m.group(1)]), text)
    if decimal:
        # Legacy substitution is all-or-nothing for each numeric reference kind.
        try:
            text = DECIMAL_PATTERN.sub(lambda m: chr(int(m.group(1))), text)
        except (ValueError, OverflowError):
            pass
    if hexadecimal:
        try:
            text = HEX_PATTERN.sub(lambda m: chr(int(m.group(1), 16)), text)
        except (ValueError, OverflowError):
            pass
    return text


def _transliterate(text: str, backend: Backend) -> str:
    if backend == 'auto':
        try:
            module = import_module('unidecode')
        except ModuleNotFoundError as error:
            if error.name != 'unidecode':
                raise
            module = import_module('text_unidecode')
    else:
        module = import_module(backend.replace('-', '_'))
    # These third-party modules share a string-to-string API; some are untyped.
    result: str = getattr(module, 'anyascii' if backend == 'anyascii' else 'unidecode')(text)
    return result


def smart_truncate(
    string: str,
    max_length: int = 0,
    word_boundary: bool = False,
    separator: str = " ",
    save_order: bool = False,
) -> str:
    """Historical public truncation behavior, including character-set stripping.

    Zero means unlimited; negative limits retain Python slicing semantics.
    An empty separator raises ValueError, as in the legacy implementation.
    """
    string = string.strip(separator)
    if not max_length:
        return string
    if len(string) < max_length:
        return string
    if not word_boundary:
        return string[:max_length].strip(separator)
    if separator not in string:
        return string[:max_length]
    truncated = ''
    for word in string.split(separator):
        if word:
            next_len = len(truncated) + len(word)
            if next_len < max_length:
                truncated += '{}{}'.format(word, separator)
            elif next_len == max_length:
                truncated += '{}'.format(word)
                break
            elif save_order:
                break
    if not truncated:
        truncated = string[:max_length]
    return truncated.strip(separator)


def slugify(
    text: str | bytes | bytearray,
    entities: bool = True,
    decimal: bool = True,
    hexadecimal: bool = True,
    max_length: int = 0,
    word_boundary: bool = False,
    separator: str = DEFAULT_SEPARATOR,
    save_order: bool = False,
    stopwords: Iterable[str] = (),
    regex_pattern: re.Pattern[str] | str | None = None,
    lowercase: bool = True,
    replacements: Iterable[Iterable[str]] = (),
    allow_unicode: bool = False,
    *,
    replacement_stage: ReplacementStage = 'both',
    backend: Backend = 'auto',
) -> str:
    """Frozen legacy output pipeline. Do not change its behavior."""
    if not isinstance(text, str):
        if not isinstance(text, (bytes, bytearray)):
            raise TypeError(f'text must be str, bytes or bytearray, not {type(text).__name__}')
        text = text.decode('utf-8', 'ignore')
    if replacement_stage not in ('both', 'pre', 'post'):
        raise ValueError("replacement_stage must be 'both', 'pre' or 'post'")
    if backend not in ('auto', 'text-unidecode', 'unidecode', 'anyascii'):
        raise ValueError("backend must be 'auto', 'text-unidecode', 'unidecode' or 'anyascii'")

    if replacements and replacement_stage in ('both', 'pre'):
        for old, new in replacements:
            text = text.replace(old, new)

    text = QUOTE_PATTERN.sub(DEFAULT_SEPARATOR, text)
    if allow_unicode:
        text = unicodedata.normalize('NFKC', text)
    else:
        text = _transliterate(unicodedata.normalize('NFKD', text), backend)
    text = _decode_entities(text, entities, decimal, hexadecimal)
    text = unicodedata.normalize('NFKC' if allow_unicode else 'NFKD', text)
    if lowercase:
        text = text.lower()
    text = QUOTE_PATTERN.sub('', text)
    text = NUMBERS_PATTERN.sub('', text)
    pattern = regex_pattern or (DISALLOWED_UNICODE_CHARS_PATTERN if allow_unicode else DISALLOWED_CHARS_PATTERN)
    text = re.sub(pattern, DEFAULT_SEPARATOR, text)
    text = DUPLICATE_DASH_PATTERN.sub(DEFAULT_SEPARATOR, text).strip(DEFAULT_SEPARATOR)

    if stopwords:
        excluded = [word.lower() for word in stopwords] if lowercase else stopwords
        text = DEFAULT_SEPARATOR.join(word for word in text.split(DEFAULT_SEPARATOR) if word not in excluded)
    if replacements and replacement_stage in ('both', 'post'):
        for old, new in replacements:
            text = text.replace(old, new)

    if max_length > 0:
        text = smart_truncate(text, max_length, word_boundary, DEFAULT_SEPARATOR, save_order)
    return text.replace(DEFAULT_SEPARATOR, separator) if separator != DEFAULT_SEPARATOR else text
