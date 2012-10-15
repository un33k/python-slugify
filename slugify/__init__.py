# -*- coding: utf-8 -*-

__version__ = '0.0.1'

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

def slugify(text, entities=True, decimal=True, hexadecimal=True):
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
    text = REPLACE2_REXP.sub('-', text.lower())

    # remove redundant -
    text = REMOVE_REXP.sub('-', text).strip('-')

    return text
