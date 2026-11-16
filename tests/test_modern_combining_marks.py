import re
import unicodedata
import unittest

from slugify import slugify
from slugify.slugify import _replace_disallowed_unicode


def modern(text, **kwargs):
    return slugify(text, allow_unicode=True, algorithm='modern', **kwargs)


class ModernCombiningMarkTests(unittest.TestCase):
    """Issue #214: combining marks and joiners must not split Unicode words."""

    def test_scripts_with_combining_marks_stay_whole(self):
        cases = (
            ('नमस्ते दुनिया', 'नमस्ते-दुनिया'),  # Hindi
            ('தமிழ் மொழி', 'தமிழ்-மொழி'),  # Tamil
            ('বাংলা ভাষা', 'বাংলা-ভাষা'),  # Bengali
            ('ਪੰਜਾਬੀ ਭਾਸ਼ਾ', 'ਪੰਜਾਬੀ-ਭਾਸ਼ਾ'),  # Gurmukhi
            ('తెలుగు భాష', 'తెలుగు-భాష'),  # Telugu
            ('ภาษาไทย ดี', 'ภาษาไทย-ดี'),  # Thai
            ('ភាសាខ្មែរ', 'ភាសាខ្មែរ'),  # Khmer
            ('မြန်မာစာ', 'မြန်မာစာ'),  # Myanmar
            ('مَرْحَبًا بِكُمْ', 'مَرْحَبًا-بِكُمْ'),  # Arabic with harakat
            ('שָׁלוֹם עוֹלָם', 'שָׁלוֹם-עוֹלָם'),  # Hebrew with niqqud
            ('ජනාධිපතිවරයා පාර්ලිමේන්තුවට ගියේය',
             'ජනාධිපතිවරයා-පාර්ලිමේන්තුවට-ගියේය'),  # Sinhala
        )
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(modern(text), unicodedata.normalize('NFKC', expected))

    def test_joiners_are_kept_only_inside_words(self):
        self.assertEqual(modern('ශ්\u200dරී ලංකාව'), 'ශ්\u200dරී-ලංකාව')  # Sinhala ZWJ
        self.assertEqual(modern('می\u200cخواهم'), 'می\u200cخواهم')  # Persian ZWNJ
        for text in ('\u200dabc', 'abc\u200d', 'a \u200d b', 'a\u200d\u200db', 'a\u200d-b'):
            with self.subTest(text=repr(text)):
                self.assertNotIn('\u200d', modern(text))

    def test_marks_without_a_base_and_emoji_selectors_are_separators(self):
        self.assertEqual(modern('\u094dक'), 'क')  # Leading orphan virama.
        self.assertEqual(modern('a \u0301 b'), 'a-b')
        self.assertEqual(modern('1\ufe0f\u20e3 go'), '1-go')  # Keycap emoji.

    def test_hard_cut_does_not_end_with_a_joiner(self):
        self.assertEqual(modern('ශ්\u200dරී', max_length=2), 'ශ්')

    def test_legacy_default_is_unchanged(self):
        self.assertEqual(slugify('नमस्ते दुनिया', allow_unicode=True), 'नमस-त-द-न-य')

    def test_custom_regex_pattern_is_unchanged(self):
        self.assertEqual(modern('नमस्ते', regex_pattern=r'[\W_]+'), 'नमस-त')

    def test_identical_to_plain_filter_without_marks_or_joiners(self):
        # Outside marks/joiners the filter keeps exactly str.isalnum() chars, so
        # equivalence reduces to: [^\W_] == isalnum for every code point. Checked
        # in bulk, without per-character calls into traced code (PyPy + coverage).
        everything = ''.join(chr(code) for code in range(0x110000)
                             if not 0xD800 <= code <= 0xDFFF)
        self.assertEqual(''.join(re.findall(r'[^\W_]', everything)),
                         ''.join(filter(str.isalnum, everything)))
        # And the filter itself, on a sample covering every general category.
        sample: dict = {}
        for char in everything[::7]:
            chars = sample.setdefault(unicodedata.category(char), [])
            if len(chars) < 40 and char not in '\u200c\u200d':
                chars.append(char)
        sample.pop('Mn', None)
        sample.pop('Mc', None)
        text = ''.join(char for chars in sample.values() for char in chars)
        self.assertGreater(len(set(map(unicodedata.category, text))), 25)
        self.assertEqual(_replace_disallowed_unicode(text), re.sub(r'[\W_]', '-', text))
