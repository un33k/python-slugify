import re
import unicodedata
import typing
import types
import sys

try:
    from htmlentitydefs import name2codepoint
    _unicode = unicode
    _unicode_type = types.UnicodeType
except ImportError:
    from html.entities import name2codepoint
    _unicode = str
    _unicode_type = str
    unichr = chr

try:
    import text_unidecode as unidecode
except ImportError:
    import unidecode

__all__ = ['slugify', 'smart_truncate']


CHAR_ENTITY_PATTERN = re.compile(r'&(%s);' % '|'.join(name2codepoint))
DECIMAL_PATTERN = re.compile(r'&#(\d+);')
HEX_PATTERN = re.compile(r'&#x([\da-fA-F]+);')
QUOTE_PATTERN = re.compile(r'[\']+')
DISALLOWED_CHARS_PATTERN = re.compile(r'[^-a-zA-Z0-9]+')
DUPLICATE_DASH_PATTERN = re.compile(r'-{2,}')
NUMBERS_PATTERN = re.compile(r'(?<=\d),(?=\d)')
DEFAULT_SEPARATOR = '-'


def smart_truncate(string, max_length=0, word_boundary=False, separator=' ', save_order=False):
    """
    Truncate a string.
    :param string (str): string for modification
    :param max_length (int): output string length
    :param word_boundary (bool):
    :param save_order (bool): if True then word order of output string is like input string
    :param separator (str): separator between words
    :return:
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
    if not truncated: # pragma: no cover
        truncated = string[:max_length]
    return truncated.strip(separator)


def slugify(text, entities=True, decimal=True, hexadecimal=True, max_length=0, word_boundary=False,
            separator=DEFAULT_SEPARATOR, save_order=False, stopwords=(), regex_pattern=None, lowercase=True,
            replacements: typing.Iterable[typing.Iterable[str]] = ()):
    """
    Make a slug from the given text.
    :param text (str): initial text
    :param entities (bool): converts html entities to unicode
    :param decimal (bool): converts html decimal to unicode
    :param hexadecimal (bool): converts html hexadecimal to unicode
    :param max_length (int): output string length
    :param word_boundary (bool): truncates to complete word even if length ends up shorter than max_length
    :param save_order (bool): if parameter is True and max_length > 0 return whole words in the initial order
    :param separator (str): separator between words
    :param stopwords (iterable): words to discount
    :param regex_pattern (str): regex pattern for disallowed characters
    :param lowercase (bool): activate case sensitivity by setting it to False
    :param replacements (iterable): list of replacement rules e.g. [['|', 'or'], ['%', 'percent']]
    :return (str):
    """

    # user-specific replacements
    if replacements:
        for old, new in replacements:
            text = text.replace(old, new)

    # ensure text is unicode
    if not isinstance(text, _unicode_type):
        text = _unicode(text, 'utf-8', 'ignore')

    # replace quotes with dashes - pre-process
    text = QUOTE_PATTERN.sub(DEFAULT_SEPARATOR, text)

    # decode unicode
    text = unidecode.unidecode(text)

    # ensure text is still in unicode
    if not isinstance(text, _unicode_type):
        text = _unicode(text, 'utf-8', 'ignore')

    # character entity reference
    if entities:
        text = CHAR_ENTITY_PATTERN.sub(lambda m: unichr(name2codepoint[m.group(1)]), text)

    # decimal character reference
    if decimal:
        try:
            text = DECIMAL_PATTERN.sub(lambda m: unichr(int(m.group(1))), text)
        except Exception:
            pass

    # hexadecimal character reference
    if hexadecimal:
        try:
            text = HEX_PATTERN.sub(lambda m: unichr(int(m.group(1), 16)), text)
        except Exception:
            pass

    # translate
    text = unicodedata.normalize('NFKD', text)
    if sys.version_info < (3,):
        text = text.encode('ascii', 'ignore')

    # make the text lowercase (optional)
    if lowercase:
        text = text.lower()

    # remove generated quotes -- post-process
    text = QUOTE_PATTERN.sub('', text)

    # cleanup numbers
    text = NUMBERS_PATTERN.sub('', text)

    # replace all other unwanted characters
    pattern = regex_pattern or DISALLOWED_CHARS_PATTERN
    text = re.sub(pattern, DEFAULT_SEPARATOR, text)

    # remove redundant
    text = DUPLICATE_DASH_PATTERN.sub(DEFAULT_SEPARATOR, text).strip(DEFAULT_SEPARATOR)

    # remove stopwords
    if stopwords:
        if lowercase:
            stopwords_lower = [s.lower() for s in stopwords]
            words = [w for w in text.split(DEFAULT_SEPARATOR) if w not in stopwords_lower]
        else:
            words = [w for w in text.split(DEFAULT_SEPARATOR) if w not in stopwords]
        text = DEFAULT_SEPARATOR.join(words)

    # finalize user-specific replacements
    if replacements:
        for old, new in replacements:
            text = text.replace(old, new)

    # smart truncate if requested
    if max_length > 0:
        text = smart_truncate(text, max_length, word_boundary, DEFAULT_SEPARATOR, save_order)

    if separator != DEFAULT_SEPARATOR:
        text = text.replace(DEFAULT_SEPARATOR, separator)

    return text
