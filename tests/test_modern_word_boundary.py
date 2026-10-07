import unittest

from slugify import slugify


class ModernWordBoundaryTests(unittest.TestCase):
    def test_replacement_delimiters_are_budgeted_and_preserved(self):
        cases = (
            ('one--two--three', '-', 13, 'one--two'),
            ('one--two--three', '::', 17, 'one::::two'),
            ('one---two--three', '-', 14, 'one---two'),
            ('--one--two', '-', 8, '--one'),
            ('--one--two', '::', 12, '::::one'),
            ('one--two--three', '', 8, 'onetwo'),
        )
        for replacement, separator, limit, expected in cases:
            for save_order in (False, True):
                with self.subTest(replacement=replacement, separator=separator,
                                  limit=limit, save_order=save_order):
                    actual = slugify(
                        'value', algorithm='modern', allow_unicode=True,
                        replacements=[('value', replacement)],
                        replacement_stage='post', separator=separator,
                        max_length=limit, word_boundary=True,
                        save_order=save_order)
                    self.assertEqual(actual, expected)
                    self.assertLessEqual(len(actual), limit)

    def test_skipped_words_keep_the_existing_order_policy(self):
        for separator in ('-', '::', ''):
            with self.subTest(separator=separator):
                actual = slugify(
                    'oversized a b', algorithm='modern', allow_unicode=True,
                    separator=separator, max_length=2 + len(separator),
                    word_boundary=True)
                self.assertEqual(actual, separator.join(('a', 'b')))
        self.assertEqual(slugify(
            'oversized a b', algorithm='modern', max_length=3,
            word_boundary=True, save_order=True), 'ove')
