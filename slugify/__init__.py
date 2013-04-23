# -*- coding: utf-8 -*-

__version__ = '0.0.3'

__all__ = ['slugify']

import re
import unicodedata
from htmlentitydefs import name2codepoint
from types import UnicodeType
from unidecode import unidecode

# character entity reference
CHAR_ENTITY_REXP = re.compile('&(%s);' % '|'.join(name2codepoint))

# decimal character reference
DECIMAL_REXP = re.compile('&#(\d+);')

# hexadecimal character reference
HEX_REXP = re.compile('&#x([\da-fA-F]+);')

REPLACE1_REXP = re.compile(r'[\']+')
REPLACE2_REXP = re.compile(r'[^-a-z0-9]+')
REMOVE_REXP = re.compile('-{2,}')

def smart_truncate(text, max_length=0, word_boundaries=False,separator='-'):
    if not max_length or len(text) < max_length:
        return text

    if not word_boundaries:
        return text[:max_length].strip(separator)

    truncated = ''
    for i, word in enumerate(text.split(separator)):
        if not word: continue
        if len(truncated) + len(word) + i <= max_length:
            truncated += '{0}{1}'.format('-' if i else '', word)
    return truncated.strip(separator)


def slugify(text, separator='-', entities=True, decimal=True, hexadecimal=True, max_length=0, word_boundary=False):
    """ Make a slug from the given text """

    # text to unicode
    if type(text) != UnicodeType:
        text = unicode(text, 'utf-8', 'ignore')

    # decode unicode ( 影師嗎 = Ying Shi Ma)
    text = unidecode(text)

    # text back to unicode
    text = unicode(text, 'utf-8', 'ignore')

    # character entity reference
    if entities:
        text = CHAR_ENTITY_REXP.sub(lambda m: unichr(name2codepoint[m.group(1)]), text)

    # decimal character reference
    if decimal:
        try:
            text = DECIMAL_REXP.sub(lambda m: unichr(int(m.group(1))), text)
        except:
            pass

    # hexadecimal character reference
    if hexadecimal:
        try:
            text = HEX_REXP.sub(lambda m: unichr(int(m.group(1), 16)), text)
        except:
            pass

    # translate
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')

    # replace unwanted characters
    text = REPLACE1_REXP.sub('', text.lower()) # replace ' with nothing instead with -
    text = REPLACE2_REXP.sub(separator, text.lower())

    # remove redundant -
    text = REMOVE_REXP.sub('-', text).strip(separator)

    # smart truncate if requested
    if max_length > 0:
        text = smart_truncate(text, max_length, word_boundary)

    return text




