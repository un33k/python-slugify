from __future__ import annotations

import re
import unicodedata
from collections.abc import Callable, Iterable
from html.entities import name2codepoint

try:
    import unidecode
except ImportError:
    import text_unidecode as unidecode

__all__ = ['slugify', 'smart_truncate']


CHAR_ENTITY_PATTERN = re.compile(r'&(%s);' % '|'.join(name2codepoint))
DECIMAL_PATTERN = re.compile(r'&#(\d+);')
HEX_PATTERN = re.compile(r'&#x([\da-fA-F]+);')
QUOTE_PATTERN = re.compile(r'[\']+')
DISALLOWED_CHARS_PATTERN = re.compile(r'[^-a-zA-Z0-9]+')
DISALLOWED_UNICODE_CHARS_PATTERN = re.compile(r'[\W_]+')
DUPLICATE_DASH_PATTERN = re.compile(r'-{2,}')
NUMBERS_PATTERN = re.compile(r'(?<=\d),(?=\d)')
DEFAULT_SEPARATOR = '-'


def smart_truncate(
    string: str,
    max_length: int = 0,
    word_boundary: bool = False,
    separator: str = " ",
    save_order: bool = False,
) -> str:
    """
    Truncate a string.
    :param string (str): string for modification
    :param max_length (int): output string length
    :param word_boundary (bool):
    :param save_order (bool): if True then word order of output string is like input string
    :param separator (str): separator between words
    :return: truncated string
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
            else:
                if save_order:
                    break
    if not truncated:  # pragma: no cover
        truncated = string[:max_length]
    return truncated.strip(separator)


def slugify(
    text: str,
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
) -> str:
    """
    Make a slug from the given text.
    """
    text = _apply_replacements(text, replacements)
    text = _ensure_unicode(text)
    text = _normalize_text(text, allow_unicode)
    text = _process_html_entities(text, entities, decimal, hexadecimal)
    text = _normalize_text(text, allow_unicode)  # Re-normalize after entity processing
    text = _adjust_case(text, lowercase)
    text = _clean_special_chars(text, allow_unicode, regex_pattern)
    text = _process_stopwords(text, stopwords, lowercase, DEFAULT_SEPARATOR)
    text = _apply_replacements(text, replacements)  # Final replacements
    text = _truncate_text(text, max_length, word_boundary, separator, save_order, DEFAULT_SEPARATOR)
    text = _adjust_separator(text, separator, DEFAULT_SEPARATOR)
    
    return text

def _apply_replacements(text: str, replacements: Iterable[Iterable[str]]) -> str:
    if not replacements:
        return text
    for old, new in replacements:
        text = text.replace(old, new)
    return text

def _ensure_unicode(text: str) -> str:
    if not isinstance(text, str):
        return str(text, 'utf-8', 'ignore')
    return text

def _normalize_text(text: str, allow_unicode: bool) -> str:
    text = QUOTE_PATTERN.sub(DEFAULT_SEPARATOR, text)
    if allow_unicode:
        return unicodedata.normalize('NFKC', text)
    text = unicodedata.normalize('NFKD', text)
    return unidecode.unidecode(text)

def _process_html_entities(text: str, entities: bool, decimal: bool, hexadecimal: bool) -> str:
    if entities:
        text = CHAR_ENTITY_PATTERN.sub(lambda m: chr(name2codepoint[m.group(1)]), text)
    
    if decimal:
        text = _safe_sub(DECIMAL_PATTERN, lambda m: chr(int(m.group(1))), text)
    
    if hexadecimal:
        text = _safe_sub(HEX_PATTERN, lambda m: chr(int(m.group(1), 16)), text)
    
    return text

def _safe_sub(pattern: re.Pattern, repl: Callable, text: str) -> str:
    try:
        return pattern.sub(repl, text)
    except Exception:
        return text

def _adjust_case(text: str, lowercase: bool) -> str:
    if lowercase:
        return text.lower()
    return text

def _clean_special_chars(text: str, allow_unicode: bool, regex_pattern: re.Pattern | str | None) -> str:
    text = QUOTE_PATTERN.sub('', text)
    text = NUMBERS_PATTERN.sub('', text)
    
    pattern = regex_pattern or (DISALLOWED_UNICODE_CHARS_PATTERN if allow_unicode else DISALLOWED_CHARS_PATTERN)
    text = re.sub(pattern, DEFAULT_SEPARATOR, text)
    return DUPLICATE_DASH_PATTERN.sub(DEFAULT_SEPARATOR, text).strip(DEFAULT_SEPARATOR)

def _process_stopwords(text: str, stopwords: Iterable[str], lowercase: bool, separator: str) -> str:
    if not stopwords:
        return text
    
    words = text.split(separator)
    if lowercase:
        stopwords_set = {s.lower() for s in stopwords}
        words = [w for w in words if w not in stopwords_set]
    else:
        words = [w for w in words if w not in stopwords]
    
    return separator.join(words)

def _truncate_text(text: str, max_length: int, word_boundary: bool, 
                  save_order: bool, default_separator: str) -> str:
    if max_length > 0:
        return smart_truncate(text, max_length, word_boundary, default_separator, save_order)
    return text

def _adjust_separator(text: str, separator: str, default_separator: str) -> str:
    if separator != default_separator:
        return text.replace(default_separator, separator)
    return text