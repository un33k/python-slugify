from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable
from html.entities import name2codepoint
from importlib import import_module
from typing import Literal

from ._legacy import slugify as _legacy_slugify, smart_truncate

__all__ = ['slugify', 'smart_truncate', 'Backend', 'ReplacementStage', 'Algorithm']


CHAR_ENTITY_PATTERN = re.compile(r'&(%s);' % '|'.join(name2codepoint))
DECIMAL_PATTERN = re.compile(r'&#(\d+);')
MODERN_HEX_PATTERN = re.compile(r'&#[xX]([\da-fA-F]+);')
QUOTE_PATTERN = re.compile(r"[']+")
DISALLOWED_CHARS_PATTERN = re.compile(r'[^-a-zA-Z0-9]+')
DISALLOWED_UNICODE_CHARS_PATTERN = re.compile(r'[\W_]+')
DUPLICATE_DASH_PATTERN = re.compile(r'-{2,}')
NUMBERS_PATTERN = re.compile(r'(?<=\d),(?=\d)')
DEFAULT_SEPARATOR = '-'

Backend = Literal['auto', 'text-unidecode', 'unidecode', 'anyascii']
ReplacementStage = Literal['both', 'pre', 'post']
Algorithm = Literal['legacy', 'modern']


def _numeric_reference(match: re.Match[str], base: int) -> str:
    """Leave invalid references for ordinary filtering, independently of neighbors."""
    try:
        value = int(match.group(1), base)
        if 0xD800 <= value <= 0xDFFF:
            return match.group(0)
        return chr(value)
    except (ValueError, OverflowError):
        return match.group(0)


def _decode_entities(text: str, entities: bool, decimal: bool, hexadecimal: bool) -> str:
    if entities:
        text = CHAR_ENTITY_PATTERN.sub(lambda m: chr(name2codepoint[m.group(1)]), text)
    if decimal:
        text = DECIMAL_PATTERN.sub(lambda m: _numeric_reference(m, 10), text)
    if hexadecimal:
        text = MODERN_HEX_PATTERN.sub(lambda m: _numeric_reference(m, 16), text)
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


def _modern_truncate(text: str, max_length: int, word_boundary: bool, separator: str, save_order: bool) -> str:
    """Budget internal dash-separated tokens before mapping output delimiters.

    Output delimiters may also occur in words; never strip or split emitted text.
    Post replacements retain the historical global dash-to-separator mapping.
    """
    if max_length <= 0:
        return text.replace(DEFAULT_SEPARATOR, separator)
    output_length = len(text) + text.count(DEFAULT_SEPARATOR) * (len(separator) - 1)
    if output_length <= max_length:
        return text.replace(DEFAULT_SEPARATOR, separator)
    tokens = text.split(DEFAULT_SEPARATOR)
    if word_boundary:
        words: list[str] = []
        length = 0
        for word in tokens:
            if not word:
                continue
            next_length = length + len(word) + (len(separator) if words else 0)
            if next_length <= max_length:
                words.append(word)
                length = next_length
            elif save_order:
                break
        if words:
            return separator.join(words)
    # A hard cut may shorten a word but must not emit a partial/trailing delimiter.
    parts: list[str] = []
    length = 0
    for index, word in enumerate(tokens):
        delimiter = separator if index else ''
        remaining = max_length - length - len(delimiter)
        if remaining <= 0:
            break
        parts.append(delimiter + word[:remaining])
        length += len(delimiter) + min(len(word), remaining)
        if len(word) > remaining:
            break
    return ''.join(parts)


def _modern_slugify(
    text: str | bytes | bytearray,
    entities: bool,
    decimal: bool,
    hexadecimal: bool,
    max_length: int,
    word_boundary: bool,
    separator: str,
    save_order: bool,
    stopwords: Iterable[str],
    regex_pattern: re.Pattern[str] | str | None,
    lowercase: bool,
    replacements: Iterable[Iterable[str]],
    allow_unicode: bool,
    replacement_stage: ReplacementStage,
    backend: Backend,
) -> str:
    # bool is an int subclass: legacy silently treats max_length=True as 1.
    # Modern rejects it, and a non-str separator, up front.
    if isinstance(max_length, bool) or not isinstance(max_length, int):
        raise TypeError(f"max_length must be an int, not {type(max_length).__name__}")
    if not isinstance(separator, str):
        raise TypeError(f"separator must be str, not {type(separator).__name__}")
    if not isinstance(text, str):
        if not isinstance(text, (bytes, bytearray)):
            raise TypeError(f'text must be str, bytes or bytearray, not {type(text).__name__}')
        text = text.decode('utf-8', 'ignore')
    if replacement_stage not in ('both', 'pre', 'post'):
        raise ValueError("replacement_stage must be 'both', 'pre' or 'post'")
    if backend not in ('auto', 'text-unidecode', 'unidecode', 'anyascii'):
        raise ValueError("backend must be 'auto', 'text-unidecode', 'unidecode' or 'anyascii'")

    # Materialize rules once: consumption of an iterator would affect output.
    rules = tuple((old, new) for old, new in replacements) if replacements else ()
    if rules and replacement_stage in ('both', 'pre'):
        for old, new in rules:
            text = text.replace(old, new)

    text = _decode_entities(text, entities, decimal, hexadecimal)
    text = QUOTE_PATTERN.sub(DEFAULT_SEPARATOR, text)
    if allow_unicode:
        text = unicodedata.normalize('NFKC', text)
    else:
        text = _transliterate(unicodedata.normalize('NFKD', text), backend)
    text = unicodedata.normalize('NFKC' if allow_unicode else 'NFKD', text)
    if lowercase:
        text = text.lower()
    text = QUOTE_PATTERN.sub('', text)
    text = NUMBERS_PATTERN.sub('', text)
    pattern = regex_pattern or (DISALLOWED_UNICODE_CHARS_PATTERN if allow_unicode else DISALLOWED_CHARS_PATTERN)
    text = re.sub(pattern, DEFAULT_SEPARATOR, text)
    text = DUPLICATE_DASH_PATTERN.sub(DEFAULT_SEPARATOR, text).strip(DEFAULT_SEPARATOR)

    if stopwords:
        excluded = {word.lower() if lowercase else word for word in stopwords}
        text = DEFAULT_SEPARATOR.join(word for word in text.split(DEFAULT_SEPARATOR) if word not in excluded)
    if rules and replacement_stage in ('both', 'post'):
        for old, new in rules:
            text = text.replace(old, new)

    return _modern_truncate(text, max_length, word_boundary, separator, save_order)


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
    algorithm: Algorithm = 'legacy',
) -> str:
    """Make a slug with the legacy output pipeline by default, permanently.

    algorithm='legacy' (the default) dispatches to the frozen legacy pipeline in
    slugify._legacy, which must never change. algorithm='modern' opts into early
    entity decoding, reusable iterator rules, stable stopword membership, a final
    emitted-character length budget, and up-front argument type validation.
    Bytes and bytearray are decoded as UTF-8, ignoring invalid bytes.
    replacements are ordered literal rules, before and after cleanup by default;
    replacement_stage selects 'pre', 'post' or 'both'. Post rules are unfiltered.
    regex_pattern matches disallowed characters; stopwords match internal words.
    allow_unicode uses NFKC without transliteration. backend='auto' prefers
    installed Unidecode, falling back to text-unidecode; explicit choices do not
    fall back. All new controls are keyword-only.
    """
    if algorithm not in ('legacy', 'modern'):
        raise ValueError("algorithm must be 'legacy' or 'modern'")
    if algorithm == 'legacy':
        return _legacy_slugify(
            text, entities, decimal, hexadecimal, max_length, word_boundary,
            separator, save_order, stopwords, regex_pattern, lowercase,
            replacements, allow_unicode,
            replacement_stage=replacement_stage, backend=backend)
    return _modern_slugify(
        text, entities, decimal, hexadecimal, max_length, word_boundary,
        separator, save_order, stopwords, regex_pattern, lowercase,
        replacements, allow_unicode, replacement_stage, backend)
