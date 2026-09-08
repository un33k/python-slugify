from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable
from html.entities import name2codepoint
from importlib import import_module
from typing import Literal

__all__ = ['slugify', 'smart_truncate', 'Backend', 'ReplacementStage', 'Algorithm']


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


def _decode_entities(text: str, entities: bool, decimal: bool, hexadecimal: bool, algorithm: Algorithm) -> str:
    if entities:
        text = CHAR_ENTITY_PATTERN.sub(lambda m: chr(name2codepoint[m.group(1)]), text)
    if decimal:
        if algorithm == 'modern':
            text = DECIMAL_PATTERN.sub(lambda m: _numeric_reference(m, 10), text)
        else:
            # Legacy substitution is all-or-nothing for each numeric reference kind.
            try:
                text = DECIMAL_PATTERN.sub(lambda m: chr(int(m.group(1))), text)
            except (ValueError, OverflowError):
                pass
    if hexadecimal:
        if algorithm == 'modern':
            text = HEX_PATTERN.sub(lambda m: _numeric_reference(m, 16), text)
        else:
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


def _modern_truncate(text: str, max_length: int, word_boundary: bool, separator: str, save_order: bool) -> str:
    """Budget internal dash-separated tokens before mapping output delimiters.

    Output delimiters may also occur in words; never strip or split emitted text.
    Post replacements retain the historical global dash-to-separator mapping.
    """
    if max_length <= 0:
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

    algorithm='modern' opts into early entity decoding, reusable iterator rules,
    stable stopword membership and a final emitted-character length budget.
    Legacy limits apply before separator mapping and may exceed max_length.
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
    if not isinstance(text, str):
        if not isinstance(text, (bytes, bytearray)):
            raise TypeError(f'text must be str, bytes or bytearray, not {type(text).__name__}')
        text = text.decode('utf-8', 'ignore')
    if replacement_stage not in ('both', 'pre', 'post'):
        raise ValueError("replacement_stage must be 'both', 'pre' or 'post'")
    if backend not in ('auto', 'text-unidecode', 'unidecode', 'anyascii'):
        raise ValueError("backend must be 'auto', 'text-unidecode', 'unidecode' or 'anyascii'")

    # Legacy iterators are deliberately not replayed: consumption affects output.
    rules = (tuple((old, new) for old, new in replacements)
             if algorithm == 'modern' and replacements else replacements)
    if rules and replacement_stage in ('both', 'pre'):
        for old, new in rules:
            text = text.replace(old, new)

    if algorithm == 'modern':
        text = _decode_entities(text, entities, decimal, hexadecimal, algorithm)
    text = QUOTE_PATTERN.sub(DEFAULT_SEPARATOR, text)
    if allow_unicode:
        text = unicodedata.normalize('NFKC', text)
    else:
        text = _transliterate(unicodedata.normalize('NFKD', text), backend)
    if algorithm == 'legacy':
        text = _decode_entities(text, entities, decimal, hexadecimal, algorithm)
    text = unicodedata.normalize('NFKC' if allow_unicode else 'NFKD', text)
    if lowercase:
        text = text.lower()
    text = QUOTE_PATTERN.sub('', text)
    text = NUMBERS_PATTERN.sub('', text)
    pattern = regex_pattern or (DISALLOWED_UNICODE_CHARS_PATTERN if allow_unicode else DISALLOWED_CHARS_PATTERN)
    text = re.sub(pattern, DEFAULT_SEPARATOR, text)
    text = DUPLICATE_DASH_PATTERN.sub(DEFAULT_SEPARATOR, text).strip(DEFAULT_SEPARATOR)

    if stopwords:
        if algorithm == 'modern':
            excluded: Iterable[str] = {word.lower() if lowercase else word for word in stopwords}
        else:
            excluded = [word.lower() for word in stopwords] if lowercase else stopwords
        text = DEFAULT_SEPARATOR.join(word for word in text.split(DEFAULT_SEPARATOR) if word not in excluded)
    if rules and replacement_stage in ('both', 'post'):
        for old, new in rules:
            text = text.replace(old, new)

    if algorithm == 'modern':
        return _modern_truncate(text, max_length, word_boundary, separator, save_order)
    if max_length > 0:
        text = smart_truncate(text, max_length, word_boundary, DEFAULT_SEPARATOR, save_order)
    return text.replace(DEFAULT_SEPARATOR, separator) if separator != DEFAULT_SEPARATOR else text
